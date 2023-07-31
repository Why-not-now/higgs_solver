from __future__ import annotations

from collections.abc import Iterator
from typing import Any, Self, TypeVar, cast

from attr import evolve
from attrs import field, frozen

from higgs_solver.logic import (annihilation_destroy, anti_single_check,
                                electric_single, hole_single_check,
                                matter_collision_single_check,
                                obstacle_destroy_single_check,
                                obstacle_exists_single_check)
from higgs_solver.protocol import (AntiSingleProtocol, AntiType, BoardProtocol,
                                   ChargeType, ColourType, MassType,
                                   MatterProtocol, PathAttrs, PathSingle,
                                   PathSingleProtocol, new_single_start)

AST_co = TypeVar("AST_co", covariant=True, bound="AntiSingleProtocol")

# def freeze_setatr(self, *args) -> NoReturn:
#     """Disables setting attributes via
#     item.prop = val or item['prop'] = val
#     """
#     raise TypeError(
#         'Immutable objects cannot have properties set after init'
#     )


# def freeze_delatr(self, *args) -> NoReturn:
#     """Disables deleting properties"""
#     raise TypeError(
#         'Immutable objects cannot have properties deleted'
#     )


def fixed_attr(default: Any, **kwargs):
    return field(default=default, repr=False, init=False, eq=False, **kwargs)


@frozen(cache_hash=True)
class Electron(AntiSingleProtocol):
    position: int
    anti: AntiType = field(default=AntiType.ORDINARY)
    mass: MassType = fixed_attr(MassType.LIGHT)
    charge: ChargeType = fixed_attr(None)
    colour: ColourType = fixed_attr(ColourType.WHITE)

    def __attrs_post_init__(self) -> None:  # pylint: disable=bad-dunder-name
        anti_multiplier = -1 if self.anti.value else 1
        if self.charge is None:
            object.__setattr__(self, "charge",
                               ChargeType(anti_multiplier * -1))

    def move_all(self, board: BoardProtocol) -> frozenset[BoardProtocol]:
        new_boards: list[BoardProtocol] = []

        start = new_single_start(self, board)
        start = electric_single(start,
                                self.charge,
                                self.position,
                                board)
        for move in cast(Iterator[PathSingle[Electron]],
                         start.non_empty()):
            if (new_board := Electron.move_one(move)) is not None:
                new_boards.append(evolve(
                    new_board,
                    prev_board=board
                ))  # type: ignore

        return frozenset(new_boards)

    @classmethod
    # type: ignore[override]
    def from_path(cls, path: PathSingle[Self]) -> Self:
        return cls(path.current_pos, anti=path.attrs_dict['anti'])

    @staticmethod
    def move_one(path: PathSingle[Electron]) -> BoardProtocol | None:
        for _ in iter(path.advance, False):
            if matter_collision_single_check(path):     # particle
                if anti_single_check(path):
                    other = cast(Electron, path.board.matter[path.current_pos])
                    return annihilation_destroy(
                        1,
                        (other.position,),
                        path.board.remove_single(other)
                    )

                if path.undo is None:
                    return None
                return path.undo.board_add()

            if obstacle_exists_single_check(path):      # obstacle
                if not obstacle_destroy_single_check(path):
                    if path.undo is None:
                        return None
                    return path.undo.board_add()

                obstacles = list(path.board.obstacles)      # remove obstacle
                obstacles[path.current_pos] = None
                path.board = evolve(
                    path.board,
                    obstacles=tuple(obstacles)
                )  # type: ignore

            if hole_single_check(path):                 # hole
                return path.board
        if not path.steps:      # if move.steps == 0
            return None
        return path.board.add_single(Electron.from_path(path))

    def to_dict(self) -> PathAttrs:
        return {
            'mass': MassType.LIGHT,
            'charge': ChargeType.NEGATIVE,
            'colour': ColourType.WHITE,
            'anti': self.anti
        }

    def is_annihilation(self, other: MatterProtocol | None) -> bool:
        if isinstance(other, Electron):
            return self.anti != other.anti
        return False

    @staticmethod
    def is_path_annihilation(path: PathSingleProtocol[AST_co],
                             other: MatterProtocol | None) -> bool:
        if isinstance(other, Electron):
            if 'anti' in path.attrs_dict:
                return path.attrs_dict['anti'] != other.anti
            raise ValueError("attrs_dict does not have the correct attrs")
        return False


# @frozen(cache_hash=True)
# class Muon(SingleProtocol, AntiProtocol):
#     position: int
#     mass: MassType
#     charge: ChargeType = \
#         field(default=ChargeType.NEGATIVE, repr=False, init=False)
#     colour: ColourType = \
#         field(default=ColourType.WHITE, repr=False, init=False)
#     anti: AntiType = \
#         field(default=AntiType.ORDINARY)

#     def move_all(self, board: BoardProtocol) -> list[Moving]:
#         moving = new_moving(Muon, self, board)

#         return moving

