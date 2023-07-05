from enum import CONTINUOUS, NAMED_FLAGS, Enum, Flag, verify, auto
from typing import TYPE_CHECKING

from attrs import define, field

if TYPE_CHECKING:
    from .board import Board


@verify(NAMED_FLAGS, CONTINUOUS)
class Colour(Flag):
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    ANTIRED = GREEN | BLUE
    ANTIGREEN = RED | BLUE
    ANTIBLUE = RED | GREEN
    WHITE = RED | GREEN | BLUE


@verify(CONTINUOUS)
class ParticleType(Enum):
    ELECTRON = auto()
    MUON = auto()
    TAU = auto()
    ELECTRINO = auto()  # flavour?
    MUTRINO = auto()
    TAUTRINO = auto()
    PROTON = auto()
    NEUTRON = auto()
    STABLE_NUCLEUS = auto()
    UNSTABLE_NUCLEUS = auto()
    WBOSON = auto()     # tentative
    HADRON = auto()
    PION = auto()


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
    TILE = auto()
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()


@define(frozen=True)
class Particles:
    mass: int
    charge: int
    colour: Colour
    type: ParticleType
    particles_set: frozenset["Particle | Particles"]

    def left(self, board: "Board"):
        pass


@define(frozen=True)
class Particle:
    x: int
    y: int
    mass: int
    charge: int = field(default=0)
    colour: Colour = field(default=Colour.WHITE)
