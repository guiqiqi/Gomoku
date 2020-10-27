"""Swap and Swap2 Rules"""


from player import Player
from .rule import Rule, GameWon, SwapRequest
from typing import List, Tuple, Dict


class Swap(Rule):
    """Swap Rule"""

    def __call__(self, position: Tuple[int, int], step: int,
                 situation: Dict[int, List[Tuple[int, int]]]) -> None:
        """
        Swap Rule:
            After third piece has been played, 
            Ask the white players if he want to swap
            After that using Gomoku Standard
        """
        def swapping(players: Dict[bool, Player]):
            """Swap players"""
            black, white = players[True], players[False]
            players[False] = black
            players[True] = white

        # Ask swapping
        if step == 3:
            request = SwapRequest(("White player: ",), {
                ("Take Black", ): swapping,
                ("Hold White", ): lambda _o: None
            })
            raise request

        # Check winning
        for pieces in situation.values():
            if len(pieces) == self.VJC:
                raise GameWon(pieces)
