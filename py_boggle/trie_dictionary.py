import typing
from typing import Optional, Dict
from collections.abc import Iterator

from py_boggle.boggle_dictionary import BoggleDictionary


class TrieNode:
    """
    Our TrieNode class. Feel free to add new properties/functions, but 
    DO NOT edit the names of the given properties (children and is_word).
    """
    def __init__(self):
        self.children : Dict[str, TrieNode] = {} # maps a child letter to its TrieNode class
        self.is_word = False # whether or not this Node is a valid word ending



class TrieDictionary(BoggleDictionary):
    """
    Your implementation of BoggleDictionary.
    Several functions have been filled in for you from our solution, but you are free to change their implementations.
    Do NOT change the name of self.root, as our autograder will manually traverse using self.root
    """

    def __init__(self):
        super().__init__()
        self.dict = []
        self.root : TrieNode = TrieNode()

    def load_dictionary(self, filename: str) -> None:
        # Remember to add every word to the trie, not just the words over some length.

        # loads a list of words into self.dict
        super().load_dictionary(filename)

        # creates the tree structure
        for word in self.dict:
            node = self.root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.is_word = True


    def traverse(self, prefix: str) -> Optional[TrieNode]:
        """
        Traverse will traverse the Trie down a given path of letters `prefix`.
        If there is ever a missing child node, then returns None.
        Otherwise, returns the TrieNode referenced by `prefix`.
        """
        prefix = prefix.upper()
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def is_prefix(self, prefix: str) -> bool:
        # return super().is_prefix(prefix)
        prefix = prefix.upper()
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def contains(self, word: str) -> bool:
        # return super().contains(word)
        word = word.upper()
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        if node.is_word: return True
        return False


    def __iter__(self) -> typing.Iterator[str]:
        return my_iterator(self.dict)




class my_iterator:
    def __init__(self, word_list):
        # dunder in front of attribute makes it private, and enforces
        # must do _class__attribute to access it outside of the object
        self.__word_list = word_list
        self.__index = 0

    def __next__(self):
        ## returns the word and increments, if index within range
        if self.__index >= len(self.__word_list):
            raise StopIteration
        return_word = self.__word_list[self.__index]
        self.__index += 1
        return return_word

    def __iter__(self):
        return self

