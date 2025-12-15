import re
from itertools import combinations


def parse_line(line):
    """Parse a machine description line."""
    # Extract indicator pattern [...]
    indicator_match = re.search(r'\[([.#]+)\]', line)
    indicator = indicator_match.group(1)
    target = [1 if c == '#' else 0 for c in indicator]
    n_lights = len(target)

    # Extract button schematics (...)
    buttons = []
    for match in re.finditer(r'\(([0-9,]+)\)', line):
        indices = [int(x) for x in match.group(1).split(',')]
        buttons.append(indices)

    # Extract joltage requirements {...}
    joltage_match = re.search(r'\{([0-9,]+)\}', line)
    joltage = [int(x) for x in joltage_match.group(1).split(',')]

    return n_lights, target, buttons, joltage


def solve_machine(n_lights, target, buttons):
    """Find minimum button presses to reach target configuration.

    Since pressing a button twice cancels out, each button is pressed 0 or 1 times.
    This is solving a system of linear equations over GF(2).
    We need the minimum Hamming weight solution.
    """
    n_buttons = len(buttons)

    # For small number of buttons, brute force all 2^n combinations
    if n_buttons <= 20:
        min_presses = float('inf')
        for mask in range(1 << n_buttons):
            # Compute resulting light state
            state = [0] * n_lights
            presses = 0
            for i in range(n_buttons):
                if mask & (1 << i):
                    presses += 1
                    for idx in buttons[i]:
                        state[idx] ^= 1

            if state == target:
                min_presses = min(min_presses, presses)

        return min_presses if min_presses != float('inf') else -1

    # For larger cases, use Gaussian elimination to find solution space,
    # then search for minimum weight solution
    return solve_with_gaussian(n_lights, target, buttons)


def solve_with_gaussian(n_lights, target, buttons):
    """Solve using Gaussian elimination over GF(2)."""
    n_buttons = len(buttons)

    # Build augmented matrix [A | b] where A is buttons matrix, b is target
    # Each row is a light, each column is a button
    # A[i][j] = 1 if button j toggles light i

    # We'll work with columns (each button is a column)
    # and do column operations to find kernel

    # Actually, let's think of it differently:
    # We want to find x (button presses) such that A @ x = target (mod 2)
    # where A[i][j] = 1 if button j affects light i

    # Build matrix A (n_lights x n_buttons)
    A = [[0] * n_buttons for _ in range(n_lights)]
    for j, btn in enumerate(buttons):
        for i in btn:
            A[i][j] = 1

    # Augment with target
    aug = [row[:] + [target[i]] for i, row in enumerate(A)]

    # Gaussian elimination (row reduction) over GF(2)
    pivot_col = 0
    pivot_rows = []
    for row in range(n_lights):
        if pivot_col >= n_buttons:
            break

        # Find pivot
        found = False
        for r in range(row, n_lights):
            if aug[r][pivot_col] == 1:
                aug[row], aug[r] = aug[r], aug[row]
                found = True
                break

        if not found:
            pivot_col += 1
            continue

        pivot_rows.append((row, pivot_col))

        # Eliminate
        for r in range(n_lights):
            if r != row and aug[r][pivot_col] == 1:
                for c in range(n_buttons + 1):
                    aug[r][c] ^= aug[row][c]

        pivot_col += 1

    # Check for inconsistency (row with all zeros in A but 1 in b)
    for row in aug:
        if all(row[j] == 0 for j in range(n_buttons)) and row[n_buttons] == 1:
            return -1  # No solution

    # Find free variables (columns not in pivot_rows)
    pivot_cols = set(pc for _, pc in pivot_rows)
    free_cols = [j for j in range(n_buttons) if j not in pivot_cols]

    # Number of free variables determines solution space size
    n_free = len(free_cols)

    if n_free > 25:
        # Too many free variables, need smarter approach
        # For now, just return a particular solution
        pass

    # Enumerate all 2^n_free combinations of free variables
    min_presses = float('inf')

    for free_mask in range(1 << n_free):
        # Set free variables
        x = [0] * n_buttons
        for i, col in enumerate(free_cols):
            x[col] = (free_mask >> i) & 1

        # Back-substitute to find pivot variables
        valid = True
        for row_idx, col in reversed(pivot_rows):
            # aug[row_idx][col] is 1 (pivot)
            # Solve: x[col] + sum(aug[row_idx][j] * x[j] for other j) = aug[row_idx][n_buttons]
            val = aug[row_idx][n_buttons]
            for j in range(n_buttons):
                if j != col:
                    val ^= aug[row_idx][j] * x[j]
            x[col] = val

        # Count presses
        presses = sum(x)
        min_presses = min(min_presses, presses)

    return min_presses if min_presses != float('inf') else -1


def solve_part1(text):
    """Find minimum total button presses for all machines."""
    total = 0
    for line in text.strip().split('\n'):
        n_lights, target, buttons, _ = parse_line(line)
        presses = solve_machine(n_lights, target, buttons)
        if presses == -1:
            raise ValueError(f"No solution for line: {line}")
        total += presses
    return total


