"""Player model"""


class Player:
    """Player for multiplayer mode"""

    def __init__(self, name: str) -> None:
        """
        Initialize a player:
            name: str - player name
        """
        self._name = name

    def __str__(self) -> str:
        """Return username"""
        return self._name
