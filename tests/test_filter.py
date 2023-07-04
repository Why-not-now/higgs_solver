from higgs_solver import straight_filter


def test_left_filter():
    my_filter = straight_filter(9, 13)
    for i in range(27, 34):
        assert i in my_filter[34][0]


def test_right_filter():
    my_filter = straight_filter(9, 13)
    for i in range(35, 36):
        assert i in my_filter[34][1]


def test_up_filter():
    my_filter = straight_filter(9, 13)
    for i in range(7, 34, 9):
        assert i in my_filter[34][2]


def test_down_filter():
    my_filter = straight_filter(9, 13)
    for i in range(43, 117, 9):
        assert i in my_filter[34][3]