def solve_joltage(buttons, joltage):
    """Find minimum button presses to reach joltage requirements.

    Minimize sum(x_i) subject to A @ x = joltage, x >= 0 integers.
    Uses Gaussian elimination over rationals, but since A is 0/1,
    the reduced form has integer coefficients.
    """
    n_buttons = len(buttons)
    n_counters = len(joltage)

    # Build matrix A
    A = [[0] * n_buttons for _ in range(n_counters)]
    for i, btn in enumerate(buttons):
        for j in btn:
            if j < n_counters:
                A[j][i] = 1

    from fractions import Fraction

    # Gaussian elimination with Fractions (needed for intermediate steps)
    aug = [[Fraction(A[i][j]) for j in range(n_buttons)] + [Fraction(joltage[i])]
           for i in range(n_counters)]

    pivot_cols = []
    row = 0
    for col in range(n_buttons):
        pivot_row = None
        for r in range(row, n_counters):
            if aug[r][col] != 0:
                pivot_row = r
                break
        if pivot_row is None:
            continue
        aug[row], aug[pivot_row] = aug[pivot_row], aug[row]
        scale = aug[row][col]
        for c in range(n_buttons + 1):
            aug[row][c] /= scale
        for r in range(n_counters):
            if r != row and aug[r][col] != 0:
                factor = aug[r][col]
                for c in range(n_buttons + 1):
                    aug[r][c] -= factor * aug[row][c]
        pivot_cols.append(col)
        row += 1

    for r in range(row, n_counters):
        if aug[r][n_buttons] != 0:
            return -1

    free_cols = [c for c in range(n_buttons) if c not in pivot_cols]
    n_free = len(free_cols)

    # Find the LCM of all denominators to work with integers
    from math import gcd
    def lcm(a, b):
        return a * b // gcd(a, b)

    all_denoms = [aug[r][n_buttons].denominator for r in range(len(pivot_cols))]
    for r in range(len(pivot_cols)):
        for fc in free_cols:
            if aug[r][fc] != 0:
                all_denoms.append(aug[r][fc].denominator)

    L = 1
    for d in all_denoms:
        L = lcm(L, d)

    # Scale everything by L to get integers
    # pivot_exprs: list of (scaled_const, [(free_idx, scaled_coef), ...], denom)
    # pivot_val = (scaled_const + sum(scaled_coef * free)) / L
    pivot_exprs = []
    for r, pc in enumerate(pivot_cols):
        const_scaled = int(aug[r][n_buttons] * L)
        coefs = []
        for fc in free_cols:
            if aug[r][fc] != 0:
                coefs.append((free_cols.index(fc), int(-aug[r][fc] * L)))
        pivot_exprs.append((const_scaled, coefs))

    def evaluate(free_vals):
        total = sum(free_vals)

        for const_scaled, coefs in pivot_exprs:
            val_scaled = const_scaled
            for fi, c in coefs:
                val_scaled += c * free_vals[fi]
            # Check divisibility and non-negativity
            if val_scaled % L != 0:
                return None
            pivot_val = val_scaled // L
            if pivot_val < 0:
                return None
            total += pivot_val

        return total

    if n_free == 0:
        result = evaluate(())
        return result if result is not None else -1

    # Enumerate free variables
    max_jolt = max(joltage)

    from itertools import product

    min_presses = float('inf')
    for free_vals in product(range(max_jolt + 1), repeat=n_free):
        result = evaluate(free_vals)
        if result is not None and result < min_presses:
            min_presses = result

    return min_presses if min_presses != float('inf') else -1


def solve_part2(text):
    """Find minimum total button presses for joltage configuration."""
    total = 0
    for line in text.strip().split('\n'):
        _, _, buttons, joltage = parse_line(line)
        presses = solve_joltage(buttons, joltage)
        if presses == -1:
            raise ValueError(f"No solution for line: {line}")
        total += presses
    return total


def test():
    example = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

    # Test parsing
    n, target, buttons, joltage = parse_line(example.split('\n')[0])
    assert n == 4, f"Expected 4 lights, got {n}"
    assert target == [0, 1, 1, 0], f"Target: {target}"
    assert len(buttons) == 6, f"Expected 6 buttons, got {len(buttons)}"
    assert joltage == [3, 5, 4, 7], f"Joltage: {joltage}"

    # Test individual machines - Part 1
    n, target, buttons, _ = parse_line(example.split('\n')[0])
    assert solve_machine(n, target, buttons) == 2, "Machine 1 should need 2 presses"

    n, target, buttons, _ = parse_line(example.split('\n')[1])
    assert solve_machine(n, target, buttons) == 3, "Machine 2 should need 3 presses"

    n, target, buttons, _ = parse_line(example.split('\n')[2])
    assert solve_machine(n, target, buttons) == 2, "Machine 3 should need 2 presses"

    # Test total Part 1
    assert solve_part1(example) == 7, f"Expected 7, got {solve_part1(example)}"

    # Test Part 2 - joltage
    _, _, buttons, joltage = parse_line(example.split('\n')[0])
    assert solve_joltage(buttons, joltage) == 10, f"Machine 1 joltage should need 10 presses"

    _, _, buttons, joltage = parse_line(example.split('\n')[1])
    assert solve_joltage(buttons, joltage) == 12, f"Machine 2 joltage should need 12 presses"

    _, _, buttons, joltage = parse_line(example.split('\n')[2])
    assert solve_joltage(buttons, joltage) == 11, f"Machine 3 joltage should need 11 presses"

    assert solve_part2(example) == 33, f"Expected 33, got {solve_part2(example)}"

    print("All tests passed!")


if __name__ == "__main__":
    test()

    with open("10_input.txt") as f:
        text = f.read()

    print(solve_part1(text))
    print(solve_part2(text))
