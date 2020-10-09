from dataclasses import dataclass, field
from typing import Any

from main.resources.env_variable import DEFAULT_LEARNING_RATE, DEFAULT_DISCOUNT_FACTOR


@dataclass
class Policy: #Q-table
    states: Any
    actions: Any
    learning_rate: float = field(default=DEFAULT_LEARNING_RATE)
    discount_factor: float = field(default=DEFAULT_DISCOUNT_FACTOR)
    table: dict = field(init=False)


    def __post_init__(self) -> None:
        self.table = {}
        for s in self.states:
            self.table[s] = {}
            for a in self.actions:
                self.table[s][a] = 0

    def __repr__(self):
        res = ''
        for state in self.table:
            res += f'{state}\t{self.table[state]}\n'
        return res

    def best_action(self, state) -> Any:
        action = None
        for a in self.table[state]:
            if action is None or self.table[state][a] > self.table[state][action]:
                action = a
        return action

    def update(self, previous_state, state, last_action, reward) -> None:
        #Q(st, at) = Q(st, at) + learning_rate * (reward + discount_factor * max(Q(state)) - Q(st, at))
        maxQ = max(self.table[state].values())
        self.table[previous_state][last_action] += self.learning_rate * \
            (reward + self.discount_factor * maxQ - self.table[previous_state][last_action])
