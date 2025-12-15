from itertools import combinations


def parse_input(text):
    """Parse red tile positions."""
    tiles = []
    for line in text.strip().split('\n'):
        x, y = map(int, line.split(','))
        tiles.append((x, y))
    return tiles


def rectangle_area(p1, p2):
    """Calculate rectangle area with p1 and p2 as opposite corners.
    Returns 0 if they're on the same row or column (not opposite corners).
    Area is inclusive of boundary tiles.
    """
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2 or y1 == y2:
        return 0  # Not opposite corners
    # +1 because we count tiles inclusively
    return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)


def solve_part1(text):
    """Find largest rectangle with two red tiles as opposite corners."""
    tiles = parse_input(text)

    max_area = 0
    for t1, t2 in combinations(tiles, 2):
        area = rectangle_area(t1, t2)
        max_area = max(max_area, area)

    return max_area


def get_path_tiles(p1, p2):
    """Get all tiles on the straight line between p1 and p2 (exclusive of endpoints)."""
    x1, y1 = p1
    x2, y2 = p2
    tiles = set()

    if x1 == x2:  # Vertical line
        for y in range(min(y1, y2) + 1, max(y1, y2)):
            tiles.add((x1, y))
    elif y1 == y2:  # Horizontal line
        for x in range(min(x1, x2) + 1, max(x1, x2)):
            tiles.add((x, y1))

    return tiles


def get_row_ranges(red_tiles):
    """Get valid x-range for each row directly from the polygon boundary.

    For a closed polygon, we can compute the x-range per row by tracking
    where the boundary crosses each row.
    """
    # Build boundary segments between consecutive red tiles
    n = len(red_tiles)

    # For each row, track the min and max x of the boundary/interior
    # Since tiles form axis-aligned paths, each row's valid range is
    # from leftmost boundary point to rightmost boundary point on that row

    row_x_values = {}  # y -> list of x values on boundary

    for i in range(n):
        p1 = red_tiles[i]
        p2 = red_tiles[(i + 1) % n]
        x1, y1 = p1
        x2, y2 = p2

        # Add the red tile itself
        if y1 not in row_x_values:
            row_x_values[y1] = []
        row_x_values[y1].append(x1)

        # Add path tiles between p1 and p2
        if x1 == x2:  # Vertical line
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if y not in row_x_values:
                    row_x_values[y] = []
                row_x_values[y].append(x1)
        elif y1 == y2:  # Horizontal line
            if y1 not in row_x_values:
                row_x_values[y1] = []
            row_x_values[y1].extend([x1, x2])

    # For each row, the valid range is min to max of boundary x values
    # Interior is automatically included since it's between boundary edges
    row_ranges = {}
    for y, x_vals in row_x_values.items():
        row_ranges[y] = (min(x_vals), max(x_vals))

    return row_ranges


def solve_part2(text):
    """Find largest rectangle with red corners containing only red/green tiles."""
    import bisect

    red_tiles = parse_input(text)

    # Get valid x-range for each row directly (no flood fill needed)
    valid_by_row = get_row_ranges(red_tiles)

    # Get all y values that have valid ranges (all rows in the polygon)
    all_ys = sorted(valid_by_row.keys())
    if not all_ys:
        return 0

    n_rows = len(all_ys)
    y_to_idx = {y: i for i, y in enumerate(all_ys)}

    # Check if rows are contiguous
    if all_ys[-1] - all_ys[0] + 1 != n_rows:
        # There are gaps - need to handle this
        pass

    # Arrays for segment tree queries
    row_mins = [valid_by_row[y][0] for y in all_ys]  # row_min values
    row_maxs = [valid_by_row[y][1] for y in all_ys]  # row_max values

    # Build sparse table for O(1) range max/min queries
    # For max of row_mins and min of row_maxs
    import math
    LOG = max(1, math.ceil(math.log2(n_rows + 1)))

    # Sparse table for range-max of row_mins
    sparse_max = [[0] * n_rows for _ in range(LOG)]
    sparse_max[0] = row_mins[:]
    for j in range(1, LOG):
        for i in range(n_rows - (1 << j) + 1):
            sparse_max[j][i] = max(sparse_max[j-1][i], sparse_max[j-1][i + (1 << (j-1))])

    # Sparse table for range-min of row_maxs
    sparse_min = [[float('inf')] * n_rows for _ in range(LOG)]
    sparse_min[0] = row_maxs[:]
    for j in range(1, LOG):
        for i in range(n_rows - (1 << j) + 1):
            sparse_min[j][i] = min(sparse_min[j-1][i], sparse_min[j-1][i + (1 << (j-1))])

    def query_max(l, r):  # max of row_mins[l:r+1]
        if l > r:
            return float('-inf')
        length = r - l + 1
        k = length.bit_length() - 1
        return max(sparse_max[k][l], sparse_max[k][r - (1 << k) + 1])

    def query_min(l, r):  # min of row_maxs[l:r+1]
        if l > r:
            return float('inf')
        length = r - l + 1
        k = length.bit_length() - 1
        return min(sparse_min[k][l], sparse_min[k][r - (1 << k) + 1])

    max_area = 0

    # Iterate over all pairs of red tiles
    for i, (x1, y1) in enumerate(red_tiles):
        for x2, y2 in red_tiles[i+1:]:
            if x1 == x2 or y1 == y2:
                continue

            min_x, max_x = min(x1, x2), max(x1, x2)
            min_y, max_y = min(y1, y2), max(y1, y2)
            width = max_x - min_x + 1
            height = max_y - min_y + 1
            area = width * height

            if area <= max_area:
                continue

            # Check if both y values are in our index
            if min_y not in y_to_idx or max_y not in y_to_idx:
                continue

            lo = y_to_idx[min_y]
            hi = y_to_idx[max_y]

            # Check if rows are contiguous
            if hi - lo != max_y - min_y:
                continue  # Missing rows in between

            # O(1) range query: check if all rows contain [min_x, max_x]
            # Need: max(row_mins) <= min_x AND min(row_maxs) >= max_x
            max_row_min = query_max(lo, hi)
            min_row_max = query_min(lo, hi)

            if max_row_min <= min_x and min_row_max >= max_x:
                max_area = area

    return max_area


def test():
    example = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

    tiles = parse_input(example)
    assert len(tiles) == 8, f"Expected 8 tiles, got {len(tiles)}"
    assert tiles[0] == (7, 1), f"First tile: {tiles[0]}"

    # Test specific rectangles from the problem
    assert rectangle_area((2, 5), (9, 7)) == 24, "2,5 to 9,7 should be 8*3=24"
    assert rectangle_area((7, 1), (11, 7)) == 35, "7,1 to 11,7 should be 5*7=35"
    assert rectangle_area((7, 3), (2, 3)) == 0, "Same y, not opposite corners"
    assert rectangle_area((2, 5), (11, 1)) == 50, "2,5 to 11,1 should be 10*5=50"

    result = solve_part1(example)
    assert result == 50, f"Expected 50, got {result}"

    # Part 2: only red and green tiles allowed
    result2 = solve_part2(example)
    assert result2 == 24, f"Expected 24, got {result2}"

    print("All tests passed!")


if __name__ == "__main__":
    test()

    with open("09_input.txt") as f:
        text = f.read()

    print(solve_part1(text))
    print(solve_part2(text))
