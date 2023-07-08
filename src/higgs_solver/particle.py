from __future__ import annotations

from collections.abc import Iterable, Iterator, Set
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


@define(frozen=True)
class Matter(Set):  # add individual?
    particle_set: frozenset[Particle | Matter]
    type: MatterType
    charge: ChargeType
    colour: ColourType
    anti: AntiType

    def __contains__(self, value) -> bool:
        return value in self.particle_set

    def __iter__(self) -> Iterator[Particle | Matter]:
        return iter(self.particle_set)

    def __len__(self) -> int:
        return len(self.particle_set)


@define(frozen=True)
class Particle:
    x: int
    y: int
    type: ParticleType
    generation: GenerationType

    mass: MassType = field(default=MassType.LIGHT)
    charge: ChargeType = field(default=ChargeType.NEUTRAL)
    colour: ColourType = field(default=ColourType.WHITE)
    anti: AntiType = field(default=AntiType.ORDINARY)

    def is_annihilation(self, other: Particle) -> bool:
        return (self.type == other.type) & \
               (self.generation == other.generation) & \
               (self.colour == other.colour) & \
               (self.anti != other.anti)

    def is_fall(self, other: HoleType) -> bool:
        return self.mass.value < other.value


def create_matter(
        particles: Iterable[Particle | Matter],
        matter_type: MatterType,
        charge: ChargeType,
        colour: ColourType,
        anti: AntiType) -> Matter:
    return Matter(
        frozenset(particles),
        matter_type,
        charge,
        colour,
        anti
    )


def _create_charged_lepton(
        x: int,
        y: int,
        generation: GenerationType,
        mass: MassType | None = None,
        anti: AntiType = AntiType.ORDINARY
) -> Matter:
    if mass is None:
        mass_tuple = (MassType.LIGHT, MassType.MEDIUM, MassType.HEAVY)
        mass = mass_tuple[generation.value - 1]
    return Matter(
        frozenset({Particle(
            x,
            y,
            ParticleType.CHARGED_LEPTON,
            generation,
            mass,
            ChargeType.NEGATIVE,
            ColourType.WHITE,
            anti
        )}),
        MatterType.CHARGED_LEPTON,
        ChargeType.NEGATIVE,
        ColourType.WHITE,
        anti
    )


def create_electron(
        x: int,
        y: int,
        anti: AntiType = AntiType.ORDINARY
) -> Matter:
    return _create_charged_lepton(
        x,
        y,
        GenerationType.FIRST,
        MassType.LIGHT,
        anti
    )


def create_muon(
        x: int,
        y: int,
        anti: AntiType = AntiType.ORDINARY
) -> Matter:
    return _create_charged_lepton(
        x,
        y,
        GenerationType.SECOND,
        MassType.MEDIUM,
        anti
    )


def create_tau(
        x: int,
        y: int,
        anti: AntiType = AntiType.ORDINARY
) -> Matter:
    return _create_charged_lepton(
        x,
        y,
        GenerationType.THIRD,
        MassType.HEAVY,
        anti
    )


def _create_neutrino(
        x: int,
        y: int,
        generation: GenerationType,
        anti: AntiType = AntiType.ORDINARY
) -> Matter:
    return Matter(
        frozenset({Particle(
            x,
            y,
            ParticleType.NEUTRINO,
            generation,
            MassType.LIGHT,
            ChargeType.NEUTRAL,
            ColourType.WHITE,
            anti
        )}),
        MatterType.NEUTRINO,
        ChargeType.NEUTRAL,
        ColourType.WHITE,
        anti
    )


def create_electrino(
        x: int,
        y: int,
        anti: AntiType = AntiType.ORDINARY
) -> Matter:
    return _create_neutrino(
        x,
        y,
        GenerationType.FIRST,
        anti
    )


def create_mutrino(
        x: int,
        y: int,
        anti: AntiType = AntiType.ORDINARY
) -> Matter:
    return _create_neutrino(
        x,
        y,
        GenerationType.SECOND,
        anti
    )


def create_tautrino(
        x: int,
        y: int,
        anti: AntiType = AntiType.ORDINARY
) -> Matter:
    return _create_neutrino(
        x,
        y,
        GenerationType.THIRD,
        anti
    )


def create_proton(
        x: int,
        y: int,
        anti: AntiType = AntiType.ORDINARY
) -> Matter:
    return Matter(
        frozenset({Particle(
            x,
            y,
            ParticleType.PROTON,
            GenerationType.FIRST,
            MassType.LIGHT,
            ChargeType.NEUTRAL,
            ColourType.WHITE,
            anti
        )}),
        MatterType.NEUTRINO,
        ChargeType.NEUTRAL,
        ColourType.WHITE,
        anti
    )
