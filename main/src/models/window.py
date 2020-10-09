from dataclasses import dataclass
from typing import Any

import arcade
from arcade import SpriteList, Sprite

from main.resources.env_variable import SPRITE_SIZE
from main.src.models.agent import Agent


class Window(arcade.Window):
    agent: Agent
    walls: SpriteList
    player: Sprite
    goal: Sprite

    def __init__(self, agent: Agent):
        super().__init__(agent.environment.width * SPRITE_SIZE,
                         agent.environment.height * SPRITE_SIZE,
                         "Escape from ESGI")
        self.agent = agent

    def setup(self) -> None:
        self.walls = arcade.SpriteList()

        for state in self.agent.environment.states:
            if self.agent.environment.states[state] == '#':
                sprite = arcade.Sprite(":resources:images/tiles/grassCenter.png", 0.5)
                sprite.center_x = sprite.width * (state[1] + 0.5)
                sprite.center_y = sprite.height * (self.agent.environment.height - state[0] - 0.5)
                self.walls.append(sprite)

        self.goal = arcade.Sprite(":resources:images/items/flagGreen1.png", 0.5)
        self.goal.center_x = self.goal.width * (self.agent.environment.goal[1] + 0.5)
        self.goal.center_y = self.goal.height * (self.agent.environment.height - self.agent.environment.goal[0] - 0.5)

        self.player = arcade.Sprite(":resources:images/animated_characters/robot/robot_idle.png", 0.5)

        self.update_player_xy()

    def update_player_xy(self) -> None:
        self.player.center_x = self.player.height * (self.agent.state[1] + 0.5)
        self.player.center_y = self.player.height * (self.agent.environment.height - self.agent.state[0] - 0.5)

    def on_update(self, delta_time: float) -> None:
        if self.agent.state != self.agent.environment.goal:
            action = self.agent.best_action()
            self.agent.do(action)
            self.agent.update_policy()
            self.update_player_xy()

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.R:
            self.agent.reset()

    def on_draw(self) -> None:
        arcade.start_render()

        self.walls.draw()
        self.goal.draw()
        self.player.draw()

        arcade.draw_text(f'Score: {self.agent.score}', 10, 10, arcade.csscolor.WHITE, 20)