import collections
import pprint
import sys
from pathlib import Path
from typing import List, Optional, Tuple


def read_map(path: Path) -> List[List[str]]:
    with open(path, "rt", encoding="utf_8_sig") as f:
        return [list(i[:-1]) if i[-1] == "\n" else list(i) for i in f.readlines()]


def find_player_pos(field: List[str]) -> Optional[Tuple[int, int]]:
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == "☺":
                return i, j
    return None


def find_destination(field: List[str]) -> Optional[Tuple[int, int]]:
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == "☼":
                return i, j
    return None


def find_solution(
    field: List[List[str]], sam_position: List[int], end_position: List[int]
) -> List[List[str]]:
    parent: List[List[Tuple[int, int]]] = [[] for i in range(len(field))]
    for i in range(len(field)):
        for j in range(len(field[i])):
            parent[i].append((-1, -1))
    queue: List[List[int]] = [sam_position]
    if end_position == (-1, -1) or sam_position == (-1, -1):
        return field
    while len(queue) > 0:
        y, x = queue.pop(0)
        for move in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_y, new_x = y + move[0], x + move[1]
            if new_y >= len(field) or new_y < 0:
                continue
            if new_x >= len(field[new_y]) or new_x < 0:
                continue
            if (
                field[new_y][new_x] == "☒"
                or parent[new_y][new_x] != (-1, -1)
                or (new_y, new_x) == sam_position
            ):
                continue
            parent[new_y][new_x] = y, x
            queue.append([new_y, new_x])
    if parent[end_position[0]][end_position[1]] == (-1, -1):
        return field
    position: Tuple[int, int] = parent[end_position[0]][end_position[1]]
    while position != sam_position:
        field[position[0]][position[1]] = "☺"
        position = parent[position[0]][position[1]]
    return field


if __name__ == "__main__":
    field = read_map(Path(f"{sys.argv[1]}"))
    player_pos = find_player_pos(field)  # type: ignore
    # print(player_pos)
    destination = find_destination(field)  # type: ignore
    # print(destination)
    solve = find_solution(field, player_pos, destination)  # type: ignore
    for _ in solve:
        print("".join(_))
