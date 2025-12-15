def parse_input(text):
    """Parse the input into ranges and ingredient IDs."""
    parts = text.strip().split('\n\n')

    ranges = []
    for line in parts[0].strip().split('\n'):
        start, end = map(int, line.split('-'))
        ranges.append((start, end))

    ingredients = []
    for line in parts[1].strip().split('\n'):
        ingredients.append(int(line))

    return ranges, ingredients


def is_fresh(ingredient_id, ranges):
    """Check if an ingredient ID falls within any fresh range."""
    for start, end in ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def count_fresh(ranges, ingredients):
    """Count how many ingredients are fresh."""
    return sum(1 for ing in ingredients if is_fresh(ing, ranges))


def count_total_fresh_ids(ranges):
    """Count total unique IDs covered by all ranges (handling overlaps)."""
    if not ranges:
        return 0

    # Sort ranges by start position
    sorted_ranges = sorted(ranges)

    # Merge overlapping ranges
    merged = [sorted_ranges[0]]
    for start, end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end + 1:
            # Overlapping or adjacent, merge them
            merged[-1] = (last_start, max(last_end, end))
        else:
            # Non-overlapping, add new range
            merged.append((start, end))

    # Count total IDs in merged ranges
    total = 0
    for start, end in merged:
        total += end - start + 1

    return total


def test():
    example = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""
    ranges, ingredients = parse_input(example)

    # Test parsing
    assert ranges == [(3, 5), (10, 14), (16, 20), (12, 18)], f"Ranges: {ranges}"
    assert ingredients == [1, 5, 8, 11, 17, 32], f"Ingredients: {ingredients}"

    # Test individual ingredients
    assert is_fresh(1, ranges) == False, "1 should be spoiled"
    assert is_fresh(5, ranges) == True, "5 should be fresh (in 3-5)"
    assert is_fresh(8, ranges) == False, "8 should be spoiled"
    assert is_fresh(11, ranges) == True, "11 should be fresh (in 10-14)"
    assert is_fresh(17, ranges) == True, "17 should be fresh (in 16-20 and 12-18)"
    assert is_fresh(32, ranges) == False, "32 should be spoiled"

    # Test count
    assert count_fresh(ranges, ingredients) == 3, f"Expected 3 fresh, got {count_fresh(ranges, ingredients)}"

    # Part 2: Test total fresh IDs
    # Fresh IDs: 3,4,5, 10,11,12,13,14,15,16,17,18,19,20 = 14 total
    # Ranges: 3-5 (3 IDs), 10-14 (5 IDs), 12-18 overlaps with 10-14 and 16-20
    # Merged: 3-5, 10-20 = 3 + 11 = 14
    assert count_total_fresh_ids(ranges) == 14, f"Expected 14 total fresh IDs, got {count_total_fresh_ids(ranges)}"

    # Test edge cases
    assert count_total_fresh_ids([]) == 0, "Empty ranges should return 0"
    assert count_total_fresh_ids([(5, 5)]) == 1, "Single point range should return 1"
    assert count_total_fresh_ids([(1, 3), (5, 7)]) == 6, "Non-overlapping ranges"
    assert count_total_fresh_ids([(1, 5), (3, 7)]) == 7, "Overlapping ranges"
    assert count_total_fresh_ids([(1, 5), (6, 10)]) == 10, "Adjacent ranges"

    print("All tests passed!")


if __name__ == "__main__":
    test()

    with open("05_input.txt") as f:
        text = f.read()

    ranges, ingredients = parse_input(text)
    print(count_fresh(ranges, ingredients))
    print(count_total_fresh_ids(ranges))
