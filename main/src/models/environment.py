from dataclasses import dataclass
from typing import Tuple, Any

from main.resources.env_variable import RIGHT, LEFT, REWARD_STUCK, REWARD_GOAL, REWARD_DEFAULT, REWARD_IMPOSSIBLE, UP, \
    DOWN


@dataclass
class Environment:
    text: str

    def __post_init__(self):
        self.states = {}
        lines = self.text.strip().split('\n')
        self.height = len(lines)
        self.width = len(lines[0])
        for row in range(self.height):
            for col in range(len(lines[row])):
                self.states[(row, col)] = lines[row][col]
                if lines[row][col] == '.':
                    self.starting_point = (row, col)
                elif lines[row][col] == '*':
                    self.goal = (row, col)

    def apply(self, state, action) -> Tuple[Any, Any]:
        if action == UP:
            new_state = (state[0] - 1, state[1])
        elif action == DOWN:
            new_state = (state[0] + 1, state[1])
        elif action == LEFT:
            new_state = (state[0], state[1] - 1)
        elif action == RIGHT:
            new_state = (state[0], state[1] + 1)
        else:
            new_state = None

        if new_state and new_state in self.states:
            #calculer la récompense
            if self.states[new_state] in ['#', '.']:
                reward = REWARD_STUCK
            elif self.states[new_state] in ['*']: #Sortie du labyrinthe : grosse récompense
                reward = REWARD_GOAL
            else:
                reward = REWARD_DEFAULT
        else:
            #Etat impossible: grosse pénalité
            new_state = state
            reward = REWARD_IMPOSSIBLE

        return new_state, reward
