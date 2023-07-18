from __future__ import annotations

# pylint: disable=unused-import
# flake8: noqa: F401
from higgs_solver.protocol import (AntiType, BoardProtocol, ChargeType,
                                   ColourType, DirectionFilter, MassType,
                                   MatterProtocol, MatterType,
                                   ParticleProtocol, BoolPair)


def _electric_f(
        board: BoardProtocol,
        charge: ChargeType,
        directional_filter: DirectionFilter
) -> tuple[bool, bool]:
    for x_plus in directional_filter:
        if (matter := board.matter[x_plus]) is None:
            continue
        attraction = matter.charge.value * charge.value
        if attraction == -1:
            return True, False
        if attraction == 1:
            return False, True
    return False, False


def _electric_p(
        board: BoardProtocol,
        position: int,
        charge: ChargeType
):
    all_filter = board._filter[position]
    horizontal = BoolPair()
    horizontal |= _electric_f(board, charge, all_filter[0])
    horizontal |= _electric_f(board, charge, all_filter[2])[::-1]
    match horizontal:
        case BoolPair(pos, neg) if pos == neg:
            hor
    vertical = BoolPair()
    vertical |= _electric_f(board, charge, all_filter[1])
    vertical |= _electric_f(board, charge, all_filter[3])[::-1]


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
