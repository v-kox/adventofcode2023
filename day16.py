from day16_utils import Grid
from day16_utils import Lightbeam
from utils import Offsets

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
EXPECTED2 = 51


def test_case1():
    assert compute(INPUT1) == EXPECTED1


def test_case2():
    assert compute2(INPUT1) == EXPECTED2


def solve(data: str, start_lb: Lightbeam) -> int:
    """Solve the grid for a given start lightbeam"""
    grid = Grid(data)
    grid.add_lightbeam(start_lb)
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


def compute(data: str) -> int:
    """compute the result for part 1"""
    lb = Lightbeam(0, 0, Offsets.EAST)
    return solve(data, lb)


def compute2(data: str) -> int:
    """compute the result for part 2"""
    grid = Grid(data)
    # Detemine all possible starting lightbeams
    lightbeams = [
        *(Lightbeam(0, n_col, Offsets.SOUTH) for n_col in range(grid.ncols)),
        *(
            Lightbeam(grid.nrows - 1, n_col, Offsets.NORTH)
            for n_col in range(grid.ncols)
        ),
        *(Lightbeam(n_row, 0, Offsets.EAST) for n_row in range(grid.nrows)),
        *(
            Lightbeam(n_row, grid.ncols - 1, Offsets.WEST)
            for n_row in range(grid.nrows)
        ),
    ]

    return max(solve(data, lb) for lb in lightbeams)


def main():
    """Run puzzle input"""
    with open("day16_input.txt", "r") as f:
        data = f.read()

    result = compute(data)
    result2 = compute2(data)

    print(f"{result=}")
    print(f"{result2=}")


if __name__ == "__main__":
    main()
