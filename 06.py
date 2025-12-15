def parse_problems_part1(lines):
    """Parse the worksheet into a list of (numbers, operator) tuples - horizontal reading."""
    # Make sure all lines have the same length (pad with spaces if needed)
    max_len = max(len(line) for line in lines)
    lines = [line.ljust(max_len) for line in lines]

    # Find columns that are all spaces (problem separators)
    # Problems are separated by full columns of only spaces
    problems = []
    col = 0
    while col < max_len:
        # Skip separator columns (all spaces)
        while col < max_len and all(line[col] == ' ' for line in lines):
            col += 1

        if col >= max_len:
            break

        # Find the end of this problem (next all-space column or end)
        start_col = col
        while col < max_len and not all(line[col] == ' ' for line in lines):
            col += 1
        end_col = col

        # Extract this problem's columns
        problem_lines = [line[start_col:end_col] for line in lines]

        # The last line should have the operator
        operator_line = problem_lines[-1].strip()
        if operator_line in ['+', '*']:
            operator = operator_line
            number_lines = problem_lines[:-1]
        else:
            # Operator might be embedded, look for it
            for i, pl in enumerate(problem_lines):
                stripped = pl.strip()
                if stripped in ['+', '*']:
                    operator = stripped
                    number_lines = problem_lines[:i]
                    break

        # Extract numbers from number lines
        numbers = []
        for nl in number_lines:
            stripped = nl.strip()
            if stripped and stripped.isdigit():
                numbers.append(int(stripped))

        if numbers and operator:
            problems.append((numbers, operator))

    return problems


def parse_problems_part2(lines):
    """Parse the worksheet into a list of (numbers, operator) tuples - vertical/column reading."""
    # Make sure all lines have the same length (pad with spaces if needed)
    max_len = max(len(line) for line in lines)
    lines = [line.ljust(max_len) for line in lines]

    num_rows = len(lines)
    operator_row = num_rows - 1  # Last row has operators

    # Find columns that are all spaces (problem separators)
    # Problems are separated by full columns of only spaces
    problems = []
    col = 0
    while col < max_len:
        # Skip separator columns (all spaces)
        while col < max_len and all(line[col] == ' ' for line in lines):
            col += 1

        if col >= max_len:
            break

        # Find the end of this problem (next all-space column or end)
        start_col = col
        while col < max_len and not all(line[col] == ' ' for line in lines):
            col += 1
        end_col = col

        # Extract columns for this problem
        # Each column (excluding operator row) represents digits of a number (top=most significant)
        # Read columns right-to-left for the numbers in order
        operator = None
        numbers = []

        for c in range(end_col - 1, start_col - 1, -1):  # Right to left
            # Check if this column has the operator
            char_at_op_row = lines[operator_row][c]
            if char_at_op_row in ['+', '*']:
                operator = char_at_op_row

            # Build number from this column (top to bottom, digits only)
            digits = []
            for r in range(operator_row):  # Exclude operator row
                char = lines[r][c]
                if char.isdigit():
                    digits.append(char)

            if digits:
                number = int(''.join(digits))
                numbers.append(number)

        if numbers and operator:
            problems.append((numbers, operator))

    return problems


def solve_problem(numbers, operator):
    """Solve a single problem."""
    if operator == '+':
        return sum(numbers)
    else:  # '*'
        result = 1
        for n in numbers:
            result *= n
        return result


def solve_part1(text):
    """Solve all problems (horizontal reading) and return the grand total."""
    lines = text.rstrip('\n').split('\n')
    # Remove empty lines at end
    while lines and not lines[-1].strip():
        lines.pop()

    problems = parse_problems_part1(lines)
    total = 0
    for numbers, operator in problems:
        total += solve_problem(numbers, operator)
    return total


def solve_part2(text):
    """Solve all problems (vertical/column reading) and return the grand total."""
    lines = text.rstrip('\n').split('\n')
    # Remove empty lines at end
    while lines and not lines[-1].strip():
        lines.pop()

    problems = parse_problems_part2(lines)
    total = 0
    for numbers, operator in problems:
        total += solve_problem(numbers, operator)
    return total


def test():
    example = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  """

    # Part 1 tests - horizontal reading
    lines = example.split('\n')
    problems = parse_problems_part1(lines)

    # Test parsing
    assert len(problems) == 4, f"Expected 4 problems, got {len(problems)}"
    assert problems[0] == ([123, 45, 6], '*'), f"Problem 0: {problems[0]}"
    assert problems[1] == ([328, 64, 98], '+'), f"Problem 1: {problems[1]}"
    assert problems[2] == ([51, 387, 215], '*'), f"Problem 2: {problems[2]}"
    assert problems[3] == ([64, 23, 314], '+'), f"Problem 3: {problems[3]}"

    # Test individual solutions
    assert solve_problem([123, 45, 6], '*') == 33210
    assert solve_problem([328, 64, 98], '+') == 490
    assert solve_problem([51, 387, 215], '*') == 4243455
    assert solve_problem([64, 23, 314], '+') == 401

    # Test grand total part 1
    assert solve_part1(example) == 4277556, f"Expected 4277556, got {solve_part1(example)}"

    # Part 2 tests - vertical/column reading
    # Rightmost problem: 4 + 431 + 623 = 1058
    # Each column is a number read top-to-bottom
    # Problems read right-to-left
    problems2 = parse_problems_part2(lines)
    assert len(problems2) == 4, f"Expected 4 problems part2, got {len(problems2)}"

    # Rightmost problem (first in list since we read right-to-left): columns 6,2,3 and 4,3,1 and 4
    # Let me trace through: columns for rightmost problem (64, 23, 314, +)
    # Column positions: let's verify the rightmost problem
    # From the example, rightmost problem should be 4 + 431 + 623 = 1058

    # Test grand total part 2
    assert solve_part2(example) == 3263827, f"Expected 3263827, got {solve_part2(example)}"

    print("All tests passed!")


if __name__ == "__main__":
    test()

    with open("06_input.txt") as f:
        text = f.read()

    print(solve_part1(text))
    print(solve_part2(text))
