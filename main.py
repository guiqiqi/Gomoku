"""Gaming Test"""

from rules import Swap
from settings import BLACK, WHITE
from controller import LocalGame


players = {BLACK: "Doge", WHITE: "Meow"}
game = LocalGame(15, 600, players, Swap())
game.start()
