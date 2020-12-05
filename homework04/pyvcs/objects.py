import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    blob = f"{fmt} {len(data)}".encode()+b"\x00" + data
    sha = hashlib.sha1(blob).hexdigest()
    if write:
        gitdir = repo_find(".")
        if not pathlib.Path(gitdir / "objects" / sha[:2]).exists():
            pathlib.Path(gitdir / "objects" / f"{sha[:2]}/").mkdir(parents=True, exist_ok=True)
            with open(gitdir / "objects" / f"{sha[:2]}/{sha[2:]}", "wb") as f:
                f.write(zlib.compress(blob))
    return sha


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    content = []
    danger = Exception(f"Not a valid object name {obj_name}")
    dir_path = pathlib.Path(gitdir / f"objects/{obj_name[:2]}")

    if len(obj_name) > 20 or len(obj_name) < 4:
        raise danger
    if not pathlib.Path(dir_path).exists():
        raise danger
    for _, _, files in os.walk(dir_path):
        for element in files:
            if element[:len(obj_name) - 2] == obj_name[2:]:
                content.append(str(obj_name[:2] + element))
    if len(content) == 0:
        raise danger
    return content


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    # PUT YOUR CODE HERE
    ...


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    # PUT YOUR CODE HERE
    ...


def cat_file(obj_name: str, pretty: bool = True) -> None:
    # PUT YOUR CODE HERE
    ...


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...
