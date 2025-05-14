from typing import TypeAlias, Sequence
from dataclasses import dataclass, KW_ONLY

from helpers.maths import Vector, IntVector

from plotly.graph_objects import Scatter3d, Surface, Mesh3d
from scipy.spatial.transform import Rotation

import numpy as np


Trace: TypeAlias = Scatter3d | Surface | Mesh3d


@dataclass(frozen=True)
class Cylinder:
    _: KW_ONLY
    center: tuple[float, float, float]
    normal: tuple[float, float, float]
    radius: float
    height: float
    color: str
    name: str
    group: str | None = None
    text: str | None = None
    angle_points: int = 360
    radial_points: int = 2
    height_points: int = 2

    def traces(self) -> Sequence[Trace]:
        cylinder = self.cylinder_trace()

        if self.text:
            return cylinder, self.text_trace(self.text)
        else:
            return (cylinder,)

    def cylinder_trace(self) -> Trace:
        x, y, z = cylinder_coordinates(
            center=self.center,
            normal=self.normal,
            radius=self.radius,
            height=self.height,
            angle_points=self.angle_points,
            height_points=self.height_points,
        )
        i, j, k = cylinder_triangles(rows=z.shape[0], columns=z.shape[1])

        return Mesh3d(
            x=x.flatten(),
            y=y.flatten(),
            z=z.flatten(),
            i=i,  # triangle indices
            j=j,
            k=k,
            color=self.color,
            name=self.name,
            legendgroup=self.effective_group,
            legendgrouptitle=dict(text=""),
            showlegend=True,
        )

    def text_trace(self, text: str) -> Trace:
        return Scatter3d(
            x=[self.center[0]],
            y=[self.center[1]],
            z=[self.center[2]],
            mode="text",
            text=[text],
            textposition="middle center",
            name=self.name,
            legendgroup=self.effective_group,
            legendgrouptitle=dict(text=""),
            showlegend=False,
        )

    @property
    def effective_group(self) -> str:
        return self.group if self.group is not None else self.name


def cylinder_coordinates(
    *,
    center: tuple[float, float, float],
    normal: tuple[float, float, float],
    radius: float,
    height: float,
    angle_points: int,
    height_points: int,
) -> tuple[Vector, Vector, Vector]:
    x, y, z = cylinder_grid(
        radius=radius,
        height=height,
        angle_points=angle_points,
        height_points=height_points,
    )
    x_rotated, y_rotated, z_rotated = rotate(
        normal, x=x.flatten(), y=y.flatten(), z=z.flatten()
    )
    x, y, z = (
        x_rotated.reshape(x.shape),
        y_rotated.reshape(y.shape),
        z_rotated.reshape(z.shape),
    )

    return x + center[0], y + center[1], z + center[2]


def cylinder_triangles(
    *, rows: int, columns: int
) -> tuple[IntVector, IntVector, IntVector]:
    # Side triangles
    row_indices = np.repeat(np.arange(rows - 1), columns - 1)
    column_indices = np.tile(np.arange(columns - 1), rows - 1)
    base = row_indices * columns + column_indices

    i_1 = base
    j_1 = base + 1
    k_1 = base + columns

    i_2 = base + 1
    j_2 = base + columns + 1
    k_2 = base + columns

    # Bottom cap
    bottom_i = np.zeros(columns - 1, dtype=np.int32)
    bottom_j = np.arange(1, columns)
    bottom_k = np.arange(2, columns + 1)

    # Top cap
    top_center = (rows - 1) * columns
    top_i = np.full(columns - 1, top_center, dtype=np.int32)
    top_j = top_center + np.arange(columns - 1)
    top_k = top_center + np.arange(1, columns)

    i = np.concatenate([i_1, i_2, bottom_i, top_i])
    j = np.concatenate([j_1, j_2, bottom_j, top_j])
    k = np.concatenate([k_1, k_2, bottom_k, top_k])

    return i, j, k


def cylinder_grid(
    *, radius: float, height: float, angle_points: int, height_points: int
) -> tuple[Vector, Vector, Vector]:
    h = np.linspace(-height / 2, height / 2, height_points)
    theta = np.linspace(0, 2 * np.pi, angle_points)
    theta_grid, h_grid = np.meshgrid(theta, h)

    x = radius * np.cos(theta_grid)
    y = radius * np.sin(theta_grid)
    z = h_grid

    return x, y, z


def normalize(vector: tuple[float, float, float]) -> Vector:
    array = np.array(vector)
    return array / np.linalg.norm(array)


def rotate(
    normal: tuple[float, float, float], *, x: Vector, y: Vector, z: Vector
) -> tuple[Vector, Vector, Vector]:
    # Find rotation matrix from [0,0,1] to normal vector
    rotation = Rotation.align_vectors([normalize(normal)], [[0, 0, 1]])[0]

    # Rotate all points
    points = np.stack([x, y, z]).T
    rotated = rotation.apply(points)

    return rotated[:, 0], rotated[:, 1], rotated[:, 2]
