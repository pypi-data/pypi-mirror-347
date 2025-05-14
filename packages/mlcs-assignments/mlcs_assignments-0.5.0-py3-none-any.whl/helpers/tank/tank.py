from dataclasses import dataclass, KW_ONLY

from helpers.tank.animation import VisualizeTankMixin
from helpers.tank.simulate import SimulateTankMixin
from helpers.tank.dynamics import TankDynamicsMixin
from helpers.tank.discretize import DiscretizeTankMixin

from math import pi, sqrt


@dataclass
class Tank(
    VisualizeTankMixin, SimulateTankMixin, TankDynamicsMixin, DiscretizeTankMixin
):
    name: str
    _: KW_ONLY
    height: float
    diameter: float
    outlet_constant: float
    max_inlet_flow: float
    liquid_height: float

    @staticmethod
    def create(
        name: str,
        *,
        height: float,
        diameter: float,
        outlet_constant: float,
        max_inlet_flow: float,
        liquid_height: float = 0,
    ) -> "Tank":
        return Tank(
            name,
            height=height,
            diameter=diameter,
            outlet_constant=outlet_constant,
            max_inlet_flow=max_inlet_flow,
            liquid_height=liquid_height,
        )

    def liquid_height_is(self, height: float) -> "Tank":
        self.liquid_height = height
        return self

    def inlet_flow_rate_for(self, control: float) -> float:
        return max(0, min(control, self.max_inlet_flow))

    def outlet_flow_rate_for(self, height: float) -> float:
        return self.outlet_constant * sqrt(height)

    @property
    def area(self) -> float:
        return pi * (self.diameter / 2) ** 2
