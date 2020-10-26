"""Gaming Test"""

from rules import Rule, Standard
from settings import BLACK, WHITE
from controller import LocalGame


print(Rule.rules())
players = {BLACK: "Doge", WHITE: "Meow"}
game = LocalGame(15, 600, players, Standard())
game.start()
