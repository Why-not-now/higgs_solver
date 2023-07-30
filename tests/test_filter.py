from higgs_solver.board import straight_filter


def test_right_filter():
    my_filter = straight_filter(9, 13)
    for i in range(34, 36):
        assert i in my_filter[34][0]


def test_down_filter():
    my_filter = straight_filter(9, 13)
    for i in range(34, 117, 9):
        assert i in my_filter[34][1]


def test_left_filter():
    my_filter = straight_filter(9, 13)
    for i in range(27, 35):
        assert i in my_filter[34][2]


def test_up_filter():
    my_filter = straight_filter(9, 13)
    for i in range(7, 35, 9):
        assert i in my_filter[34][3]
