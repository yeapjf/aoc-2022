import math

def get_min_node(shortest_path: dict[str, int], visited: dict[str, bool]) -> [str, int]:
    min_node = None
    min_steps = math.inf

    for k, v in shortest_path.items():
        if v < min_steps and not visited[k]:
            min_steps = v
            min_node = k

    return min_node, min_steps

def dijkstra(
    height_map: list[list[int]], shortest_path: dict[str, int], visited: dict[str, int],
    start_pos: str, end_pos: str, sequence: dict[str, list[str]]
) -> int:
    rows = len(height_map)
    columns = len(height_map[0])
    shortest_path[start_pos] = 0
    sequence[start_pos] = [start_pos]

    def calculate_steps(height: int, steps: int, new_i: int, new_j: int) -> int:
        if not (new_i >= 0 and new_i < rows and new_j >= 0 and new_j < columns):
            return -1

        if height_map[new_i][new_j] - height < 2:
            new_pos = '%d,%d' % (new_i, new_j)
            new_steps = steps + 1

            if new_steps < shortest_path[new_pos]:
                shortest_path[new_pos] = new_steps
                sequence[new_pos] = sequence[pos] + [new_pos]

    for _ in range(rows * columns):
        pos, steps = get_min_node(shortest_path, visited)

        # Dead end when pos is None
        if pos == end_pos or pos is None:
            return shortest_path[end_pos]

        i, j = map(int, pos.split(','))
        height = height_map[i][j]

        calculate_steps(height, steps, i + 1, j)
        calculate_steps(height, steps, i - 1, j)
        calculate_steps(height, steps, i, j + 1)
        calculate_steps(height, steps, i, j - 1)

        visited[pos] = True

# Return a list of [part_1_answer, part_2_answer]
def get_result(file_path: str) -> [int, int]:
    with open(file_path, 'r') as file:
        data = file.read().rstrip('\n')
        lines = data.split('\n')

        height_map = []
        shortest_path = {}
        visited = {}
        start_poses_shortest = {}
        start_pos = None
        end_pos = None

        for i, line in enumerate(lines):
            heights = []

            for j, node in enumerate(line):
                pos = '%d,%d' % (i, j)

                if node == 'a':
                    height = 1
                    start_poses_shortest[pos] = math.inf
                elif node == 'S':
                    height = 1
                    start_pos = pos
                    start_poses_shortest[pos] = math.inf
                elif node == 'E':
                    height = 26
                    end_pos = pos
                else:
                    height = ord(node) - 96

                shortest_path[pos] = math.inf
                visited[pos] = False
                heights.append(height)

            height_map.append(heights)

        # Part 1
        min_steps = dijkstra(height_map[:], dict(shortest_path), dict(visited), start_pos, end_pos, {})

        # Part 2
        for pos in start_poses_shortest.keys():
            # Don't recalculate if shortest path already known
            if start_poses_shortest[pos] < math.inf:
                continue

            temp_shortest_path = dict(shortest_path)
            temp_sequence = {}

            steps = dijkstra(height_map[:], temp_shortest_path, dict(visited), pos, end_pos, temp_sequence)
            start_poses_shortest[pos] = steps

            # Check if other start nodes are on the shortest path of this node
            if temp_shortest_path[end_pos] < math.inf:
                for k, v in start_poses_shortest.items():
                    if v == math.inf and k in temp_sequence[end_pos]:
                        start_poses_shortest[k] = temp_shortest_path[end_pos] - temp_shortest_path[k]

        min_steps_2 = min(start_poses_shortest.values())
        return min_steps, min_steps_2

# Test solution against sample input
sample_results = get_result('sample.txt')
assert sample_results[0] ==  31, 'Test 1 failed, got: %d' % sample_results[0]
assert sample_results[1] ==  29, 'Test 2 failed, got: %d' % sample_results[1]

input_results = get_result('input.txt')
print('Part 1:', input_results[0])
print('Part 2:', input_results[1])