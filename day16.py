from utils import Offsets

from day16_utils import Grid, Lightbeam

INPUT1 = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""
EXPECTED1 = 46


def test_case1():
    assert compute(INPUT1) == EXPECTED1


def compute(data: str) -> int:
    lb = Lightbeam(0, 0, Offsets.EAST)
    grid = Grid(data)
    grid.add_lightbeam(lb)

    while grid.has_lightbeams:
        lb = grid.get_lightbeam()
        if lb in grid.seen:
            continue

        grid.seen.add(lb)

        res = grid.step(lb)

        for lb in res:
            if grid.is_lightbeam_inside_grid(lb):
                grid.add_lightbeam(lb)

    return grid.n_energized


def main():
    """Run puzzle input"""
    with open("day16_input.txt", "r") as f:
        data = f.read()

    result = compute(data)

    print(f"{result=}")


if __name__ == "__main__":
    main()
