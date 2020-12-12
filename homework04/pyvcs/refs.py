import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    if isinstance(ref, str):
        ref = pathlib.Path(ref)

    path = gitdir / ref
    path.touch()
    path.write_text(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    pass


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    if refname == "HEAD":
        with open(gitdir / refname, "r") as f:
            content = f.read()
        refname = content[content.find(" ") + 1 :].strip()
    path = gitdir / refname
    if path.exists():
        with open(path, "r") as f:
            return f.read()
    return None  # type: ignore


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    if ref_resolve(gitdir, "HEAD") is not None:
        return ref_resolve(gitdir, "HEAD")
    return None


def is_detached(gitdir: pathlib.Path) -> bool:
    path = gitdir / "HEAD"
    with open(path, "r") as f:
        content = f.read()
    if content.startswith("ref:"):
        return False
    return True


def get_ref(gitdir: pathlib.Path) -> str:
    with open(gitdir / "HEAD", "r") as f:
        content = f.read()
    if is_detached(gitdir):
        return content
    pos = content.find(" ")
    return content[pos + 1 :].strip()
