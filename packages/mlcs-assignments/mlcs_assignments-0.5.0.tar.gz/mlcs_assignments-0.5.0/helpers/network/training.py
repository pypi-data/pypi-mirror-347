from typing import Iterator
from dataclasses import dataclass, field

from helpers.maths import Matrix

from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from plotly.graph_objs import Figure
from torch.utils.data import DataLoader, TensorDataset
from torch import Tensor


@dataclass(frozen=True)
class BatchLoader:
    loader: DataLoader

    @property
    def element_count(self) -> int:
        return len(self.loader.dataset)  # type: ignore

    @property
    def batch_count(self) -> int:
        return len(self.loader)

    def __iter__(self) -> Iterator[tuple[Tensor, Tensor]]:
        yield from self.loader

    def __len__(self) -> int:
        return self.batch_count


@dataclass(frozen=True)
class Data:
    train: tuple[Matrix, Matrix]
    val: tuple[Matrix, Matrix]
    test: tuple[Matrix, Matrix]

    @staticmethod
    def partitions(
        train: tuple[Matrix, Matrix],
        val: tuple[Matrix, Matrix],
        test: tuple[Matrix, Matrix],
    ) -> "Data":
        return Data(train=train, val=val, test=test)

    def training(self, *, batch_size: int) -> BatchLoader:
        return self._data_loader_for(self.train, batch_size=batch_size)

    def validation(self, *, batch_size: int) -> BatchLoader:
        return self._data_loader_for(self.val, batch_size=batch_size)

    def testing(self, *, batch_size: int) -> BatchLoader:
        return self._data_loader_for(self.test, batch_size=batch_size)

    def _data_loader_for(
        self, data_partition: tuple[Matrix, Matrix], *, batch_size: int
    ) -> BatchLoader:
        X, y = data_partition
        X_tensor = Tensor(X).float()
        y_tensor = Tensor(y).float()

        dataset = TensorDataset(X_tensor, y_tensor)
        return BatchLoader(DataLoader(dataset, batch_size=batch_size, shuffle=True))


@dataclass
class TrainingVisualizer:
    total_epochs: int

    last_epoch: int = field(init=False, default=0)
    training_losses: list[float] = field(init=False, default_factory=list)
    val_losses: list[float] = field(init=False, default_factory=list)

    app: Dash = field(init=False)

    def __post_init__(self) -> None:
        self.app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
        self._create_layout_for(self.app)
        self._setup_callbacks_for(self.app)

    def start(self, *, height: int = 450) -> "TrainingVisualizer":
        self.app.run(jupyter_height=height)
        return self

    def complete(self, *, epoch: int, training_loss: float, val_loss: float) -> None:
        self.last_epoch = epoch
        self.training_losses.append(training_loss)
        self.val_losses.append(val_loss)

    def visualize(self) -> Figure:
        return Figure(
            data=[
                {
                    "x": list(range(1, self.last_epoch + 1)),
                    "y": self.training_losses,
                    "name": "Training Loss",
                },
                {
                    "x": list(range(1, self.last_epoch + 1)),
                    "y": self.val_losses,
                    "name": "Validation Loss",
                },
                {
                    "x": [self.last_epoch, self.last_epoch],
                    "y": [
                        0,
                        max(max(self.training_losses), max(self.val_losses))
                        if self.last_epoch > 0
                        else 1,
                    ],
                    "mode": "lines",
                    "line": {"color": "black", "width": 2, "dash": "dash"},
                    "name": f"Epoch {self.last_epoch}",
                },
            ],
            layout={
                "title": "Training and Validation Loss",
                "xaxis": {"title": "Epoch", "range": [1, self.total_epochs]},
                "yaxis": {"title": "Loss"},
            },
        )

    def _create_layout_for(self, app: Dash) -> None:
        app.layout = dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                [
                                    dcc.Graph(id="loss-graph", figure=self.visualize()),
                                    dcc.Interval(
                                        id="interval-component",
                                        interval=500,  # in milliseconds
                                        n_intervals=0,
                                    ),
                                ]
                            )
                        )
                    ]
                )
            ]
        )

    def _setup_callbacks_for(self, app: Dash) -> None:
        @app.callback(
            Output("loss-graph", "figure"),
            Input("interval-component", "n_intervals"),
        )
        def update_graph(n: int) -> Figure:
            return self.visualize()
