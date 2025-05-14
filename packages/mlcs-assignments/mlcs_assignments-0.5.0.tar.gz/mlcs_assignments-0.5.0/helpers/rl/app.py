from typing import Final, NamedTuple, TypeAlias
from enum import Enum

from helpers.rl.game import (
    GridGame,
    RewardFunction,
    TransitionFunction,
    Policy,
    DeterministicTransition,
    Moves,
    EndGame,
)
from helpers.rl.animate import GridGameVisualizer

import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from dash.development.base_component import Component
import dash_bootstrap_components as dbc

from plotly.graph_objects import Figure


Content: TypeAlias = str | list[str | Component] | Component


class PlayerActionItems(str, Enum):
    RESTART = "restart"
    END_GAME = "end-game"
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class AgentActionItems(str, Enum):
    START = "start"
    STOP = "stop"
    INTERVAL = "interval"


class PlayerUpdateGame(NamedTuple):
    figure: Figure
    score_display: Content
    score_color: str


class AgentUpdateGame(NamedTuple):
    figure: Figure
    score_display: Content
    score_color: str
    stop_disabled: bool
    interval_disabled: bool

    @staticmethod
    def stopped(
        figure: Figure, score_display: Content, score_color: str
    ) -> "AgentUpdateGame":
        return AgentUpdateGame(
            figure,
            score_display,
            score_color,
            stop_disabled=True,
            interval_disabled=True,
        )

    @staticmethod
    def running(
        figure: Figure, score_display: Content, score_color: str
    ) -> "AgentUpdateGame":
        return AgentUpdateGame(
            figure,
            score_display,
            score_color,
            stop_disabled=False,
            interval_disabled=False,
        )


class UpdateButtons(NamedTuple):
    up_disabled: bool
    down_disabled: bool
    left_disabled: bool
    right_disabled: bool

    @staticmethod
    def all_enabled() -> "UpdateButtons":
        return UpdateButtons(False, False, False, False)

    @staticmethod
    def all_disabled() -> "UpdateButtons":
        return UpdateButtons(True, True, True, True)


