from typing import Protocol, runtime_checkable


class Control(Protocol):
    """This represents a control system for the tank system."""

    def __call__(self, *, t: float, h: float) -> float:
        """Returns the control signal defining the inflow rate at the given time.

        Args:
            t: The current time.
            h: The current height of the liquid in the tank.

        Returns:
            The control signal defining the inflow rate.
        """
        ...


@runtime_checkable
class StatefulControl(Control, Protocol):
    def reset(self) -> None:
        """Resets the state of the control system."""
        ...
