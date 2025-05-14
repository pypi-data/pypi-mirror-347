from typing import Protocol
from dataclasses import dataclass

from helpers.maths import Matrix, Vector
from helpers.tank.control import Control
from helpers.tank.simulate import (
    TankDynamics,
    SimulationResults,
    IntermediateValueRecorder,
    TankT,
)


import numpy as np


class Tank(Protocol):
    def inlet_flow_rate_for(self, control: float) -> float:
        """Returns the inlet flow rate for the given control value."""
        ...

    def outlet_flow_rate_for(self, height: float) -> float:
        """Returns the outlet flow rate for the given liquid height."""
        ...

    @property
    def area(self) -> float:
        """Returns the cross-sectional area of the tank."""
        ...

    @property
    def liquid_height(self) -> float:
        """Returns the current height of the liquid in the tank."""
        ...

    @property
    def height(self) -> float:
        """Returns the total height of the tank."""
        ...


@dataclass(frozen=True)
class SimpleTankDynamics:
    tank: Tank
    control: Control
    recorder: IntermediateValueRecorder
    limiting_factor: float = 10.0

    def __call__(self, t: float, state: Vector) -> Vector:
        """Returns the derivative of the tank height.

        Note:
            The state vector contains just the liquid height in the tank.
            The derivative is calculated directly from inflow - outflow.
        """
        h = state[0]
        inlet_flow_rate = self.tank.inlet_flow_rate_for(self.control(t=t, h=h))
        outlet_flow_rate = self.tank.outlet_flow_rate_for(h)

        # The inlet flow rate is limited by the available space in the tank. We
        # use a smooth function to limit the flow rate to the maximum possible value.
        space_left = self.tank.height - h
        inlet_flow_rate = inlet_flow_rate * np.tanh(self.limiting_factor * space_left)

        self.recorder.record(
            t=t, inlet_flow_rate=inlet_flow_rate, outlet_flow_rate=outlet_flow_rate
        )

        dh_dt = (inlet_flow_rate - outlet_flow_rate) / self.tank.area

        return np.array([dh_dt])

    def jacobian(self) -> None:
        return None


class TankDynamicsMixin:
    def dynamics_for(
        self: Tank, control: Control, recorder: IntermediateValueRecorder
    ) -> TankDynamics:
        return SimpleTankDynamics(self, control, recorder)

    def initial_conditions(self: Tank) -> Vector:
        return np.array([self.liquid_height])

    def results_for(
        self: TankT,
        t_range: tuple[float, float],
        recorded_points: int,
        t: Vector,
        inflow_rate: Vector,
        outflow_rate: Vector,
        solution: Matrix,
    ) -> SimulationResults[TankT]:
        return SimulationResults(
            tank=self,
            time=t,
            inlet_flow_rate=inflow_rate,
            outlet_flow_rate=outflow_rate,
            liquid_height=solution[0],
        )
