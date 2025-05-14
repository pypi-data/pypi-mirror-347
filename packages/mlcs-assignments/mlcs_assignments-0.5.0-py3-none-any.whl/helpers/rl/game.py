from typing import NamedTuple, Final, Sequence, Protocol
from dataclasses import dataclass, KW_ONLY

from helpers.maths import IntMatrix, BoolMatrix

import numpy as np


class GridGameSolver(Protocol):
    def solve(self, game: "GridGame") -> "Solution":
        """Find the optimal solution to the given grid game."""
        ...


class Position(NamedTuple):
    row: int
    column: int

    @staticmethod
    def center_of(grid: IntMatrix) -> "Position":
        """Returns the center position of a grid.

        Args:
            grid: The grid to find the center of.

        Returns:
            The center position of the grid.
        """
        rows, columns = grid.shape
        return Position(rows // 2, columns // 2)

    def within_bounds_of(self, grid: IntMatrix) -> bool:
        """Checks if the position is within the bounds of a grid.

        Args:
            grid: The grid to check against.

        Returns:
            True if the position is within the bounds of the grid, False otherwise.
        """
        rows, columns = grid.shape
        return 0 <= self.row < rows and 0 <= self.column < columns


class Move(NamedTuple):
    row: int
    column: int

    def apply(self, position: Position) -> Position:
        """Applies the move to a position.

        Args:
            position: The position to apply the move to.

        Returns:
            The new position after applying the move.
        """
        return Position(position.row + self.row, position.column + self.column)

    def __neg__(self) -> "Move":
        return Move(-self.row, -self.column)


class Moves:
    UP = Move(1, 0)
    DOWN = Move(-1, 0)
    LEFT = Move(0, -1)
    RIGHT = Move(0, 1)

    @staticmethod
    def all() -> Sequence[Move]:
        return (Moves.UP, Moves.DOWN, Moves.LEFT, Moves.RIGHT)


@dataclass(frozen=True)
class Solution:
    """A solution to a grid game.

    Attributes:
        moves: The moves made in the solution.
        reward: The total reward accumulated in the solution.
    """

    moves: Sequence[Move]
    reward: int


# TODO: Test and refactor this class
class GreedySolver:
    def solve(self, game: "GridGame") -> "Solution":
        all_moves = Moves.all()
        best_moves: list[Move] = []
        visited: set[Position] = set()
        total_reward = 0

        while True:
            next_moves: list[tuple[Move, int]] = []
            visited.add(game.current_position)

            # Find all possible moves and their rewards
            for move in all_moves:
                reward = game.move(move)
                next_moves.append((move, reward))
                game.undo()

            # If all moves give negative rewards, stop
            if max(r for _, r in next_moves) < 0:
                break

            # Choose the move with highest reward
            best_move, _ = max(next_moves, key=lambda x: x[1])

            # Make the move
            best_moves.append(best_move)
            total_reward += game.move(best_move)

            # If we're stuck, stop
            if game.current_position in visited:
                break

        return Solution(moves=best_moves, reward=total_reward)


@dataclass(frozen=True)
class StateChange:
    """A change in the state of a grid game.

    Attributes:
        move: The move that was made.
        reward: The reward for making the move.
        position: The new position after making the move.
        moves: The total number of moves made so far.
        accumulated_reward: The total reward accumulated so far.
    """

    start_position: Position
    reward_change: int
    was_covered: bool


class TransitionFunction(Protocol):
    def __call__(self, position: Position, move: Move) -> Position:
        """Calculates the next position after making a move."""
        ...


class RewardFunction(Protocol):
    def __call__(
        self,
        position: Position,
        move: Move,
        transition: TransitionFunction,
        *,
        rewards: IntMatrix,
        visited: BoolMatrix,
    ) -> int:
        """Calculates the reward for a move in the grid game."""
        ...


class EndGame(Exception):
    """This exception is raised when the game should end."""

    ...


class Policy(Protocol):
    def __call__(self, position: Position) -> Move:
        """Returns the move to make from a given position.

        Raises:
            EndGame: If the game should end.
        """
        ...

    def reset(self) -> None:
        """Resets the policy to its initial state.

        This should be called whenever the game is reset."""
        ...


class DeterministicTransition:
    def __call__(self, position: Position, move: Move) -> Position:
        return move.apply(position)


@dataclass
class CachedTransition:
    transition: TransitionFunction
    caching: bool = False
    last: Position | None = None

    def __call__(self, position: Position, move: Move) -> Position:
        if self.caching and self.last is not None:
            return self.last

        self.last = self.transition(position, move)
        return self.last

    def start(self) -> None:
        self.caching = True

    def stop(self) -> None:
        self.caching = False
        self.last = None


@dataclass(frozen=True)
class BoundaryChecked:
    grid: IntMatrix
    transition: TransitionFunction

    def __call__(self, position: Position, move: Move) -> Position:
        new_position = self.transition(position, move)
        return new_position if new_position.within_bounds_of(self.grid) else position


# TODO: Test this class
@dataclass
class GridGame:
    _: KW_ONLY
    safe_transition: Final[BoundaryChecked]
    cached_transition: Final[CachedTransition]
    original_transition: Final[TransitionFunction]
    reward_function: Final[RewardFunction]
    rewards: Final[IntMatrix]
    uncovered: Final[BoolMatrix]
    start_position: Final[Position]
    solver: Final[GridGameSolver]
    policy: Final[Policy | None] = None

    current_position: Position
    moves: int = 0
    accumulated_reward: int = 0
    last_change: StateChange | None = None
    solution: Solution | None = None

    @staticmethod
    def create(
        *,
        rows: int,
        columns: int,
        reward_function: RewardFunction,
        transition_function: TransitionFunction = DeterministicTransition(),
        reward_range: tuple[int, int] = (-5, 5),
        start_position: Position | None = None,
        solver: GridGameSolver = GreedySolver(),
        policy: Policy | None = None,
    ) -> "GridGame":
        """Creates a grid game with random rewards.

        Args:
            rows: The number of rows in the grid.
            columns: The number of columns in the grid.
            reward_function: The function to calculate rewards.
            transition_function: The function to calculate transitions (default is deterministic).
            reward_range: The range of rewards that can be generated (default is (-5, 5)).
            start_position: The starting position of the player in the grid (default is the center).
            solver: The solver to use to find the optimal solution (default is GreedySolver).
            policy: The policy to use for making moves (default is None).

        Returns:
            A grid game with random rewards.
        """
        assert rows > 0, "The number of rows must be positive."
        assert columns > 0, "The number of columns must be positive."
        assert reward_range[0] < reward_range[1], (
            "The lower bound of the reward range must be less than the upper bound."
        )

        rewards = random_rewards(rows=rows, columns=columns, reward_range=reward_range)
        start_position = start_position or Position.center_of(rewards)
        rewards[start_position] = 0

        uncovered = mask_for(rewards, start_position)
        cached_transition = CachedTransition(transition_function)
        game = GridGame(
            safe_transition=BoundaryChecked(rewards, cached_transition),
            cached_transition=cached_transition,
            original_transition=transition_function,
            reward_function=reward_function,
            rewards=rewards,
            uncovered=uncovered,
            start_position=start_position,
            solver=solver,
            policy=policy,
            current_position=start_position,
        )

        solution = solver.solve(game)

        return game.reset().with_solution(solution)

    def move(self, move: Move | None = None) -> int:
        """Moves the player in the grid game.

        Args:
            move: The move to make or None to use the policy.

        Returns:
            The reward for making the move.
        """
        if move is None:
            assert self.policy is not None, (
                "Either a move or a policy must be provided."
            )
            move = self.policy(self.current_position)

        self.cached_transition.start()

        reward = self.reward_function(
            position=self.current_position,
            move=move,
            transition=self.cached_transition,
            rewards=self.rewards,
            visited=self.uncovered,
        )

        new_position = self.safe_transition(position=self.current_position, move=move)

        self.last_change = StateChange(
            start_position=self.current_position,
            reward_change=reward,
            was_covered=self.uncovered[new_position],
        )

        self.uncovered[new_position] = True
        self.accumulated_reward += reward
        self.current_position = new_position
        self.moves += 1

        self.cached_transition.stop()

        return reward

    def undo(self) -> int:
        """Undoes the last move made in the grid game.

        Returns:
            The reward for undoing the last move.
        """
        assert (change := self.last_change) is not None, "No moves have been made yet."

        self.uncovered[self.current_position] = change.was_covered
        self.accumulated_reward -= change.reward_change
        self.current_position = change.start_position
        self.moves -= 1

        return -change.reward_change

    def reset(self) -> "GridGame":
        """Creates a new grid game starting fresh from the initial position."""
        if self.policy is not None:
            self.policy.reset()

        return GridGame(
            safe_transition=self.safe_transition,
            cached_transition=self.cached_transition,
            original_transition=self.original_transition,
            reward_function=self.reward_function,
            rewards=self.rewards,
            uncovered=mask_for(self.rewards, self.start_position),
            start_position=self.start_position,
            solver=self.solver,
            policy=self.policy,
            current_position=self.start_position,
            solution=self.solution,
        )

    def regenerate(self) -> "GridGame":
        """Creates a new grid game with different rewards."""
        return GridGame.create(
            rows=self.rows,
            columns=self.columns,
            reward_function=self.reward_function,
            transition_function=self.original_transition,
            reward_range=(self.rewards.min(), self.rewards.max()),
            start_position=self.start_position,
            solver=self.solver,
            policy=self.policy,
        )

    def with_solution(self, solution: Solution) -> "GridGame":
        """Creates a new grid game that has an optimal solution."""
        return GridGame(
            safe_transition=self.safe_transition,
            cached_transition=self.cached_transition,
            original_transition=self.original_transition,
            reward_function=self.reward_function,
            rewards=self.rewards,
            uncovered=self.uncovered,
            start_position=self.start_position,
            solver=self.solver,
            policy=self.policy,
            current_position=self.current_position,
            solution=solution,
        )

    def optimal_solution(self) -> Solution:
        """Returns the optimal solution to the grid game."""
        assert self.solution is not None, (
            "The optimal solution has not been computed yet."
        )

        return self.solution

    @property
    def rows(self) -> int:
        """The number of rows in the grid."""
        return self.rewards.shape[0]

    @property
    def columns(self) -> int:
        """The number of columns in the grid."""
        return self.rewards.shape[1]

    @property
    def all_positions(self) -> list[Position]:
        """Returns all valid positions in the grid."""
        return [Position(r, c) for r in range(self.rows) for c in range(self.columns)]

    @property
    def last_reward(self) -> int:
        """The reward for the last move made."""
        return self.last_change.reward_change if self.last_change else 0


def random_rewards(
    *, rows: int, columns: int, reward_range: tuple[int, int] = (-5, 5)
) -> IntMatrix:
    min_rewards, max_reward = reward_range

    # Extra shift to get more negative rewards
    rewards = (
        np.random.randint(*reward_range, size=(rows, columns)) - abs(max_reward) // 2
    )

    # Add pattern: higher rewards along edges and from center to right
    extra_rewards = abs(max_reward) // 2, 2 * abs(max_reward)

    rewards[0, :] += np.random.randint(*extra_rewards, size=columns)
    rewards[rows - 1, :] += np.random.randint(*extra_rewards, size=columns)
    rewards[:, 0] += np.random.randint(*extra_rewards, size=rows)
    rewards[:, columns - 1] += np.random.randint(*extra_rewards, size=rows)
    rewards[rows // 2, columns // 2 :] += np.random.randint(
        *extra_rewards, size=columns - columns // 2
    )

    return np.clip(rewards, min_rewards, max_reward)


def mask_for(grid: IntMatrix, start_position: Position) -> BoolMatrix:
    mask = np.zeros_like(grid, dtype=bool)
    mask[start_position] = True
    return mask
