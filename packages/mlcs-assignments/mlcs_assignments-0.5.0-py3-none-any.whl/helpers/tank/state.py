from dataclasses import dataclass, KW_ONLY

from helpers.maths import Vector


@dataclass(frozen=True)
class TankStates:
    """The states of a tank system over a period of time.

    Attributes:
        time: The time points.
        inlet_flow_rate: The inlet flow rates.
        liquid_height: The liquid heights.
        outlet_flow_rate: The outlet flow rates.
    """

    _: KW_ONLY
    time: Vector
    inlet_flow_rate: Vector
    liquid_height: Vector
    outlet_flow_rate: Vector

    def __post_init__(self) -> None:
        assert (
            len(self.time)
            == len(self.inlet_flow_rate)
            == len(self.liquid_height)
            == len(self.outlet_flow_rate)
        ), (
            f"Expected all vectors to have the same length."
            f"Got time: {len(self.time)}, inlet_flow_rate: {len(self.inlet_flow_rate)}, "
            f"liquid_height: {len(self.liquid_height)}, outlet_flow_rate: {len(self.outlet_flow_rate)}."
        )

    def until(self, index: int) -> "TankStates":
        return TankStates(
            time=self.time[:index],
            inlet_flow_rate=self.inlet_flow_rate[:index],
            liquid_height=self.liquid_height[:index],
            outlet_flow_rate=self.outlet_flow_rate[:index],
        )

    @property
    def time_range(self) -> tuple[float, float]:
        return self.time[0], self.time[-1]

    @property
    def flow_rate_range(self) -> tuple[float, float]:
        return (
            min(self.inlet_flow_rate.min(), self.outlet_flow_rate.min()),
            max(self.inlet_flow_rate.max(), self.outlet_flow_rate.max()),
        )

    @property
    def points(self) -> int:
        return len(self.time)
