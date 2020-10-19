"""Player model"""


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

    def __str__(self) -> str:
        """Return username"""
        return self._name

    def __bool__(self) -> bool:
        """Return color"""
        return self._color
