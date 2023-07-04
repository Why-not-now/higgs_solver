from dataclasses import dataclass, field
from typing import Optional, TypeAlias

DirectionFilter: TypeAlias = tuple[int, ...]
LeftFilter: TypeAlias = DirectionFilter
RightFilter: TypeAlias = DirectionFilter
UpFilter: TypeAlias = DirectionFilter
DownFilter: TypeAlias = DirectionFilter
GeneralFilter: TypeAlias = \
    tuple[LeftFilter, RightFilter, UpFilter, DownFilter]


def empty_particles_board(width: int, height: int) -> tuple[None, ...]:
    return tuple(None for _ in range(width * height))


@dataclass(frozen=True)
class Board():
    r"""Generic board class for game"""
    width: int
    height: int
    particles: tuple[Optional[int], ...] = field(compare=False)
    _particles_set: frozenset[int]
    # TODO: replace with Particles
    # TODO: obstacles tuple[ObstacleType (enum)]
    # TODO: higgs tuple[bool]
    # TODO: goals tuple[int (pointer)]

    def left(self, particles) -> "Board":
        raise NotImplementedError
        return Board(self.width, self.height, *particles._left(self))

    def right(self, particles) -> "Board":
        raise NotImplementedError
        return Board(self.width, self.height, *particles._right(self))

    def up(self, particles) -> "Board":
        raise NotImplementedError
        return Board(self.width, self.height, *particles._up(self))

    def down(self, particles) -> "Board":
        raise NotImplementedError
        return Board(self.width, self.height, *particles._down(self))


def new_board(
        width: int,
        height: int,
        particles: Optional[tuple[Optional[int], ...]],
        _particles_set: Optional[frozenset[int]],
) -> Board:
    r"""Returns a generic board for game"""
    if particles is None:
        particles = empty_particles_board(width, height)

    if _particles_set is None:
        _particles_mutable_set: list[int] = \
            [elem for elem in particles if elem is not None]
        _particles_set = frozenset(_particles_mutable_set)

    return Board(width, height, particles, _particles_set)


def straight_filter(width: int, height: int) \
        -> tuple[GeneralFilter, ...]:
    r"""Returns an object that itself returns the horizontal and vertical
directional filter for a given position"""

    lookup_table: list[GeneralFilter] = []

    for y in range(0, height * width, width):
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
                tuple(range(y + x + width, width * height, width))
            lookup_table.append((left, right, up, down))

    return tuple(lookup_table)
