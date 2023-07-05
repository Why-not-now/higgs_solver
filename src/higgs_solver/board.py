from typing import TYPE_CHECKING, TypeAlias, TypeVar

from attrs import define, field

if TYPE_CHECKING:
    from .particle import Particle, Particles

T = TypeVar('T')

DirectionFilter: TypeAlias = tuple[int, ...]
LeftFilter: TypeAlias = DirectionFilter
RightFilter: TypeAlias = DirectionFilter
UpFilter: TypeAlias = DirectionFilter
DownFilter: TypeAlias = DirectionFilter
GeneralFilter: TypeAlias = \
    tuple[LeftFilter, RightFilter, UpFilter, DownFilter]


def data_board(width: int, height: int, data: T | None = None) \
        -> tuple[T | None, ...]:
    return tuple(data for _ in range(width * height))


@define(frozen=True)
class Board():
    r"""Generic board class for game"""
    width: int
    height: int
    # TODO: goals tuple[int (pointer)]
    # TODO: obstacles tuple[ObstacleType (enum)]
    # TODO: holes tuple[HolesType (enum)]
    # TODO: decay tuple?[decayType (flag)]
    # TODO: higgs tuple[bool]
    particles: tuple["Particles" | None, ...] = field(eq=False)
    particle: tuple["Particle" | None, ...] = field(eq=False)
    _particles_set: frozenset["Particles"]

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
        particles: tuple["Particles" | None, ...] | None,
        particle: tuple["Particle" | None, ...] | None,
        _particles_set: frozenset["Particles"] | None,
) -> Board:
    r"""Returns a generic board class for game"""
    if particle is None:
        particle = data_board(width, height)
    if particles is None:
        particles = data_board(width, height)
    if particles is None:
        particles = data_board(width, height)

    if _particles_set is None:
        _particles_mutable_set: list["Particles"] = \
            [elem for elem in particles if elem is not None]
        _particles_set = frozenset(_particles_mutable_set)

    return Board(width, height, particles, particle, _particles_set)


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
