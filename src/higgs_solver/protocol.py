from __future__ import annotations

from collections.abc import Hashable, Iterator, Sequence
from enum import CONTINUOUS, NAMED_FLAGS, Enum, Flag, auto, verify
from typing import Any, Generic, Protocol, Self, TypeAlias, TypeVar

from attrs import define, field, frozen

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)

DirectionFilter: TypeAlias = tuple[int, ...]
LeftFilter: TypeAlias = DirectionFilter
DownFilter: TypeAlias = DirectionFilter
RightFilter: TypeAlias = DirectionFilter
UpFilter: TypeAlias = DirectionFilter
GeneralFilter: TypeAlias = \
    tuple[LeftFilter, RightFilter, UpFilter, DownFilter]
OptionalMove: TypeAlias = "MovingProtocol | None"
AllMoveDirection: TypeAlias = \
    tuple[OptionalMove, OptionalMove, OptionalMove, OptionalMove]


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


@verify(NAMED_FLAGS, CONTINUOUS)
class ColourType(Flag):
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    ANTIRED = GREEN | BLUE
    ANTIGREEN = RED | BLUE
    ANTIBLUE = RED | GREEN
    WHITE = RED | GREEN | BLUE


@verify(CONTINUOUS)
class MatterType(Enum):
    CHARGED_LEPTON = auto()
    NEUTRINO = auto()
    PROTON = auto()
    NEUTRON = auto()
    STABLE_NUCLEUS = auto()
    UNSTABLE_NUCLEUS = auto()

    WBOSON = auto()     # tentative
    PION = auto()
    BARYON = auto()
    NEG_QUARK = auto()
    POS_QUARK = auto()


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
    _filter: tuple[GeneralFilter, ...]
    _matter_set: frozenset[MatterProtocol]
    _prev_board: Self | None

    def move_all(self) -> frozenset[Self]:
        ...


@frozen
class MatterProtocol(SetProtocol["ParticleProtocol"], Hashable, Protocol):
    particle_set: frozenset[ParticleProtocol]
    type: MatterType
    mass: MassType
    charge: ChargeType
    colour: ColourType
    anti: AntiType

    def move_all(self, board: BoardProtocol) -> frozenset[BoardProtocol]:
        ...


@frozen
class ManyProtocol(MatterProtocol, Protocol):
    matter_set: frozenset[MatterProtocol]


@frozen
class ParticleProtocol(Protocol):
    position: int
    anti: AntiType

    def particle_init(self, other: MovingParticle) -> None:
        ...

    def is_annihilation(self, other: ParticleProtocol) -> bool:
        ...


class StartingProtocol(Protocol):
    matter: MatterProtocol
    _direction_info: AllMoveDirection

    def __getitem__(self, index: Direction) -> OptionalMove:
        ...

    def __setitem__(self, index: Direction, value: OptionalMove):
        ...

    def __iter__(self) -> Iterator[OptionalMove]:
        ...

    def nonempty(self) -> Iterator[MovingProtocol]:
        ...


# class MovingParticleProtocol(Protocol):
#     ty pe: t ype[ParticleProtocol]
#     position: list[int]
#     prev_position: int | None
#     anti: AntiType


class MovingProtocol(Protocol):
    mass: MassType
    charge: ChargeType
    colour: ColourType
    anti: AntiType
    steps: int
    attraction: AttractType
    replace: dict[str, Any]


@define(slots=False)
class MovingParticle:
    particle: ParticleProtocol
    position: DirectionFilter
    type: type[ParticleProtocol]

    def __attrs_post_init__(self) -> None:  # pylint: disable=bad-dunder-name
        self.particle.particle_init(self)

    @classmethod
    def from_particle(
            cls,
            particle: ParticleProtocol,
            position: DirectionFilter
    ) -> MovingParticle:
        return cls(particle, position, type(particle))

    def is_annihilation(self, other: ParticleProtocol) -> bool:
        return self.type.is_annihilation(self, other)  # type: ignore


@define
class Moving:
    type: type[ParticleProtocol]
    particle_set: list[MovingParticle]
    mass: MassType
    charge: ChargeType
    colour: ColourType
    anti: AntiType
    steps: int = field(default=0)
    attraction: AttractType = field(default=AttractType.NONE)
    replace: dict[str, Any] = field(factory=set)


def new_particle_move(
        particle: ParticleProtocol,
        board: BoardProtocol
) -> tuple[MovingParticle, ...]:
    direction_filters = board._filter[particle.position]
    return tuple(MovingParticle.from_particle(
        particle,
        direction_filters[direction.value]
    ) for direction in Direction)


def new_moving(
        cls: type[ParticleProtocol],
        matter: MatterProtocol,
        board: BoardProtocol
) -> list[Moving]:
    particles = tuple(new_particle_move(p, board) for p in matter.particle_set)
    return [Moving(
        cls,
        [p[direction.value] for p in particles],
        matter.mass,
        matter.charge,
        matter.colour,
        matter.anti
    ) for direction in Direction]


@define
class BoolPair:
    pos: bool = False
    neg: bool = False

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


# class _GenerationProtocol(Protocol):
#     generation: GenerationType
