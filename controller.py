"""
Game mode - controller:
    Game - Abstract Game Class
    SingleGame - LocalSingleGame
"""

import tkinter
from abc import abstractmethod
from threading import Thread
from typing import Dict

from rules import Rule, GameWon, InvalidPosition, SwapRequest
from model import Manager
from player import LocalPlayer, Player
from settings import GameEndedError, GameWonError, SettedGridError
from view import Board


class Game:
    """Gaming Abstract model"""

    def __init__(self, grids: int, size: int,
                 players: Dict[bool, str], rule: Rule) -> None:
        """Initial a new Game"""
        self._tkroot = tkinter.Tk()
        self._game = Manager(grids)
        self._size, self._grids = size, grids

        # Make players
        self._curplayer: Player
        self._players: Dict[bool, Player] = dict()
        self._rule = rule

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

        # Play piece for looking winner
        # If rule said is invalid, cancel this operation
        self._game[row, column] = bool(self.player)
        situation = self._game.find(row, column)

        # Check rule
        try:
            self._rule((row, column), self._game.steps, situation)
        except GameWon as error:
            self._game.end()
            raise GameWonError(error.pieces)
        except InvalidPosition as error:
            self._game[row, column] = None
            self.player.announce(error.title, error.msg)
            return
        except SwapRequest as error:
            # TODO: Add options callback with view.selpanel
            # options = error.options
            pass

        # Check Tie - dont check tie for now
        # if self._game.steps == self._grids ** 2:
        #     raise GameTiedError("Game has already tied")

    def restart(self) -> None:
        """Restart handler function"""
        self._game.reset()
        self._curplayer = self._players[True]
        self.player.active()

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
                 players: Dict[bool, str], rule: Rule) -> None:
        """Initlize a new local game"""
        super().__init__(grids, size, players, rule)

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

        # Select panel test
        # self._board.selpanel({
        #     ("Local - Person", "Free Style", "No"): lambda: print(1),
        #     ("Local - AI", "Free Style", "Yes"): lambda: print(2),
        #     ("Local - Person", "Free Style", "Yes"): lambda: print(3),
        #     ("Local - AI", "Free Style", "No"): lambda: print(4),
        # }, ("Game Type", "Game Rule", "Allow Undo")).mainloop()

        # Mainloop
        self._tkroot.mainloop()
