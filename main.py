"""Gaming Test"""

from settings import BLACK, WHITE
from player import Player
from controller import SingleGame


players = {
    BLACK: Player("Doge", color=BLACK),
    WHITE: Player("Meow", color=WHITE)
}

game = SingleGame(15, 600, players)
game.start()
