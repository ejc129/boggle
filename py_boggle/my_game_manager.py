import copy
import random
from typing import List, Optional, Set, Tuple

from py_boggle.boggle_dictionary import BoggleDictionary
from py_boggle.boggle_game import BoggleGame
from py_boggle.trie_dictionary import TrieDictionary

"""
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************

If you worked in a group on this project, please type the EIDs of your groupmates below (do not include yourself).
Leave it as TODO otherwise.
Groupmate 1: TODO
Groupmate 2: TODO
"""

SHORT = 3
CUBE_SIDES = 6

class MyGameManager(BoggleGame):
    """Your implementation of `BoggleGame`
    """

    def __init__(self):
        """Constructs an empty Boggle Game.

        A newly-constructed game is unplayable.
        The `new_game` method will be called to initialize a playable game.
        Do not call `new_game` here.

        This method is provided for you, but feel free to change it.
        """

        self.board: List[List[str]] # current game board
        self.size: int # board size
        self.words: List[str] # player's current words
        self.dictionary: TrieDictionary # the dictionary to use
        self.last_added_word: Optional[List[Tuple[int, int]]] # the position of the last added word, or None

    def new_game(self, size: int, cubefile: str, dictionary: TrieDictionary) -> None:
        """This method is provided for you, but feel free to change it.
        """
        with open(cubefile, 'r') as infile:
            faces = [line.strip() for line in infile]
        cubes = [f.lower() for f in faces if len(f) == CUBE_SIDES]
        if size < 2 or len(cubes) < size*size:
            raise ValueError('ERROR: Invalid Dimensions (size, cubes)')
        random.shuffle(cubes)
        # Set all of the game parameters
        self.board =[[random.choice(cubes[r*size + c])
                    for r in range(size)] for c in range(size)]
        self.size = size
        self.words = []
        self.dictionary = dictionary
        self.dictionary
        self.last_added_word = None



    def get_board(self) -> List[List[str]]:
        """This method is provided for you, but feel free to change it.
        """

        return self.board

    def find_word_in_board(self, word: str) -> Optional[List[Tuple[int, int]]]:
        """Helper method called by add_word()
        Expected behavior:
        Returns an ordered list of coordinates of a word on the board in the same format as get_last_added_word()
        (see documentation in boggle_game.py).
        If `word` is not present on the board, return None.
        """
        word = word.upper()

        # helper function START
        # depth first search
        def dfs(row, col, index, visited):
            # r = row
            # c = col
            # index = the letter of the word we're looking for

            # creates the base list to start adding onto
            if index == len(word):
                return []

            # stops out of bounds coordinates
            if not (0 <= row < self.size and 0 <= col < self.size):
                return None

            # stops wrong paths, and stops cubes from being used more than once
            if (row, col) in visited or self.board[row][col].upper() != word[index]:
                return None

            # recurse in (up to) 8 directions
            visited.add((row, col))
            for direction_row in [-1, 0, 1]:
                for direction_col in [-1, 0, 1]:
                    if direction_row == 0 and direction_col == 0:
                        continue
                    path = dfs(row + direction_row, col + direction_col, index + 1, visited)
                    if path is not None:
                        return [(row, col)] + path
            visited.remove((row, col))
            return None

        for row in range(self.size):
            for col in range(self.size):
                path = dfs(row, col, 0, set())
                if path is not None:
                    return path
        return None


    def add_word(self, word: str) -> int:
        """This method is provided for you, but feel free to change it.
        """
        word = word.upper()
        if (len(word) > SHORT and word not in self.words and self.dictionary.contains(word)):
            location = self.find_word_in_board(word)
            if location is not None:
                self.last_added_word = location
                self.words.append(word)
                return len(word) - SHORT
        return 0

    def get_last_added_word(self) -> Optional[List[Tuple[int, int]]]:
        """This method is provided for you, but feel free to change it.
        """
        return self.last_added_word

    def set_game(self, board: List[List[str]]) -> None:
        """This method is provided for you, but feel free to change it.
        """
        self.board = [[c.lower() for c in row] for row in board]

    def get_score(self) -> int:
        """This method is provided for you, but feel free to change it.
        """
        return sum([len(word) - SHORT for word in self.words])

    def dictionary_driven_search(self) -> Set[str]:
        """Find all words using a dictionary-driven search.

        The dictionary-driven search attempts to find every word in the
        dictionary on the board.

        Returns:
            A set containing all words found on the board.
        """

        found_words = set()

        # loop through all words in dictionary
        for word in self.dictionary:

            # prevents meaninglessly short words from being added
            if len(word) > SHORT:

                # returns the path
                path = self.find_word_in_board(word)

                if path is not None:
                    found_words.add(word)
        return found_words

    def board_driven_search(self) -> Set[str]:
        """Find all words using a board-driven search.

        The board-driven search constructs a string using every path on
        the board and checks whether each string is a valid word in the
        dictionary.

        Returns:
            A set containing all words found on the board.
        """
        found_words = set()


        # define helper function to call recursively
        # depth first search
        def dfs(row, col, node, path, visited):
            # row = row
            # column = col
            # path = the current letters traversed
            # visited = the cells we've already used once

            # check that our coordinate is not outside of bounds
            if not (0 <= row < self.size and 0 <= col < self.size):
                return
            if (row, col) in visited:
                return

            # reached a dead end, current combination not in dictionary
            letter = self.board[row][col].upper()
            if letter not in node.children:
                return

            # updating for recursion
            visited.add((row, col))
            node = node.children[letter]
            path += letter

            # add path of letters (word) into found words
            if len(path) > SHORT and node.is_word:
                found_words.add(path)

            # explore all 8 options, excluding the cells we've visited
            for direction_row in [-1, 0, 1]:
                for direction_col in [-1, 0, 1]:
                    if direction_row == 0 and direction_col == 0:
                        continue
                    dfs(row + direction_row, col + direction_col, node, path, visited)

            visited.remove((row, col))
        ### END HELPER FUNCTION

        # start recursion on every cell
        for r in range(self.size):
            for c in range(self.size):
                dfs(r, c, self.dictionary.root, "", set())

        return found_words

        raise NotImplementedError("method board_driven_search") # TODO: implement your code here

if __name__ == "__main__":
    import copy
    import random
    import string
    from typing import List, Optional, Set, Tuple

    import pytest
    from py_boggle.boggle_dictionary import BoggleDictionary
    from py_boggle.trie_dictionary import TrieDictionary
    from py_boggle.boggle_game import BoggleGame

    # read words file
    CUBE_FILE = "cubes.txt"
    WORDS_FILE = "words.txt"
    words: Set[str] = set()
    with open(WORDS_FILE, "r") as fin:
        for line in fin:
            line = line.strip().upper()
            words.add(line)

    # handout
    example_board = [
        ["E", "E", "C", "A"],
        ["A", "L", "E", "P"],
        ["H", "N", "B", "O"],
        ["Q", "T", "T", "Y"],
    ]
    example_words = set("""
    alec alee anele becap bent benthal blae blah blent bott cape capelan capo celeb cent
    cento clan clean elan hale hant lane lean leant leap lent lento neap open pace peace
    peel pele penal pent thae than thane toby toecap tope topee
    """.upper().strip().split())

    """Test a 3x3 board
    """

    game_dict = TrieDictionary()
    game_dict.load_dictionary(WORDS_FILE)

    game = MyGameManager()
    game.new_game(len(example_board), CUBE_FILE, game_dict)
    game.set_game(example_board)

    game.board_driven_search()

