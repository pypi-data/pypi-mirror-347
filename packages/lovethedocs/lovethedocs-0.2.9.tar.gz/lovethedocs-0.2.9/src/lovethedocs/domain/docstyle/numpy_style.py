from lovethedocs.domain.docstyle.base import DocStyle


class NumPyDocStyle(DocStyle):
    name = "numpy"
    section_order = (
        "Parameters",
        "Returns",
        "Yields",
        "Raises",
        "Examples",
        "Notes",
        "References",
    )


# Register the NumPyDocStyle in the registry
DocStyle.register("numpy", NumPyDocStyle)
