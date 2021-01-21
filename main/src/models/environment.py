import random
from dataclasses import dataclass, field
from typing import Tuple

from main.resources.env_variable import RIGHT, LEFT, REWARD_STUCK, REWARD_DEFAULT, REWARD_IMPOSSIBLE, \
    STILL, REWARD_HIT, REWARD_STILL, REWARD_HEAL, REWARD_GOTO_HEAL, REWARD_ALMOST_HIT

ROCK_FREQUENCY = 3
ROCK_FREQUENCY_MOVE = 2
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
        self.print_states()

    def reset(self):
        self.create_default_state()
        self.rock_frequency = ROCK_FREQUENCY
        self.rock_frequency_move = ROCK_FREQUENCY_MOVE
        self.heal_frequency = HEAL_FREQUENCY

    def apply(self, state: Tuple[int, int], action: str) -> Tuple[Tuple[int, int], int]:
        reward = 0
        if action == STILL:
            new_state = (state[0], state[1])
        elif action == LEFT:
            new_state = (state[0], state[1] - 1)
        elif action == RIGHT:
            new_state = (state[0], state[1] + 1)
        else:
            new_state = None

        if new_state and new_state in self.states:
            (ynew, xnew) = new_state
            (y, x) = state
            fov = 5
            above = [self.states[pos, x] for pos in range(y - 3, y)]  # Above the current position
            above_new = [self.states[pos, xnew] for pos in range(y - 3, y)]  # Above the current position
            left = [self.states[y, pos] for pos in range((1 if x - fov < 1 else x - fov), x)]  # Left Heal check
            right = [self.states[y, pos] for pos in range(x, (21 if x + fov > 21 else x + fov + 1))]  # Right Heal check
            # calculer la récompense
            if self.states[new_state] in ['#']:
                # print('stuck')
                reward += REWARD_STUCK
            if self.states[new_state] in ['-']:
                # print('healed')
                self.states[new_state] = ' '
                reward += REWARD_HEAL
            if self.states[new_state] in ['*']:
                # print('hit')
                reward += REWARD_HIT
            else:
                if action == STILL:
                    reward += REWARD_STILL
                else:
                    reward += REWARD_DEFAULT
            if '*' in above:
                # print('rock < 3 block above curr pos')
                reward += REWARD_ALMOST_HIT
            if '*' in above_new:
                # print('rock < 3 block above new pos')
                reward += REWARD_ALMOST_HIT
            if '-' in left and action != LEFT:
                # print('Heal on left')
                reward += (REWARD_GOTO_HEAL * (x - left[::-1].index('-')))
            if '-' in right and action != RIGHT:
                # print('Heal on right')
                reward += (REWARD_GOTO_HEAL * (1 + right.index('-')))
        else:
            # Etat impossible: grosse pénalité
            new_state = state
            reward = REWARD_IMPOSSIBLE

        return new_state, reward

    def update_rocks(self) -> None:
        self.rock_frequency_move -= 1

        if self.rock_frequency_move >= 0:
            return
        self.rock_frequency_move = ROCK_FREQUENCY_MOVE
        self.rock_frequency -= 1

        list_tmp = {}
        for x, y in self.states:
            resource = self.states[(x, y)]
            if resource == '*':
                if x + 1 < self.height - 1:
                    list_tmp[(x + 1, y)] = resource
                    list_tmp[(x, y)] = " "
                else:
                    list_tmp[(x + 1, y)] = "#"
                list_tmp[(x, y)] = " "
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
                list_tmp[(x, y)] = " "
            elif (x, y) not in list_tmp:
                list_tmp[(x, y)] = resource
        self.states = list_tmp

        if self.heal_frequency <= 0:
            self.heal_frequency = HEAL_FREQUENCY

            heal_x = random.randrange(1, self.width - 1)
            heal_y = 0
            self.states[(heal_y, heal_x)] = '-'

    def print_states(self):
        print("\n" + "-" * 90 + "\n")
        for y, x in self.states:
            pos = (y, x)
            val = self.states[pos]
            if val == '#' and x != 0 and y != 15 and y != 0:
                print(pos, val)
            else:
                sep = ''
                if x < 10:
                    sep += ' '
                if y < 10:
                    sep += ' '
                print(pos, val, sep=sep, end='')
        print("\n" + "-" * 90 + "\n")

    def is_states_full(self):
        total_state = {}
        for i in range(0, 16):
            for j in range(0, 21):
                total_state[(i, j)] = 0
        if all(key in total_state for key in self.states):
            print("keys are present")
        else:
            print("keys are not present")
            for key in total_state:
                if key not in self.states:
                    print(key, "is not in")
