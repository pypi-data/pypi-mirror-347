from typing import Sequence
from dataclasses import dataclass

from helpers.maths import Vector, Matrix
from helpers.robot.simulate.types import (
    RobotDynamics,
)

from scipy.integrate import solve_ivp

import numpy as np


@dataclass(frozen=True)
class DivergenceChecker:
    divergence_threshold: float = 1e3

    def __call__(self, t: float, state: Vector) -> float:
        return 0.0 if np.linalg.norm(state) > self.divergence_threshold else 1.0

    @property
    def terminal(self) -> bool:
        return True


@dataclass(frozen=True)
class LsodaSolver:
    checker: DivergenceChecker = DivergenceChecker()

    @staticmethod
    def with_divergence_threshold(threshold: float) -> "LsodaSolver":
        """Creates an LSODA solver with the specified divergence threshold.

        Args:
            threshold: The divergence threshold for the solver.

        Returns:
            A new LSODA solver with the specified divergence threshold.
        """
        return LsodaSolver(checker=DivergenceChecker(threshold))

    def __call__(
        self,
        dynamics: RobotDynamics,
        *,
        initial_conditions: Sequence[float] | Vector,
        t_range: tuple[float, float],
        t_evaluation: Vector,
    ) -> Matrix:
        result = solve_ivp(
            fun=dynamics,
            jac=dynamics.jacobian(),
            y0=initial_conditions,
            t_span=t_range,
            t_eval=t_evaluation,
            method="LSODA",
            events=self.checker,
        )

        if result.status == 1:
            raise RuntimeError(
                "The simulation diverged. The system is unstable or the initial conditions are invalid."
            )

        return result.y


class EulerSolver:
    def __call__(
        self,
        dynamics: RobotDynamics,
        *,
        initial_conditions: Sequence[float] | Vector,
        t_range: tuple[float, float],
        t_evaluation: Vector,
    ) -> Matrix:
        states = []
        last_state = np.array(initial_conditions)
        last_t = t_range[0]

        for t in t_evaluation:
            delta_t = t - last_t
            derivative = dynamics(last_t, last_state)
            last_state = last_state + delta_t * derivative

            states.append(last_state)

        return np.array(states).T
