import math
from itertools import combinations


def parse_input(text):
    """Parse junction box positions."""
    boxes = []
    for line in text.strip().split('\n'):
        x, y, z = map(int, line.split(','))
        boxes.append((x, y, z))
    return boxes


def distance(p1, p2):
    """Calculate Euclidean distance between two 3D points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # Already in same circuit
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        self.size[px] += self.size[py]
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True

    def get_circuit_sizes(self):
        sizes = []
        for i in range(len(self.parent)):
            if self.parent[i] == i:
                sizes.append(self.size[i])
        return sorted(sizes, reverse=True)


def solve_part1(text, num_connections=1000):
    """Connect num_connections closest pairs and return product of 3 largest circuits."""
    boxes = parse_input(text)
    n = len(boxes)

    # Calculate all pairwise distances
    edges = []
    for i, j in combinations(range(n), 2):
        d = distance(boxes[i], boxes[j])
        edges.append((d, i, j))

    # Sort by distance
    edges.sort()

    # Connect the closest pairs using Union-Find
    uf = UnionFind(n)
    connections_made = 0

    for d, i, j in edges:
        uf.union(i, j)  # Union even if already connected (it just returns False)
        connections_made += 1
        if connections_made >= num_connections:
            break

    # Get circuit sizes and multiply top 3
    sizes = uf.get_circuit_sizes()
    return sizes[0] * sizes[1] * sizes[2]


def solve_part2(text):
    """Connect pairs until all in one circuit, return product of X coords of last connection."""
    boxes = parse_input(text)
    n = len(boxes)

    # Calculate all pairwise distances
    edges = []
    for i, j in combinations(range(n), 2):
        d = distance(boxes[i], boxes[j])
        edges.append((d, i, j))

    # Sort by distance
    edges.sort()

    # Connect pairs until all in one circuit
    uf = UnionFind(n)
    circuits_remaining = n

    for d, i, j in edges:
        if uf.union(i, j):  # Only count if actually merged two circuits
            circuits_remaining -= 1
            if circuits_remaining == 1:
                # This was the last connection needed
                return boxes[i][0] * boxes[j][0]

    return None


def test():
    example = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""

    boxes = parse_input(example)
    assert len(boxes) == 20, f"Expected 20 boxes, got {len(boxes)}"
    assert boxes[0] == (162, 817, 812), f"First box: {boxes[0]}"

    # Test after 10 connections
    result = solve_part1(example, num_connections=10)
    assert result == 40, f"Expected 40, got {result}"

    # Part 2: last connection to form single circuit
    result2 = solve_part2(example)
    assert result2 == 25272, f"Expected 25272, got {result2}"

    print("All tests passed!")


if __name__ == "__main__":
    test()

    with open("08_input.txt") as f:
        text = f.read()

    print(solve_part1(text))
    print(solve_part2(text))
