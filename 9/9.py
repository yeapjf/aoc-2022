import math

def calculate_tail_pos(head_pos: (int, int), tail_pos: (int, int)) -> (int, int):
    v_distance = head_pos[0] - tail_pos[0]
    h_distance = head_pos[1] - tail_pos[1]

    if h_distance in [-1, 0, 1] and v_distance in [-1, 0, 1]:
        return tail_pos
    else:
        new_y = tail_pos[0]
        new_x = tail_pos[1]

        if v_distance != 0:
            new_y += math.copysign(1, v_distance)
        if h_distance != 0:
            new_x += math.copysign(1, h_distance)

        return (new_y, new_x)

# Return a list of [part_1_answer, part_2_answer]
def get_result(file_path: str) -> list[int]:
    with open(file_path, 'r') as file:
        data = file.read().rstrip('\n')
        steps = data.split('\n')

        # Part 1
        head_pos = (0, 0)
        tail_pos = (0, 0)
        visited = [(0, 0)]

        for step in steps:
            direction, num_steps = step.split(' ')
            num_steps = int(num_steps)

            for i in range(num_steps):
                if direction == 'U':
                    head_pos = (head_pos[0] - 1, head_pos[1])
                elif direction == 'D':
                    head_pos = (head_pos[0] + 1, head_pos[1])
                elif direction == 'L':
                    head_pos = (head_pos[0], head_pos[1] - 1)
                elif direction == 'R':
                    head_pos = (head_pos[0], head_pos[1] + 1)

                tail_pos = calculate_tail_pos(head_pos, tail_pos)
                visited.append(tail_pos)

        unique_pos = len(set(visited))

        # Part 2
        poses = [(0, 0)] * 10
        tail_visited = [(0, 0)]

        for step in steps:
            direction, num_steps = step.split(' ')
            num_steps = int(num_steps)

            for i in range(num_steps):
                head_pos = poses[0]
                if direction == 'U':
                    head_pos = (head_pos[0] - 1, head_pos[1])
                elif direction == 'D':
                    head_pos = (head_pos[0] + 1, head_pos[1])
                elif direction == 'L':
                    head_pos = (head_pos[0], head_pos[1] - 1)
                elif direction == 'R':
                    head_pos = (head_pos[0], head_pos[1] + 1)

                poses[0] = head_pos
                for pos_index in range(1, len(poses)):
                    tail_pos = calculate_tail_pos(poses[pos_index - 1], poses[pos_index])
                    poses[pos_index] = tail_pos

                    if pos_index == len(poses) - 1:
                        tail_visited.append(tail_pos)

        unique_tail_pos = len(set(tail_visited))
        return unique_pos, unique_tail_pos

# Test solution against sample input
sample_results = get_result('sample.txt')
assert sample_results[0] ==  88, 'Test 1 failed, got: %d' % sample_results[0]
assert sample_results[1] ==  36, 'Test 2 failed, got: %d' % sample_results[1]

input_results = get_result('input.txt')
print('Part 1:', input_results[0])
print('Part 2:', input_results[1])