from enum import CONTINUOUS, Enum, verify
from typing import TYPE_CHECKING, TypeAlias, TypeVar, overload

from attrs import define, field

if TYPE_CHECKING:
    from .particle import (DecayType, HoleType, ObstacleType, Particle,
                           Particles)

T = TypeVar('T')

DirectionFilter: TypeAlias = tuple[int, ...]
LeftFilter: TypeAlias = DirectionFilter
RightFilter: TypeAlias = DirectionFilter
UpFilter: TypeAlias = DirectionFilter
DownFilter: TypeAlias = DirectionFilter
GeneralFilter: TypeAlias = \
    tuple[LeftFilter, RightFilter, UpFilter, DownFilter]


@verify(CONTINUOUS)
class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


@define(frozen=True)
class Board():
    r"""Generic board class for game"""
    width: int
    height: int
    goals: tuple[int, ...]
    obstacles: tuple["ObstacleType" | None, ...]
    holes: tuple["HoleType" | None, ...]
    decay: tuple["DecayType" | None, ...]
    higgs: tuple[bool, ...]
    particles: tuple["Particles" | None, ...] = field(eq=False)
    particle: tuple["Particle" | None, ...] = field(eq=False)
    _particles_set: frozenset["Particles"]

    def move(self, particle: "Particle", direction: Direction) -> "Board":
        raise NotImplementedError
        particles = self.particles[particle.x + self.width * particle.y]
        return particles.move(self, particle, direction)

    def move_all(self) -> set["Board"]:
        raise NotImplementedError
        return {particles.move_all(self) for particles in self._particles_set}


@overload
def default_board(width: int, height: int) -> tuple[None, ...]:
    ...


@overload
def default_board(width: int, height: int, data: T) -> tuple[T, ...]:
    ...


def default_board(width, height, data=None):
    return tuple(data for _ in range(width * height))


def new_board(
        width: int,
        height: int,
        *,
        goals: tuple[int, ...] | None,
        obstacles: tuple["ObstacleType" | None, ...] | None,
        holes: tuple["HoleType" | None, ...] | None,
        decay: tuple["DecayType" | None, ...] | None,
        higgs: tuple[bool, ...] | None,
        particles: tuple["Particles" | None, ...] | None,
        particle: tuple["Particle" | None, ...] | None,
        _particles_set: frozenset["Particles"] | None,
) -> Board:
    r"""Returns a generic board class for game"""
    if goals is None:
        goals = ()
    if obstacles is None:
        obstacles = default_board(width, height)
    if holes is None:
        holes = default_board(width, height)
    if decay is None:
        decay = default_board(width, height)
    if higgs is None:
        higgs = default_board(width, height, False)
    if particle is None:
        particle = default_board(width, height)
    if particles is None:
        particles = default_board(width, height)

    if _particles_set is None:
        _particles_mutable_set: list["Particles"] = \
            [elem for elem in particles if elem is not None]
        _particles_set = frozenset(_particles_mutable_set)

    return Board(
        width,
        height,
        goals,
        obstacles,
        holes,
        decay,
        higgs,
        particles,
        particle,
        _particles_set
    )


def straight_filter(width: int, height: int) \
        -> tuple[GeneralFilter, ...]:
    r"""Returns an object that itself returns the horizontal and vertical
        directional filter for a given position"""

    lookup_table: list[GeneralFilter] = []
    length = width * height

    for y in range(0, length, width):
        for x in range(width):
            left: LeftFilter = \
                tuple(range(y + x - 1, y - 1, -1))
            # reversed(range(y, y + x))
            right: RightFilter = \
                tuple(range(y + x + 1, y + width))
            up: UpFilter = \
                tuple(range(y + x - width, -1, -width))
            # reversed(range(x, y + x, width))
            down: DownFilter = \
                tuple(range(y + x + width, length, width))
            lookup_table.append((left, right, up, down))

    return tuple(lookup_table)
