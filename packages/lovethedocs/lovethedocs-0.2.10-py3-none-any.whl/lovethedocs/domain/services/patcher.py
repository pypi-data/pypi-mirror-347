"""
ModulePatcher - apply a `ModuleEdit` to old source code.

For this first cut we splice in (or replace) docstrings only; signature edits
can be added later by extending the visitor.
"""

from __future__ import annotations

import textwrap

import libcst as cst

from lovethedocs.domain.models import ClassEdit, FunctionEdit, ModuleEdit

# --------------------------------------------------------------------------- #
#  Low-level CST transformer                                                  #
# --------------------------------------------------------------------------- #


def _make_docstring_stmt(body: str, indent: str) -> cst.SimpleStatementLine:
    """
    Return a CST node representing a properly formatted docstring.

    Parameters
    ----------
    body : str
        The docstring content to insert.
    indent : str
        The indentation string to use for multi-line docstrings.

    Returns
    -------
    cst.SimpleStatementLine
        A CST node containing the formatted docstring.
    """
    clean = body.strip("\n")
    if "\n" in clean:  # multi-liner
        indented = textwrap.indent(clean, indent)
        literal = f'"""\n{indented}\n{indent}"""'
    else:  # one-liner
        literal = f'"""{clean}"""'
    return cst.SimpleStatementLine(
        body=[cst.Expr(cst.SimpleString(literal))],
        leading_lines=[],
    )


# TODO: Check type hinting.
def _parse_header(header: str) -> cst.FunctionDef:
    """
    Parse a function header string into a CST FunctionDef node.

    If the header ends with a colon, appends 'pass' to ensure valid syntax for parsing.

    Parameters
    ----------
    header : str
        The function header string, e.g., 'def foo(x: int) -> None:'.

    Returns
    -------
    cst.FunctionDef
        The parsed FunctionDef node.
    """
    hdr = header.strip()
    if hdr.endswith(":"):
        hdr += " pass"
    return cst.parse_module(hdr).body[0]  # FunctionDef


def _first_stmt_is_docstring(body: list[cst.BaseStatement]) -> bool:
    """Return True if the first statement in the list is a docstring."""
    if not body:
        return False
    first_stmt = body[0]
    return (
        isinstance(first_stmt, cst.SimpleStatementLine)
        and isinstance(first_stmt.body[0], cst.Expr)
        and isinstance(
            first_stmt.body[0].value, (cst.SimpleString, cst.ConcatenatedString)
        )
    )


