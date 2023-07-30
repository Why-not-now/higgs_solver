def main():
    from higgs_solver.board import new_board
    from higgs_solver.protocol import ObstacleType
    from higgs_solver.particle import Electron
    width = 7
    height = 8

    obstacles = (
        None, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
        ObstacleType.STRONG, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
        ObstacleType.STRONG, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
    )
    test_electron = Electron(21)
    matter = (
        None, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
        test_electron, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
    )
    particle = (
        None, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
        test_electron, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
        None, None, None, None, None, None, None,
    )
    initial_board = new_board(
        width,
        height,
        obstacles=obstacles,
        matter=matter,
        particle=particle
    )
    print(initial_board)
    # print(initial_board.move_all())
    for board in initial_board.move_all():
        print(board.particle)


if __name__ == "__main__":
    main()
