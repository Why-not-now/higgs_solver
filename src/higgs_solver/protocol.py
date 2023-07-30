from __future__ import annotations

from collections.abc import Iterator, MutableSequence, Sequence
from copy import deepcopy
from enum import CONTINUOUS, NAMED_FLAGS, Enum, Flag, auto, verify
from typing import (Generic, Protocol, Required, Self, TypeAlias, TypedDict,
                    TypeVar)

from attrs import define, field, frozen

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
MTT = TypeVar("MTT", bound="MatterProtocol")
ST = TypeVar("ST", bound="SingleProtocol")
PTT = TypeVar("PTT", bound="PathTopProtocol")

DirectionFilter: TypeAlias = tuple[int, ...]
LeftFilter: TypeAlias = DirectionFilter
DownFilter: TypeAlias = DirectionFilter
RightFilter: TypeAlias = DirectionFilter
UpFilter: TypeAlias = DirectionFilter
GeneralFilter: TypeAlias = \
    tuple[LeftFilter, RightFilter, UpFilter, DownFilter]


class PathAttrs(TypedDict):
    mass: Required[MassType]
    charge: ChargeType
    colour: ColourType
    anti: AntiType


@verify(CONTINUOUS)
class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    # pylint: disable=bad-dunder-name
    @classmethod
    def _missing_(cls, value) -> Self:
        if isinstance(value, int):
            return cls(value % 4)
        raise ValueError(f"{value} is not a valid Direction")

    def clockwise(self) -> Direction:
        return Direction(self.value + 1)

    def anticlockwise(self) -> Direction:
        return Direction(self.value - 1)

    def opposite(self) -> Direction:
        return Direction(self.value + 2)


horizontal = (Direction.RIGHT, Direction.LEFT)
vertical = (Direction.DOWN, Direction.UP)


@verify(NAMED_FLAGS, CONTINUOUS)
class ColourType(Flag):
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    ANTIRED = GREEN | BLUE
    ANTIGREEN = RED | BLUE
    ANTIBLUE = RED | GREEN
    WHITE = RED | GREEN | BLUE


# @verify(CONTINUOUS)
# class MatterType(Enum):
#     CHARGED_LEPTON = auto()
#     NEUTRINO = auto()
#     PROTON = auto()
#     NEUTRON = auto()
#     STABLE_NUCLEUS = auto()
#     UNSTABLE_NUCLEUS = auto()

#     WBOSON = auto()     # tentative
#     PION = auto()
#     BARYON = auto()
#     NEG_QUARK = auto()
#     POS_QUARK = auto()


# @verify(CONTINUOUS)
# class ParticleType(Enum):
#     CHARGED_LEPTON = auto()
#     NEUTRINO = auto()
#     PROTON = auto()
#     NEUTRON = auto()

#     WBOSON = auto()     # tentative
#     NEG_QUARK = auto()
#     POS_QUARK = auto()


# @verify(CONTINUOUS)
# class GenerationType(Enum):
#     FIRST = auto()
#     SECOND = auto()
#     THIRD = auto()


@verify(CONTINUOUS)
class ChargeType(Enum):
    NEGATIVE = -1
    NEUTRAL = 0
    POSITIVE = 1


@verify(CONTINUOUS)
class MassType(Enum):
    LIGHT = 0
    MEDIUM = 1
    HEAVY = 2
    MASSIVE = 3


@verify(CONTINUOUS)
class AntiType(Enum):
    ORDINARY = 0
    ANTI = 1


@verify(CONTINUOUS)
class ObstacleType(Enum):
    WEAK = auto()       # flimsy
    NORMAL = auto()     # wooden
    STRONG = auto()     # steel

    def is_weak(self) -> bool:
        return self in (self.WEAK,)

    def is_explodable(self) -> bool:
        return self in (self.WEAK, self.NORMAL)


@verify(CONTINUOUS)
class HoleType(Enum):
    ALL = 0
    LIGHT = 1
    MEDIUM = 2
    HEAVY = 3


@verify(CONTINUOUS)
class DecayType(Flag):
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()
    UP = auto()
    TILE = auto()


@verify(CONTINUOUS)
class AttractType(Enum):
    NONE = 0
    ELECTRIC = 1
    STRONG = 2


