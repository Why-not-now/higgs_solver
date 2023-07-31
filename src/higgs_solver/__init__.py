def main():
    import pprint

    from typing import TypeVar

    from higgs_solver.board import new_board, default_board
    from higgs_solver.protocol import AntiType, ObstacleType
    from higgs_solver.particle import Electron

    T = TypeVar("T")
    pp = pprint.PrettyPrinter(indent=4)
    width = 7
    height = 8

    def pprint_grid(tup: tuple[T, ...]) -> tuple[tuple[T, ...], ...]:
        return tuple(tup[i:i + width] for i in range(0, width * height, width))

    def pos(x: int, y: int) -> int:
        return y * width + x

    obstacles = (
        None, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
        ObstacleType.STRONG, None, None, None, None, None, ObstacleType.STRONG,
        None, None, None, None, None, None, None,
        ObstacleType.STRONG, None, None, None, None, None, ObstacleType.STRONG,
        None, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
    )
    electrons = (Electron(pos(0, 3)),
                 Electron(pos(6, 3), anti=AntiType.ANTI))
    matter = list(default_board(width, height))
    particle = list(default_board(width, height))
    for e in electrons:
        matter[e.position] = e  # type: ignore
        particle[e.position] = e  # type: ignore
    initial_board = new_board(
        width,
        height,
        obstacles=obstacles,
        matter=tuple(matter),
        particle=tuple(particle)
    )
    # pp.pprint(initial_board.filter)
    # pp.pprint(initial_board.move_all())
    for board in initial_board.move_all():
        pp.pprint(board.matter_set)
        pp.pprint(pprint_grid(board.obstacles))


if __name__ == "__main__":
    main()
