import os
from map import *

def test_find_player_pos():
    test_field = [
        ["☒", "☒", "☒"],
        ["☒", "☺", "☒"],
        ["☒", "☒", "☒"]
    ]
    actual_pos = (1, 1)
    code_pos = find_player_pos(test_field)
    assert code_pos == actual_pos
    test_field = [
        ["☺", "☒", "☒"],
        ["☒", "☒", "☒"],
        ["☒", "☒", "☒"]
    ]
    actual_pos = (0, 0)
    code_pos = find_player_pos(test_field)
    assert code_pos == actual_pos

def test_find_destination():
    test_field = [
        ["☒", "☒", "☒"],
        ["☒", "☼", "☒"],
        ["☒", "☒", "☒"]
    ]
    actual_pos = (1, 1)
    code_pos = find_destination(test_field)
    assert code_pos == actual_pos

def test_find_solution():
    test_field = [
        ["☒", "☒", "☒"],
        ["☒", "☺", "☒"],
        ["☒", ".", "☒"],
        ["☒", ".", "☒"],
        ["☒", "☼", "☒"],
        ["☒", "☒", "☒"]
    ]
    start = find_player_pos(test_field)
    end = find_destination(test_field)
    solved = find_solution(test_field, start, end)
    actual_solution = [
        ["☒", "☒", "☒"],
        ["☒", "☺", "☒"],
        ["☒", "☺", "☒"],
        ["☒", "☺", "☒"],
        ["☒", "☼", "☒"],
        ["☒", "☒", "☒"]
    ] 
    assert solved == actual_solution