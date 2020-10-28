"""Swap and Swap2 Rules"""


from player import Player
from error import GameWon, SwapRequest
from .rule import Rule
from typing import List, Tuple, Dict


class Swap(Rule):
    """Swap Rule"""

    def swapping(self, players: Dict[bool, Player]):
        """Swap players"""
        black, white = players[True], players[False]

        # Swap player name
        black._color = False
        white._color = True

        # Swap player color
        players[True] = white
        players[False] = black

    def __call__(self, position: Tuple[int, int], step: int,
                 situation: Dict[int, List[Tuple[int, int]]]) -> None:
        """
        Swap Rule:
            After third piece has been played, 
            Ask the white players if he want to swap
            After that using Gomoku Standard
        """

        # Ask swapping
        if step == 3:
            request = SwapRequest(("Selection for White player: ",), {
                ("Take Black", ): lambda _o: self.swapping(_o),
                ("Hold White", ): lambda _o: None
            })
            raise request

        # Check winning
        for pieces in situation.values():
            if len(pieces) == self.VJC:
                raise GameWon(pieces)
