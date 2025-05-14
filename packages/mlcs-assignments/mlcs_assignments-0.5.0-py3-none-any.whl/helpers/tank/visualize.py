from typing import Protocol, Sequence, Generic, Callable

from helpers.tank.policy import Policy, StateT, ActionT, State, RewardFunction
from helpers.tank.learn import TrainingResult

from plotly.graph_objects import Figure, Scatter, Bar
from plotly.subplots import make_subplots


import numpy as np


class PolicyVisualizationAddOn(Protocol, Generic[ActionT]):
    def __call__(
        self, figure: Figure, actions: Sequence[tuple[ActionT, float]]
    ) -> None:
        """Adds additional information to the policy visualization."""
        ...


def no_add_on(figure: Figure, actions: Sequence[tuple[ActionT, float]]) -> None:
    """Does nothing."""
    pass


def visualize_discretization(
    discretization: Sequence[State],
    *,
    min_value: float | None = None,
    max_value: float,
    state_name: str,
    unit: str | None = None,
    title: str,
) -> None:
    """
    Visualizes the discretization of a system state.

    Args:
        discretization: A sequence of states that have been discretized.
        min_value: The minimum value of the state (optional).
        max_value: The maximum value of the state.
        state_name: The name of the state.
        unit: The unit of the state (if it is a physical quantity).
        title: The title of the plot.
    """
    discrete_values = [state.value for state in discretization]

    figure = Figure()

    figure.add_vline(
        x=0,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"No {state_name}",
        annotation_position="top",
    )

    if min_value is not None:
        figure.add_vline(
            x=min_value,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Min {state_name}",
            annotation_position="bottom",
            annotation=dict(yshift=-20),
        )

    figure.add_vline(
        x=max_value,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Max {state_name}",
        annotation_position="bottom",
        annotation=dict(yshift=-20),
    )

    figure.add_trace(
        Scatter(
            x=discrete_values,
            y=[0] * len(discrete_values),
            mode="markers",
            name="Discrete States",
            marker=dict(size=12, symbol="diamond-tall"),
        )
    )

    # Update layout
    figure.update_layout(
        title=title,
        xaxis_title=f"{state_name} ({unit})" if unit else state_name,
        yaxis_showticklabels=False,
        yaxis_zeroline=False,
        showlegend=True,
        yaxis_range=[-0.5, 0.5],
    )

    figure.show()


def visualize_reward_function(
    reward_function: RewardFunction[StateT],
    states: Sequence[StateT],
    state_from: Callable[[float], StateT],
    *,
    state_name: str,
    unit: str | None = None,
    samples: int = 2000,
    title: str = "Tank System Reward Function",
) -> None:
    """
    Visualizes the reward function and discretized states.

    Args:
        reward_function: The reward function to visualize.
        states: Sequence of states following the State protocol.
        state_from: A function that creates a state from a numerical value.
        state_name: The name of the state.
        unit: The unit of the state (if it is a physical quantity).
        samples: Number of points for smooth reward function curve.
        title: Title of the plot.
    """
    discrete_values = [state.value for state in states]
    continuous_values = np.linspace(min(discrete_values), max(discrete_values), samples)

    rewards_discrete = [reward_function(state) for state in states]
    rewards_continuous = [
        reward_function(state_from(value)) for value in continuous_values
    ]

    figure = Figure()

    figure.add_trace(
        Scatter(
            x=discrete_values,
            y=rewards_discrete,
            mode="markers",
            name="Discrete States",
            marker=dict(size=12, symbol="diamond-tall"),
        )
    )

    figure.add_trace(
        Scatter(
            x=continuous_values,
            y=rewards_continuous,
            mode="lines",
            name="Reward Function",
            line=dict(width=2),
            opacity=0.6,
        )
    )

    figure.update_layout(
        title=title,
        xaxis_title=f"{state_name} ({unit})" if unit else state_name,
        yaxis_title="Reward",
        showlegend=True,
    )

    figure.show()


