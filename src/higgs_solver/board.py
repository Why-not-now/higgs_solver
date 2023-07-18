from __future__ import annotations

from typing import TypeVar, overload

from attrs import field, frozen

# pylint: disable=unused-import
# flake8: noqa: F401
from higgs_solver.protocol import (AntiType, BoardProtocol, ChargeType,
                                   ColourType, DecayType, Direction,
                                   DownFilter, GeneralFilter, HoleType,
                                   LeftFilter, MassType, MatterProtocol,
                                   MatterType, ObstacleType, ParticleProtocol,
                                   RightFilter, UpFilter)

T = TypeVar('T')


@frozen
class Board(BoardProtocol):
    r"""Generic board class for game"""
    width: int
    height: int
    goals: frozenset[int]
    obstacles: tuple[ObstacleType | None, ...]
    holes: tuple[HoleType | None, ...]
    decay: tuple[DecayType | None, ...]
    higgs: tuple[bool, ...]
    matter: tuple[MatterProtocol | None, ...] = field(eq=False)
    particle: tuple[ParticleProtocol | None, ...] = field(eq=False)
    _filter: tuple[GeneralFilter, ...] = field(eq=False)
    _matter_set: frozenset[MatterProtocol]
    _prev_board: BoardProtocol | None = field(eq=False)

    # def move(self, particle: ParticleProtocol, direction: Direction) -> Board
    #     raise NotImplementedError
    #     matter = self.matter[particle.x + self.width * particle.y]
    #     return matter.move(self, particle, direction)

    def move_all(self) -> frozenset[Board]:
        raise NotImplementedError
        return {Matter.move_all(self) for Matter in self._matter_set}


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
        goals: frozenset[int] | None = None,
        obstacles: tuple[ObstacleType | None, ...] | None = None,
        holes: tuple[HoleType | None, ...] | None = None,
        decay: tuple[DecayType | None, ...] | None = None,
        higgs: tuple[bool, ...] | None = None,
        matter: tuple[MatterProtocol | None, ...] | None = None,
        particle: tuple[ParticleProtocol | None, ...] | None = None,
        _filter: tuple[GeneralFilter, ...] | None = None,
        _matter_set: frozenset[MatterProtocol] | None = None,
        _prev_board: BoardProtocol | None = None,
) -> Board:
    r"""Returns a generic board class for game"""
    if goals is None:
        goals = frozenset()
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
    if matter is None:      # TODO: initialisation of matter
        matter = default_board(width, height)

    if _filter is None:
        _filter = straight_filter(width, height)
    if _matter_set is None:
        _matter_mutable_set: list[MatterProtocol] = \
            [elem for elem in matter if elem is not None]
        _matter_set = frozenset(_matter_mutable_set)

    return Board(
        width,
        height,
        goals,
        obstacles,
        holes,
        decay,
        higgs,
        matter,
        particle,
        _filter,
        _matter_set,
        _prev_board
    )


def straight_filter(width: int, height: int) \
        -> tuple[GeneralFilter, ...]:
    r"""Returns an object that itself returns the horizontal and vertical
        directional filter for a given position"""

    lookup_table: list[GeneralFilter] = []
    length = width * height

    for y in range(0, length, width):
        for x in range(width):
            right: RightFilter = \
                tuple(range(y + x + 1, y + width))
            down: DownFilter = \
                tuple(range(y + x + width, length, width))
            left: LeftFilter = \
                tuple(range(y + x - 1, y - 1, -1))
            # reversed(range(y, y + x))
            up: UpFilter = \
                tuple(range(y + x - width, -1, -width))
            # reversed(range(x, y + x, width))
            lookup_table.append((right, down, left, up))

    return tuple(lookup_table)
