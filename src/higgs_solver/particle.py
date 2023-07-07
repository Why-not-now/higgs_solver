from collections.abc import Iterator, Set
from enum import CONTINUOUS, NAMED_FLAGS, Enum, Flag, auto, verify
from typing import TYPE_CHECKING, Literal

from attrs import define, field

if TYPE_CHECKING:
    from .board import Board, Direction


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
    HADRON = auto()
    NEG_QUARK = auto()
    POS_QUARK = auto()


@verify(CONTINUOUS)
class ParticleType(Enum):
    CHARGED_LEPTON = auto()
    NEUTRINO = auto()
    PROTON = auto()
    NEUTRON = auto()

    WBOSON = auto()     # tentative
    NEG_QUARK = auto()
    POS_QUARK = auto()


@verify(CONTINUOUS)
class GenerationType(Enum):
    FIRST = auto()
    SECOND = auto()
    THIRD = auto()


@verify(CONTINUOUS)
class ChargeType(Enum):
    NEGATIVE = -1
    NEUTRAL = 0
    POSITIVE = 1


@verify(CONTINUOUS)
class WeightType(Enum):
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


@define(frozen=True)
class Matter(Set):  # add individual?
    particle_set: frozenset["Particle | Matter"]
    type: MatterType
    anti: AntiType
    mass: WeightType
    charge: ChargeType
    colour: ColourType

    def __contains__(self, value) -> bool:
        return value in self.particle_set

    def __iter__(self) -> Iterator["Particle | Matter"]:
        return iter(self.particle_set)

    def __len__(self) -> int:
        return len(self.particle_set)

    def generate_function(self):
        raise NotImplementedError

    # pylint: disable=unused-argument
    def move(self, board: "Board", direction: "Direction") \
            -> "Board | Literal[False]":
        return board


@define(frozen=True)
class Particle:
    x: int
    y: int
    type: ParticleType
    generation: GenerationType

    anti: AntiType = field(default=AntiType.ORDINARY)
    mass: WeightType = field(default=WeightType.LIGHT)
    charge: ChargeType = field(default=ChargeType.NEUTRAL)
    colour: ColourType = field(default=ColourType.WHITE)

    def is_annihilation(self, other: "Particle") -> bool:
        return (self.type == other.type) & \
               (self.generation == other.generation) & \
               (self.colour == other.colour) & \
               (self.anti != other.anti)
