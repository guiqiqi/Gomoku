"""Player model"""

from abc import abstractmethod
from queue import Queue
from typing import Tuple, Iterable
from view import Board


class Player:
    """Player for multiplayer mode"""

    def __init__(self, name: str, color: bool) -> None:
        """
        Initialize a player:
            sente: bool - if player is sente
            name: str - player name
        """
        self._color = color
        self._name = name
        self._event: "Queue[Tuple[int, int]]" = Queue(maxsize=1)

    def handler(self, row, column):
        """Set click event bounding to click function"""
        if not self._event.empty():
            self._event.get_nowait()
        self._event.put((row, column))

    @property
    def event(self) -> Tuple[int, int]:
        """Return event blocking way"""
        return self._event.get()

    def __str__(self) -> str:
        """Return username"""
        return self._name

    def __bool__(self) -> bool:
        """Return color"""
        return self._color

    @abstractmethod
    def play(self, row: int, column: int) -> None:
        """Play a piece"""
        ...

    @abstractmethod
    def active(self) -> None:
        """Active current user"""
        ...

    @abstractmethod
    def win(self, pieces: Iterable[Tuple[int, int]]) -> None:
        """This player win game"""
        ...

    @abstractmethod
    def tie(self) -> None:
        """Game tied"""
        ...


class LocalPlayer(Player):
    """Player for multiplayer mode"""

    def __init__(self, name: str, color: bool, board: Board) -> None:
        super().__init__(name, color)
        self._board = board

    def play(self, row: int, column: int) -> None:
        """Play piece using Board UI function"""
        self._board.play(row, column, bool(self))
        self._board.hint(not bool(self))

    def active(self) -> None:
        """Set active state as current player"""
        self._board.click = self.handler
        self._board.hint(bool(self))

    def win(self, pieces: Iterable[Tuple[int, int]]) -> None:
        """This player win game"""
        self._board.click = None
        self._board.win(self, pieces)

    def tie(self) -> None:
        """Game tied"""
        self._board.click = None
        self._board.showmsg("Info", "Game tied!")
