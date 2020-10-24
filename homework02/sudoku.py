from typing import Tuple, List, Set, Optional
import random as random
import time as time


def read_sudoku(filename: str) -> List[List[str]]:
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: List[List[str]]) -> None:
    """ Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "")
                for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: List[str], number_of_elements: int) -> List[List[str]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    result = []
    for val in range(0, len(values) - 1, number_of_elements):
        result.append(values[val : val + number_of_elements])
    return result


def get_row(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]


def get_col(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    result = []
    for column in grid:
        result.append(column[pos[1]])
    return result


def get_block(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    block_values = []
    for column in range((pos[0] // 3) * 3, (pos[0] // 3) * 3 + 3):
        for row in range((pos[1] // 3) * 3, (pos[1] // 3) * 3 + 3):
            block_values.append(grid[column][row])
    return block_values


def find_empty_positions(grid: List[List[str]]) -> Tuple[int, int]:
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for row in range(len(grid)):
        for column in grid[row]:
            if column == ".":
                return (row, grid[row].index(column))
    return -9, -9


def find_possible_values(grid: List[List[str]], pos: Tuple[int, int]) -> Set[str]:
    """ Вернуть множество возможных значений для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    static_set = set("123456789")
    row_set = set(get_row(grid, pos))
    col_set = set(get_col(grid, pos))
    block_set = set(get_block(grid, pos))
    return static_set - row_set - block_set - col_set


def solve(grid: List[List[str]]) -> List[List[str]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [ ['5', '3', '4', '6', '7', '8', '9', '1', '2'], 
      ['6', '7', '2', '1', '9', '5', '3', '4', '8'], 
      ['1', '9', '8', '3', '4', '2', '5', '6', '7'], 
      ['8', '5', '9', '7', '6', '1', '4', '2', '3'], 
      ['4', '2', '6', '8', '5', '3', '7', '9', '1'], 
      ['7', '1', '3', '9', '2', '4', '8', '5', '6'], 
      ['9', '6', '1', '5', '3', '7', '2', '8', '4'], 
      ['2', '8', '7', '4', '1', '9', '6', '3', '5'], 
      ['3', '4', '5', '2', '8', '6', '1', '7', '9'] ]
    """
    if find_empty_positions(grid) == (-9, -9):
        return grid
    pos = find_empty_positions(grid)
    for value in find_possible_values(grid, pos):
        grid[pos[0]][pos[1]] = value
        if solve(grid):
            return solve(grid)
        grid[pos[0]][pos[1]] = "."
    return []


def check_solution(solution: List[List[str]]) -> bool:
    """
    Если решение solution верно, то вернуть True, в противном случае False

    >>> grid = read_sudoku('puzzle1.txt')
    >>> grid[4][2] = 0
    >>> check_solution(grid)
    False

    >>> grid = read_sudoku('puzzle2.txt')
    >>> check_solution(solve(grid))
    True
    """
    for row in range(len(solution)):
        if set(get_row(solution, (row, 0))) != set("123456789"):
            return False
    for col in range(len(solution)):
        if set(get_col(solution, (0, col))) != set("123456789"):
            return False
    for row in (0, 3, 6):
        for col in (0, 3, 6):
            if set(get_block(solution, (row, col))) != set("123456789"):
                return False
    return True


def generate_sudoku(number_of_elements: int) -> List[List[str]]:
    """ Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    if number_of_elements > 9 * 9:
        number_of_elements = 9 * 9
    new_grid = solve([["." for _ in range(9)] for _ in range(9)])
    deleted_values = 0
    while number_of_elements + deleted_values < 81:
        random_col = random.randint(0, 8)
        random_row = random.randint(0, 8)
        if new_grid[random_col][random_row] != ".":
            new_grid[random_col][random_row] = "."
            deleted_values += 1
    return new_grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        print(f"Trying to solve {fname} \n")
        display(grid)
        solution = solve(grid)
        # time.sleep(3)
        if not solution:
            print(f"Puzzle {fname} can't be solved \n")
        else:
            print(f"Puzzle {fname} can be solved in this way: \n")
            display(solution)
        # time.sleep(3)