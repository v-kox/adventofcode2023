from dataclasses import dataclass
import re

INPUT1 = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

EXPECTED1 = 8

N_CUBES = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


@dataclass
class Game:
    idx: int
    results: list[tuple[int, int, int]]

    @property
    def max_red(self) -> int:
        return max([x[0] for x in self.results])

    @property
    def max_green(self) -> int:
        return max([x[1] for x in self.results])

    @property
    def max_blue(self) -> int:
        return max([x[2] for x in self.results])

    @property
    def is_valid_game(self):
        return (
            self.max_red <= N_CUBES["red"]
            and self.max_green <= N_CUBES["green"]
            and self.max_blue <= N_CUBES["blue"]
        )
    
    def __repr__(self) -> str:
        return f"Game({self.idx=},{self.max_red=},{self.max_green=},{self.max_blue=})"


def _get_game_idx_from_string(idx_str: str) -> int:
    idx_re = r"\d+"
    return int(re.findall(idx_re, idx_str)[0])


def _get_game_samples_from_str(samples: str) -> list[tuple[int, int, int]]:
    sample_re = r"(\d+) (red|green|blue)"
    res = []
    for sample in samples.split(";"):
        red = 0
        green = 0
        blue = 0
        parsed = re.findall(sample_re, sample)

        for n, color in parsed:
            if color == "red":
                red = int(n)
            elif color == "green":
                green = int(n)
            elif color == "blue":
                blue = int(n)
            else:
                raise ValueError(f"Unknown color value found {color=}.")

        res.append((red, green, blue))

    return res


def parse_game(line: str) -> Game:
    idx_str, samples_str = line.split(":")

    idx = _get_game_idx_from_string(idx_str)
    samples = _get_game_samples_from_str(samples_str)

    return Game(idx, samples)


def compute(data: str) -> int:
    games = [parse_game(line) for line in data.splitlines()]

    valid_games = [game for game in games if game.is_valid_game]

    # for game in valid_games:
    #     print(game)
    return sum([game.idx for game in valid_games])

def test_case1():
    assert compute(INPUT1) == EXPECTED1

def main() -> int:
    with open("day2_input.txt", "r") as f:
        data = f.read()

    total = compute(data)
    print(total)

if __name__ == "__main__":
    main()