@verify(CONTINUOUS)
class Collision(Enum):
    NONE = 0
    NORMAL = 1
    ANTI = 2


# pylint: disable=eq-without-hash
class SetProtocol(Generic[T_co], Protocol):
    def __contains__(self, value) -> bool:
        ...

    def __iter__(self) -> Iterator[T_co]:
        ...

    def __len__(self) -> int:
        ...

    def __le__(self, other) -> bool:
        ...

    def __lt__(self, other) -> bool:
        ...

    def __eq__(self, other) -> bool:
        ...

    def __ne__(self, other) -> bool:
        ...

    def __gt__(self, other) -> bool:
        ...

    def __ge__(self, other) -> bool:
        ...

    def __and__(self, other) -> SetProtocol:
        ...

    def __or__(self, other) -> SetProtocol:
        ...

    def __sub__(self, other) -> SetProtocol:
        ...

    def __xor__(self, other) -> SetProtocol:
        ...

    def isdisjoint(self, other) -> bool:
        ...


@frozen
class BoardProtocol(Protocol):
    r"""Generic board class for game"""
    width: int
    height: int
    goals: frozenset[int]
    obstacles: tuple[ObstacleType | None, ...]
    holes: tuple[HoleType | None, ...]
    decay: tuple[DecayType | None, ...]
    higgs: tuple[bool, ...]
    matter: tuple[MatterProtocol | None, ...]
    particle: tuple[ParticleProtocol | None, ...]
    filter: tuple[GeneralFilter, ...]
    matter_set: frozenset[MatterProtocol]
    prev_board: BoardProtocol | None

    def move_all(self) -> frozenset[Self]:
        ...

    def remove_single(self, single: SingleProtocol) -> Self:
        ...

    def add_single(self, single: SingleProtocol) -> Self:
        ...


@frozen
class MatterProtocol(Protocol):
    mass: MassType
    charge: ChargeType
    colour: ColourType

    def move_all(self, board: BoardProtocol) -> frozenset[BoardProtocol]:
        ...

    def to_dict(self) -> PathAttrs:
        ...

    @classmethod
    def from_path(cls, path: PathProtocol[Self]) -> Self:
        ...


@frozen
class ParticleProtocol(Protocol):
    position: int


@frozen
class ManyProtocol(SetProtocol[MatterProtocol], MatterProtocol, Protocol):
    matter_set: frozenset[MatterProtocol]
    horizontal: tuple[int]
    vertical: tuple[int]


@frozen
class SingleProtocol(MatterProtocol, ParticleProtocol, Protocol):
    ...


class AntiProtocol(Protocol):
    anti: AntiType

    def is_annihilation(self, other: MatterProtocol | None) -> bool:
        ...

    @staticmethod
    def is_path_annihilation(path: PathSingleProtocol[AntiSingleProtocol],
                             other: MatterProtocol | None) -> bool:
        ...


class AntiSingleProtocol(SingleProtocol, AntiProtocol, Protocol):
    ...


# class ChargeProtocol(Protocol):
#     charge: ChargeType

#     def attraction(self, other: ParticleProtocol) -> bool:
#         ...


class PathProtocol(Generic[MTT], Protocol):
    type: type[MTT]
    attrs_dict: PathAttrs


class PathTopProtocol(PathProtocol, Protocol):
    steps: int
    attraction: AttractType
    board: BoardProtocol
    undo: PathTopProtocol | None

    def advance(self) -> bool:
        ...

    def board_add(self) -> BoardProtocol:
        ...


class PathParticleProtocol(PathProtocol, Protocol):
    position: DirectionFilter
    current_pos: int


class PathSingleProtocol(Generic[ST],
                         PathTopProtocol,
                         PathParticleProtocol,
                         Protocol):
    type: type[ST]


class PathManyProtocol(PathTopProtocol, Protocol):
    matter_set: set[PathProtocol]
    particle_set: set[PathParticleProtocol]


