def num_unique(max_uniques: list[int], input: str, pos: int) -> int:
    previous_max = max_uniques[pos - 1]
    duplicate_pos = -1

    for i in range(pos - previous_max, pos):
        if input[pos] == input[i]:
            duplicate_pos = i

    if duplicate_pos == -1:
        new_max = previous_max + 1
    else:
        new_max = pos - duplicate_pos

    # print(previous_max, input[pos - previous_max : pos + 1], new_max)
    max_uniques.append(new_max)

# Return a list of [part_1_answer, part_2_answer]
def get_result(file_path: str) -> list[int]:
    with open(file_path, 'r') as file:
        data = file.read().rstrip('\n')
        max_uniques = [1]

        for i in range(1, len(data)):
            num_unique(max_uniques, data, i)

        # Part 1
        pos = max_uniques.index(4)

        # Part 2
        pos_2 = max_uniques.index(14)
        return pos + 1, pos_2 + 1

# Test solution against sample input
sample_results = get_result('sample.txt')
assert sample_results[0] ==  11, 'Test 1 failed, got: %d' % sample_results[0]
assert sample_results[1] ==  26, 'Test 2 failed, got: %d' % sample_results[1]

input_results = get_result('input.txt')
print('Part 1:', input_results[0])
print('Part 2:', input_results[1])