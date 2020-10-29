"""Gaming Test"""

from rules import Swap2
from settings import BLACK, WHITE
from controller import LocalGame

size = 15
players = {BLACK: "Doge", WHITE: "Meow"}
game = LocalGame(size, 600, players, Swap2())
game.start()
