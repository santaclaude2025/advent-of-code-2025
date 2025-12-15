def parse_input(text):
    """Parse device connections into a graph."""
    graph = {}
    for line in text.strip().split('\n'):
        parts = line.split(': ')
        device = parts[0]
        outputs = parts[1].split() if len(parts) > 1 else []
        graph[device] = outputs
    return graph


def count_paths(graph, start, end):
    """Count all paths from start to end using memoization."""
    memo = {}

    def dfs(node):
        if node == end:
            return 1
        if node in memo:
            return memo[node]
        if node not in graph:
            return 0

        total = 0
        for next_node in graph[node]:
            total += dfs(next_node)

        memo[node] = total
        return total

    return dfs(start)


def solve_part1(text):
    """Count paths from 'you' to 'out'."""
    graph = parse_input(text)
    return count_paths(graph, 'you', 'out')


def count_paths_with_required(graph, start, end, required):
    """Count paths from start to end that visit all required nodes.

    Use memoization with state = (node, frozenset of required nodes visited so far)
    """
    memo = {}
    required_set = set(required)

    def dfs(node, visited_required):
        # Update visited_required if current node is required
        if node in required_set:
            visited_required = visited_required | {node}

        if node == end:
            # Only count if all required nodes were visited
            return 1 if visited_required == required_set else 0

        state = (node, frozenset(visited_required))
        if state in memo:
            return memo[state]

        if node not in graph:
            return 0

        total = 0
        for next_node in graph[node]:
            total += dfs(next_node, visited_required)

        memo[state] = total
        return total

    return dfs(start, frozenset())


def solve_part2(text):
    """Count paths from 'svr' to 'out' that visit both 'dac' and 'fft'."""
    graph = parse_input(text)
    return count_paths_with_required(graph, 'svr', 'out', ['dac', 'fft'])


def test():
    example = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""

    graph = parse_input(example)
    assert 'you' in graph
    assert graph['you'] == ['bbb', 'ccc']
    assert graph['bbb'] == ['ddd', 'eee']

    result = solve_part1(example)
    assert result == 5, f"Expected 5 paths, got {result}"

    # Part 2 test
    example2 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""

    graph2 = parse_input(example2)
    total_paths = count_paths(graph2, 'svr', 'out')
    assert total_paths == 8, f"Expected 8 total paths, got {total_paths}"

    result2 = count_paths_with_required(graph2, 'svr', 'out', ['dac', 'fft'])
    assert result2 == 2, f"Expected 2 paths with dac and fft, got {result2}"

    print("All tests passed!")


if __name__ == "__main__":
    test()

    with open("11_input.txt") as f:
        text = f.read()

    print(solve_part1(text))
    print(solve_part2(text))
