from typing import Protocol
from dataclasses import dataclass, field

from helpers.rl import LearningAgent
from helpers.tank.discretize import TankSystemState, TankSystemAction


@dataclass(frozen=True)
class TrainingResult:
    learning_rate: float
    starting_height: float
    setpoint: float
    height_difference: float
    accumulated_reward: float


class RewardFunction(Protocol):
    def __call__(self, *, state: TankSystemState) -> float:
        """Returns the reward for transitioning to the given state."""
        ...


class SetpointProvider(Protocol):
    def __call__(self, *, at: float) -> float:
        """Returns the setpoint for the given time."""
        ...


@dataclass(frozen=True)
class SetpointRecorder:
    setpoint: SetpointProvider
    times: list[float] = field(default_factory=list, init=False)
    setpoints: list[float] = field(default_factory=list, init=False)

    def __call__(self, *, at: float) -> float:
        setpoint = self.setpoint(at=at)
        self.times.append(at)
        self.setpoints.append(setpoint)

        return setpoint


@dataclass
class LearningController:
    agent: LearningAgent[TankSystemState, TankSystemAction]
    reward: RewardFunction
    setpoint: SetpointProvider

    accumulated_reward: float = field(default=0, init=False)
    last_time_step: float | None = field(default=None, init=False)
    last_state: TankSystemState | None = field(default=None, init=False)
    last_action: TankSystemAction | None = field(default=None, init=False)

    def __call__(self, *, t: float, h: float) -> float:
        self.verify(t)

        setpoint = self.setpoint(at=t)
        state = TankSystemState(height_difference=setpoint - h)
        self.update(state)

        self.last_state = state
        self.last_action = self.agent(state)

        return self.last_action.inflow_rate

    def verify(self, t: float) -> None:
        assert self.last_time_step is None or t > self.last_time_step, (
            f"The time must be strictly increasing, but {t} is not greater than "
            f"the last time step {self.last_time_step}."
        )

    def update(self, state: TankSystemState) -> None:
        if self.last_state is None or self.last_action is None:
            return

        reward = self.reward(state=state)

        self.accumulated_reward += reward
        self.agent.update(
            state=self.last_state,
            action=self.last_action,
            next_state=state,
            reward=reward,
        )

    def reset(self) -> None:
        self.accumulated_reward = 0
        self.last_time_step = None
        self.last_state = None
        self.last_action = None
