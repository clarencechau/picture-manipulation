from __future__ import annotations
import math
from typing import List, Tuple, Optional
from copy import deepcopy


# No other imports allowed


def mean_and_count(matrix: List[List[int]]) -> Tuple[float, int]:
    """
    Returns the average of the values in a 2D list
    Also returns the number of values in the list
    """
    total = 0
    count = 0
    for row in matrix:
        for v in row:
            total += v
            count += 1
    return total / count, count


def standard_deviation_and_mean(matrix: List[List[int]]) -> Tuple[float, float]:
    """
    Return the standard deviation and mean of the values in <matrix>

    https://en.wikipedia.org/wiki/Root-mean-square_deviation

    Note that the returned average is a float.
    It may need to be rounded to int when used.
    """
    avg, count = mean_and_count(matrix)
    total_square_error = 0
    for row in matrix:
        for v in row:
            total_square_error += ((v - avg) ** 2)
    return math.sqrt(total_square_error / count), avg


class QuadTreeNode:
    """
    Base class for a node in a quad tree
    """

    def __init__(self) -> None:
        pass

    def tree_size(self) -> int:
        raise NotImplementedError

    def convert_to_pixels(self, width: int, height: int) -> List[List[int]]:
        raise NotImplementedError

    def preorder(self) -> str:
        raise NotImplementedError


class QuadTreeNodeEmpty(QuadTreeNode):
    """
    An empty node represents an area with no pixels included
    """

    def __init__(self) -> None:
        super().__init__()

    def tree_size(self) -> int:
        """
        Note: An empty node still counts as 1 node in the quad tree
        """
        return 1

    def convert_to_pixels(self, width: int, height: int) -> List[List[int]]:
        """
        Convert to a properly formatted empty list
        """
        # Note: Normally, this method should return an empty list or a list of
        # empty lists. However, when the tree is mirrored, this returned list
        # might not be empty and may contain the value 255 in it. This will
        # cause the decompressed image to have unexpected white pixels.
        # You may ignore this caveat for the purpose of this assignment.
        return [[255] * width for _ in range(height)]

    def preorder(self) -> str:
        """
        The letter E represents an empty node
        """
        return 'E'


class QuadTreeNodeLeaf(QuadTreeNode):
    """
    A leaf node in the quad tree could be a single pixel or an area in which
    all pixels have the same colour (indicated by self.value).
    """

    value: int  # the colour value of the node

    def __init__(self, value: int) -> None:
        super().__init__()
        assert isinstance(value, int)
        self.value = value

    def tree_size(self) -> int:
        """
        Return the size of the subtree rooted at this node
        """
        return 1

    def convert_to_pixels(self, width: int, height: int) -> List[List[int]]:
        """
        Return the pixels represented by this node as a 2D list

        >>> sample_leaf = QuadTreeNodeLeaf(5)
        >>> sample_leaf.convert_to_pixels(2, 2)
        [[5, 5], [5, 5]]
        >>> sample_leaf = QuadTreeNodeLeaf(6)
        >>> sample_leaf.convert_to_pixels(1, 5)
        [[6], [6], [6], [6], [6]]
        >>> sample_leaf = QuadTreeNodeLeaf(7)
        >>> sample_leaf.convert_to_pixels(5, 1)
        [[7, 7, 7, 7, 7]]
        """
        return_list = []
        for _ in range(height):
            appended_list = []
            for _ in range(width):
                appended_list.append(self.value)
            return_list.append(appended_list)
        return return_list

    def preorder(self) -> str:
        """
        A leaf node is represented by an integer value in the preorder string
        """
        return str(self.value)


