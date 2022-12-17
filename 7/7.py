from collections import defaultdict
import re

# Calculate total size of each directory with dynamic program
def calculate_size(dir_sizes: dict, dir_contents: defaultdict, dir_path: str) -> None:
    total_size = 0

    for v in dir_contents[dir_path]:
        if v.isnumeric():
            total_size += int(v)
        else:
            total_size += dir_sizes[v]

    dir_sizes[dir_path] = total_size

# Return a list of [part_1_answer, part_2_answer]
def get_result(file_path: str) -> list[int]:
    with open(file_path, 'r') as file:
        data = file.read().rstrip('\n')
        lines = data.split('\n')

        current_path = []
        dir_contents = defaultdict(lambda: [])

        for line in lines:
            cd_m = re.match(r'^\$ cd (.+)', line)
            dir_m = re.match(r'^dir (.+)', line)
            size_m = re.match(r'^(\d+) (.+)', line)

            if cd_m:
                cd_dir = cd_m.group(1)

                if cd_dir == '..':
                    current_path = current_path[:-1]
                elif cd_dir == '/':
                    current_path = ['/']
                else:
                    current_path.append(cd_dir + '/')
            else:
                path_str = ''.join(current_path)

                if dir_m:
                    child_path_str = path_str + dir_m.group(1) + '/'
                    dir_contents[path_str].append(child_path_str)
                elif size_m:
                    dir_contents[path_str].append(size_m.group(1))

                dir_contents[path_str].sort()

        dir_sizes = {}
        for k in sorted(dir_contents.keys(), reverse=True, key=lambda v: len(v)):
            calculate_size(dir_sizes, dir_contents, k)

        # Part 1
        small_dirs = { k: v for k, v in dir_sizes.items() if v <= 100000 }
        small_dirs_size = sum(small_dirs.values())

        # Part 2
        required_size = 30000000 - 70000000 + dir_sizes['/']
        large_dirs = { k: v for k, v in dir_sizes.items() if v >= required_size }
        min_large_dir_size = min(large_dirs.values())

        return small_dirs_size, min_large_dir_size

# Test solution against sample input
sample_results = get_result('sample.txt')
assert sample_results[0] ==  95437, 'Test 1 failed, got: %d' % sample_results[0]
assert sample_results[1] ==  24933642, 'Test 2 failed, got: %d' % sample_results[1]

input_results = get_result('input.txt')
print('Part 1:', input_results[0])
print('Part 2:', input_results[1])