#     def to_dict(self) -> PathAttrs:
#         return {'mass': self.mass, 'anti': self.anti}

#     def moving_init(self, other: Any) -> None:
#         other.anti = self.anti  # type: ignore
#         # pylint: disable=no-value-for-parameter
#         other.is_annihilation = self.is_annihilation.__get__(other)

#     @classmethod
#     def step(cls, board: BoardProtocol) -> frozenset[BoardProtocol]:
#         return frozenset((board,))

#     def is_annihilation(self, other: ParticleProtocol) -> bool:
#         if isinstance(other, Muon):
#             return self.anti != other.anti
#         return False


# @frozen(cache_hash=True)
# class Tau(SingleProtocol, AntiProtocol):
#     position: int
#     mass: MassType
#     charge: ChargeType = \
#         field(default=ChargeType.NEGATIVE, repr=False, init=False)
#     colour: ColourType = \
#         field(default=ColourType.WHITE, repr=False, init=False)
#     anti: AntiType = \
#         field(default=AntiType.ORDINARY)

#     def move_all(self, board: BoardProtocol) -> frozenset[BoardProtocol]:
#         moving = new_moving(Tau, self, board)

#         return frozenset((board,))

#     def moving_init(self, other: Any) -> None:
#         other.anti = self.anti  # type: ignore
#         # pylint: disable=no-value-for-parameter
#         other.is_annihilation = self.is_annihilation.__get__(other)

#     def is_annihilation(self, other: ParticleProtocol) -> bool:
#         if isinstance(other, Tau):
#             return self.anti != other.anti
#         return False


# @frozen(cache_hash=True)
# class ChargedLeptonMatter(MatterProtocol):  # add individual?
#     mass: MassType
#     charge: ChargeType = \
#         field(default=ChargeType.NEGATIVE, repr=False, init=False)
#     colour: ColourType = \
#         field(default=ColourType.WHITE, repr=False, init=False)
#     anti: AntiType = \
#         field(default=AntiType.ORDINARY)

#     def move_all(self, board: BoardProtocol) -> frozenset[BoardProtocol]:
#         moving = new_moving(ChargedLeptonMatter, self, board)

#         return frozenset((board,))


# @frozen(cache_hash=True)
# class ElectrinoParticle(ParticleProtocol, AntiProtocol):
#     position: int

#     anti: AntiType = \
#         field(default=AntiType.ORDINARY)

#     def moving_init(self, other: Any) -> None:
#         other.anti = self.anti  # type: ignore
#         # pylint: disable=no-value-for-parameter
#         other.is_annihilation = self.is_annihilation.__get__(other)

#     def is_annihilation(self, other: ParticleProtocol) -> bool:
#         if isinstance(other, ElectrinoParticle):
#             return self.anti != other.anti
#         return False


# @frozen(cache_hash=True)
# class Mutrino(SingleProtocol, AntiProtocol):
#     position: int

#     anti: AntiType = \
#         field(default=AntiType.ORDINARY)

#     def moving_init(self, other: Any) -> None:
#         other.anti = self.anti  # type: ignore
#         # pylint: disable=no-value-for-parameter
#         other.is_annihilation = self.is_annihilation.__get__(other)

#     def is_annihilation(self, other: ParticleProtocol) -> bool:
#         if isinstance(other, Mutrino):
#             return self.anti != other.anti
#         return False


# @frozen(cache_hash=True)
# class Tautrino(SingleProtocol, AntiProtocol):
#     position: int

#     anti: AntiType = \
#         field(default=AntiType.ORDINARY)

#     def moving_init(self, other: Any) -> None:
#         other.anti = self.anti  # type: ignore
#         # pylint: disable=no-value-for-parameter
#         other.is_annihilation = self.is_annihilation.__get__(other)

#     def is_annihilation(self, other: ParticleProtocol) -> bool:
#         if isinstance(other, Tautrino):
#             return self.anti != other.anti
#         return False


# @frozen(cache_hash=True)
# class Proton(SingleProtocol, AntiProtocol):
#     position: int

#     anti: AntiType = \
#         field(default=AntiType.ORDINARY)

#     def moving_init(self, other: Any) -> None:
#         other.anti = self.anti  # type: ignore
#         # pylint: disable=no-value-for-parameter
#         other.is_annihilation = self.is_annihilation.__get__(other)

#     def is_annihilation(self, other: ParticleProtocol) -> bool:
#         if isinstance(other, Proton):
#             return self.anti != other.anti
#         return False


# @frozen(cache_hash=True)
# class Neutron(SingleProtocol, AntiProtocol):
#     position: int

#     anti: AntiType = \
#         field(default=AntiType.ORDINARY)

#     def moving_init(self, other: Any) -> None:
#         other.anti = self.anti  # type: ignore
#         # pylint: disable=no-value-for-parameter
#         other.is_annihilation = self.is_annihilation.__get__(other)

#     def is_annihilation(self, other: ParticleProtocol) -> bool:
#         if isinstance(other, Neutron):
#             return self.anti != other.anti
#         return False
