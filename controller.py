"""
Game mode - controller:
    Game - Abstract Game Class
    SingleGame - LocalSingleGame
"""

import tkinter
from abc import abstractmethod
from threading import Thread
from typing import Callable, Dict, Tuple

from rules import Rule, GameWon, InvalidPosition, SwapRequest, RuleException
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
        self._pause = False

        # Make players
        self._curplayer: Player
        self._players: Dict[bool, Player] = dict()
        self._rule = rule

    @property
    def player(self) -> Player:
        """Return current player"""
        return self._curplayer

    @property
    def paused(self) -> bool:
        """Return if gaming paused"""
        return self._pause

    def toggle(self) -> None:
        """Toggle game player"""
        self._curplayer = self._players[not bool(self._curplayer)]
        self.player.active()

    @abstractmethod
    def swap(self, request: SwapRequest) -> None:
        """Swap player handler"""
        ...

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
            raise RuleException(error)
        except SwapRequest as error:
            self.swap(error)

    def restart(self) -> None:
        """Restart handler function"""
        self._game.reset()
        self._curplayer = self._players[True]
        self.player.active()

    def gaming(self) -> None:
        """Game logistic"""
        while position := self.player.event:
            
            # Check if gaming paused
            if self.paused:
                continue

            row, column = position
            try:
                self.click(row, column)
            except GameEndedError:
                break
            except SettedGridError:
                continue

            # For Rule check exception dont play piece
            except RuleException as _error:
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
        ...


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

    def swap(self, request: SwapRequest) -> None:
        """Swap handler for Local Game using tkinter"""
        labels = request.hint
        options = request.options
        title = request.SwapSelectionPanelTitle

        # Wrap all callback handlers
        _options: Dict[Tuple[str, ...], Callable[[], None]] = dict()
        for key, callback in options.items():
            _options[key] = lambda: callback(self._players)
        self._board.selpanel(title, labels, options).mainloop()

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
