from typing import Protocol, Sequence

from helpers.ui import basic_animation_configuration
from helpers.tank.state import TankStates
from helpers.tank.geometry import Cylinder, Trace

from plotly.graph_objects import Figure, Frame, Scatter
from plotly.subplots import make_subplots
from concurrent.futures import ProcessPoolExecutor, Future
from multiprocessing import cpu_count
from tqdm import tqdm


class OnFrame(Protocol):
    def __call__(self, figure: Figure, *, index: int, total: int) -> Figure:
        """This function is called after generating each frame of the animation.

        Args:
            figure: The figure representing the current frame.
            index: The index of the current frame.
            total: The total number of frames.

        Note:
            You can assume the figure is fully prepared and ready to be displayed.
        """
        ...


def do_nothing(figure: Figure, *, index: int, total: int) -> Figure:
    """Does nothing."""
    return figure


class Tank(Protocol):
    def draw(self, *, show: bool = True) -> Figure:
        """Draws the tank in its current state."""
        ...

    def draw_state_diagrams(
        self, states: TankStates, *, show: bool = True
    ) -> tuple[Figure, Figure]:
        """Draws the state diagrams of the tank system."""
        ...

    def liquid_height_is(self, height: float) -> "Tank":
        """Returns a new tank with the liquid height set to the given value."""
        ...

    @property
    def name(self) -> str:
        """The name of the tank."""
        ...

    @property
    def height(self) -> float:
        """The height of the tank."""
        ...

    @property
    def diameter(self) -> float:
        """The diameter of the tank."""
        ...

    @property
    def liquid_height(self) -> float:
        """The height of the liquid in the tank."""
        ...

    def _draw_height_diagram(self, states: TankStates) -> Figure:
        """Draws the height diagram of the tank system."""
        ...

    def _draw_flow_diagram(self, states: TankStates) -> Figure:
        """Draws the flow diagram of the tank system."""
        ...

    def _draw_tank_surface(self) -> Sequence[Trace]:
        """Draws the surface of the tank."""
        ...

    def _draw_liquid_surface(self) -> Sequence[Trace]:
        """Draws the surface of the liquid in the tank."""
        ...

    def _draw_inlet(self) -> Sequence[Trace]:
        """Draws the inlet of the tank."""
        ...

    def _draw_outlet(self) -> Sequence[Trace]:
        """Draws the outlet of the tank."""
        ...

    def _configure_layout_of(self, figure: Figure) -> None:
        """Configures the layout of the figure."""
        ...


