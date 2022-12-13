from functools import cmp_to_key
from typing import Union

def recursive_compare(signal_1: Union[list, int], signal_2: Union[list, int]) -> int:
    length_1 = len(signal_1)
    length_2 = len(signal_2)

    for i in range(max(length_1, length_2)):
        if i >= length_1:
            return 1
        elif i >= length_2:
            return -1

        entry_1 = signal_1[i]
        entry_2 = signal_2[i]
        order = None

        if type(entry_1) is type(entry_2) and type(entry_1) is int:
            if entry_1 > entry_2:
                return -1
            elif entry_2 > entry_1:
                return 1
        elif type(entry_1) is list and type(entry_2) is not list:
            order = recursive_compare(entry_1, [entry_2])
        elif type(entry_1) is not list and type(entry_2) is list:
            order = recursive_compare([entry_1], entry_2)
        else:
            order = recursive_compare(entry_1, entry_2)
        
        if order is not None:
            return order

# Return a list of [part_1_answer, part_2_answer]
def get_result(file_path: str) -> [int, int]:
    with open(file_path, 'r') as file:
        data = file.read().rstrip('\n')
        lines = data.split('\n')

        # Part 1
        current_index = 0
        total_index = 0

        # Part 2
        signals = [[[2]], [[6]]]

        while len(lines):
            current_index += 1
            pair = lines[:3]
            lines = lines[3:]

            signal_1 = eval(pair[0])
            signal_2 = eval(pair[1])
            order = recursive_compare(signal_1, signal_2)
            signals += [signal_1, signal_2]

            if order == 1:
                total_index += current_index

        sorted_signals = sorted(signals, key=cmp_to_key(recursive_compare), reverse=True)
        separator_1_index = sorted_signals.index([[2]]) + 1
        separator_2_index = sorted_signals.index([[6]]) + 1

        return total_index, separator_1_index * separator_2_index

# Test solution against sample input
sample_results = get_result('sample.txt')
assert sample_results[0] ==  13, 'Test 1 failed, got: %d' % sample_results[0]
assert sample_results[1] ==  140, 'Test 2 failed, got: %d' % sample_results[1]

input_results = get_result('input.txt')
print('Part 1:', input_results[0])
print('Part 2:', input_results[1])