"""Test gaming"""

import tkinter
from typing import Dict
from model import Manager
from view import Board


class Game:
    """Test gaming"""

    def __init__(self, grids: int, size: int, users: Dict[bool, str]) -> None:
        """Inital a game"""
        self._users = users
        self._tkroot = tkinter.Tk()
        self._game = Manager(grids)
        self._board = Board(self._tkroot, size, grids)
        self._board.click = self.click

    def click(self, row, column) -> bool:
        """Click handler function"""

        # Check over
        current = self._game.turn
        if current == None:
            raise RuntimeError("Game over!")

        self._game[row, column] = current
        self._game.turn = not current

        # Check win
        search = self._game.find(row, column)
        for _, pieces in search.items():
            if len(pieces) == self._game.VJC:
                self._board.win(self._users[current],
                                current, pieces)
                self._game.turn = None
                raise RuntimeError("Game Over!")

        return current

    def start(self) -> None:
        """Start game"""
        self._board.draw()
        self._tkroot.mainloop()


# Test start game
game = Game(15, 500, {
    True: "Doge", False: "Meow"
})
game.start()