class VisualizeTankMixin:
    TANK_COLOR = "rgba(0, 0, 0, 0.1)"
    LIQUID_COLOR = "rgba(0, 0, 255, 0.3)"
    INLET_COLOR = "rgba(0, 255, 0, 0.25)"
    OUTLET_COLOR = "rgba(255, 0, 0, 0.25)"

    def animate(
        self: Tank, states: TankStates, *, on_frame: OnFrame = do_nothing
    ) -> None:
        """Animates the tank system over time.

        Args:
            states: The states of the tank system over time.
        """

        frames = animation_frames_for(self, states, on_frame=on_frame)

        def with_progress(figure: Figure, index: int) -> Frame:
            return frame_with_progress_from(
                figure, time=states.time[index - 1], total=states.time[-1]
            )

        prepared_frames = [
            with_progress(frame, index=index)
            for index, frame in enumerate(
                tqdm(frames, desc="Preparing frames", unit=" frame"), start=1
            )
        ]

        figure = animation_figure(frames=prepared_frames)

        figure.show()

    def draw(self: Tank, *, show: bool = True) -> Figure:
        """Draws the tank in its current state.

        Args:
            show: Whether to display the visualization immediately.

        Returns:
            A Plotly figure representing the tank.
        """
        figure = Figure()

        figure.add_traces(self._draw_tank_surface())
        figure.add_traces(self._draw_liquid_surface())
        figure.add_traces(self._draw_inlet())
        figure.add_traces(self._draw_outlet())

        self._configure_layout_of(figure)

        if show:
            figure.show()

        return figure

    def draw_state_diagrams(
        self: Tank, states: TankStates, *, show: bool = True
    ) -> tuple[Figure, Figure]:
        """Draws the state diagrams of the tank system.

        Args:
            states: The states of the tank system.
            show: Whether to display the visualization immediately.

        Returns:
            A tuple containing the height and flow diagrams.
        """
        height_diagram = self._draw_height_diagram(states)
        flow_diagram = self._draw_flow_diagram(states)

        if show:
            height_diagram.show()
            flow_diagram.show()

        return height_diagram, flow_diagram

    def _draw_height_diagram(self: Tank, states: TankStates) -> Figure:
        t_0, t_f = states.time_range
        figure = Figure()

        figure.add_trace(
            Scatter(
                x=states.time,
                y=states.liquid_height,
                mode="lines",
                name="Liquid Height",
                line=dict(color="blue"),
            )
        )

        figure.add_trace(
            Scatter(
                x=[t_0, t_f],
                y=[self.height, self.height],
                mode="lines",
                name="Tank Height",
                line=dict(color="black", dash="dash"),
            )
        )

        figure.update_layout(title="Liquid Height Over Time")

        figure.update_xaxes(title_text="Time (s)", range=states.time_range)
        figure.update_yaxes(title_text="Height (m)", range=[0, self.height * 1.25])

        return figure

    def _draw_flow_diagram(self: Tank, states: TankStates) -> Figure:
        figure = Figure()

        figure.add_trace(
            Scatter(
                x=states.time,
                y=states.inlet_flow_rate,
                mode="lines",
                name="Inlet Flow Rate",
                line=dict(color="green"),
            )
        )

        figure.add_trace(
            Scatter(
                x=states.time,
                y=states.outlet_flow_rate,
                mode="lines",
                name="Outlet Flow Rate",
                line=dict(color="red"),
            )
        )

        figure.update_xaxes(title_text="Time (s)", range=states.time_range)
        figure.update_yaxes(
            title_text="Flow Rate (m³/s)",
            range=[
                0,
                max(states.inlet_flow_rate.max(), states.outlet_flow_rate.max()) * 1.1,
            ],
        )

        figure.update_layout(title="Flow Rates Over Time")

        return figure

    def _draw_tank_surface(self: Tank) -> Sequence[Trace]:
        return Cylinder(
            center=(0, 0, self.height / 2),
            normal=(0, 0, 1),
            radius=self.diameter / 2,
            height=self.height,
            color=VisualizeTankMixin.TANK_COLOR,
            name="Tank",
        ).traces()

    def _draw_liquid_surface(self: Tank) -> Sequence[Trace]:
        return Cylinder(
            center=(0, 0, self.liquid_height / 2),
            normal=(0, 0, 1),
            radius=self.diameter / 2,
            height=self.liquid_height,
            color=VisualizeTankMixin.LIQUID_COLOR,
            name="Liquid",
        ).traces()

    def _draw_inlet(self: Tank) -> Sequence[Trace]:
        return Cylinder(
            center=(0, 0, self.height),
            normal=(0, 0, 1),
            radius=self.diameter / 8,
            height=self.height / 10,
            color=VisualizeTankMixin.INLET_COLOR,
            name="Inlet",
            text="Inlet",
        ).traces()

    def _draw_outlet(self: Tank) -> Sequence[Trace]:
        return Cylinder(
            center=(0, 0, 0),
            normal=(0, 0, 1),
            radius=self.diameter / 8,
            height=self.height / 10,
            color=VisualizeTankMixin.OUTLET_COLOR,
            name="Outlet",
            text="Outlet",
        ).traces()

    def _configure_layout_of(
        self: Tank, figure: Figure, *, padding: float = 0.25
    ) -> None:
        def pad(range_: tuple[float, float]) -> tuple[float, float]:
            return range_[0] - padding, range_[1] + padding

        figure.update_layout(
            title=f"{self.name} the Tank",
            scene=dict(
                xaxis=dict(
                    title="X", range=pad((-self.diameter / 2, self.diameter / 2))
                ),
                yaxis=dict(
                    title="Y", range=pad((-self.diameter / 2, self.diameter / 2))
                ),
                zaxis=dict(title="Z", range=pad((0, self.height))),
                aspectmode="cube",
            ),
        )


def display_setpoint(*, times: Sequence[float], setpoints: Sequence[float]) -> OnFrame:
    """Creates an on-frame callback that displays the setpoint on the tank diagram.

    Args:
        setpoints: The setpoints to display.
    """

    def on_frame(figure: Figure, *, index: int, total: int) -> Figure:
        time_index = int(index * len(times) / (total - 1))

        figure.add_trace(
            Scatter(
                x=times[: time_index + 1],
                y=setpoints[: time_index + 1],
                mode="lines",
                name="Setpoint",
                line=dict(color="red", dash="dash"),
            ),
            row=1,
            col=2,
        )

        return figure

    return on_frame


