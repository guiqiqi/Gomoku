"""
Game mode - controller:
    Game - Abstract Game Class
    SingleGame - LocalSingleGame
"""

from abc import abstractmethod
from view import Board
from model import Manager
from player import Player, LocalPlayer
from settings import GameEndedError, GameTiedError, GameWonError, SettedGridError

import tkinter
from threading import Thread
from typing import Dict


class Game:
    """Gaming Abstract model"""

    def __init__(self, grids: int, size: int,
                 players: Dict[bool, str]) -> None:
        """Initial a new Game"""
        self._tkroot = tkinter.Tk()
        self._game = Manager(grids)
        self._size, self._grids = size, grids

        # Make players
        self._curplayer: Player
        self._players: Dict[bool, Player] = dict()

    @property
    def player(self) -> Player:
        """Return current player"""
        return self._curplayer

    def toggle(self) -> None:
        """Toggle game player"""
        self._curplayer = self._players[not bool(self._curplayer)]
        self.player.active()

    def click(self, row: int, column: int) -> None:
        """Click handler function"""
        # Check if game already over
        if self._game.ended:
            raise GameEndedError("Game has already ended!")

        # Play piece
        self._game[row, column] = bool(self.player)

        # Check Win
        search = self._game.find(row, column)
        for _, pieces in search.items():
            if len(pieces) == self._game.VJC:
                self._game.end()
                raise GameWonError(pieces)

        # Check Tie
        if self._game.steps == self._grids ** 2:
            raise GameTiedError("Game has already tied")

    def restart(self) -> None:
        """Restart handler function"""
        self._game.reset()

    def gaming(self) -> None:
        """Game logistic"""
        while position := self.player.event:
            row, column = position
            try:
                self.click(row, column)
            except GameEndedError:
                break
            except SettedGridError:
                continue
            except GameWonError as error:
                self.player.play(row, column)
                self.player.win(error.pieces)
                break
            except GameTiedError:
                self.player.tie()
                break
            self.player.play(row, column)
            self.toggle()

        # Restore resources
        ...

    @abstractmethod
    def start(self) -> None:
        """Start game"""


class LocalGame(Game):
    """LocalGame"""

    def __init__(self, grids: int, size: int,
                 players: Dict[bool, str]) -> None:
        """Initlize a new local game"""
        super().__init__(grids, size, players)

        # Initialize tkUI
        self._board = Board(self._tkroot, self._size, self._grids)
        self._board.click = self.click
        self._board.restart = self.restart

        # Initialize gamer
        for color, name in players.items():
            self._players[color] = LocalPlayer(name, color, self._board)

    def start(self) -> None:
        """Start Local Game with UI settings etc."""

        # Bind sente player
        self._curplayer = self._players[True]
        self.player.active()

        # Draw UI and run tk mainloop in thread
        self._board.draw()
        thread = Thread(target=self.gaming)
        thread.setDaemon(True)
        thread.setName("Gaming")
        thread.start()

        # Mainloop
        self._tkroot.mainloop()
