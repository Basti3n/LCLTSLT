from main.resources.map import MAP
from main.src.models.environment import Environment
from main.src.models.game import Game

if __name__ == "__main__":
    Game(Environment(MAP)).setup()
