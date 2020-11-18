import random
from dataclasses import dataclass, field
from typing import Tuple

from main.resources.env_variable import RIGHT, LEFT, REWARD_STUCK, REWARD_DEFAULT, REWARD_IMPOSSIBLE, \
    STILL, REWARD_HIT, REWARD_STILL, REWARD_HEAL

ROCK_FREQUENCY = 2
ROCK_FREQUENCY_MOVE = 10
HEAL_FREQUENCY = 50


@dataclass
class Environment:
    text: str
    states: dict = field(init=False)
    height: int = field(init=False)
    width: int = field(init=False)
    rock_frequency: int = field(default=ROCK_FREQUENCY, init=False)
    rock_frequency_move: int = field(default=ROCK_FREQUENCY_MOVE, init=False)
    heal_frequency: int = field(default=HEAL_FREQUENCY, init=False)
    starting_point: Tuple[int, int] = field(init=False)

    def __post_init__(self) -> None:
        self.create_default_state()

    def create_default_state(self) -> None:
        self.states = {}
        lines = self.text.strip().split('\n')
        self.height = len(lines)
        self.width = len(lines[0])
        for row in range(self.height):
            for col in range(len(lines[row])):
                self.states[(row, col)] = lines[row][col]
                if lines[row][col] == '.':
                    self.starting_point = (row, col)

    def reset(self):
        self.create_default_state()
        self.rock_frequency = ROCK_FREQUENCY
        self.rock_frequency_move = ROCK_FREQUENCY_MOVE
        self.heal_frequency = HEAL_FREQUENCY

    def apply(self, state: Tuple[int, int], action: str) -> Tuple[Tuple[int, int], int]:
        if action == STILL:
            new_state = (state[0], state[1])
        elif action == LEFT:
            new_state = (state[0], state[1] - 1)
        elif action == RIGHT:
            new_state = (state[0], state[1] + 1)
        else:
            new_state = None

        if new_state and new_state in self.states:
            # calculer la récompense
            if self.states[new_state] in ['#']:
                reward = REWARD_STUCK
            elif self.states[new_state] in ['*']:
                reward = REWARD_HIT
            elif self.states[new_state] in ['-']:
                self.states[new_state] = ' '
                reward = REWARD_HEAL
            else:
                reward = REWARD_DEFAULT
        else:
            # Etat impossible: grosse pénalité
            new_state = state
            reward = REWARD_IMPOSSIBLE

        return new_state, reward

    def update_rocks(self) -> None:
        # self.rock_frequency_move -= 1
        #
        # if self.rock_frequency_move >= 0:
        #     return
        # self.rock_frequency_move = ROCK_FREQUENCY_MOVE
        self.rock_frequency -= 1

        list_tmp = {}
        for x, y in self.states:
            resource = self.states[(x, y)]
            if resource == '*':
                if x + 1 < self.height - 1:
                    list_tmp[(x + 1, y)] = resource
            elif (x, y) not in list_tmp:
                list_tmp[(x, y)] = resource
        self.states = list_tmp

        if self.rock_frequency <= 0:
            block_number = random.randrange(5)
            for block in range(0, block_number):
                self.rock_frequency = ROCK_FREQUENCY

                rock_x = random.randrange(1, self.width - 1)
                rock_y = 0
                self.states[(rock_y, rock_x)] = '*'

    def update_heals(self) -> None:
        self.heal_frequency -= 1

        list_tmp = {}
        for x, y in self.states:
            resource = self.states[(x, y)]
            if resource == '-' and x + 1 < self.height - 1:
                list_tmp[(x + 1, y)] = resource
            elif (x, y) not in list_tmp:
                list_tmp[(x, y)] = resource
        self.states = list_tmp

        if self.heal_frequency <= 0:
            self.heal_frequency = HEAL_FREQUENCY

            heal_x = random.randrange(1, self.width - 1)
            heal_y = 0
            self.states[(heal_y, heal_x)] = '-'
