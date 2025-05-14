from typing import Protocol, TypeVar, Generic, Self, Any, Final
from dataclasses import dataclass, KW_ONLY, field

from helpers.maths import Vector, Matrix
from helpers.tank.control import Control, StatefulControl
from helpers.tank.state import TankStates
from helpers.tank.animation import OnFrame, do_nothing
from scipy.integrate import solve_ivp

import numpy as np

GOOD_STEP_SIZE: Final = 0.001

TankT = TypeVar("TankT", bound="Tank")


@dataclass(frozen=True)
class SimulationResults(Generic[TankT]):
    tank: TankT
    _: KW_ONLY
    time: Vector
    inlet_flow_rate: Vector
    outlet_flow_rate: Vector
    liquid_height: Vector

    def animate(self, *, take: int = 1, on_frame: OnFrame = do_nothing) -> Self:
        """Animates the simulation results.

        Args:
            take: The stride to use when animating the simulation results. A stride of 1 will animate
                every point in the simulation results.

        Returns:
            The same simulation results.
        """

        mask = np.concat(
            [np.arange(0, self.points - 2, take), np.array([self.points - 1])]
        )

        self.tank.animate(
            TankStates(
                time=self.time[mask],
                inlet_flow_rate=self.inlet_flow_rate[mask],
                liquid_height=self.liquid_height[mask],
                outlet_flow_rate=self.outlet_flow_rate[mask],
            ),
            on_frame=on_frame,
        )

        return self

    @property
    def points(self) -> int:
        return len(self.time)

    @property
    def final_liquid_height(self) -> float:
        return self.liquid_height[-1]


@dataclass(frozen=True)
class IntermediateValueRecorder:
    t: list[float] = field(default_factory=list)
    inlet_flow_rate: list[float] = field(default_factory=list)
    outlet_flow_rate: list[float] = field(default_factory=list)

    def record(
        self, *, t: float, inlet_flow_rate: float, outlet_flow_rate: float
    ) -> None:
        self.t.append(t)
        self.inlet_flow_rate.append(inlet_flow_rate)
        self.outlet_flow_rate.append(outlet_flow_rate)

    def inlet_flow_rates_for(self, t: Vector) -> Vector:
        return np.interp(t, self.t, self.inlet_flow_rate)

    def outlet_flow_rates_for(self, t: Vector) -> Vector:
        return np.interp(t, self.t, self.outlet_flow_rate)


class TankDynamicsJacobian(Protocol):
    def __call__(self, t: float, state: Vector) -> Matrix:
        """The Jacobian matrix of the right-hand side of the tank dynamics.

        Args:
            t: The current time point.
            state: The current state of the robot arm.

        Returns:
            The Jacobian matrix of the right-hand side of the tank dynamics. This matrix must be
            $n \\times n$, where $n$ is the number of states in the system. Entry $(i, j)$ of the
            matrix must be the partial derivative of the $i$-th element of the right-hand side with
            respect to the $j$-th state variable.
        """
        ...


class TankDynamics(Protocol):
    def __call__(self, t: float, state: Vector) -> Vector:
        """The dynamics of the tank at the given time point.

        Args:
            t: The current time point.
            state: The current state of the tank.

        Returns:
            The derivative of the state vector.

        Note:
            The state vector is typically just the liquid height in the tank.
        """
        ...

    def jacobian(self) -> TankDynamicsJacobian | None:
        """Returns a function that computes the Jacobian of the right-hand side of the tank dynamics.

        Returns:
            A function that computes the Jacobian of the right-hand side of the tank dynamics or None. If
            None, the Jacobian will be approximated numerically.
        """
        ...


class Tank(Protocol):
    def animate(self, states: TankStates, *, on_frame: OnFrame) -> Any:
        """Animates the tank over the specified time points."""
        ...

    def dynamics_for(
        self, control: Control, recorder: IntermediateValueRecorder
    ) -> TankDynamics:
        """Returns the dynamics of the tank for the given control signal."""
        ...

    def initial_conditions(self) -> Vector:
        """Returns the initial state of the tank as a state vector."""
        ...

    def results_for(
        self,
        t_range: tuple[float, float],
        recorded_points: int,
        t: Vector,
        inflow_rate: Vector,
        outflow_rate: Vector,
        solution: Matrix,
    ) -> "SimulationResults[Self]":
        """Returns the simulation results for the tank."""
        ...


class Solver(Protocol):
    def solve(
        self,
        dynamics: TankDynamics,
        initial_conditions: Vector,
        *,
        t_range: tuple[float, float],
        t: Vector,
    ) -> Matrix:
        """Solves the initial value problem for the given tank dynamics."""
        ...


class ScipySolver:
    def solve(
        self,
        dynamics: TankDynamics,
        initial_conditions: Vector,
        *,
        t_range: tuple[float, float],
        t: Vector,
    ) -> Matrix:
        return solve_ivp(
            fun=dynamics,
            jac=dynamics.jacobian(),
            y0=initial_conditions,
            t_span=t_range,
            t_eval=t,
            method="LSODA",
        ).y


class EulerSolver:
    def solve(
        self,
        dynamics: TankDynamics,
        initial_conditions: Vector,
        *,
        t_range: tuple[float, float],
        t: Vector,
    ) -> Matrix:
        y = initial_conditions
        delta_t = t[1] - t[0]

        solution = np.zeros((len(y), len(t)))
        solution[:, 0] = y

        for i in range(1, len(t)):
            y = y + delta_t * dynamics(t[i], y)
            solution[:, i] = y

        return solution


class SimulateTankMixin:
    def simulate(
        self: TankT,
        control: Control | StatefulControl,
        t_range: tuple[float, float],
        *,
        recorded_points: int | None = None,
        solver: Solver = EulerSolver(),
    ) -> SimulationResults[TankT]:
        """Simulate the tank with the given control signal.

        Args:
            control: The control signal to apply to the tank.
            t_range: The range of time points to simulate over.
            recorded_points: The number of points to use for simulating the tank. If None, the number
                of points will be determined automatically to match a step size of 1 ms.
            solver: The solver to use for solving the initial value problem. By default, the Euler
                method is used, since the dynamics are typically not stiff.

        Returns:
            The simulation results for the tank.
        """
        assert recorded_points is None or recorded_points > 1, (
            f"The number of recorded points must be greater than 1. Got: {recorded_points}"
        )

        assert t_range[0] < t_range[1], (
            f"The time range is incorrectly ordered. Got: {t_range}"
        )

        if isinstance(control, StatefulControl):
            control.reset()

        time_span = t_range[1] - t_range[0]
        recorded_points = recorded_points or int(time_span / GOOD_STEP_SIZE)
        t = np.linspace(*t_range, recorded_points)

        recorder = IntermediateValueRecorder()
        dynamics = self.dynamics_for(control, recorder)

        solution = solver.solve(
            dynamics=dynamics,
            initial_conditions=self.initial_conditions(),
            t_range=t_range,
            t=t,
        )

        return self.results_for(
            t_range=t_range,
            recorded_points=recorded_points,
            t=t,
            inflow_rate=recorder.inlet_flow_rates_for(t),
            outflow_rate=recorder.outlet_flow_rates_for(t),
            solution=solution,
        )
