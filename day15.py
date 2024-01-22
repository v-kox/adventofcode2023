import pytest

INPUT1 = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
EXPECTED1 = 1320


@pytest.mark.parametrize(
    "char, result",
    [
        ("H", 200),
    ],
)
def test_hash_char(char, result):
    """Test hashing of 1 characted"""
    assert hash_char(char) == result


def test_HASH():
    """test HASH implementation"""
    assert HASH("HASH") == 52


def test_case1():
    """test case example part 1"""
    assert compute(INPUT1) == EXPECTED1


def HASH(data: str):
    """HASH alghoritm of input steps"""
    value = 0

    for c in data:
        value = hash_char(c, value)

    return value


def hash_char(char: str, start_val=0) -> int:
    """Hashing of a single character witha  given start value"""
    hash_val = (17 * (ord(char) + start_val)) % 256

    return hash_val


def compute(data: str) -> int:
    """Compute puzzle output"""
    steps = data.strip().split(",")

    return sum(HASH(step) for step in steps)


def main():
    """Run puzzle input"""
    with open("day15_input.txt", "r") as f:
        data = f.read()

    result = compute(data)
    print(f"{result=}")


if __name__ == "__main__":
    main()