def animation_frames_for(
    tank: Tank,
    states: TankStates,
    *,
    on_frame: OnFrame,
    min_core_count: int = 4,
    min_state_count: int = 500,
) -> list[Figure]:
    if (cores := cpu_count()) < min_core_count or states.points < min_state_count:
        return [
            on_frame(
                create_frame_for(
                    tank, states.until(i + 1), states.time_range, states.flow_rate_range
                ),
                index=i,
                total=states.points,
            )
            for i in tqdm(
                range(states.points),
                total=states.points,
                desc="Creating animation frames",
                unit=" frame",
            )
        ]
    else:
        with ProcessPoolExecutor(max_workers=cores - 2) as executor:
            futures: list[Future] = []
            frames: list[Figure] = []
            time_range = states.time_range
            flow_rate_range = states.flow_rate_range

            for step in tqdm(
                range(states.points),
                desc="Splitting animation tasks",
                unit=" task",
                total=states.points,
            ):
                future = executor.submit(
                    create_frame_for,
                    tank,
                    states.until(step + 1),
                    time_range,
                    flow_rate_range,
                )
                futures.append(future)

            for i, future in enumerate(
                tqdm(
                    futures,
                    desc="Creating animation frames",
                    unit=" frame",
                    total=states.points,
                )
            ):
                frames.append(on_frame(future.result(), index=i, total=states.points))

            return frames


def create_frame_for(
    tank: Tank,
    states: TankStates,
    time_range: tuple[float, float],
    flow_rate_range: tuple[float, float],
) -> Figure:
    tank_figure = tank.liquid_height_is(states.liquid_height[-1]).draw(show=False)
    height_diagram, flow_diagram = tank.draw_state_diagrams(states, show=False)

    return combine_figures(
        f"{tank.name} the Tank",
        tank_figure=tank_figure,
        height_diagram=height_diagram,
        flow_diagram=flow_diagram,
        time_range=time_range,
        flow_rate_range=flow_rate_range,
    )


def combine_figures(
    title: str,
    *,
    tank_figure: Figure,
    height_diagram: Figure,
    flow_diagram: Figure,
    time_range: tuple[float, float],
    flow_rate_range: tuple[float, float],
) -> Figure:
    def pad(range_: tuple[float, float]) -> tuple[float, float]:
        return range_[0] - 0.1, range_[1] + 0.1

    figure = make_subplots(
        rows=2,
        cols=2,
        column_widths=[0.5, 0.5],
        subplot_titles=["Tank", "Liquid Height", "Flow Rates"],
        specs=[
            [{"type": "scene", "rowspan": 2}, {"type": "xy"}],
            [None, {"type": "xy"}],
        ],
    )

    figure.add_traces(tank_figure.data, rows=1, cols=1)
    figure.add_traces(height_diagram.data, rows=1, cols=2)
    figure.add_traces(flow_diagram.data, rows=2, cols=2)

    figure.update_layout(title=title)
    figure.update_scenes(
        tank_figure.layout.scene,  # type: ignore
        row=1,
        col=1,
    )
    figure.update_xaxes(range=time_range, row=1, col=2)
    figure.update_xaxes(title="Time (s)", range=time_range, row=2, col=2)
    figure.update_yaxes(
        title="Height (m)",
        range=height_diagram.layout.yaxis.range,  # type: ignore
        row=1,
        col=2,
    )
    figure.update_yaxes(
        title="Flow Rate (m³/s)", range=pad(flow_rate_range), row=2, col=2
    )

    return figure


def animation_figure(
    frames: list[Frame],
) -> Figure:
    figure = Figure(data=frames[0].data, layout=frames[0].layout, frames=frames)
    figure.update_layout(
        updatemenus=[basic_animation_configuration(redraw=True, duration=1)],
    )
    return figure


def frame_with_progress_from(figure: Figure, *, time: float, total: float) -> Frame:
    return Frame(
        data=with_progress_information(figure, time=time, total=total).data,
        layout=figure.layout,
    )


def with_progress_information(figure: Figure, *, time: float, total: float) -> Figure:
    title = figure.layout.title.text  # type: ignore

    figure.update_layout(
        title=f"{title} (at t={time:.2f} s / {total:.2f} s)",
    )
    return figure
