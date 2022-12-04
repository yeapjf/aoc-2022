def get_result(file_path: str) -> list[int]:
    with open(file_path, 'r') as file:
        data = file.read().rstrip('\n')
        lines = data.split('\n')

        full_overlap_count = 0
        any_overlap_count = 0

        for line in lines:
            range_1, range_2 = line.split(',')
            range_1 = range_1.split('-')
            range_2 = range_2.split('-')
            range_1_min, range_1_max, range_2_min, range_2_max = map(int, range_1 + range_2)

            if (
                (range_1_min <= range_2_min and range_1_max >= range_2_max)
                or (range_2_min <= range_1_min and range_2_max >= range_1_max)
            ):
                full_overlap_count += 1
                any_overlap_count += 1
            elif (
                (range_1_min <= range_2_min and range_1_max >= range_2_min)
                or (range_2_min <= range_1_min and range_2_max >= range_1_min)
            ):
                any_overlap_count += 1

        
        return full_overlap_count, any_overlap_count

sample_results = get_result('sample.txt')
assert sample_results[0] ==  2, 'Test 1 failed, got: %d' % sample_results[0]
assert sample_results[1] ==  4, 'Test 2 failed, got: %d' % sample_results[1]

input_results = get_result('input.txt')
print('Part 1:', input_results[0])
print('Part 2:', input_results[1])