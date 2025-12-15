def solve_part1(rotations):
    """Count times dial ends on 0 after a rotation."""
    position = 50
    count = 0
    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:])
        if direction == "L":
            position = (position - distance) % 100
        else:
            position = (position + distance) % 100
        if position == 0:
            count += 1
    return count


def count_zeros_in_rotation(position, direction, distance):
    """Count how many times dial lands on 0 during a single rotation."""
    if direction == "L":
        # Landing positions: P-1, P-2, ..., P-D (before mod)
        # Count multiples of 100 in [P-D, P-1]
        return ((position - 1) // 100) - ((position - distance - 1) // 100)
    else:
        # Landing positions: P+1, P+2, ..., P+D (before mod)
        # Count multiples of 100 in [P+1, P+D]
        return ((position + distance) // 100) - (position // 100)


def solve_part2(rotations):
    """Count times dial passes through or lands on 0 during any rotation."""
    position = 50
    count = 0
    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:])
        count += count_zeros_in_rotation(position, direction, distance)
        if direction == "L":
            position = (position - distance) % 100
        else:
            position = (position + distance) % 100
    return count


def test():
    # Example from problem
    example = ['L68', 'L30', 'R48', 'L5', 'R60', 'L55', 'L1', 'L99', 'R14', 'L82']

    # Part 1: should be 3 (lands on 0 after R48, L55, L99)
    assert solve_part1(example) == 3, f"Part 1 example failed: got {solve_part1(example)}"

    # Part 2: should be 6 (3 at end + 3 during rotations)
    assert solve_part2(example) == 6, f"Part 2 example failed: got {solve_part2(example)}"

    # Individual rotation tests from problem description:
    # L68 from 50 -> 82: hits 0 once during rotation
    assert count_zeros_in_rotation(50, 'L', 68) == 1, "L68 from 50 should hit 0 once"

    # L30 from 82 -> 52: doesn't hit 0
    assert count_zeros_in_rotation(82, 'L', 30) == 0, "L30 from 82 should not hit 0"

    # R48 from 52 -> 0: hits 0 (lands on it)
    assert count_zeros_in_rotation(52, 'R', 48) == 1, "R48 from 52 should hit 0 once"

    # L5 from 0 -> 95: doesn't hit 0 (starts at 0, but no click lands on 0)
    assert count_zeros_in_rotation(0, 'L', 5) == 0, "L5 from 0 should not hit 0"

    # R60 from 95 -> 55: hits 0 once during rotation
    assert count_zeros_in_rotation(95, 'R', 60) == 1, "R60 from 95 should hit 0 once"

    # L55 from 55 -> 0: hits 0 (lands on it)
    assert count_zeros_in_rotation(55, 'L', 55) == 1, "L55 from 55 should hit 0 once"

    # L1 from 0 -> 99: doesn't hit 0
    assert count_zeros_in_rotation(0, 'L', 1) == 0, "L1 from 0 should not hit 0"

    # L99 from 99 -> 0: hits 0 (lands on it)
    assert count_zeros_in_rotation(99, 'L', 99) == 1, "L99 from 99 should hit 0 once"

    # R14 from 0 -> 14: doesn't hit 0
    assert count_zeros_in_rotation(0, 'R', 14) == 0, "R14 from 0 should not hit 0"

    # L82 from 14 -> 32: hits 0 once during rotation
    assert count_zeros_in_rotation(14, 'L', 82) == 1, "L82 from 14 should hit 0 once"

    # Special case from problem: R1000 from 50 should hit 0 ten times
    assert count_zeros_in_rotation(50, 'R', 1000) == 10, f"R1000 from 50 should hit 0 ten times, got {count_zeros_in_rotation(50, 'R', 1000)}"

    print("All tests passed!")


if __name__ == "__main__":
    test()

    with open("01_input.txt") as f:
        rotations = [line.strip() for line in f if line.strip()]

    print(solve_part1(rotations))
    print(solve_part2(rotations))
