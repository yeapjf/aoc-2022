import re

def process_monkeys(monkey_num, monkey_items, monkey_operations, monkey_tests, monkey_inspections, part_2=False):
    common_divide = 1
    for test_data in monkey_tests:
        common_divide *= test_data[0]

    for i in range(monkey_num):
        operation = lambda old: eval(monkey_operations[i])
        test_data = monkey_tests[i]
        test = lambda x: test_data[1] if x % test_data[0] == 0 else test_data[2]

        while monkey_items[i]:
            item = monkey_items[i].pop(0)

            if not part_2:
                new_value = operation(item)
                new_value //= 3
                new_monkey = test(new_value)
                monkey_items[new_monkey].append(new_value)
                monkey_inspections[i] += 1
            else:
                new_value = operation(item)
                new_value %= common_divide
                new_monkey = test(new_value)
                monkey_items[new_monkey].append(new_value)
                monkey_inspections[i] += 1

# Return a list of [part_1_answer, part_2_answer]
def get_result(file_path: str) -> list[int]:
    with open(file_path, 'r') as file:
        data = file.read().rstrip('\n')
        lines = data.split('\n')

        current_monkey = 0
        current_test = [None, None, None]

        monkey_num = len(re.findall(r'Monkey', data))
        monkey_items = [None] * monkey_num
        monkey_items_2 = [None] * monkey_num
        monkey_operations = [None] * monkey_num
        monkey_tests = [None] * monkey_num

        # Initialise starting items, operations and tests
        for line in lines:
            monkey_match = re.match(r'^Monkey (\d+):', line)
            items_match = re.search(r'Starting items: (.*)$', line)
            operation_match = re.search(r'Operation: new = (.*)$', line)
            test_match = re.search(r'Test: divisible by (\d+)$', line)
            true_match = re.search(r'If true: throw to monkey (\d+)$', line)
            false_match = re.search(r'If false: throw to monkey (\d+)$', line)

            if monkey_match:
                current_monkey = int(monkey_match.group(1))
            elif items_match:
                items_str = items_match.group(1) 
                items = list(map(int, items_str.split(',')))
                monkey_items[current_monkey] = items[:]
                monkey_items_2[current_monkey] = items[:]
            elif operation_match:
                operation_str = operation_match.group(1)
                monkey_operations[current_monkey] = operation_str
            elif test_match:
                test_str = test_match.group(1)
                current_test[0] = int(test_str)
            elif true_match:
                true_str = true_match.group(1)
                current_test[1] = int(true_str)
            elif false_match:
                false_str = false_match.group(1)
                current_test[2] = int(false_str)
                monkey_tests[current_monkey] = current_test[:]

        monkey_inspections = [0] * monkey_num
        monkey_inspections_2 = [0] * monkey_num

        for i in range(20):
            process_monkeys(monkey_num, monkey_items, monkey_operations, monkey_tests, monkey_inspections)
            
        for i in range(10000):
            process_monkeys(monkey_num, monkey_items_2, monkey_operations, monkey_tests, monkey_inspections_2, True)

        monkey_inspections.sort(reverse=True)
        monkey_inspections_2.sort(reverse=True)
        monkey_business = monkey_inspections[0] * monkey_inspections[1]
        monkey_business_2 = monkey_inspections_2[0] * monkey_inspections_2[1]

        return monkey_business, monkey_business_2

# Test solution against sample input
sample_results = get_result('sample.txt')
assert sample_results[0] ==  10605, 'Test 1 failed, got: %d' % sample_results[0]
assert sample_results[1] ==  2713310158, 'Test 2 failed, got: %d' % sample_results[1]

input_results = get_result('input.txt')
print('Part 1:', input_results[0])
print('Part 2:', input_results[1])