class _DocSigPatcher(cst.CSTTransformer):
    """
    A CSTTransformer that applies docstring and signature edits.

    This transformer uses FunctionEdit and ClassEdit objects to update or insert docstrings
    and replace function signatures in a module's CST.
    """

    def __init__(self, edits_by_qualname: dict[str, FunctionEdit | ClassEdit]):
        """
        Initialize the DocSigPatcher with a mapping of qualified names to edits.

        Parameters
        ----------
        edits_by_qualname : dict[str, FunctionEdit | ClassEdit]
            A mapping from qualified names to their corresponding edit objects.
        """
        self._edits = edits_by_qualname
        self._scope: list[str] = []  # qualname breadcrumb

    # ----------------- internal helpers -----------------
    def _fqname(self) -> str:
        """Return the current qualified name based on the traversal scope."""
        return ".".join(self._scope)

    def _patch_doc(self, block: cst.BaseSuite, text: str, indent: str) -> cst.BaseSuite:
        """
        Insert or replace a docstring in the given code block.

        If the block is a stub, convert it to an indented block and insert the
        docstring. If a docstring already exists, replace it; otherwise, insert a new
        docstring at the top.

        Parameters
        ----------
        block : cst.BaseSuite
            The code block in which to patch the docstring.
        text : str
            The docstring text to insert.
        indent : str
            The indentation string to use for formatting.

        Returns
        -------
        cst.BaseSuite
            The updated code block with the new or replaced docstring.
        """
        doc_stmt = _make_docstring_stmt(text, indent)

        # Convert stubs (`SimpleStatementSuite`) to a real block if needed.
        if isinstance(block, cst.SimpleStatementSuite):
            # Discard the original inline ellipsis and build a proper body.
            ellipsis_stmt = cst.SimpleStatementLine(body=[cst.Expr(cst.Ellipsis())])
            return cst.IndentedBlock(body=[doc_stmt, ellipsis_stmt])
        else:
            body = list(block.body)
            if _first_stmt_is_docstring(body):
                body[0] = doc_stmt
            else:
                body.insert(0, doc_stmt)
            return block.with_changes(body=body)

    # ----------------- class traversal -----------------
    def visit_ClassDef(self, node: cst.ClassDef) -> None:
        """
        Enter a class definition node and update the scope for qualified naming.

        Parameters
        ----------
        node : cst.ClassDef
            The class definition node being visited.
        """
        self._scope.append(node.name.value)

    def leave_ClassDef(
        self, original: cst.ClassDef, updated: cst.ClassDef
    ) -> cst.ClassDef:
        """
        Apply class-level docstring edits when leaving a class definition node.

        Parameters
        ----------
        original : cst.ClassDef
            The original class definition node.
        updated : cst.ClassDef
            The potentially updated class definition node.

        Returns
        -------
        cst.ClassDef
            The class definition node with applied docstring edits, if any.
        """
        edit = self._edits.get(self._fqname())
        # set indent string to 4 spaces for each scope level
        indent_str = " " * (4 * len(self._scope))

        if isinstance(edit, ClassEdit) and edit.docstring:
            updated = updated.with_changes(
                body=self._patch_doc(updated.body, edit.docstring, indent_str)
            )
        self._scope.pop()
        return updated

    # ----------------- function / method traversal -----------------
    def visit_FunctionDef(self, node: cst.FunctionDef) -> None:
        """
        Enter a function definition node and update the scope for qualified naming.

        Parameters
        ----------
        node : cst.FunctionDef
            The function or method definition node being visited.
        """
        self._scope.append(node.name.value)

    def leave_FunctionDef(
        self, original: cst.FunctionDef, updated: cst.FunctionDef
    ) -> cst.FunctionDef:
        """
        Apply docstring and signature edits when leaving a function definition node.

        Parameters
        ----------
        original : cst.FunctionDef
            The original function definition node.
        updated : cst.FunctionDef
            The potentially updated function definition node.

        Returns
        -------
        cst.FunctionDef
            The function definition node with applied docstring and signature edits, if
            any.
        """
        edit = self._edits.get(self._fqname())
        indent_str = " " * (4 * len(self._scope))
        if isinstance(edit, FunctionEdit):
            # 1. Docstring
            if edit.docstring:
                updated = updated.with_changes(
                    body=self._patch_doc(updated.body, edit.docstring, indent_str)
                )

            # 2. Signature
            if edit.signature:
                stub = _parse_header(edit.signature)
                updated = updated.with_changes(params=stub.params, returns=stub.returns)

        self._scope.pop()
        return updated


# --------------------------------------------------------------------------- #
#  Public service                                                             #
# --------------------------------------------------------------------------- #
class ModulePatcher:
    """
    Pure function-object:  old_code + ModuleEdit  ─►  new_code.
    """

    def apply(self, edit: ModuleEdit, old_code: str) -> str:
        """
        Apply the given ModuleEdit to the old source code and return the patched code.

        Parameters
        ----------
        edit : ModuleEdit
            The module edit instructions to apply.
        old_code : str
            The original source code to patch.

        Returns
        -------
        str
            The patched source code.
        """
        # Build lookup {qualname: FunctionEdit|ClassEdit}
        edits_by_qname = edit.map_qnames_to_edits()

        patched = cst.parse_module(old_code).visit(_DocSigPatcher(edits_by_qname))
        return patched.code
