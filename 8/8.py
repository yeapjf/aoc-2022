import numpy as np

# Return a list of [part_1_answer, part_2_answer]
def get_result(file_path: str) -> list[int]:
    with open(file_path, 'r') as file:
        data = file.read().rstrip('\n')
        lines = data.split('\n')

        num_rows = len(lines)
        num_cols = len(lines[0])
        height_map = np.zeros([num_rows, num_cols])

        num_visible = 0
        max_score = 0

        for i, line in enumerate(lines):
            line_heights = np.array(list(map(int, list(line))))
            height_map[i] = line_heights

        for i, row in enumerate(height_map):
            for j, col in enumerate(row):
                # Trees along the edge
                if i == 0 or j == 0 or (i == num_cols - 1) or (j == num_rows - 1):
                    num_visible += 1
                else:
                    pos_height = height_map[i][j]
                    current_score = 1

                    # Flip left and up trees for score calculation
                    left_trees = np.flip(height_map[i, 0:j])
                    right_trees = height_map[i, j+1:num_cols]
                    up_trees = np.flip(height_map[0:i, j])
                    down_trees = height_map[i+1:num_rows, j]

                    # Check if tree is visible (part 1)
                    if any(
                        pos_height > max_height for max_height in [
                            max(left_trees), max(right_trees),
                            max(up_trees), max(down_trees)
                        ]
                    ):
                        num_visible += 1
                    
                    # Score calculation for tree (part 2)
                    for k, height in enumerate(left_trees):
                        if height >= pos_height or k == len(left_trees) - 1:
                            current_score *= (k + 1)
                            break

                    for k, height in enumerate(right_trees):
                        if height >= pos_height or k == len(right_trees) - 1:
                            current_score *= (k + 1)
                            break

                    for k, height in enumerate(up_trees):
                        if height >= pos_height or k == len(up_trees) - 1:
                            current_score *= (k + 1)
                            break

                    for k, height in enumerate(down_trees):
                        if height >= pos_height or k == len(down_trees) - 1:
                            current_score *= (k + 1)
                            break
                    
                    if current_score > max_score:
                        max_score = current_score

        return num_visible, max_score

# Test solution against sample input
sample_results = get_result('sample.txt')
assert sample_results[0] ==  21, 'Test 1 failed, got: %d' % sample_results[0]
assert sample_results[1] ==  8, 'Test 2 failed, got: %d' % sample_results[1]

input_results = get_result('input.txt')
print('Part 1:', input_results[0])
print('Part 2:', input_results[1])