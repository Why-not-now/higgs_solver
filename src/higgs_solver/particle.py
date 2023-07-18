from __future__ import annotations

from collections.abc import Iterator, Set

from attrs import field, frozen

from higgs_solver.protocol import (AntiType, BoardProtocol, ChargeType,
                                   ColourType, MassType, MatterProtocol,
                                   MatterType, ParticleProtocol)


@frozen
class ElectronParticle(ParticleProtocol):
    position: int

    anti: AntiType = \
        field(default=AntiType.ORDINARY)

    def is_annihilation(self, other: ParticleProtocol) -> bool:
        if isinstance(other, ElectronParticle):
            return self.anti != other.anti
        return False


@frozen
class MuonParticle(ParticleProtocol):
    position: int

    anti: AntiType = \
        field(default=AntiType.ORDINARY)

    def is_annihilation(self, other: ParticleProtocol) -> bool:
        if isinstance(other, MuonParticle):
            return self.anti != other.anti
        return False


@frozen
class TauParticle(ParticleProtocol):
    position: int

    anti: AntiType = \
        field(default=AntiType.ORDINARY)

    def is_annihilation(self, other: ParticleProtocol) -> bool:
        if isinstance(other, TauParticle):
            return self.anti != other.anti
        return False


@frozen
class ChargedLeptonMatter(Set):  # add individual?
    particle_set: frozenset[ParticleProtocol]
    type: MatterType = \
        field(default=MatterType.CHARGED_LEPTON, repr=False, init=False)
    charge: ChargeType = \
        field(default=ChargeType.NEGATIVE, repr=False, init=False)
    colour: ColourType = \
        field(default=ColourType.WHITE, repr=False, init=False)
    anti: AntiType = \
        field(default=AntiType.ORDINARY)

    def __contains__(self, value) -> bool:
        return value in self.particle_set

    def __iter__(self) -> Iterator[ParticleProtocol]:
        return iter(self.particle_set)

    def __len__(self) -> int:
        return len(self.particle_set)

    def move_all(self, board: BoardProtocol) -> frozenset[BoardProtocol]:
        

        return frozenset(self)


@frozen
class ElectrinoParticle(ParticleProtocol):
    position: int

    anti: AntiType = \
        field(default=AntiType.ORDINARY)

    def is_annihilation(self, other: ParticleProtocol) -> bool:
        if isinstance(other, ElectrinoParticle):
            return self.anti != other.anti
        return False


@frozen
class MutrinoParticle(ParticleProtocol):
    position: int

    anti: AntiType = \
        field(default=AntiType.ORDINARY)

    def is_annihilation(self, other: ParticleProtocol) -> bool:
        if isinstance(other, MutrinoParticle):
            return self.anti != other.anti
        return False


@frozen
class TautrinoParticle(ParticleProtocol):
    position: int

    anti: AntiType = \
        field(default=AntiType.ORDINARY)

    def is_annihilation(self, other: ParticleProtocol) -> bool:
        if isinstance(other, TautrinoParticle):
            return self.anti != other.anti
        return False


@frozen
class ProtonParticle(ParticleProtocol):
    position: int

    anti: AntiType = \
        field(default=AntiType.ORDINARY)

    def is_annihilation(self, other: ParticleProtocol) -> bool:
        if isinstance(other, ProtonParticle):
            return self.anti != other.anti
        return False


@frozen
class NeutronParticle(ParticleProtocol):
    position: int

    anti: AntiType = \
        field(default=AntiType.ORDINARY)

    def is_annihilation(self, other: ParticleProtocol) -> bool:
        if isinstance(other, NeutronParticle):
            return self.anti != other.anti
        return False
