"""Gaming Test"""

from rules import FreeStyle, Standard
from settings import BLACK, WHITE
from controller import LocalGame


players = {BLACK: "Doge", WHITE: "Meow"}
game = LocalGame(15, 600, players, Standard())
game.start()
