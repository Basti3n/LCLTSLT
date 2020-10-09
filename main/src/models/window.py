import arcade
from arcade import SpriteList, Sprite

from main.resources.env_variable import SPRITE_SIZE
from main.src.models.agent import Agent


class Window(arcade.Window):
    agent: Agent
    walls: SpriteList
    rocks: SpriteList
    player: Sprite

    def __init__(self, agent: Agent):
        super().__init__(agent.environment.width * SPRITE_SIZE,
                         agent.environment.height * SPRITE_SIZE,
                         "Escape from ESGI")
        self.agent = agent

    def setup(self) -> None:
        self.walls = arcade.SpriteList()
        self.rocks = arcade.SpriteList()

        for state in self.agent.environment.states:
            if self.agent.environment.states[state] == '#':
                sprite = arcade.Sprite(":resources:images/tiles/grassCenter.png", 0.5)
                sprite.center_x = sprite.width * (state[1] + 0.5)
                sprite.center_y = sprite.height * (self.agent.environment.height - state[0] - 0.5)
                self.walls.append(sprite)
            if self.agent.environment.states[state] == '*':
                sprite = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", 0.5)
                sprite.center_x = sprite.width * (state[1] + 0.5)
                sprite.center_y = sprite.height * (self.agent.environment.height - state[0] - 0.5)
                self.rocks.append(sprite)

        self.player = arcade.Sprite(":resources:images/animated_characters/robot/robot_idle.png", 0.5)
        # self.player = ASTERIX

        self.update_player_xy()

    def update_player_xy(self) -> None:
        self.player.center_x = self.player.height * (self.agent.state[1] + 0.5)
        self.player.center_y = self.player.height * (self.agent.environment.height - self.agent.state[0] - 0.5)

    def on_update(self, delta_time: float) -> None:
        if self.agent.lives > 0:
            action = self.agent.best_action()
            self.agent.do(action)
            self.agent.update_policy()
            self.update_player_xy()
            self.update_rocks()

    def update_rocks(self) -> None:
        hit_list = arcade.check_for_collision_with_list(self.player, self.rocks)

        # Loop through each colliding sprite, remove it.
        for rock in hit_list:
            self.agent.lives -= 1
            rock.remove_from_sprite_lists()

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.R:
            self.agent.reset()
        elif key == arcade.key.BACKSPACE:
            self.agent.lives -= 1

    def on_draw(self) -> None:
        arcade.start_render()

        self.walls.draw()
        self.rocks.draw()
        self.player.draw()

        arcade.draw_text(f'Score: {self.agent.score}', 10, 10, arcade.csscolor.WHITE, 20)
        arcade.draw_text(f'Live: {self.agent.lives}', 10, 40, arcade.csscolor.WHITE, 20)
