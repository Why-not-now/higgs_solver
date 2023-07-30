from __future__ import annotations

# pylint: disable=unused-import
# flake8: noqa: F401
from typing import TypeVar, cast

from higgs_solver.protocol import (AntiProtocol, AntiSingleProtocol, AntiType,
                                   AttractType, BoardProtocol, BoolPair,
                                   ChargeType, Direction, DirectionFilter,
                                   ObstacleType, PathManyProtocol,
                                   PathSingleProtocol, SingleProtocol, Start,
                                   horizontal, vertical)

PST = TypeVar("PST", bound=PathSingleProtocol)
PMT = TypeVar("PMT", bound=PathManyProtocol)


def electric_path(
        board: BoardProtocol,
        charge: ChargeType,
        path: DirectionFilter
) -> BoolPair:
    for x_plus in path:
        if (matter := board.matter[x_plus]) is None:
            continue
        attraction = matter.charge.value * charge.value
        if attraction == -1:
            return BoolPair(True, False)
        if attraction == 1:
            return BoolPair(False, True)
    return BoolPair(False, False)


def electric_single(
        single: Start[PST],
        charge: ChargeType,
        position: int,
        board: BoardProtocol
) -> Start[PST]:
    all_filter = board.filter[position]
    for straight in (horizontal, vertical):
        axis = BoolPair(False, False)   # BoolPair(right/up, left/down) pos,neg
        axis |= electric_path(board,
                              charge,
                              all_filter[straight[0].value])
        axis |= electric_path(board,
                              charge,
                              all_filter[straight[1].value]).reverse()
        match axis:
            case BoolPair(True, False):
                single[straight[1]] = None
                if (attracted := single[straight[0]]) is not None:
                    attracted.attraction = AttractType.ELECTRIC
            case BoolPair(False, True):
                single[straight[0]] = None
                if (attracted := single[straight[1]]) is not None:
                    attracted.attraction = AttractType.ELECTRIC
            # case BoolPair(pos, neg) if pos == neg:  # for checks
            #     pass
    return single


def matter_collision_single_check(
        single: PathSingleProtocol[SingleProtocol]
) -> bool:
    return single.board.matter[single.current_pos] is not None


def obstacle_destroy_single_check(
        single: PathSingleProtocol[SingleProtocol]
) -> bool:
    obstacle = cast(ObstacleType, single.board.obstacles[single.current_pos])
    if single.attraction is not AttractType.NONE:
        return obstacle.is_weak()
    return False


def obstacle_exists_single_check(
        single: PathSingleProtocol[SingleProtocol]
) -> bool:
    return single.board.obstacles[single.current_pos] is None


def anti_single_check(
        single: PathSingleProtocol[AntiSingleProtocol]
) -> bool:
    return single.type.is_path_annihilation(
        single,
        single.board.matter[single.current_pos]
    )


def hole_single_check(
        single: PathSingleProtocol[SingleProtocol]
) -> bool:
    if (hole := single.board.holes[single.current_pos]) is None:
        return False
    return hole.value <= single.attrs_dict['mass'].value


# def electric_many(
#         many: Start[PMT],
#         charge: ChargeType,
#         positions: list[int],
#         board: BoardProtocol
# ) -> Start[PMT]:
#     for p in positions:
#         many = electric_single(many, charge, p, board)
#     return many


# pre movement

# TODO: direction (also ambiguity)
# TODO:     strong force (attraction)
# TODO:     electromagnetic repulsion/attraction

# TODO: decay??? (how to create particle)
# TODO:     if particle is none then continue
# TODO:     if particle is annihilation then annihilate
# TODO:     else false

# TODO: higgs

# movement

# TODO: particle collision (sans antimatter, check move flag)

# TODO: obstacle destruction (if attraction flag)

# TODO: obstacle collision

# TODO: antimatter annihilation (add to annihilation flag)

# TODO: higgs (if not attraction flag)

# TODO: holes (set holes flag)

# TODO: strong force (if not strong attraction flag)

# post movement

# TODO: light/heavy annihilation (annihilation flag, check connected component)

# TODO: hadron formation (which way to combine? Ambiguity here. Set false hole)

# TODO: nucleus formation

# TODO: check holes, set flag (if holes is None)

# TODO: breaking holes

# TODO: add situation awareness
