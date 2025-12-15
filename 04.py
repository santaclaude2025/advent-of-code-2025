def get_accessible(grid):
    """Get list of positions that have fewer than 4 adjacent rolls."""
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1),  (1, 0), (1, 1)]

    accessible = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '@':
                continue

            # Count adjacent rolls
            adjacent = 0
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                    adjacent += 1

            if adjacent < 4:
                accessible.append((r, c))

    return accessible


def count_accessible(grid):
    """Count rolls that have fewer than 4 adjacent rolls (8-directional)."""
    return len(get_accessible(grid))


def count_total_removable(grid):
    """Count total rolls that can be removed by iteratively removing accessible ones."""
    # Convert to mutable grid
    grid = [list(row) for row in grid]
    total_removed = 0

    while True:
        accessible = get_accessible(grid)
        if not accessible:
            break

        # Remove all accessible rolls
        for r, c in accessible:
            grid[r][c] = '.'
        total_removed += len(accessible)

    return total_removed


def count_neighbors(grid, r, c):
    """Count adjacent @ neighbors for a cell."""
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1),  (1, 0), (1, 1)]
    count = 0
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
            count += 1
    return count


def test():
    example = [
        "..@@.@@@@.",
        "@@@.@.@.@@",
        "@@@@@.@.@@",
        "@.@@@@..@.",
        "@@.@@@@.@@",
        ".@@@@@@@.@",
        ".@.@.@.@@@",
        "@.@@@.@@@@",
        ".@@@@@@@@.",
        "@.@.@@@.@."
    ]

    # Test full example
    result = count_accessible(example)
    assert result == 13, f"Expected 13, got {result}"

    # Expected accessible positions (from problem's x markers):
    # ..xx.xx@x.  -> (0,2), (0,3), (0,5), (0,6), (0,8)
    # x@@.@.@.@@  -> (1,0)
    # @@@@@.x.@@  -> (2,6)
    # @.@@@@..@.  -> none
    # x@.@@@@.@x  -> (4,0), (4,9)
    # .@@@@@@@.@  -> none
    # .@.@.@.@@@  -> none
    # x.@@@.@@@@  -> (7,0)
    # .@@@@@@@@.  -> none
    # x.x.@@@.x.  -> (9,0), (9,2), (9,8)
    expected_accessible = [
        (0, 2), (0, 3), (0, 5), (0, 6), (0, 8),
        (1, 0),
        (2, 6),
        (4, 0), (4, 9),
        (7, 0),
        (9, 0), (9, 2), (9, 8)
    ]

    # Verify each expected accessible cell has < 4 neighbors
    for r, c in expected_accessible:
        assert example[r][c] == '@', f"({r},{c}) should be @"
        neighbors = count_neighbors(example, r, c)
        assert neighbors < 4, f"({r},{c}) has {neighbors} neighbors, expected < 4"

    # Test a non-accessible cell (should have >= 4 neighbors)
    # Pick (1,1) which is @ surrounded by many @s
    assert example[1][1] == '@'
    neighbors = count_neighbors(example, 1, 1)
    assert neighbors >= 4, f"(1,1) has {neighbors} neighbors, expected >= 4"

    # Test edge case: single roll with no neighbors
    single = ["@"]
    assert count_accessible(single) == 1, "Single @ should be accessible"

    # Test edge case: roll with exactly 4 neighbors (not accessible)
    cross = [
        ".@.",
        "@@@",
        ".@."
    ]
    assert count_accessible(cross) == 4, f"Cross pattern: corners accessible, center has 4 neighbors"

    # Part 2: Test total removable
    # From the example: 13 + 12 + 7 + 5 + 2 + 1 + 1 + 1 + 1 = 43
    total = count_total_removable(example)
    assert total == 43, f"Expected 43 total removable, got {total}"

    # Test that cross pattern can be fully removed (center becomes accessible after corners removed)
    assert count_total_removable(cross) == 5, "Cross pattern should be fully removable"

    print("All tests passed!")


if __name__ == "__main__":
    test()

    with open("04_input.txt") as f:
        grid = [line.rstrip('\n') for line in f if line.strip()]

    print(count_accessible(grid))
    print(count_total_removable(grid))
