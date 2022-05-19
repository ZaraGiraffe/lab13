"""
File: linkedbst.py
Author: Ken Lambert
"""

import sys
sys.setrecursionlimit(1000000)

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log2

INF = 10**30


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self.root = None
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

        return recurse(self.root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self.root)
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

        recurse(self.root)
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

        return recurse(self.root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self.root = None
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
            self.root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self.root)
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
        preRoot.left = self.root
        parent = preRoot
        direction = 'L'
        currentNode = self.root
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
            self.root = None
        else:
            self.root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self.root
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
        now = self.root

        def height1(nod):
            if not nod:
                return 0
            else:
                return 1 + max(height1(nod.right), height1(nod.left))

        return height1(now)-1

    def is_balanced(self):
        return self.height() < 2 * log2(self._size+1) - 1

    def range_find(self, low, high):
        mas = []

        def add(nod):
            if not nod:
                return
            if nod.data >= low and nod.data <= high:
                mas.append(nod.data)
            if nod.data >= low:
                add(nod.left)
            if nod.data <= high:
                add(nod.right)

        add(self.root)
        mas.sort()
        return mas

    def rebalance(self):
        now = self.root
        mas = []

        def dfs(nod):
            if not nod:
                return
            else:
                mas.append(nod)
                dfs(nod.left)
                dfs(nod.right)
                nod.left, nod.right = None, None

        dfs(now)
        mas.sort(key=lambda x: x.data)

        def cr(l, r):
            if l > r:
                return None
            if l == r:
                return mas[l]
            else:
                m = (l + r) // 2
                mas[m].left = cr(l, m-1)
                mas[m].right = cr(m+1, r)
                return mas[m]

        self.root = cr(0, len(mas)-1)

    def successor(self, item):
        now = self.root

        def find(nod):
            if not nod:
                return None
            if nod.data <= item:
                return find(nod.right)
            else:
                d2 = find(nod.left)
                if not d2:
                    return nod.data
                return min(nod.data, d2)

        return find(now)

    def predecessor(self, item):
        now = self.root

        def find(nod):
            if not nod:
                return None
            if nod.data >= item:
                return find(nod.left)
            else:
                d2 = find(nod.right)
                if not d2:
                    return nod.data
                return max(nod.data, d2)

        return find(now)

    def demo_bst(self, path, sample_size=1000):
        letter = """Warning!!!
        I don't know why, but code here perfectly works on lists of words less than 10000,
        but when I tried to make list bigger my program crashes. I think its because python 
        can't handle big amount of data
        """
        print(letter)
        import time
        import numpy as np
        from random import sample

        words = []
        with open(path, 'r') as file:
            for line in file:
                words.append(line.strip())

        mas = sample(words, sample_size)
        mas.sort()

        """first"""
        st = time.time()
        for i in mas:
            mas.index(i)
        en = time.time() - st
        print(f'find random {sample_size} elements in list: {en}')

        """second"""
        self.root = BSTNode(words[0])
        now = self.root
        for i in range(1, len(words)):
            nxt = BSTNode(words[i])
            now.right = nxt
            now, nxt = nxt, now
        self._size = len(words)
        st = time.time()
        for i in mas:
            assert(self.find(i))
        en = time.time() - st
        self.clear()
        print(f'find random {sample_size} elements in BST without balancing and without randomized addition of elements: {en}')

        """third"""
        mas = np.random.permutation(mas)
        for i in words:
            self.add(i)
        st = time.time()
        for i in mas:
            assert(self.find(i))
        en = time.time() - st
        mas.sort()
        self.clear()
        print(f'find random {sample_size} elements in BST without balancing, but with randomized addition of elements: {en}')

        """fourth"""
        for i in words:
            self.add(i)
        self.rebalance()
        st = time.time()
        for i in mas:
            assert (self.find(i))
        en = time.time() - st
        print(f'find random {sample_size} elements in BST with balancing: {en}')
