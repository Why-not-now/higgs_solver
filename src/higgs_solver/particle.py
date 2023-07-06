from enum import CONTINUOUS, NAMED_FLAGS, Enum, Flag, verify, auto
from typing import TYPE_CHECKING

from attrs import define, field

if TYPE_CHECKING:
    from .board import Board, Direction


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
class MatterType(Enum):
    CHARGED_LEPTON = auto()
    NEUTRINO = auto()
    PROTON = auto()
    NEUTRON = auto()
    STABLE_NUCLEUS = auto()
    UNSTABLE_NUCLEUS = auto()
    WBOSON = auto()     # tentative
    HADRON = auto()
    PION = auto()
    QUARK = auto()


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
class Matter:  # add individual?
    mass: int
    charge: int
    colour: Colour
    type: MatterType
    matter_set: frozenset["Particle | Matter"]

    def generate_function(self):
        raise NotImplementedError

    # pylint: disable=unused-argument
    def move(self, board: "Board", direction: "Direction") -> "Board":
        return board


@define(frozen=True)
class Particle:
    x: int
    y: int
    mass: int = field(default=0)
    charge: int = field(default=0)
    colour: Colour = field(default=Colour.WHITE)
