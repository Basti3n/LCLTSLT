from dataclasses import dataclass, field

import arcade

from main.src.models.agent import Agent
from main.src.models.environment import Environment
from main.src.models.window import Window


@dataclass
class Game:
    environment: Environment
    agent: Agent = field(init=False)
    window: Window = field(init=False)

    def setup(self) -> None:
        # Initialiser l'environment
        self.agent = Agent(self.environment)
        # Lancer le jeu
        self.window = Window(self.agent)
        self.window.setup()
        arcade.run()
