"""
Concrete asynchronous pipeline.
"""

import asyncio
from pathlib import Path
from typing import Callable, List, Sequence, Union

from lovethedocs.domain import docstyle
from lovethedocs.domain.models import SourceModule
from lovethedocs.domain.use_cases.update_docs import DocumentationUpdateUseCase
from lovethedocs.gateways.project_file_system import ProjectFileSystem

from .progress import make_progress
from .summary import summarize


async def _inner(
    *,
    paths: Sequence[str | Path],
    concurrency: int,
    fs_factory: Callable[[Path], ProjectFileSystem],
    use_case: DocumentationUpdateUseCase,
    style: docstyle.DocStyle,
) -> List[ProjectFileSystem]:
    failures: list[tuple[Path, Exception]] = []
    processed = 0
    file_systems: list[ProjectFileSystem] = []

    with make_progress() as progress:
        proj_task = progress.add_task("Projects", total=len(paths))

        for raw in paths:
            root = Path(raw).resolve()

            # project-scoped FS
            # TODO: DRY this up with the sync version
            if root.is_file() and root.suffix == ".py":
                fs = fs_factory(root.parent)
                module_map = {root.relative_to(root.parent): root.read_text("utf-8")}
            elif root.is_dir():
                fs = fs_factory(root)
                module_map = fs.load_modules()
            else:
                progress.advance(proj_task)
                continue

            src_modules = [
                SourceModule(path, code) for path, code in module_map.items()
            ]
            mod_task = progress.add_task(f"[cyan]{root.name}", total=len(src_modules))
            async for result in use_case.run_async(
                src_modules, style=style, concurrency=concurrency
            ):
                rel_path = Path(result.module.path)

                if result.ok:
                    fs.stage_file(rel_path, result.new_code)
                else:
                    failures.append((rel_path, result.error))
                processed += 1
                progress.advance(mod_task)

            file_systems.append(fs)
            progress.advance(proj_task)

    summarize(failures, processed)
    return file_systems


def run_async(
    *,
    paths: Union[str | Path, Sequence[str | Path]],
    concurrency: int,
    fs_factory: Callable[[Path], ProjectFileSystem],
    use_case: DocumentationUpdateUseCase,
    style: docstyle.DocStyle,
) -> List[ProjectFileSystem]:
    """Entry-point called by pipeline.__init__."""
    if isinstance(paths, (str, Path)):
        paths = [paths]
    return asyncio.run(
        _inner(
            paths=list(paths),
            concurrency=concurrency,
            fs_factory=fs_factory,
            use_case=use_case,
            style=style,
        )
    )
