import re

# Return a list of [part_1_answer, part_2_answer]
def get_result(file_path: str) -> list[str]:
    with open(file_path, 'r') as file:
        data = file.read().rstrip('\n')
        arrangements_str, procedures_str = data.split('\n\n')
        arrangements = arrangements_str.split('\n')
        procedures = procedures_str.split('\n')

        total_stacks = len([e for e in arrangements[-1].split(' ') if e != ''])
        arrangements = arrangements[:-1]

        stacks = {}
        stacks_2 = {}

        for arrangement in arrangements:
            for pos, char in enumerate(arrangement):
                if char == '[':
                    letter = arrangement[pos + 1]
                    stack_index = pos / 4
                    stacks.setdefault(stack_index, []).append(letter)
                    stacks_2.setdefault(stack_index, []).append(letter)

        top_items = ''
        for procedure in procedures:
            total_items, src_stack, dest_stack = re.findall(r'\d+', procedure)
            total_items, src_stack, dest_stack = map(int, [total_items, src_stack, dest_stack])
            src_stack, dest_stack = [e - 1 for e in [src_stack, dest_stack]]

            for i in range(total_items):
                item = stacks[src_stack].pop(0)
                stacks[dest_stack].insert(0, item)

        for i in range(total_stacks):
            top_items += stacks[i][0]

        top_items_2 = ''
        for procedure in procedures:
            total_items, src_stack, dest_stack = re.findall(r'\d+', procedure)
            total_items, src_stack, dest_stack = map(int, [total_items, src_stack, dest_stack])
            src_stack, dest_stack = [e - 1 for e in [src_stack, dest_stack]]

            stacks_2[dest_stack] = stacks_2[src_stack][0:total_items] + stacks_2[dest_stack]
            stacks_2[src_stack] = stacks_2[src_stack][total_items:]

        for i in range(total_stacks):
            top_items_2 += stacks_2[i][0]

        return top_items, top_items_2

# Test solution against sample input
sample_results = get_result('sample.txt')
assert sample_results[0] ==  'CMZ', 'Test 1 failed, got: %s' % sample_results[0]
assert sample_results[1] ==  'MCD', 'Test 2 failed, got: %s' % sample_results[1]

input_results = get_result('input.txt')
print('Part 1:', input_results[0])
print('Part 2:', input_results[1])