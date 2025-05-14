from dataclasses import dataclass, field
from enum import Enum

from helpers.maths import BoolMatrix, IntMatrix
from helpers.rl.game import GridGame

from plotly.graph_objects import Figure, Scatter, Heatmap

import numpy as np


class TraceName(Enum):
    UNCOVERED = "Uncovered"
    PLAYER = "Player"
    POSITIVE_REWARDS = "Positive Rewards"
    NEGATIVE_REWARDS = "Negative Rewards"


@dataclass(frozen=True)
class GridGameVisualizer:
    game: GridGame
    trace_indices_by_name: dict[TraceName, int] = field(default_factory=dict)

    def create(self) -> Figure:
        figure = Figure()

        figure, uncovered_index = self._draw_grid_on(figure)
        figure, player_index = self._draw_player_marker(figure)

        figure, positive_rewards_index = self._draw_rewards(
            figure,
            mask=self.game.uncovered,
            condition=self.game.rewards > 0,
            rewards=self.game.rewards,
            color="green",
        )

        figure, negative_rewards_index = self._draw_rewards(
            figure,
            mask=self.game.uncovered,
            condition=self.game.rewards < 0,
            rewards=self.game.rewards,
            color="red",
        )

        self._configure_layout(figure)

        self.trace_indices_by_name.clear()
        self.trace_indices_by_name.update(
            {
                TraceName.UNCOVERED: uncovered_index,
                TraceName.PLAYER: player_index,
                TraceName.POSITIVE_REWARDS: positive_rewards_index,
                TraceName.NEGATIVE_REWARDS: negative_rewards_index,
            }
        )

        return figure

    def update(self, figure: Figure) -> Figure:
        self._update_uncovered_tiles(figure)
        self._update_player_marker(figure)
        self._update_rewards(
            figure,
            self.game.rewards > 0,
            self.trace_indices_by_name[TraceName.POSITIVE_REWARDS],
        )
        self._update_rewards(
            figure,
            self.game.rewards < 0,
            self.trace_indices_by_name[TraceName.NEGATIVE_REWARDS],
        )

        return figure

    def _draw_grid_on(self, figure: Figure) -> tuple[Figure, int]:
        """Draws the grid on the figure and returns the trace index of the trace representing the
        uncovered tiles."""
        traces = trace_count_of(figure)

        self._draw_base_tiles(figure)
        self._draw_uncovered_tiles(figure)
        self._draw_grid_lines(figure)

        return figure, traces + 1

    def _draw_base_tiles(self, figure: Figure) -> Figure:
        figure.add_trace(
            Heatmap(
                z=np.ones_like(self.game.rewards),
                showscale=False,
                colorscale=[[0, "#e0e0e0"], [1, "#e0e0e0"]],  # light gray
                hoverongaps=False,
                hoverinfo="skip",
            )
        )

        return figure

    def _draw_uncovered_tiles(self, figure: Figure) -> Figure:
        uncovered = np.where(self.game.uncovered, 1, np.nan)
        figure.add_trace(
            Heatmap(
                z=uncovered,
                showscale=False,
                colorscale=[[0, "#a0a0a0"], [1, "#a0a0a0"]],  # darker gray
                hoverongaps=False,
                hoverinfo="skip",
            )
        )

        return figure

    def _draw_grid_lines(self, figure: Figure) -> Figure:
        for i in range(self.game.rows + 1):
            figure.add_shape(
                type="line",
                x0=-0.5,
                x1=self.game.columns - 0.5,
                y0=i - 0.5,
                y1=i - 0.5,
                line=dict(color="white", width=2),
            )

        for i in range(self.game.columns + 1):
            figure.add_shape(
                type="line",
                x0=i - 0.5,
                x1=i - 0.5,
                y0=-0.5,
                y1=self.game.rows - 0.5,
                line=dict(color="white", width=2),
            )

        return figure

    def _draw_player_marker(self, figure: Figure) -> tuple[Figure, int]:
        """Draws the player marker on the figure and returns the trace index of the trace."""
        traces = trace_count_of(figure)

        row, column = self.game.current_position
        figure.add_trace(
            Scatter(
                x=[column],
                y=[row],
                mode="markers",
                marker=dict(
                    symbol="circle",
                    size=25,
                    color="rgba(255, 255, 255, 0.75)",
                    line=dict(color="black", width=2),
                ),
                name="Player",
                hoverinfo="skip",
            )
        )

        return figure, traces

    def _draw_rewards(
        self,
        figure: Figure,
        *,
        mask: BoolMatrix,
        condition: BoolMatrix,
        rewards: IntMatrix,
        color: str,
    ) -> tuple[Figure, int]:
        """Draws the rewards on the figure and returns the trace index of the trace."""
        traces = trace_count_of(figure)
        full_mask = mask & condition
        row_idx, col_idx = np.where(full_mask)

        figure.add_trace(
            Scatter(
                x=col_idx,
                y=row_idx,
                text=rewards[full_mask],
                mode="text",
                textfont=dict(color=color, size=20),
                hoverinfo="none",
            )
        )

        return figure, traces

    def _configure_layout(self, figure: Figure) -> None:
        figure.update_layout(
            xaxis=dict(
                showgrid=False,
                range=[-0.5, self.game.columns - 0.5],
                constrain="domain",
                showticklabels=False,
                fixedrange=True,
            ),
            yaxis=dict(
                showgrid=False,
                range=[-0.5, self.game.rows - 0.5],
                scaleanchor="x",
                constrain="domain",
                showticklabels=False,
                fixedrange=True,
            ),
            width=225,
            height=225,
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )

    def _update_uncovered_tiles(self, figure: Figure) -> None:
        uncovered = np.where(self.game.uncovered, 1, np.nan)
        figure.data[self.trace_indices_by_name[TraceName.UNCOVERED]].z = uncovered  # type: ignore

    def _update_player_marker(self, figure: Figure) -> None:
        row, column = self.game.current_position
        figure.data[self.trace_indices_by_name[TraceName.PLAYER]].x = [column]  # type: ignore
        figure.data[self.trace_indices_by_name[TraceName.PLAYER]].y = [row]  # type: ignore

    def _update_rewards(
        self, figure: Figure, condition: BoolMatrix, trace_index: int
    ) -> None:
        full_mask = self.game.uncovered & condition
        row_idx, col_idx = np.where(full_mask)

        figure.data[trace_index].x = col_idx  # type: ignore
        figure.data[trace_index].y = row_idx  # type: ignore
        figure.data[trace_index].text = self.game.rewards[full_mask]  # type: ignore


def trace_count_of(figure: Figure) -> int:
    return len(figure.data) if figure.data else 0  # type: ignore


def annotation_count_of(figure: Figure) -> int:
    return len(figure.layout.annotations) if figure.layout.annotations else 0  # type: ignore


def trace_of(figure: Figure, index: int) -> dict:
    return figure.data[index]  # type: ignore