def visualize_policy(
    policy: Policy[ActionT],
    actions: Sequence[tuple[ActionT, float]],
    *,
    title: str,
    samples: int = 1000,
    add_on: PolicyVisualizationAddOn[ActionT] = no_add_on,
) -> None:
    """
    Visualizes epsilon-greedy policy decisions.

    Args:
        actions: Sequence of (action, value) pairs.
        epsilon: Exploration parameter.
        samples: Number of policy samples to simulate.
        title: Plot title.
    """
    figure = make_subplots(specs=[[{"secondary_y": True}]])

    actions = sorted(actions, key=lambda x: x[1], reverse=True)
    action_names = [str(action) for action, _ in actions]
    values = [value for _, value in actions]

    # Simulate policy decisions
    selections = [policy(actions) for _ in range(samples)]
    selection_counts = [selections.count(action[0]) / samples for action in actions]

    # Add value bars
    figure.add_trace(
        Bar(
            x=action_names,
            y=values,
            name="Action Values",
            opacity=0.6,
        ),
        secondary_y=False,
    )

    figure.add_trace(
        Scatter(
            x=action_names,
            y=selection_counts,
            name="Selection Probability",
            mode="lines+markers",
            marker=dict(size=10),
            line=dict(width=2),
        ),
        secondary_y=True,
    )

    add_on(figure, actions)

    figure.update_layout(
        title=title, xaxis_title="Actions", showlegend=True, height=500
    )

    figure.update_yaxes(title_text="Action Value", secondary_y=False)
    figure.update_yaxes(
        title_text="Selection Probability", secondary_y=True, range=[0, 1]
    )

    figure.show()


def theoretical_epsilon_greedy_probabilities(
    epsilon: float,
) -> PolicyVisualizationAddOn:
    """Returns a policy visualization add-on that includes theoretical probabilities.

    Args:
        epsilon: Exploration parameter.

    Returns:
        A policy visualization add-on that includes theoretical probabilities.
    """

    def add_on(figure: Figure, actions: Sequence[tuple[ActionT, float]]) -> None:
        actions = sorted(actions, key=lambda x: x[1], reverse=True)
        action_names = [str(action) for action, _ in actions]

        random_probability = epsilon / len(actions)
        best_action_probability = 1 - epsilon + random_probability
        theoretical_probs = [
            best_action_probability if i == 0 else random_probability
            for i in range(len(actions))
        ]

        figure.add_trace(
            Scatter(
                x=action_names,
                y=theoretical_probs,
                name="Theoretical Probability",
                mode="lines+markers",
                line=dict(width=2, dash="dash"),
                marker=dict(size=10, symbol="x"),
            ),
            secondary_y=True,
        )

    return add_on


def visualize_training_results(results: Sequence[TrainingResult]) -> None:
    """Visualizes training results in a 4x1 subplot layout.

    Args:
        results: Sequence of training results.
    """

    figure = make_subplots(
        rows=4,
        cols=1,
        subplot_titles=(
            "Tank Heights",
            "Learning Rate",
            "Height Difference",
            "Accumulated Reward",
        ),
        vertical_spacing=0.1,
    )

    # Heights plot (starting height and setpoint)
    figure.add_trace(
        Scatter(
            y=[r.starting_height for r in results],
            name="Starting Height",
            line=dict(color="blue"),
        ),
        row=1,
        col=1,
    )

    figure.add_trace(
        Scatter(
            y=[r.setpoint for r in results],
            name="Setpoint",
            line=dict(color="red", dash="dash"),
        ),
        row=1,
        col=1,
    )

    # Learning rate
    figure.add_trace(
        Scatter(
            y=[r.learning_rate for r in results],
            name="Learning Rate",
            line=dict(color="green"),
        ),
        row=2,
        col=1,
    )

    # Height difference
    figure.add_trace(
        Scatter(
            y=[r.height_difference for r in results],
            name="Height Difference",
            line=dict(color="purple"),
        ),
        row=3,
        col=1,
    )

    # Add zero line for height difference
    figure.add_hline(
        y=0,
        line_dash="dash",
        line_color="gray",
        row=3,  # type: ignore
        col=1,  # type: ignore
    )

    # Accumulated reward
    figure.add_trace(
        Scatter(
            y=[r.accumulated_reward for r in results],
            name="Accumulated Reward",
            line=dict(color="orange"),
        ),
        row=4,
        col=1,
    )

    # Update layout
    figure.update_layout(
        height=1000, showlegend=True, title_text="Training Results Over Time"
    )

    figure.update_yaxes(title_text="Height (m)", row=1, col=1)
    figure.update_yaxes(title_text="Learning Rate", row=2, col=1)
    figure.update_yaxes(title_text="Height Diff (m)", row=3, col=1)
    figure.update_yaxes(title_text="Reward", row=4, col=1)
    figure.update_xaxes(title_text="Episode", row=4, col=1)

    figure.show()
