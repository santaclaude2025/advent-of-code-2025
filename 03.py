def max_joltage(bank, num_digits=2):
    """Find the maximum num_digits-digit joltage from a bank.

    Greedy approach: for each position, pick the largest digit that
    leaves enough remaining digits to complete the number.
    """
    result = []
    start = 0
    for i in range(num_digits):
        # Need to pick (num_digits - i) more digits including this one
        # So we can pick from start to len(bank) - (num_digits - i - 1) - 1
        # = len(bank) - num_digits + i
        end = len(bank) - (num_digits - i - 1)

        # Find the largest digit in range [start, end)
        best_idx = start
        for j in range(start, end):
            if bank[j] > bank[best_idx]:
                best_idx = j

        result.append(bank[best_idx])
        start = best_idx + 1

    return int(''.join(result))


def solve(lines, num_digits=2):
    """Sum of max joltage from each bank."""
    total = 0
    for line in lines:
        line = line.strip()
        if line:
            total += max_joltage(line, num_digits)
    return total


def test():
    # Part 1: Test individual banks from example
    assert max_joltage("987654321111111") == 98, f"Expected 98, got {max_joltage('987654321111111')}"
    assert max_joltage("811111111111119") == 89, f"Expected 89, got {max_joltage('811111111111119')}"
    assert max_joltage("234234234234278") == 78, f"Expected 78, got {max_joltage('234234234234278')}"
    assert max_joltage("818181911112111") == 92, f"Expected 92, got {max_joltage('818181911112111')}"

    # Part 1: Test full example
    example = [
        "987654321111111",
        "811111111111119",
        "234234234234278",
        "818181911112111"
    ]
    assert solve(example) == 357, f"Expected 357, got {solve(example)}"

    # Part 2: Test individual banks from example (12 digits)
    assert max_joltage("987654321111111", 12) == 987654321111, f"Expected 987654321111, got {max_joltage('987654321111111', 12)}"
    assert max_joltage("811111111111119", 12) == 811111111119, f"Expected 811111111119, got {max_joltage('811111111111119', 12)}"
    assert max_joltage("234234234234278", 12) == 434234234278, f"Expected 434234234278, got {max_joltage('234234234234278', 12)}"
    assert max_joltage("818181911112111", 12) == 888911112111, f"Expected 888911112111, got {max_joltage('818181911112111', 12)}"

    # Part 2: Test full example
    assert solve(example, 12) == 3121910778619, f"Expected 3121910778619, got {solve(example, 12)}"

    print("All tests passed!")


if __name__ == "__main__":
    test()

    with open("03_input.txt") as f:
        lines = f.readlines()

    print(solve(lines))
    print(solve(lines, 12))