class QuadTreeNodeInternal(QuadTreeNode):
    """
    An internal node is a non-leaf node, which represents an area that will be
    further divided into quadrants (self.children).

    The four quadrants must be ordered in the following way in self.children:
    bottom-left, bottom-right, top-left, top-right

    (List indices increase from left to right, bottom to top)

    Representation Invariant:
    - len(self.children) == 4
    """
    children: List[Optional[QuadTreeNode]]

    def __init__(self) -> None:
        """
        Order of children: bottom-left, bottom-right, top-left, top-right
        """
        super().__init__()

        # Length of self.children must be always 4.
        self.children = [None, None, None, None]

    def tree_size(self) -> int:
        """
        The size of the subtree rooted at this node.

        This method returns the number of nodes that are in this subtree,
        including the root node.
        """
        count = 0
        for i in range(4):
            if isinstance(self.children[i], QuadTreeNodeInternal):
                count += self.children[i].tree_size()
            else:
                count += 1
        return count

    def convert_to_pixels(self, width: int, height: int) -> List[List[int]]:
        """
        Return the pixels represented by this node as a 2D list.

        You'll need to recursively get the pixels for the quadrants and
        combine them together.

        Make sure you get the sizes (width/height) of the quadrants correct!
        Read the docstring for split_quadrants() for more info.
        """
        bottom_left = self.children[0].convert_to_pixels(width // 2,
                                                         height // 2)
        bottom_right = self.children[1].convert_to_pixels(
            self.normal_round(width / 2), height // 2)
        top_left = self.children[2].convert_to_pixels(width // 2,
                                                      self.normal_round(
                                                          height / 2))
        top_right = self.children[3].convert_to_pixels(
            self.normal_round(width / 2), self.normal_round(height / 2))
        bottom_half = []
        top_half = []
        for i in range(len(bottom_left)):
            bottom_half.append(bottom_left[i] + bottom_right[i])
        for i in range(len(top_left)):
            top_half.append(top_left[i] + top_right[i])
        return bottom_half + top_half

    @staticmethod
    def normal_round(n: float) -> int:
        """
        Rounds decimals to the nearest whole number, without using bankers
        rounding.
        """
        if n - math.floor(n) < 0.5:
            return math.floor(n)
        return math.ceil(n)

    def preorder(self) -> str:
        """
        Return a string representing the preorder traversal or the tree rooted
        at this node. See the docstring of the preorder() method in the
        QuadTree class for more details.

        An internal node is represented by an empty string in the preorder
        string.
        """
        return_string = ''
        for i in range(4):
            return_string += ',' + self.children[i].preorder()
        return return_string

    def restore_from_preorder(self, lst: List[str], start: int) -> int:
        """
        Restore subtree from preorder list <lst>, starting at index <start>
        Return the number of entries used in the list to restore this subtree
        """
        assert lst[start] == ''
        if lst[start + 1] != '' and lst[start + 2] != '' and \
                lst[start + 3] != '' and lst[start + 4] != '':
            for i in range(4):
                if lst[start + 1 + i] == 'E':
                    self.children[i] = QuadTreeNodeEmpty()
                else:
                    self.children[i] = QuadTreeNodeLeaf(int(lst[start + i + 1]))
            return 5
        else:
            count = 1
            for i in range(4):
                if lst[start + count] == 'E':
                    self.children[i] = QuadTreeNodeEmpty()
                    count += 1
                elif lst[start + count] == '':
                    tree = QuadTreeNodeInternal()
                    count += tree.restore_from_preorder(lst, start + count)
                    self.children[i] = tree
                else:
                    self.children[i] = QuadTreeNodeLeaf(int(lst[start + count]))
                    count += 1
            return count

    def mirror(self) -> None:
        """
        Mirror the bottom half of the image represented by this tree over
        the top half

        Example:
            Original Image
            1 2
            3 4

            Mirrored Image
            3 4 (this row is flipped upside down)
            3 4

        See the assignment handout for a visual example.
        >>> tree = QuadTree()
        >>> tree.build_quad_tree([[1,2,3],[4,5,6],[7,8,9]], True)
        >>> tree.convert_to_pixels()
        [[1, 2, 3], [1, 2, 3], [1, 255, 255]]
        """
        quadrant1 = deepcopy(self.children[0])
        quadrant2 = deepcopy(self.children[1])
        quadrant3 = quadrant1
        quadrant4 = quadrant2
        if isinstance(quadrant3, QuadTreeNodeInternal):
            self.mirror_helper(quadrant3)
        if isinstance(quadrant4, QuadTreeNodeInternal):
            self.mirror_helper(quadrant4)
        self.children[2] = quadrant3
        self.children[3] = quadrant4

    @staticmethod
    def mirror_helper(q: QuadTreeNodeInternal) -> None:
        copy1 = deepcopy(q.children[0])
        copy2 = deepcopy(q.children[1])
        copy3 = deepcopy(q.children[2])
        copy4 = deepcopy(q.children[3])
        q.children[0] = deepcopy(copy3)
        q.children[1] = deepcopy(copy4)
        q.children[2] = deepcopy(copy1)
        q.children[3] = deepcopy(copy2)
        for i in range(4):
            if isinstance(q.children[i], QuadTreeNodeInternal):
                q.mirror_helper(q.children[i])


class QuadTree:
    """
    The class for the overall quadtree
    """

    loss_level: float
    height: int
    width: int
    root: Optional[QuadTreeNode]  # safe to assume root is an internal node

    def __init__(self, loss_level: int = 0) -> None:
        """
        Precondition: the size of <pixels> is at least 1x1
        """
        self.loss_level = float(loss_level)
        self.height = -1
        self.width = -1
        self.root = None

    def build_quad_tree(self, pixels: List[List[int]],
                        mirror: bool = False) -> None:
        """
        Build a quad tree representing all pixels in <pixels>
        and assign its root to self.root

        <mirror> indicates whether the compressed image should be mirrored.
        See the assignment handout for examples of how mirroring works.
        """
        # print('building_quad_tree...')
        self.height = len(pixels)
        self.width = len(pixels[0])
        self.root = self._build_tree_helper(pixels)
        if mirror:
            self.root.mirror()
        return

    def _build_tree_helper(self, pixels: List[List[int]]) -> QuadTreeNode:
        """
        Build a quad tree representing all pixels in <pixels>
        and return the root

        Note that self.loss_level should affect the building of the tree.
        This method is where the compression happens.

        IMPORTANT: the condition for compressing a quadrant is the standard
        deviation being __LESS THAN OR EQUAL TO__ the loss level. You must
        implement this condition exactly; otherwise, you could fail some
        test cases unexpectedly.
        """
        #  working method
        standard_deviation = standard_deviation_and_mean(pixels)[0]
        mean = standard_deviation_and_mean(pixels)[1]
        if standard_deviation <= self.loss_level:
            return QuadTreeNodeLeaf(self.normal_round(mean))
        else:
            return_quad_tree = QuadTreeNodeInternal()
            quadrants = self._split_quadrants(pixels)
            for i in range(4):
                if quadrants[i] == [] or quadrants[i][0] == []:
                    return_quad_tree.children[i] = QuadTreeNodeEmpty()
                if quadrants[i] != [] and quadrants[i][0] != []:
                    return_quad_tree.children[i] = self._build_tree_helper(
                        quadrants[i])
            return return_quad_tree

    @staticmethod
    def normal_round(n):
        """
        Rounds decimals to the nearest whole number, without using bankers
        rounding
        """
        if n - math.floor(n) < 0.5:
            return math.floor(n)
        return math.ceil(n)

    @staticmethod
    def _split_quadrants(pixels: List[List[int]]) -> List[List[List[int]]]:
        """
        Precondition: size of <pixels> is at least 1x1
        Returns a list of four lists of lists, correspoding to the quadrants in
        the following order: bottom-left, bottom-right, top-left, top-right

        IMPORTANT: when dividing an odd number of entries, the smaller half
        must be the left half or the bottom half, i.e., the half with lower
        indices.

        Postcondition: the size of the returned list must be 4

        >>> example = QuadTree(0)
        >>> example._split_quadrants([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        [[[1]], [[2, 3]], [[4], [7]], [[5, 6], [8, 9]]]
        >>> example = QuadTree(0)
        >>> example._split_quadrants([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
        [[[1, 2], [5, 6]], [[3, 4], [7, 8]], [[9, 10], [13, 14]], [[11, 12], [15, 16]]]
        >>> example = QuadTree(0)
        >>> example._split_quadrants([[1, 2]])
        [[], [], [[1]], [[2]]]
        >>> example = QuadTree(0)
        >>> example._split_quadrants([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
        [[[1], [4]], [[2, 3], [5, 6]], [[7], [10]], [[8, 9], [11, 12]]]
        >>> example = QuadTree(0)
        >>> example._split_quadrants([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
        [[[1, 2]], [[3, 4]], [[5, 6], [9, 10]], [[7, 8], [11, 12]]]
        >>> QuadTree._split_quadrants([[1], [2], [3], [4]])
        [[[], []], [[1], [2]], [[], []], [[3], [4]]]
        """
        #  working method
        bottom_left = []
        bottom_right = []
        top_left = []
        top_right = []
        horizontal_middle = len(pixels) // 2
        vertical_middle = len(pixels[0]) // 2
        for i, row in enumerate(pixels):
            if i < horizontal_middle:
                bottom_left.append(row[:vertical_middle])
                bottom_right.append(row[vertical_middle:])
            else:
                top_left.append(row[:vertical_middle])
                top_right.append(row[vertical_middle:])
        return [bottom_left, bottom_right, top_left, top_right]

    def tree_size(self) -> int:
        """
        Return the number of nodes in the tree, including all Empty, Leaf, and
        Internal nodes.
        """
        return self.root.tree_size()

    def convert_to_pixels(self) -> List[List[int]]:
        """
        Return the pixels represented by this tree as a 2D matrix
        """
        return self.root.convert_to_pixels(self.width, self.height)

    def preorder(self) -> str:
        """
        return a string representing the preorder traversal of the quadtree.
        The string is a series of entries separated by comma (,).
        Each entry could be one of the following:
        - empty string '': represents a QuadTreeNodeInternal
        - string of an integer value such as '5': represents a QuadTreeNodeLeaf
        - string 'E': represents a QuadTreeNodeEmpty

        For example, consider the following tree with a root and its 4 children
                __      Root       __
              /      |       |        \
            Empty  Leaf(5), Leaf(8), Empty

        preorder() of this tree should return exactly this string: ",E,5,8,E"

        (Note the empty-string entry before the first comma)
        """
        return self.root.preorder()

    @staticmethod
    def restore_from_preorder(lst: List[str],
                              width: int, height: int) -> QuadTree:
        """
        Restore the quad tree from the preorder list <lst>
        The preorder list <lst> is the preorder string split by comma

        Precondition: the root of the tree must be an internal node (non-leaf)
        """
        tree = QuadTree()
        tree.width = width
        tree.height = height
        tree.root = QuadTreeNodeInternal()
        tree.root.restore_from_preorder(lst, 0)
        return tree


def maximum_loss(original: QuadTreeNode, compressed: QuadTreeNode) -> float:
    """
    Given an uncompressed image as a quad tree and the compressed version,
    return the maximum loss across all compressed quadrants.

    Precondition: original.tree_size() >= compressed.tree_size()

    Note: original, compressed are the root nodes (QuadTreeNode) of the
    trees, *not* QuadTree objects

    >>> pixels = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    >>> orig, comp = QuadTree(0), QuadTree(2)
    >>> orig.build_quad_tree(pixels)
    >>> comp.build_quad_tree(pixels)
    >>> maximum_loss(orig.root, comp.root)
    1.5811388300841898
    """
    return_max = 0
    print(original.preorder())
    print(compressed.preorder())
    if isinstance(compressed, QuadTreeNodeLeaf):
        return 0





if __name__ == '__main__':

    import doctest

    doctest.testmod()

    # import python_ta
    # python_ta.check_all()
