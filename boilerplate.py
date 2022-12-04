# Return a list of [part_1_answer, part_2_answer]
def get_result(file_path: str) -> list[int]:
    with open(file_path, 'r') as file:
        data = file.read().rstrip('\n')

        return 0, 0

# Test solution against sample input
sample_results = get_result('sample.txt')
assert sample_results[0] ==  0, 'Test 1 failed, got: %d' % sample_results[0]
assert sample_results[1] ==  0, 'Test 2 failed, got: %d' % sample_results[1]

input_results = get_result('input.txt')
print('Part 1:', input_results[0])
print('Part 2:', input_results[1])