import asyncio
from cyclopts import App
import logging
import niquests
import os
from pathlib import Path
from rich import print
from rich.logging import RichHandler
import sys

from .pkgstatus import get_locklist, package_item_action, Action, Options
from .reporter import Reporter, TagMatcher
from . import VERSION


logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("wheel_getter")
reporter = Reporter()
app = App(version=VERSION)


@app.default
def get_wheels(
        wheelhouse: Path = Path("wheels"),
        # lockfile: Path = Path("uv.lock"),
        package: Path | None = None,
        directory: Path | None = None,
        python: str | None = None,
        debug: bool = False,
        dry_run: bool = False,
        ) -> None:
    """Gets and/or builds wheels if necessary, putting them in the wheelhouse."""
    if debug:
        logger.setLevel(logging.DEBUG)
    
    if directory is not None:
        os.chdir(directory)
        logger.debug("changed to %s", directory)
    
    if package is None:
        base_dir = Path.cwd()
        while not (base_dir / "pyproject.toml").exists():
            parent = base_dir.parent
            if parent == base_dir:
                logger.error("no project found")
                raise ValueError("no project found")
            base_dir = parent
    else:
        base_dir = package
        if not (base_dir / "pyproject.toml").exists():
            logger.error("%s is not a package directory", package)
            raise ValueError("no project found")
    logger.debug("using base directory %s", base_dir)
    
    if python is None:
        if (pin_file := base_dir / ".python-version").exists():
            python_version = pin_file.read_text().strip()
        else:
            python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        logger.info("working with Python version %s", python_version)
    else:
        python_version = python
    py_marker = f"cp{python_version.replace('.', '')}"
    logger.debug("using python marker %s", py_marker)
    
    lockfile = base_dir / "uv.lock"
    if not lockfile.exists():
        logger.error("no lockfile found at %s", base_dir)
        raise ValueError("no lockfile found")
    locklist = get_locklist(base_dir, reporter=reporter)
    
    if not wheelhouse.exists():
        if dry_run:
            print(f"[green]would create wheelhouse “{wheelhouse}”")
        else:
            wheelhouse.mkdir(parents=True, exist_ok=True)
            logging.info("created wheelhouse directory “%s”", wheelhouse)
    
    matcher = TagMatcher(python=python_version)
    
    options = Options(wheelhouse=wheelhouse, base_dir=base_dir, python=python_version,
            debug=debug, dry_run=dry_run, matcher=matcher, reporter=reporter)
    
    actions: list[Action] = []
    for item in locklist:
        action = package_item_action(item, options=options)
        if action is not None:
            actions.append(action)
    
    asyncio.run(process_actions(actions))
    for action in actions:
        if action.failed:
            reporter.error(action.message)
    
    reporter.report()


async def process_actions(actions: list[Action]) -> None:
    async with niquests.AsyncSession() as s:
        await asyncio.gather(*[
                action.execute(session=s)
                for action in actions
                ])
