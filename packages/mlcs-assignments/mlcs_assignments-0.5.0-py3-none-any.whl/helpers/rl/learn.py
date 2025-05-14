from typing import Protocol, Generic, TypeVar


StateT = TypeVar("StateT", infer_variance=True)
ActionT = TypeVar("ActionT", infer_variance=True)


class LearningAgent(Protocol, Generic[StateT, ActionT]):
    def __call__(self, state: StateT) -> ActionT:
        """Returns the action to take for the given state."""
        ...

    def update(
        self, state: StateT, action: ActionT, next_state: StateT, reward: float
    ) -> None:
        """Updates the learning agent based on the observed transition."""
        ...

    @property
    def learning_rate(self) -> float:
        """Returns the learning rate of the agent."""
        ...

    @learning_rate.setter
    def learning_rate(self, value: float) -> None:
        """Sets the learning rate of the agent."""
        ...

    @property
    def discount_factor(self) -> float:
        """Returns the discount factor of the agent."""
        ...

    @discount_factor.setter
    def discount_factor(self, value: float) -> None:
        """Sets the discount factor of the agent."""
        ...
