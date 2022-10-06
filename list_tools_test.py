from list_tools import *
import pytest

def test_find_one():
    l1 = []
    l2 = [1, 2, 3]
    l3 = [2, 3, 1]
    l4 = [1, 2, 1, 3]

    assert find_one(l1, 1) == False
    assert find_one(l2, 1) == True
    assert find_one(l3, 1) == True
    assert find_one(l4, 1) == True

def test_find_n():
    l1 = []
    l2 = [1, 2, 3, 4, 3, 3]
    
    assert find_n(l1, 2, 3) == False
    assert find_n(l2, 3, 2) == True

def test_find_n_cons():
    l1 = []
    l2 = [1, 3, 1, 1]
    l3 = [1, 1, 1, 3]

    assert find_n_cons(l1, 1, 2) == False
    assert find_n_cons(l2, 1, 3) == False
    assert find_n_cons(l2, 1, 2) == True
    assert find_n_cons(l3, 1, 2) == True
    assert find_n_cons(l3, 1, 3) == True

def test_transpose_matrix():
    m1 = []
    m2 = [[2]]
    m3 = [[1, 3], [2, 4]]
    m4 = [[1, 2],[3, 4]]
    assert transpose_matrix(m1) == m1
    assert transpose_matrix(m2) == m2
    assert transpose_matrix(m3) == m4

def test_shift_list():
    l1 = ["x", "o", None, None]
    l2 = ["o", None, None, None]
    l3 = [None, "x", "o", None]
    l4 = [None, None, "x", "o"]

    assert shift_list(l1, -1) == l2
    assert shift_list(l1, 0) == l1
    assert shift_list(l1, 1) == l3
    assert shift_list(l1, 2) == l4

def test_rot_matrix_ccw():
    m = [[1, 2],
         [3, 4]]
    mr = [[2, None],
          [3, 4]]
    n = [["x", "o", "x", None],
         ["o", "x", None, None],
         ["x", None, None, None],
         [None, None, None, None]]
    nr = [["o", "x", None, None],
         ["o", "x", None, None],
         [None, "x", None, None],
         [None, None, None, None]]
    
    assert rot_matrix_ccw(m) == mr
    assert rot_matrix_ccw(n) == nr

def test_collapse_list():
    assert collapse_list([]) == ""
    assert collapse_list(["x", "o", "o", "x"]) == "xoox"
    assert collapse_list(["x", "x", None, None, None]) == "xx..."

def test_collapse_matrix():
    assert collapse_matrix([]) == ""
    m = [["x", "o", None, None],
         [None, None, None, None],
         ["o", None, None, None],
         ["x", "o", "o", "x"]]
    assert collapse_matrix(m) == "xo..|....|o...|xoox"

def test_explode_to_list():
    assert explode_to_list("xo.") == ["x", "o", None]
    assert explode_to_list("..") == [None, None]
    assert explode_to_list("") == []

def test_explode_to_matrix():
    assert explode_to_matrix("xox|...|o..") == [["x", "o", "x"], 
                                     [None, None, None], 
                                     ["o", None, None]]