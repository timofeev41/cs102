import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    tree_content: tp.List[tp.Tuple[int, pathlib.Path, bytes]] = []
    subtrees: tp.Dict[str, tp.List[GitIndexEntry]] = dict()
    files = []
    for x in (gitdir.parent / dirname).glob("*"):
        files.append(str(x))
    for entry in index:
        if entry.name in files:
            tree_content.append((entry.mode, gitdir.parent / entry.name, entry.sha1))
        else:
            directory = entry.name.lstrip(dirname).split("/", 1)[0]
            if directory not in subtrees:
                subtrees[directory] = []
            subtrees[directory].append(entry)
    for tree in subtrees:
        tree_content.append(
            (
                0o40000,
                gitdir.parent / dirname / tree,
                bytes.fromhex(
                    write_tree(
                        gitdir, subtrees[tree], dirname + "/" + tree if dirname != "" else tree
                    )
                ),
            )
        )
    tree_content.sort(key=lambda _: _[1])
    data = b"".join(
        f"{elem[0]:o} {elem[1].name}".encode() + b"\00" + elem[2] for elem in tree_content
    )
    return hash_object(data, "tree", write=True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    now = int(time.mktime(time.localtime()))
    timezone = time.timezone
    if timezone > 0:
        tz_str = "." + f"{abs(timezone) // 60 // 60:02}{abs(timezone) // 60 % 60:02}"
    else:
        tz_str = "+" + f"{abs(timezone) // 60 // 60:02}{abs(timezone) // 60 % 60:02}"
    cont = [f"tree {tree}"]
    if parent is not None:
        cont.append(f"parent {parent}")
    cont.append(f"author {author} {now} {tz_str}")
    cont.append(f"committer {author} {now} {tz_str}")
    cont.append(f"\n{message}\n")
    return hash_object("\n".join(cont).encode(), "commit", write=True)
