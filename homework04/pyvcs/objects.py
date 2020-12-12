import hashlib
import os
import pathlib
import typing as tp
import zlib

from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    blob = f"{fmt} {len(data)}".encode() + b"\x00" + data
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
    dir_path = repo_find(gitdir) / "objects" / obj_name[:2]
    if len(obj_name) > 40 or len(obj_name) < 4:
        raise danger
    for _, _, dir_files in os.walk(dir_path):
        for file in dir_files:
            if file.startswith(obj_name[2:]):
                content.append(obj_name[:2] + file)
            else:
                raise danger
    return content


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    pass


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    path = repo_find(gitdir) / "objects" / sha[:2]
    with open(path / sha[2:], mode="rb") as f:
        object = zlib.decompress(f.read())
    pos = object.find(b"\x00")
    head = object[:pos]
    head_index = head.find(b" ")
    head = head[:head_index]
    content = object[pos + 1 :]
    return head.decode(), content


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    content = []
    while len(data):
        mode = int(data[: data.find(b" ")].decode())
        data = data[data.find(b" ") + 1 :]
        name = data[: data.find(b"\x00")].decode()
        data = data[data.find(b"\x00") + 1 :]
        sha1 = bytes.hex(data[:20])
        data = data[20:]
        content.append((int(mode), str(name), str(sha1)))
    return content


def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir = repo_find(".")
    obj = resolve_object(obj_name, gitdir)
    if obj:
        head, things = read_object(obj_name, gitdir)
        if head == "tree":
            cat = ""
            tree_files = read_tree(things)
            for file in tree_files:
                cat += str(file[0]).zfill(6) + " "
                cat += read_object(file[2], repo_find())[0] + " "
                cat += str(file[2] + "\t")
                cat += str(file[1] + "\n")
            print(cat, end="\n")
        else:
            print(things.decode())


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    content = []
    name: str
    header, data = read_object(tree_sha, gitdir)
    for file in read_tree(data):
        if read_object(file[2], gitdir)[0] == "tree":
            tree = find_tree_files(file[2], gitdir)
            for blob in tree:
                name = str(file[1] + "/" + blob[0])
            content.append((name, blob[1]))
        else:
            content.append((file[1], file[2]))
    return content


def commit_parse(raw: bytes, start: int = 0, dct=None):
    data = zlib.decompress(raw)
    pos = data.find(b"tree")
    return data[pos + 5 : pos + 45]
