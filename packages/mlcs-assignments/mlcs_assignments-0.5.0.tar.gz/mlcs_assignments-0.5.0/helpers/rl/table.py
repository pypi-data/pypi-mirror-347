from typing import Protocol, Generic, TypeVar, Sequence, Self, overload
from dataclasses import dataclass, field


from helpers.maths import Matrix
from numpy.random import Generator

import numpy as np


StateT = TypeVar("StateT", bound="State", infer_variance=True)
ActionT = TypeVar("ActionT", bound="Action", infer_variance=True)


class Sortable(Protocol):
    def __lt__(self, other: Self) -> bool:
        """Returns whether this instance is less than the other instance."""
        ...


class Hashable(Protocol):
    def __hash__(self) -> int:
        """Returns the hash value of this instance."""
        ...

    def __eq__(self, other: object) -> bool:
        """Returns whether this instance is equal to the other instance."""
        ...


class State(Sortable, Hashable, Protocol):
    @property
    def value(self) -> float:
        """Returns the value of the state."""
        ...


class Action(Sortable, Hashable, Protocol):
    @property
    def value(self) -> float:
        """Returns the value of the action."""
        ...


class QTable(Protocol, Generic[StateT, ActionT]):
    @overload
    def get(self, state: StateT) -> Sequence[tuple[ActionT, float]]:
        """Returns all possible actions and their Q-values for the given state.

        Args:
            state: The state for which to get the Q-values.

        Returns:
            A sequence of tuples, where each tuple contains an action and its corresponding Q-value.

        Example:
            You can get the actions and Q-values for a state like this:

            ```python
            state = ... # Some state
            actions = q_table.get(state)

            print(actions)
            # This will print something like this:
            # [(action_1, q_value_1), (action_2, q_value_2), ...]
            ```
        """
        ...

    @overload
    def get(self, state: StateT, action: ActionT) -> float:
        """Returns the Q-value for the given state-action pair.

        Args:
            state: The state for which to get the Q-value.
            action: The action for which to get the Q-value.

        Returns:
            The Q-value for the given state-action pair.

        Example:
            You can get the Q-value for a state-action pair like this:

            ```python
            state = ... # Some state
            action = ... # Some action
            q_value = q_table.get(state, action)

            print(q_value)
            # This will print the Q-value for the state-action pair, like this:
            # 42.0
            ```
        """
        ...

    def update(self, state: StateT, action: ActionT, *, q_value: float) -> None:
        """Updates the Q-value for the given state-action pair.

        Args:
            state: The state for which to update the Q-value.
            action: The action for which to update the Q-value.
            q_value: The new Q-value for the state-action pair.

        Example:
            You can update the Q-value for a state-action pair like this:

            ```python
            state = ... # Some state
            action = ... # Some action
            new_q_value = ... # Some new Q-value
            q_table.update(state, action, q_value=new_q_value)
            ```
        """
        ...


class QValueInitializer(Protocol):
    def initialize(self, *, state_count: int, action_count: int) -> Matrix:
        """Creates a matrix of Q-values with the given dimensions."""
        ...


class ZeroInitializer:
    def initialize(self, *, state_count: int, action_count: int) -> Matrix:
        return np.zeros((state_count, action_count))


@dataclass(frozen=True)
class ConstantInitializer:
    value: float

    def initialize(self, *, state_count: int, action_count: int) -> Matrix:
        return np.full((state_count, action_count), self.value)


@dataclass(frozen=True)
class RandomInitializer:
    min_value: float = 0.0
    max_value: float = 1.0
    random: Generator = field(default_factory=np.random.default_rng)

    def initialize(self, *, state_count: int, action_count: int) -> Matrix:
        return self.random.uniform(
            self.min_value, self.max_value, (state_count, action_count)
        )


@dataclass(frozen=True)
class SimpleQTable(Generic[StateT, ActionT]):
    table: dict[StateT, dict[ActionT, float]]
    states: Sequence[StateT]
    actions: Sequence[ActionT]

    delta_state: float
    delta_action: float

    @staticmethod
    def create_for(
        *,
        states: Sequence[StateT],
        actions: Sequence[ActionT],
        initializer: QValueInitializer,
        delta_state: float,
        delta_action: float,
    ) -> "SimpleQTable":
        """Creates a simple Q-table with all Q-values initialized"""
        states = sorted(states)
        actions = sorted(actions)
        q_values = initializer.initialize(
            state_count=len(states), action_count=len(actions)
        )

        return SimpleQTable._from_q_values(
            q_values,
            states=states,
            actions=actions,
            delta_state=delta_state,
            delta_action=delta_action,
        )

    @staticmethod
    def from_file(
        file: str,
        *,
        states: Sequence[StateT],
        actions: Sequence[ActionT],
        delta_state: float,
        delta_action: float,
        verify: bool = True,
    ) -> "SimpleQTable":
        array = np.loadtxt(file)
        q_values = np.zeros((len(states), len(actions)))

        for i, row in enumerate(array):
            for j, (state, action, q_value) in enumerate(row):
                if verify:
                    assert state == states[i].value, (
                        f"Incorrect state at row {i}. Expected the state value "
                        f"to be {states[i].value}, but got {state}."
                    )
                    assert action == actions[j].value, (
                        f"Incorrect action at column {j}. Expected the action value "
                        f"to be {actions[j].value}, but got {action}."
                    )

                q_values[i, j] = q_value

        return SimpleQTable._from_q_values(
            q_values,
            states=states,
            actions=actions,
            delta_state=delta_state,
            delta_action=delta_action,
        )

    @overload
    def get(self, state: StateT) -> Sequence[tuple[ActionT, float]]: ...

    @overload
    def get(self, state: StateT, action: ActionT) -> float: ...

    def get(
        self, state: StateT, action: ActionT | None = None
    ) -> Sequence[tuple[ActionT, float]] | float:
        if action is None:
            return tuple(
                (action, value)
                for action, value in self.table[self._state_for(state)].items()
            )
        else:
            return self.table[self._state_for(state)][self._action_for(action)]

    def update(self, state: StateT, action: ActionT, *, q_value: float) -> None:
        self.table[self._state_for(state)][self._action_for(action)] = q_value

    def save_to(self, path: str) -> None:
        array = np.array(
            [
                [state.value, action.value, q_value]
                for state, actions in self.table.items()
                for action, q_value in actions.items()
            ]
        )

        np.savetxt(path, array)

    @staticmethod
    def _from_q_values(
        q_values: Matrix,
        *,
        states: Sequence[StateT],
        actions: Sequence[ActionT],
        delta_state: float,
        delta_action: float,
    ) -> "SimpleQTable":
        return SimpleQTable(
            table={
                state: {action: q_values[i, j] for j, action in enumerate(actions)}
                for i, state in enumerate(states)
            },
            states=states,
            actions=actions,
            delta_state=delta_state,
            delta_action=delta_action,
        )

    def _state_for(self, state: StateT) -> StateT:
        min_state = self.states[0].value
        index = int((state.value - min_state) / self.delta_state)
        index = np.clip(index, 0, len(self.states) - 1)

        return self.states[index]

    def _action_for(self, action: ActionT) -> ActionT:
        min_action = self.actions[0].value
        index = int((action.value - min_action) / self.delta_action)
        index = np.clip(index, 0, len(self.actions) - 1)

        return self.actions[index]
