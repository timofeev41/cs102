import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        return struct.pack(
            f">10i20sh{len(self.name)}s{8 - (62 + len(self.name)) % 8}x",
            self.ctime_s,
            self.ctime_n,
            self.mtime_s,
            self.mtime_n,
            self.dev,
            self.ino,
            self.mode,
            self.uid,
            self.gid,
            self.size,
            self.sha1,
            self.flags,
            self.name.encode(),
        )

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        raw = list(struct.unpack(f">10i20sh{len(data) - 62:}s", data))
        raw[-1] = raw[-1].strip(b"\x00").decode()
        return GitIndexEntry(*raw)


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    if not (gitdir / "index").exists():
        return []
    with open(gitdir / "index", "rb") as f:
        raw = f.read()
    result = []
    index_length = struct.unpack("!i", raw[8:12])
    pos_end = 12
    for _ in range(index_length[0]):
        for i in range(pos_end + 63, len(raw), 8):
            if raw[i] == 0:
                pos_start = pos_end
                pos_end = i + 1
                break
        result.append(GitIndexEntry.unpack(raw[pos_start:pos_end]))
    return result


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    entries.sort(key=lambda x: x.name)
    content = (
        b"DIRC"
        + struct.pack("!2i", 2, len(entries))
        + b"".join(GitIndexEntry.pack(_) for _ in entries)
    )
    with open(gitdir / "index", "wb") as f:
        f.write(content + hashlib.sha1(content).digest())


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    content = read_index(gitdir)
    if details:
        print(*[f"{_.mode:o} {_.sha1.hex()} 0\t{_.name}" for _ in content], sep="\n")
    else:
        print(*[_.name for _ in content], sep="\n")


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    data = read_index(gitdir)
    for i in paths:
        stats = os.stat(i)
        data.append(
            GitIndexEntry(
                int(stats.st_ctime),
                0,
                int(stats.st_mtime),
                0,
                stats.st_dev,
                stats.st_ino,
                stats.st_mode,
                stats.st_uid,
                stats.st_gid,
                stats.st_size,
                bytes.fromhex(hash_object(i.open("rb").read(), "blob", True)),
                len(i.name),
                str(i),
            )
        )
    write_index(gitdir, data)
