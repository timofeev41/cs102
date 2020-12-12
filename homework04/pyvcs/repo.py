import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    workdir = pathlib.Path(workdir).absolute()
    gitdir = pathlib.Path(".pyvcs")
    if "GIT_DIR" in os.environ:
        gitdir = pathlib.Path(os.environ["GIT_DIR"])
    while pathlib.Path(workdir) is not pathlib.Path("/"):
        if pathlib.Path(workdir / gitdir).exists():
            return workdir / gitdir
        if pathlib.Path(workdir) == pathlib.Path("/"):
            break
        workdir = workdir.parent
    raise Exception("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    if not pathlib.Path(workdir).is_dir():
        raise Exception(f"{workdir} is not a directory")
    gitdir = pathlib.Path(".pyvcs")
    if "GIT_DIR" in os.environ:
        gitdir = pathlib.Path(os.environ["GIT_DIR"])
    pathlib.Path(gitdir).mkdir()
    pathlib.Path(gitdir / "refs").mkdir()
    pathlib.Path(gitdir / "refs" / "heads").mkdir()
    pathlib.Path(gitdir / "refs" / "tags").mkdir()
    pathlib.Path(gitdir / "objects").mkdir()
    with open(gitdir / "HEAD", "w") as f:
        f.write("ref: refs/heads/master\n")
    with open(gitdir / "config", "w") as f:
        f.write(
            "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n"
        )
    with open(gitdir / "description", "w") as f:
        f.write("Unnamed pyvcs repository.\n")
    return workdir / gitdir
