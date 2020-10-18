"""
Game mode - controller:
    Game - Abstract Game Class
    SingleGame - LocalSingleGame
"""

from view import Board
from model import Manager
from player import Player
from settings import GameEndedError

import tkinter
from typing import Dict, abstractmethod


class Game:
    """Gaming Abstract model"""

    def __init__(self, grids: int, size: int,
                 players: Dict[bool, Player],
                 sente: bool, mpmode: bool) -> None:
        """Initial a new Game"""
        self._players = players
        self._tkroot = tkinter.Tk()
        self._game = Manager(grids)
        self._size, self._grids = size, grids
        self._board = Board(
            self._tkroot, self._size,
            self._grids, sente, mpmode)
        self._board.click = self.click
        self._board.restart = self.restart

    @abstractmethod
    def click(self, row: int, column: int) -> None:
        """Click handler function"""

    @abstractmethod
    def restart(self) -> None:
        """Restart handler function"""

    def start(self) -> None:
        """Start game"""
        self._board.draw()
        self._tkroot.mainloop()


class SingleGame(Game):
    """Single game mode"""

    def __init__(self, grids: int, size: int,
                 players: Dict[bool, Player]) -> None:
        """Initialize a Single game"""
        super().__init__(grids, size, players,
                         sente=True, mpmode=False)

    def restart(self) -> None:
        """Restart game will reset board"""
        self._game.reset()

    def click(self, row: int, column: int) -> None:
        """Click handler function for single player"""
        # Check if game already over
        if self._game.ended:
            raise GameEndedError("Game has already ended!")

        current = self._game.turn
        self._game[row, column] = current

        # Check win
        search = self._game.find(row, column)
        for _, pieces in search.items():
            if len(pieces) == self._game.VJC:
                player = self._players[current]
                self._board.win(player, current, pieces)
                self._game.end()
                raise GameEndedError("{username} has won game!".format(
                    username=str(player)))
