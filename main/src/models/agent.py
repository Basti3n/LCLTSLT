from dataclasses import dataclass, field
from typing import Any, Tuple

from main.resources.env_variable import ACTIONS
from main.src.models.environment import Environment

from main.src.models.policy import Policy


@dataclass
class Agent:
    environment: Environment
    game: Any
    policy: Policy = field(init=False)
    state: Tuple[int, int] = field(init=False)
    previous_state: Tuple[int, int] = field(init=False)
    score: int = field(init=False)
    last_action: str = field(init=False)
    reward: int = field(init=False)

    def __post_init__(self) -> None:
        self.policy = Policy(self.game.environment.states.keys(), ACTIONS)
        self.reset()

    def reset(self) -> None:
        self.state = self.game.environment.starting_point
        self.previous_state = self.state
        self.score = 0

    def best_action(self) -> str:
        return self.policy.best_action(self.state)

    def do(self, action: str) -> None:
        self.previous_state = self.state
        self.state, self.reward = self.environment.apply(self.state, action)
        self.score += self.reward
        self.last_action = action

    def update_policy(self) -> None:
        self.policy.update(self.game.agent.previous_state, self.game.agent.state, self.last_action, self.reward)
