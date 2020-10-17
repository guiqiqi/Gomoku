"""Gaming Test"""

from settings import BLACK, WHITE
from player import Player
from game import SingleGame


players = {
    BLACK: Player("Doge"),
    WHITE: Player("Meow")
}

game = SingleGame(15, 600, players)
game.start()
