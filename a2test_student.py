"""
Assignment 2: Quadtree Compression

=== CSC148 Winter 2021 ===
Department of Mathematical and Computational Sciences,
University of Toronto Mississauga

=== Module Description ===
This module contains the test suite
"""

import pytest
from a2tree import QuadTreeNode, QuadTreeNodeEmpty, QuadTreeNodeLeaf, \
    QuadTree, QuadTreeNodeInternal

"""
Test cases
"""


def test_split_quadrants_1():
    """
    Tests _split_quadrants for an average sized 3x3 nested list.
    """
    example = QuadTree(0)
    x = example._split_quadrants([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert x == [[[1]], [[2, 3]], [[4], [7]], [[5, 6], [8, 9]]]


def test_split_quadrants_2():
    """
    Tests _split_quadrants for a long nested list.
    """
    example = QuadTree(0)
    x = example._split_quadrants([[1, 2, 3, 4], [5, 6, 7, 8],
                                  [9, 10, 11, 12], [13, 14, 15, 16]])
    assert x == [[[1, 2], [5, 6]], [[3, 4], [7, 8]], [[9, 10], [13, 14]],
                 [[11, 12], [15, 16]]]


def test_split_quadrants_3():
    """
    Tests _split_quadrants for a very short nested list.
    """
    example = QuadTree(0)
    x = example._split_quadrants([[1, 2]])
    assert x == [[], [], [[1]], [[2]]]


def test_restore_from_preorder_1():
    """
    Tests restore_from_preorder to check for an average length internal node.
    """
    tree1 = QuadTreeNodeInternal()
    lst = ['', '1', '', 'E', 'E', '2', '3', '', 'E', '4', 'E', '', '1', '2',
           '3', '4', '', '5', '6', '8', '9']
    assert tree1.restore_from_preorder(lst, 0) == 21


def test_restore_from_preorder_2():
    """
    Tests restore_from_preorder to check for a very long list with nested
    internal nodes.
    """
    tree1 = QuadTreeNodeInternal()
    lst = ['', '1', '', 'E', 'E', '2', '3', '', 'E', '4', 'E', '', '1', '2',
           '3', '4', '', '5', '6', '8', '', '1', '2', '3', '4']
    assert tree1.restore_from_preorder(lst, 0) == 25


def test_restore_from_preorder_3():
    """
    Tests restore_from_preorder to check for the edge case of only 5 elements.
    """
    tree1 = QuadTreeNodeInternal()
    lst = ['', '1', '2', '3', '4']
    assert tree1.restore_from_preorder(lst, 0) == 5


if __name__ == '__main__':

    pytest.main(['a2test_student.py'])
