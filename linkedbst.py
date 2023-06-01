"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
import random
import timeit
import sys

sys.setrecursionlimit(10000)

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            else:
                return 1 + max(height1(top.left), height1(top.right))
        if self.isEmpty():
            return 0
        else:
            return height1(self._root)

            

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        n_nodes = 2**(self.height() + 1) - 1
        if self.height() < 2 * log(n_nodes + 1, 2) - 1:
            return True
        return False
    
    def _range_find_recursive(self, node, start, end, result):
        if node is None:
            return None
        if start <= node.data <= end:
            result.append(node.data)
        if node.data > start:
            self._range_find_recursive(node.left, start, end, result)
        if node.data < end:
            self._range_find_recursive(node.right, start, end, result)

    def rangeFind(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''

        result = []
        self._range_find_recursive(self._root, low, high, result)
        return result

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        sorted_list = []

        def copy_nodes(node):
            if node is None:
                return
            copy_nodes(node.left)
            sorted_list.append(node.data)
            copy_nodes(node.right)

        copy_nodes(self._root)
        self.clear()

        def build_balanced_tree(lst, start_index, end_index):
            if start_index >= end_index:
                return None
            mid_index = (start_index + end_index) // 2
            new_node = BSTNode(lst[mid_index])
            new_node.left = build_balanced_tree(lst, start_index, mid_index)
            new_node.right = build_balanced_tree(lst, mid_index + 1, end_index)
            return new_node

        self._root = build_balanced_tree(sorted_list, 0, len(sorted_list))


    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        if self._root is None:
            return None

        successor = None
        current = self._root

        while current is not None:
            if current.data > item:
                successor = current.data
                current = current.left
            else:
                current = current.right

        return successor

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        if self._root is None:
            return None

        predecessor = None
        current = self._root

        while current is not None:
            if current.data < item:
                predecessor = current.data
                current = current.right
            else:
                current = current.left

        return predecessor
        
    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path: Path to the file.
        :type path: str
        """
        tree = LinkedBST()
        tree2 = LinkedBST()
        tree3 = LinkedBST()
        l_dict = []
        file = open(path, 'r', encoding='utf-8')
        counter = 0
        for line in file:
            counter += 1
            if counter <= 10000:
                l_dict.append(line.strip())
                tree.add(line.strip())
                tree3.add(line.strip())
        LinkedBST().rebalance(tree3)
        #випадковим чином закидую елементи в дерево
        random_elements = random.sample(l_dict, 10000)
        for ele in random_elements:
            tree2.add(ele)

        def select_random_elements():
            random_elements = random.sample(l_dict, 10000)

        def bintree_1():
            random_elements = random.sample(l_dict, 10000)
            for word in random_elements:
                tree.find(word)

        def bintree_2():
            random_elements = random.sample(l_dict, 10000)
            for word in random_elements:
                tree2.find(word)

        def bintree_3():
            random_elements = random.sample(l_dict, 10000)
            for word in random_elements:
                tree3.find(word)
        
            

        

        execution_time = timeit.timeit(select_random_elements, number=1)
        execution_time2 = timeit.timeit(bintree_1, number=1)
        ex_t3 = timeit.timeit(bintree_2, number=1)
        ex_t4 = timeit.timeit(bintree_3, number=1)
        print("Час виконання ліста:", execution_time, "сек.")
        print("Час виконання дерева:", execution_time2, "сек.")
        print("Час виконання рандом дерева:", ex_t3, "сек.")
        print("Час виконання баланс дерева:", ex_t4, "сек.")
LinkedBST.demo_bst(LinkedBST, 'binary_search_tree-master\words.txt')


            