class GridGameApp:
    visualizer: GridGameVisualizer
    figure: Figure
    app: Dash
    game: GridGame

    MOVE_MAP: Final = {
        PlayerActionItems.UP: Moves.UP,
        PlayerActionItems.DOWN: Moves.DOWN,
        PlayerActionItems.LEFT: Moves.LEFT,
        PlayerActionItems.RIGHT: Moves.RIGHT,
    }

    @staticmethod
    def create(
        *,
        rows: int,
        columns: int,
        reward_function: RewardFunction,
        transition_function: TransitionFunction = DeterministicTransition(),
        policy: Policy | None = None,
        move_interval_ms: int = 500,
    ) -> "GridGameApp":
        """Create a new grid game application.

        Args:
            rows: Number of rows in the grid.
            columns: Number of columns in the grid.
            reward_function: A reward function for the game.
            transition_function: A transition function for the game.
            policy: A policy to use for the game. If not provided, the user will play the game.
            move_interval_ms: The interval in milliseconds between moves for the agent
                (only applicable if a policy is provided).

        Returns:
            A GridGameApp instance.

        Example:
            You can start a new game with 5 rows and 5 columns as follows:

            ```python
            app = GridGameApp.create(rows=5, columns=5, reward_function=MyAwesomeRewardFunction())
            app.run()
            ```
        """
        return GridGameApp(
            GridGame.create(
                rows=rows,
                columns=columns,
                reward_function=reward_function,
                transition_function=transition_function,
                policy=policy,
            ),
            move_interval_ms=move_interval_ms,
        )

    def __init__(self, game: GridGame, *, move_interval_ms: int) -> None:
        self.app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

        self._initialize(game)
        self._create_layout(self.app, self.figure, move_interval_ms=move_interval_ms)
        self._setup_callbacks()

    def run(self, debug: bool = False, port: str = "8050") -> None:
        self.app.run(debug=debug, port=port, jupyter_height=400, jupyter_width="500")

    def _initialize(self, game: GridGame) -> None:
        self.game = game
        self.visualizer = GridGameVisualizer(game)
        self.figure = self.visualizer.create()

    def _create_layout(
        self, app: Dash, figure: Figure, *, move_interval_ms: int
    ) -> None:
        app.layout = dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H1("Grid Game", className="text-center my-2"),
                                self._score_display(),
                                self._result_area(),
                            ],
                            style={"maxWidth": "500px"},
                        ),
                    ],
                    align="top",
                    justify="center",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [self._game_board(figure)], style={"maxWidth": "250px"}
                        ),
                        dbc.Col(
                            [self._controls(move_interval_ms=move_interval_ms)],
                            style={"maxWidth": "250px"},
                        ),
                    ],
                    align="top",
                    justify="center",
                ),
            ],
            fluid=True,
            className="py-2",
        )

    def _score_display(self) -> dbc.Alert:
        return dbc.Alert(
            id="score-display",
            color="light",
            className="text-center mb-4",
        )

    def _game_board(self, figure: Figure) -> dcc.Graph:
        return dcc.Graph(
            id="game-board",
            figure=figure,
            config={"displayModeBar": False},
        )

    def _controls(self, *, move_interval_ms: int) -> dbc.Card:
        return (
            self._player_controls()
            if self.game.policy is None
            else self._agent_controls(move_interval_ms=move_interval_ms)
        )

    def _player_controls(self) -> dbc.Card:
        return dbc.Card(
            [
                dbc.CardBody(
                    [
                        self._player_explanation(),
                        self._direction_pad(),
                        html.Div(self._player_game_menu(), className="mt-auto"),
                    ],
                    className="d-flex flex-column h-100",
                )
            ],
            className="h-100",
        )

    def _agent_controls(self, *, move_interval_ms: int) -> dbc.Card:
        return dbc.Card(
            [
                dbc.CardBody(
                    [
                        self._agent_explanation(),
                        html.Div(self._agent_game_menu(), className="mt-auto"),
                        dcc.Interval(
                            id=AgentActionItems.INTERVAL,
                            interval=move_interval_ms,
                            n_intervals=0,
                            disabled=True,
                        ),
                    ],
                    className="d-flex flex-column h-100",
                )
            ],
            className="h-100",
        )

    def _player_explanation(self) -> html.Div:
        return html.Div(
            [
                html.P([html.Strong("• Movements: "), "↑ ↓ ← →"], className="mb-0"),
                html.P([html.Strong("• Player: "), "White Dot"], className="mb-0"),
                html.Hr(className="my-2"),
            ],
            className="text-start small",
            style={"fontSize": "12px", "padding": "0 0 5px 0"},
        )

    def _agent_explanation(self) -> html.Div:
        return html.Div(
            [html.Strong("Press Start to begin.")],
            className="text-center small",
            style={"fontSize": "12px", "padding": "0 0 5px 0"},
        )

    def _direction_pad(self, *, element_width: int = 2) -> dbc.Container:
        button_style = {
            "width": "30px",
            "height": "30px",
            "padding": "0px",
        }

        return dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(width=element_width),
                        dbc.Col(
                            dbc.Button(
                                "↑",
                                id=PlayerActionItems.UP,
                                color="primary",
                                n_clicks=0,
                                style=button_style,
                            ),
                            width=element_width,
                            className="text-center p-0",
                        ),
                        dbc.Col(width=element_width),
                    ],
                    className="g-0",
                    justify="center",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button(
                                "←",
                                id=PlayerActionItems.LEFT,
                                color="primary",
                                n_clicks=0,
                                style=button_style,
                            ),
                            width=element_width,
                            className="text-center p-0",
                        ),
                        dbc.Col(width=element_width),
                        dbc.Col(
                            dbc.Button(
                                "→",
                                id=PlayerActionItems.RIGHT,
                                color="primary",
                                n_clicks=0,
                                style=button_style,
                            ),
                            width=element_width,
                            className="text-center p-0",
                        ),
                    ],
                    className="g-0 my-1",
                    justify="center",
                ),
                dbc.Row(
                    [
                        dbc.Col(width=element_width),
                        dbc.Col(
                            dbc.Button(
                                "↓",
                                id=PlayerActionItems.DOWN,
                                color="primary",
                                n_clicks=0,
                                style=button_style,
                            ),
                            width=element_width,
                            className="text-center p-0",
                        ),
                        dbc.Col(width=element_width),
                    ],
                    className="g-0",
                    justify="center",
                ),
            ],
            fluid=True,
            className="p-0",
        )

    def _player_game_menu(self) -> dbc.Row:
        button_style = {"width": "80px", "margin": "0", "font-size": "0.7rem"}

        return dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Button(
                            "Restart",
                            id=PlayerActionItems.RESTART,
                            color="secondary",
                            n_clicks=0,
                            style=button_style,
                        ),
                    ],
                    className="text-center mt-2",
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            "End Game",
                            id=PlayerActionItems.END_GAME,
                            color="info",
                            n_clicks=0,
                            style=button_style,
                        ),
                    ],
                    className="text-center mt-2",
                ),
            ]
        )

    def _agent_game_menu(self) -> dbc.Row:
        button_style = {"width": "80px", "margin": "0 5px", "font-size": "0.7rem"}

        return dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Button(
                            "Start",
                            id=AgentActionItems.START,
                            color="primary",
                            n_clicks=0,
                            style=button_style,
                        ),
                        dbc.Button(
                            "Stop",
                            id=AgentActionItems.STOP,
                            color="light",
                            n_clicks=0,
                            style=button_style,
                        ),
                    ],
                    className="text-center mt-2",
                ),
            ]
        )

    def _result_area(self) -> dbc.Alert:
        return dbc.Alert(
            id="message-area",
            color="info",
            is_open=False,
            duration=None,
            className="mt-4",
        )

    def _setup_callbacks(self) -> None:
        if self.game.policy is None:
            self._setup_player_callbacks()
        else:
            self._setup_agent_callbacks()

    def _setup_player_callbacks(self) -> None:
        @self.app.callback(
            Output("game-board", "figure"),
            Output("score-display", "children"),
            Output("score-display", "color"),
            [
                Input(PlayerActionItems.UP, "n_clicks"),
                Input(PlayerActionItems.DOWN, "n_clicks"),
                Input(PlayerActionItems.LEFT, "n_clicks"),
                Input(PlayerActionItems.RIGHT, "n_clicks"),
                Input(PlayerActionItems.RESTART, "n_clicks"),
                Input(PlayerActionItems.END_GAME, "n_clicks"),
            ],
        )
        def update_game(up, down, left, right, restart, end_game) -> PlayerUpdateGame:
            ctx = dash.callback_context
            if not ctx.triggered:
                return PlayerUpdateGame(
                    self.figure, self._score_info(self.game), "light"
                )

            button_id = ctx.triggered[0]["prop_id"].split(".")[0]

            match button_id:
                case PlayerActionItems.RESTART:
                    self._initialize(self.game.regenerate())
                    return PlayerUpdateGame(
                        self.figure, self._score_info(self.game), "light"
                    )
                case PlayerActionItems.END_GAME:
                    solution = self.game.optimal_solution()
                    return PlayerUpdateGame(
                        self.figure,
                        (
                            f"Game Over! Your score: {self.game.accumulated_reward} | "
                            f"Our high score: {solution.reward}"
                        ),
                        "info",
                    )
                case _:
                    assert button_id in GridGameApp.MOVE_MAP, (
                        f"Unknown button: {button_id}"
                    )

                    self.game.move(GridGameApp.MOVE_MAP[button_id])

                    return PlayerUpdateGame(
                        self.visualizer.update(self.figure),
                        self._score_info(self.game),
                        "light",
                    )

        @self.app.callback(
            [
                Output(PlayerActionItems.UP, "disabled"),
                Output(PlayerActionItems.DOWN, "disabled"),
                Output(PlayerActionItems.LEFT, "disabled"),
                Output(PlayerActionItems.RIGHT, "disabled"),
            ],
            [
                Input(PlayerActionItems.RESTART, "n_clicks"),
                Input(PlayerActionItems.END_GAME, "n_clicks"),
            ],
        )
        def update_buttons(restart_clicks, end_clicks) -> UpdateButtons:
            ctx = dash.callback_context
            if not ctx.triggered:
                return UpdateButtons.all_enabled()

            button_id = ctx.triggered[0]["prop_id"].split(".")[0]

            match button_id:
                case PlayerActionItems.END_GAME:
                    return UpdateButtons.all_disabled()
                case _:
                    return UpdateButtons.all_enabled()

    def _setup_agent_callbacks(self) -> None:
        @self.app.callback(
            Output("game-board", "figure"),
            Output("score-display", "children"),
            Output("score-display", "color"),
            Output(AgentActionItems.INTERVAL, "disabled"),
            Output(AgentActionItems.STOP, "disabled"),
            [
                Input(AgentActionItems.INTERVAL, "n_intervals"),
                Input(AgentActionItems.START, "n_clicks"),
                Input(AgentActionItems.STOP, "n_clicks"),
            ],
        )
        def update_agent_game(
            n_intervals, start_clicks, stop_clicks
        ) -> AgentUpdateGame:
            ctx = dash.callback_context
            if not ctx.triggered:
                return AgentUpdateGame.stopped(
                    self.figure, self._score_info(self.game), "light"
                )

            button_id = ctx.triggered[0]["prop_id"].split(".")[0]

            match button_id:
                case AgentActionItems.START:
                    self._initialize(self.game.regenerate())
                    return AgentUpdateGame.running(
                        self.figure, self._score_info(self.game), "light"
                    )
                case AgentActionItems.STOP:
                    return AgentUpdateGame.stopped(
                        self.figure, self._score_info(self.game), "light"
                    )
                case _:
                    try:
                        self.game.move()
                        return AgentUpdateGame.running(
                            self.visualizer.update(self.figure),
                            self._score_info(self.game),
                            "light",
                        )
                    except EndGame:
                        solution = self.game.optimal_solution()
                        return AgentUpdateGame.stopped(
                            self.visualizer.update(self.figure),
                            (
                                f"Game Over! Your score: {self.game.accumulated_reward} | "
                                f"Our high score: {solution.reward}"
                            ),
                            "info",
                        )

    def _score_info(self, game: GridGame) -> Component:
        accumulated = game.accumulated_reward
        last = game.last_reward

        last_reward_color = "green" if last > 0 else "red" if last < 0 else "inherit"

        return html.Div(
            [
                html.P(f"Score: {accumulated}", className="mb-0 me-4"),
                html.P(
                    [
                        "Last Reward: ",
                        html.Span(f"{last}", style={"color": last_reward_color}),
                    ],
                    className="mb-0",
                ),
            ],
            className="d-flex",
            style={"justifyContent": "space-around", "alignItems": "center"},
        )