@define
class PathSingle(Generic[ST], PathSingleProtocol):
    type: type[ST]
    position: DirectionFilter
    board: BoardProtocol
    attrs_dict: PathAttrs
    steps: int = field(default=0)
    attraction: AttractType = field(default=AttractType.NONE)
    current_pos: int = field(default=0)
    undo: PathTopProtocol | None = field(default=None)

    def __post_init__(self) -> None:
        self.current_pos = self.position[self.steps]

    def advance(self) -> bool:
        if self.steps >= len(self.position):
            return False
        self.undo = deepcopy(self)
        self.steps += 1
        self.current_pos = self.position[self.steps]
        return True

    @classmethod
    def from_single_direction(
            cls,
            particle: ST,
            position: DirectionFilter,
            board: BoardProtocol
    ) -> PathSingle:
        return cls(type(particle), position, board, particle.to_dict())

    def board_add(self) -> BoardProtocol:
        return self.board.add_single(self.type.from_path(self))


class StartProtocol(Generic[PTT], Protocol):
    direction_info: MutableSequence[PTT | None]

    def __init__(self, move: list[PTT]) -> None:
        ...

    def __getitem__(self, index: Direction) -> PTT | None:
        ...

    def __setitem__(self, index: Direction, value: PTT | None):
        ...

    def __iter__(self) -> Iterator[PTT | None]:
        ...

    def non_empty(self) -> Iterator[PTT]:
        ...


class Start(Generic[PTT], StartProtocol):
    def __init__(self, move: list[PTT | None]) -> None:
        self.direction_info = move

    def __getitem__(self, index: Direction) -> PTT | None:
        return self.direction_info[index.value]

    def __setitem__(self, index: Direction, value: PTT | None):
        self.direction_info[index.value] = value

    def __iter__(self) -> Iterator[PTT | None]:
        return iter(self.direction_info)

    def non_empty(self) -> Iterator[PTT]:
        return (value for value in self.direction_info if value is not None)


def new_single_start(
        single: SingleProtocol,
        board: BoardProtocol
) -> Start[PathSingle]:
    board = board.remove_single(single)

    direction_filters = board.filter[single.position]
    return Start([PathSingle.from_single_direction(
        single,
        direction_filters[direction.value],
        board
    ) for direction in Direction])


# @define
# class PathSingle(PathSingleProtocol):
#     position: DirectionFilter
#     ty pe: ty pe[ParticleProtocol]
#     attrs_dict: PathAttrs

#     @classmethod
#     def from_single(
#             cls,
#             particle: SingleProtocol,
#             position: DirectionFilter
#     ) -> PathSingle:
#         return cls(position, type(particle), particle.to_dict())


# def new_particle_move(
#         particle: ParticleProtocol,
#         board: BoardProtocol
# ) -> tuple[PathParticle, ...]:
#     direction_filters = board._filter[particle.position]
#     return tuple(PathParticle.from_single(
#         particle,
#         direction_filters[direction.value]
#     ) for direction in Direction)


# def new_moving(
#         cls: type[SingleProtocol],
#         single: SingleProtocol,
#         board: BoardProtocol
# ) -> list[Move]:
#     all_moving = new_particle_move(single, board)
#     return [Move(
#         cls,
#         all_moving[direction.value],
#         single.mass,
#         single.charge,
#         single.colour
#     ) for direction in Direction]


@define
class BoolPair:
    pos: bool
    neg: bool

    def __or__(self, other: BoolPair | Sequence[bool]) -> BoolPair:
        if isinstance(other, BoolPair):
            # type: ignore
            return BoolPair(self.pos | other.pos, self.neg | other.neg)
        if isinstance(other, Sequence):
            return BoolPair(self.pos | other[0], self.neg | other[1])
        raise TypeError(f"unsupported operand type(s) for |:"
                        f"'BoolPair' and {type(other)}")

    def __ior__(self, other: BoolPair | Sequence[bool]) -> Self:
        if isinstance(other, BoolPair):
            self.pos |= other.pos
            self.neg |= other.neg
            return self
        if isinstance(other, Sequence):
            self.pos |= other[0]
            self.neg |= other[1]
            return self
        raise TypeError(f"unsupported operand type(s) for |=:"
                        f"'BoolPair' and {type(other)}")

    def reverse(self) -> Self:
        self.pos, self.neg = self.neg, self.pos
        return self


# class _GenerationProtocol(Protocol):
#     generation: GenerationType
