def parse_grid(text):
    """Parse the input into a grid and find the start position."""
    lines = text.strip().split('\n')
    grid = [list(line) for line in lines]

    # Find S position
    start_col = None
    for col, char in enumerate(grid[0]):
        if char == 'S':
            start_col = col
            break

    return grid, start_col


def simulate_beams(grid):
    """Simulate tachyon beams and count splits."""
    rows = len(grid)
    cols = len(grid[0])

    # Find start position
    start_col = None
    for col, char in enumerate(grid[0]):
        if char == 'S':
            start_col = col
            break

    # Track active beams as (row, col) - all beams move downward
    # Start beam just below S
    active_beams = {(0, start_col)}
    split_count = 0

    # Process row by row
    for row in range(1, rows):
        new_beams = set()

        for _, col in active_beams:
            # Beam moves down to current row
            if col < 0 or col >= cols:
                # Beam exited left or right
                continue

            char = grid[row][col]
            if char == '^':
                # Splitter! Count this split and emit two beams
                split_count += 1
                # Left beam continues from col-1
                # Right beam continues from col+1
                new_beams.add((row, col - 1))
                new_beams.add((row, col + 1))
            else:
                # Empty space, beam continues straight down
                new_beams.add((row, col))

        active_beams = new_beams

        if not active_beams:
            break

    return split_count


def solve_part1(text):
    """Count total number of beam splits."""
    grid, _ = parse_grid(text)
    return simulate_beams(grid)


def simulate_timelines(grid):
    """Simulate tachyon particle with many-worlds interpretation.

    Track how many timelines have a particle at each position.
    Each split creates two timelines from one.
    """
    rows = len(grid)
    cols = len(grid[0])

    # Find start position
    start_col = None
    for col, char in enumerate(grid[0]):
        if char == 'S':
            start_col = col
            break

    # Track number of timelines at each column position
    # Key: column, Value: number of timelines with particle at that column
    timelines = {start_col: 1}

    # Process row by row
    for row in range(1, rows):
        new_timelines = {}

        for col, count in timelines.items():
            # Particle moves down to current row
            if col < 0 or col >= cols:
                # Particle exited left or right - these timelines end
                continue

            char = grid[row][col]
            if char == '^':
                # Splitter! Each timeline splits into two
                # Left particle goes to col-1
                # Right particle goes to col+1
                new_timelines[col - 1] = new_timelines.get(col - 1, 0) + count
                new_timelines[col + 1] = new_timelines.get(col + 1, 0) + count
            else:
                # Empty space, particle continues straight down
                new_timelines[col] = new_timelines.get(col, 0) + count

        timelines = new_timelines

        if not timelines:
            break

    # Total timelines is sum of all timeline counts
    return sum(timelines.values())


def solve_part2(text):
    """Count total number of timelines after particle completes journey."""
    grid, _ = parse_grid(text)
    return simulate_timelines(grid)


def test():
    example = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

    result = solve_part1(example)
    assert result == 21, f"Expected 21 splits, got {result}"

    # Part 2: count timelines
    result2 = solve_part2(example)
    assert result2 == 40, f"Expected 40 timelines, got {result2}"

    print("All tests passed!")


if __name__ == "__main__":
    test()

    with open("07_input.txt") as f:
        text = f.read()

    print(solve_part1(text))
    print(solve_part2(text))
