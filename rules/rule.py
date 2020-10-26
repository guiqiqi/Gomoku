"""Rule abstract class"""

from abc import abstractmethod
from player import Player
from typing import Callable, Iterable, List, Tuple, Dict, Type


class RuleException(Exception):
    """Basic Rule Exception"""


class GameWon(RuleException):
    """Game Won by curret player"""

    def __init__(self, pieces: Iterable[Tuple[int, int]]) -> None:
        self.pieces = pieces


class InvalidPosition(RuleException):
    """Invalid position played"""

    def __init__(self, title: str, msg: str) -> None:
        self.title = title
        self.msg = msg


class SwapRequest(RuleException):
    """Request swap"""

    SwapSelectionPanelTitle = "Swap"

    def __init__(self, hint: Tuple[str, ...],
                 callbacks: Dict[Tuple[str, ...], Callable[
                     [Dict[bool, Player]], None
                 ]]) -> None:
        self.hint = hint
        self.options = callbacks


class Rule:
    """Abstract Rule class"""

    @abstractmethod
    def __init__(self) -> None:
        """
        Usually do not need implement this method
        Initialize additonal swapped flag when using Swap* Rules:
            flag: bool - have player been swaped
        """
        self._swapped = False
        ...

    def __repr__(self) -> str:
        """Console entity name"""
        return "<Rule {name}>".format(str(self))

    def __str__(self) -> str:
        """Return name of rule"""
        return type(self).__name__

    @staticmethod
    def rules() -> List[Type["Rule"]]:
        """Return all subclasses of Rule using reflection"""
        return Rule.__subclasses__()

    @abstractmethod
    def __call__(self, position: Tuple[int, int], step: int,
                 situation: Dict[int, Iterable[Tuple[int, int]]]) -> None:
        """
        The instantiated class needs to support this
        __call__ function so that the upper-level 
        click callback function can be successfully called.

        Function signature:
            __call__(self, position: Tuple[int, int], step: int,
                     situation: Iterable[Tuple[int, int]]) -> None
            position: The position of piece of this round
            step: Total step count
            situation: The situation of consecutive pieces 
                       around the current position.

        Function does not need to return a value,
        relevant process is determined by the exception thrown:
            GameWon(
                pieces: Iterable[Tuple[int, int]]
            ) - current player won this game
            InvalidPosition() - player could not play in this pos
            SwapRequest(
                options: Dict[str, Callable[[Dict[bool, Player]], Callable]]
                    Callback method vectors
            ) - Request swap player this turn
            ...
        """
