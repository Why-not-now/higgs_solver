from __future__ import annotations

from typing import cast
import cProfile
import os
import pstats
from multiprocessing import Pool, cpu_count

from higgs_solver.board import Board, default_board, new_board
from higgs_solver.particle import Electron
# from higgs_solver.protocol import MatterProtocol  # , ObstacleType


DEBUG = False


def evaluate_board(evaluating: Board) -> set[Board]:
    return evaluating.move_all()


def create_board() -> Board:
    width = 7
    height = 8

    def pos(x: int, y: int) -> int:
        return y * width + x

    def coords(i: int) -> tuple[int, int]:
        return divmod(i, width)

    goals = frozenset({
        pos(3, 3)
    })
    obstacles = (
        None, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
    )
    electrons_grid = (
        0, 0, 1, 1, 1, 0, 0,
        0, 1, 1, 0, 1, 1, 0,
        1, 1, 0, 0, 0, 1, 1,
        1, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 1,
        1, 1, 0, 0, 0, 1, 1,
        0, 1, 1, 0, 1, 1, 0,
        0, 0, 1, 1, 1, 0, 0,
    )
    electrons = tuple(
        Electron(i) for i, x in enumerate(electrons_grid) if x == 1
    )
    matter = list(default_board(width, height))
    particle = list(default_board(width, height))
    for e in electrons:
        matter[e.position] = e  # type: ignore
        particle[e.position] = e  # type: ignore
    return new_board(
        width,
        height,
        obstacles=obstacles,
        goals=goals,
        matter=tuple(matter),
        particle=tuple(particle)
    )


def solve() -> None:
    MAX_EVAL = 10
    MAX_CPU = 8

    # start 8 worker processes
    with Pool(processes=min(MAX_CPU, cpu_count() - 1 or 1)) as pool:
        winning: Board | None = None

        visited: set[Board] = set()
        current = {create_board()}
        evaluated: set[Board] = set()
        for i in range(MAX_EVAL):

            print(f"step {i + 1}")

            evaluated = cast(set[Board], set.union(
                *((evaluate_board(board) for board in current) if DEBUG else
                  pool.imap_unordered(evaluate_board, current))  # not debug
            ))

            visited |= current
            print(len(visited))
            print(len(current))
            current = evaluated - visited
            print(len(evaluated))
            print(len(current))

            print(f"visited length: {len(visited)}")
            # print(*(_._str() for _ in visited))
            for board in current:
                if board.win():
                    winning = board
                    break
            if winning is not None:
                break

            print(f"next length: {len(current)}")
            # print(*(_._str() for _ in current))
            if not current:
                break

            print("")

    if winning is None:
        print("There is no solution")
        return
    current_set = winning.matter_set
    winning = winning.prev_board
    while winning is not None:  # pylint: disable=while-used
        print(f"{set(current_set - winning.matter_set)} <- "
              f"{set(winning.matter_set - current_set)}")
        current_set = winning.matter_set
        winning = winning.prev_board


def main() -> None:
    if DEBUG:
        with cProfile.Profile() as pr:
            solve()

        stats = pstats.Stats(pr)
        stats.sort_stats(pstats.SortKey.TIME)
        # stats.print_stats()
        i = 1
        # pylint: disable=while-used
        while os.path.exists(f"solver_profiling_sync{i}.prof"):
            i += 1

        print(f"writing to \"solver_profiling_sync{i}.prof\"")
        stats.dump_stats(filename=f"solver_profiling_sync{i}.prof")
    else:
        solve()


if __name__ == '__main__':
    main()

# learn multiprocessing

# create visited boards set
# create current boards set
# create evaluated boards set

# move current set to visited set
# move evaluated set to current set
# evaluated set remove current set
