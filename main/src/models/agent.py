from dataclasses import dataclass, field
from typing import Tuple

from main.resources.env_variable import ACTIONS
from main.src.models.environment import Environment
from main.src.models.policy import Policy

LIVES = 5


@dataclass
class Agent:
    environment: Environment
    lives: int = field(default=LIVES)
    policy: Policy = field(init=False)
    state: Tuple[int, int] = field(init=False)
    previous_state: Tuple[int, int] = field(init=False)
    score: int = field(init=False)
    coins: int = field(init=False)
    last_action: str = field(init=False)
    reward: int = field(init=False)

    def __post_init__(self) -> None:
        self.policy = Policy(self.environment.states.keys(), ACTIONS)
        self.reset()
        print(f'Tour 1 :')

    def reset(self) -> None:
        self.state = self.environment.starting_point
        self.previous_state = self.state
        self.environment.reset()
        self.score = 0
        self.coins = 0
        self.lives = LIVES

    def best_action(self) -> str:
        return self.policy.best_action(self.state)

    def do(self, action: str) -> None:
        self.previous_state = self.state
        self.state, self.reward = self.environment.apply(self.state, action)
        self.score += self.reward
        self.last_action = action

    def update_policy(self) -> None:
        self.policy.update(self.previous_state, self.state, self.last_action, self.reward)
