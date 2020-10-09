from dataclasses import dataclass, field
from typing import Tuple

from main.resources.env_variable import RIGHT, LEFT, REWARD_STUCK, REWARD_DEFAULT, REWARD_IMPOSSIBLE, \
    STILL, REWARD_DEAD


@dataclass
class Environment:
    text: str
    states: dict = field(init=False)
    height: int = field(init=False)
    width: int = field(init=False)
    starting_point: Tuple[int, int] = field(init=False)

    def __post_init__(self) -> None:
        self.states = {}
        lines = self.text.strip().split('\n')
        self.height = len(lines)
        self.width = len(lines[0])
        for row in range(self.height):
            for col in range(len(lines[row])):
                self.states[(row, col)] = lines[row][col]
                if lines[row][col] == '.':
                    self.starting_point = (row, col)

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
            if self.states[new_state] in ['#', '.']:
                reward = REWARD_STUCK
            elif self.states[new_state] in ['*']:  # Se prendre un cailloux: mourir
                reward = REWARD_DEAD
            else:
                reward = REWARD_DEFAULT
        else:
            # Etat impossible: grosse pénalité
            new_state = state
            reward = REWARD_IMPOSSIBLE

        return new_state, reward
