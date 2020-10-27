"""Gaming Test"""

from rules import Pro
from settings import BLACK, WHITE
from controller import LocalGame


players = {BLACK: "Doge", WHITE: "Meow"}
game = LocalGame(15, 600, players, Pro(15))
game.start()
