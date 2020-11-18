import arcade
from arcade import SpriteList, Sprite
import random

from main.resources.env_variable import SPRITE_SIZE
from main.resources.sprites.sprite import *
from main.src.models.agent import Agent


class Window(arcade.Window):
    agent: Agent
    walls: SpriteList
    rocks: SpriteList
    heals: SpriteList
    player: Sprite

    def __init__(self, agent: Agent):
        super().__init__(agent.environment.width * SPRITE_SIZE,
                         agent.environment.height * SPRITE_SIZE,
                         "Escape from ESGI")
        self.set_update_rate(1 / 60)
        self.agent = agent
        self.WIDTH = (agent.environment.width - 2) * SPRITE_SIZE
        self.HEIGHT = agent.environment.height * SPRITE_SIZE
        self.turn = 2
        self.maxturns = 30

    def setup(self) -> None:
        self.walls = arcade.SpriteList()
        self.rocks = arcade.SpriteList()
        self.heals = arcade.SpriteList()
        for state in self.agent.environment.states:
            if self.agent.environment.states[state] == '#':
                sprite = arcade.Sprite(":resources:images/tiles/grassCenter.png", 0.5)
                sprite.center_x = sprite.width * (state[1] + 0.5)
                sprite.center_y = sprite.height * (self.agent.environment.height - state[0] - 0.5)
                self.walls.append(sprite)
            if self.agent.environment.states[state] == '*':
                # sprite = ROCK
                sprite = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", 0.5)
                sprite.center_x = sprite.width * (state[1] + 0.5)
                sprite.center_y = sprite.height * (self.agent.environment.height - state[0] - 0.5)
                self.rocks.append(sprite)
            if self.agent.environment.states[state] == '-':
                sprite = arcade.Sprite(":resources:images/items/gold_1.png", 1)
                sprite.center_x = sprite.width * (state[1] + 0.5)
                sprite.center_y = sprite.height * (self.agent.environment.height - state[0] - 0.5)
                self.heals.append(sprite)

        self.player = arcade.Sprite(":resources:images/animated_characters/robot/robot_idle.png", 0.5)
        # self.player = ASTERIX

        self.update_player_xy()

    def update_player_xy(self) -> None:
        self.player.center_x = self.player.height * (self.agent.state[1] + 0.5)
        self.player.center_y = self.player.height * (self.agent.environment.height - self.agent.state[0] - 0.5)

    def on_update(self, delta_time: float) -> None:
        if self.agent.lives > 0:
            action = self.agent.best_action()
            self.setup()
            self.agent.environment.update_rocks()
            self.agent.environment.update_heals()
            self.agent.do(action)
            self.agent.update_policy()
            self.update_player_xy()
            self.update_rocks()
            self.remove_rocks()
            self.update_heal_player()
            self.update_heal_rocks()
        elif self.turn <= self.maxturns:
            [print(str(x) + " -> " + str(self.agent.policy.table[x])) for x in self.agent.policy.table if self.agent.policy.table[x] != {'R': 0, 'L': 0, 'S': 0}]
            print(self.agent.policy.table)
            self.agent.reset()
            self.turn += 1
            print("\n" + "-" * 90 + "\n")
            print(f'Tour {self.turn}')

    def update_rocks(self) -> None:
        self.rocks.move(0, -4)
        hit_list = arcade.check_for_collision_with_list(self.player, self.rocks)
        for rock in hit_list:
            sprite = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", 0.5)
            x = (rock.center_x / sprite.width) - 0.5
            self.agent.lives -= 1
            rock.remove_from_sprite_lists()
            self.agent.update_score('HIT')
            print(f' - rock: c{int(x)}')
            self.agent.environment.states[14, (int(x))] = ' '

    def remove_rocks(self) -> None:
        for rock in self.rocks:
            hit_list = arcade.check_for_collision_with_list(rock, self.walls)
            if len(hit_list) != 0:
                rock.remove_from_sprite_lists()
                self.agent.update_score('DODGE')

    def update_heal_player(self) -> None:
        hit_list = arcade.check_for_collision_with_list(self.player, self.heals)
        for heal in hit_list:
            sprite = arcade.Sprite(":resources:images/items/gold_1.png", 1)
            x = (heal.center_x / sprite.width) - 0.5
            self.agent.lives += 1
            heal.remove_from_sprite_lists()
            self.agent.update_score('HEAL')
            print(f' - heal: c{int(x)}')
            self.agent.environment.states[14, (int(x))] = ' '

    def update_heal_rocks(self) -> None:
        for heal in self.heals:
            hit_list = arcade.check_for_collision_with_list(heal, self.rocks)
            if len(hit_list) != 0:
                heal.remove_from_sprite_lists()

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.R:
            self.agent.reset()
        elif key == arcade.key.BACKSPACE:
            self.agent.lives -= 1

    def on_draw(self) -> None:
        arcade.start_render()

        self.walls.draw()
        self.rocks.draw()
        self.heals.draw()
        self.player.draw()

        arcade.draw_text(f'Score: {self.agent.score}', 10, 10, arcade.csscolor.WHITE, 20)
        arcade.draw_text(f'Live: {self.agent.lives}', 10, 40, arcade.csscolor.WHITE, 20)
