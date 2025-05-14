from typing import Protocol, TypeVar, Generic, Sequence

StateT = TypeVar("StateT", bound="State", infer_variance=True)
ActionT = TypeVar("ActionT", infer_variance=True)


class State(Protocol):
    @property
    def value(self) -> float:
        """Returns the value of the state."""
        ...


class RewardFunction(Protocol, Generic[StateT]):
    def __call__(self, state: StateT, /) -> float:
        """Returns the reward for the given state."""
        ...


class Policy(Protocol, Generic[ActionT]):
    def __call__(self, actions: Sequence[tuple[ActionT, float]], /) -> ActionT:
        """Returns the action to take based on the policy."""
        ...
