from itertools import permutations
import re

SCORE_CACHE = {}

def dijkstra(start_node: str, node_paths: dict[str, list]) -> dict[str, int]:
    shortest_path = { start_node: 0 }
    visited = {}
    queue = [ [start_node, 0] ]

    while len(queue):
        node, distance = queue.pop(0)

        if node in visited:
            continue
        else:
            visited[node] = 1

        for dest_node in node_paths[node]:
            new_distance = distance + 1
            queue.append([dest_node, new_distance])
            queue.sort(key=lambda x: x[1])

            if dest_node not in shortest_path or shortest_path[dest_node] > distance + 1:
                shortest_path[dest_node] = new_distance

    return shortest_path

def get_max_score(node: str, weight: int, children_nodes: [str], node_scores: dict[str, int], shortest_paths: dict[str, dict]) -> int:
    node_score = 0 if node not in node_scores else weight * node_scores[node]
    max_child_score = 0

    for child_node in children_nodes:
        child_score = 0
        new_weight = weight - (shortest_paths[node][child_node] + 1)

        if new_weight > 0:
            new_children_nodes = list(filter(lambda x: x != child_node, children_nodes))
            child_score = get_max_score(child_node, new_weight, new_children_nodes, node_scores, shortest_paths)

        if child_score > max_child_score:
            max_child_score = child_score

    return node_score + max_child_score

def cache_score(nodes: [str, str], weights: [int, int], children_nodes: [str], store: bool = False, score: int = 0) -> int | None:
    node_1, node_2 = nodes
    weight_1, weight_2 = weights
    node_weights = sorted([[node_1, weight_1], [node_2, weight_2]], key=lambda x: x[0])
    key = str(node_weights) + str(children_nodes)

    if store:
        SCORE_CACHE[key] = score
    elif key in SCORE_CACHE:
        return SCORE_CACHE[key]

    return None

def get_dual_max_score(nodes: [str, str], weights: [int, int], children_nodes: [str], node_scores: dict[str, int], shortest_paths: dict[str, dict]) -> int:
    cached_score = cache_score(nodes, weights, children_nodes)
    if cached_score is not None:
        return cached_score

    node_1, node_2 = nodes
    weight_1, weight_2 = weights
    dual_node_score = sum([0 if nodes[i] not in node_scores else weights[i] * node_scores[nodes[i]] for i in range(2)])
    max_child_score = 0

    for child_node_1, child_node_2 in permutations(children_nodes, 2):
        child_score = 0
        new_weight_1 = weight_1 - (shortest_paths[node_1][child_node_1] + 1)
        new_weight_2 = weight_2 - (shortest_paths[node_2][child_node_2] + 1)

        if new_weight_1 > 0 and new_weight_2 > 0:
            new_children_nodes = list(filter(lambda x: x not in [child_node_1, child_node_2], children_nodes))
            child_score = get_dual_max_score([child_node_1, child_node_2],
                [new_weight_1, new_weight_2], new_children_nodes, node_scores, shortest_paths)
        elif new_weight_1 > 0 and new_weight_2 <= 0:
            new_children_nodes = list(filter(lambda x: x not in [child_node_1], children_nodes))
            child_score = get_dual_max_score([child_node_1, node_2],
                [new_weight_1, 0], new_children_nodes, node_scores, shortest_paths)
        elif new_weight_1 <= 0 and new_weight_2 > 0:
            new_children_nodes = list(filter(lambda x: x not in [child_node_2], children_nodes))
            child_score = get_dual_max_score([node_1, child_node_2],
                [0, new_weight_2], new_children_nodes, node_scores, shortest_paths)

        if child_score > max_child_score:
            max_child_score = child_score

    max_score = dual_node_score + max_child_score
    cache_score(nodes, weights, children_nodes, True, max_score)

    return max_score

# Return (part_1_answer, part_2_answer)
def get_result(file_path: str) -> (int, int):
    with open(file_path, 'r') as file:
        data = file.read().rstrip('\n')
        lines = data.split('\n')

        root_node = 'AA'
        node_scores = {}
        node_paths = {}

        for line in lines:
            node = line.split(' ')[1]
            score = int(re.search(r'rate=(\d+);', line).group(1))
            paths = re.findall(r'(?:valves?|,) (\w+)', line)
            node_paths[node] = paths

            if score > 0:
                node_scores[node] = score

        shortest_paths = {}
        for node in [root_node] + list(node_scores.keys()):
            distances = dijkstra(node, node_paths)
            shortest_paths[node] = {}
            dest_nodes = filter(lambda k: k != node, node_scores.keys())

            for dest_node in dest_nodes:
                if dest_node in distances:
                    shortest_paths[node][dest_node] = distances[dest_node]

        children_nodes = sorted(node_scores.keys(), key=lambda k: node_scores[k])
        max_score = get_max_score(root_node, 30, children_nodes, node_scores, shortest_paths)
        dual_max_score = get_dual_max_score([root_node, root_node], [26, 26], children_nodes, node_scores, shortest_paths)

        return max_score, dual_max_score

# Test solution against sample input
sample_results = get_result('sample.txt')
assert sample_results[0] ==  1651, 'Test 1 failed, got: %d' % sample_results[0]
assert sample_results[1] ==  1707, 'Test 2 failed, got: %d' % sample_results[1]

input_results = get_result('input.txt')
print('Part 1:', input_results[0])
print('Part 2:', input_results[1])