from typing import Protocol, Sequence
from dataclasses import dataclass


import numpy as np


class Tank(Protocol):
    @property
    def max_inlet_flow(self) -> float:
        """Returns the maximum inflow rate of the tank."""
        ...


@dataclass(frozen=True)
class TankSystemState:
    """This represents the state of the tank system.

    Attributes:
        height_difference: The difference in height between the desired and
            actual liquid levels in the tank.
    """

    height_difference: float

    def __str__(self) -> str:
        return f"Δh = {self.height_difference} m"

    def __lt__(self, other: "TankSystemState") -> bool:
        return self.height_difference < other.height_difference

    @property
    def value(self) -> float:
        return self.height_difference


@dataclass(frozen=True)
class TankSystemAction:
    """This represents an action for the tank system.

    Attributes:
        inflow_rate: The inflow rate of the tank.
    """

    inflow_rate: float

    def __str__(self) -> str:
        return f"u = {self.inflow_rate} m³/s"

    def __lt__(self, other: "TankSystemAction") -> bool:
        return self.inflow_rate < other.inflow_rate

    @property
    def value(self) -> float:
        return self.inflow_rate


class DiscretizeTankMixin:
    def actions(self: Tank, delta_u: float) -> Sequence[TankSystemAction]:
        """Returns a sequence of all possible actions for the tank.

        Args:
            delta_u: The discretization step size for the inflow rate.

        Returns:
            A sequence of all possible actions for the tank.
        """
        u_max = self.max_inlet_flow
        points = int(u_max / delta_u) + 1

        return tuple(
            TankSystemAction(inflow_rate=inflow_rate)
            for inflow_rate in np.linspace(0, u_max, points)
        )
