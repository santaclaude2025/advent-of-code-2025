def is_invalid_part1(n):
    """Check if n is made of a digit sequence repeated exactly twice."""
    s = str(n)
    if len(s) % 2 != 0:
        return False
    half = len(s) // 2
    return s[:half] == s[half:]


def is_invalid_part2(n):
    """Check if n is made of a digit sequence repeated at least twice."""
    s = str(n)
    # Try all possible repeat lengths (1 to len/2)
    for repeat_len in range(1, len(s) // 2 + 1):
        if len(s) % repeat_len == 0:
            pattern = s[:repeat_len]
            repeats = len(s) // repeat_len
            if repeats >= 2 and pattern * repeats == s:
                return True
    return False


def find_invalid_in_range(start, end, is_invalid_func):
    """Find all invalid IDs in range [start, end]."""
    invalid = []
    for n in range(start, end + 1):
        if is_invalid_func(n):
            invalid.append(n)
    return invalid


def solve(input_text, is_invalid_func):
    """Sum all invalid IDs in the given ranges."""
    ranges = input_text.strip().split(',')
    total = 0
    for r in ranges:
        r = r.strip()
        if not r:
            continue
        start, end = map(int, r.split('-'))
        for n in range(start, end + 1):
            if is_invalid_func(n):
                total += n
    return total


def test():
    # Part 1: Test is_invalid_part1
    assert is_invalid_part1(55) == True, "55 should be invalid"
    assert is_invalid_part1(99) == True, "99 should be invalid"
    assert is_invalid_part1(6464) == True, "6464 should be invalid"
    assert is_invalid_part1(123123) == True, "123123 should be invalid"
    assert is_invalid_part1(1010) == True, "1010 should be invalid"
    assert is_invalid_part1(222222) == True, "222222 should be invalid"
    assert is_invalid_part1(446446) == True, "446446 should be invalid"
    assert is_invalid_part1(1188511885) == True, "1188511885 should be invalid"
    assert is_invalid_part1(38593859) == True, "38593859 should be invalid"

    assert is_invalid_part1(101) == False, "101 should be valid (odd length)"
    assert is_invalid_part1(12) == False, "12 should be valid"
    assert is_invalid_part1(1234) == False, "1234 should be valid"

    # Part 1: Test ranges from example
    assert find_invalid_in_range(11, 22, is_invalid_part1) == [11, 22], "11-22 should have 11, 22"
    assert find_invalid_in_range(95, 115, is_invalid_part1) == [99], "95-115 should have 99"
    assert find_invalid_in_range(998, 1012, is_invalid_part1) == [1010], "998-1012 should have 1010"
    assert find_invalid_in_range(1188511880, 1188511890, is_invalid_part1) == [1188511885]
    assert find_invalid_in_range(222220, 222224, is_invalid_part1) == [222222]
    assert find_invalid_in_range(1698522, 1698528, is_invalid_part1) == []
    assert find_invalid_in_range(446443, 446449, is_invalid_part1) == [446446]
    assert find_invalid_in_range(38593856, 38593862, is_invalid_part1) == [38593859]

    # Part 1: Test full example
    example = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124"""
    assert solve(example, is_invalid_part1) == 1227775554, f"Part 1 example failed: {solve(example, is_invalid_part1)}"

    # Part 2: Test is_invalid_part2 with new examples
    assert is_invalid_part2(12341234) == True, "12341234 should be invalid (1234 x2)"
    assert is_invalid_part2(123123123) == True, "123123123 should be invalid (123 x3)"
    assert is_invalid_part2(1212121212) == True, "1212121212 should be invalid (12 x5)"
    assert is_invalid_part2(1111111) == True, "1111111 should be invalid (1 x7)"
    assert is_invalid_part2(111) == True, "111 should be invalid (1 x3)"
    assert is_invalid_part2(999) == True, "999 should be invalid (1 x3)"
    assert is_invalid_part2(565656) == True, "565656 should be invalid (56 x3)"
    assert is_invalid_part2(824824824) == True, "824824824 should be invalid (824 x3)"
    assert is_invalid_part2(2121212121) == True, "2121212121 should be invalid (21 x5)"

    # Part 2: All part 1 invalids should still be invalid
    assert is_invalid_part2(55) == True
    assert is_invalid_part2(99) == True
    assert is_invalid_part2(6464) == True
    assert is_invalid_part2(1010) == True

    # Part 2: Test ranges from example
    assert find_invalid_in_range(11, 22, is_invalid_part2) == [11, 22], "11-22 should have 11, 22"
    assert find_invalid_in_range(95, 115, is_invalid_part2) == [99, 111], "95-115 should have 99, 111"
    assert find_invalid_in_range(998, 1012, is_invalid_part2) == [999, 1010], "998-1012 should have 999, 1010"
    assert find_invalid_in_range(1188511880, 1188511890, is_invalid_part2) == [1188511885]
    assert find_invalid_in_range(222220, 222224, is_invalid_part2) == [222222]
    assert find_invalid_in_range(1698522, 1698528, is_invalid_part2) == []
    assert find_invalid_in_range(446443, 446449, is_invalid_part2) == [446446]
    assert find_invalid_in_range(38593856, 38593862, is_invalid_part2) == [38593859]
    assert find_invalid_in_range(565653, 565659, is_invalid_part2) == [565656], "565653-565659 should have 565656"
    assert find_invalid_in_range(824824821, 824824827, is_invalid_part2) == [824824824], "824824821-824824827 should have 824824824"
    assert find_invalid_in_range(2121212118, 2121212124, is_invalid_part2) == [2121212121], "2121212118-2121212124 should have 2121212121"

    # Part 2: Test full example
    assert solve(example, is_invalid_part2) == 4174379265, f"Part 2 example failed: {solve(example, is_invalid_part2)}"

    print("All tests passed!")


if __name__ == "__main__":
    test()

    with open("02_input.txt") as f:
        input_text = f.read()

    print(solve(input_text, is_invalid_part1))
    print(solve(input_text, is_invalid_part2))
