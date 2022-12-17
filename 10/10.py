import numpy as np

# Return a list of [part_1_answer, part_2_answer]
def get_result(file_path: str) -> list[int]:
    with open(file_path, 'r') as file:
        data = file.read().rstrip('\n')
        commands = data.split('\n')

        cycle = 1
        x_value = 1
        total_signal = 0

        crt_pointer = 0
        crt = np.full((6, 40), ' ')
        sprite_locations = [0, 1, 2]

        for command in commands:
            if crt_pointer in sprite_locations:
                crt[cycle//40][crt_pointer] = '#'

            if cycle in [20, 60, 100, 140, 180, 220]:
                total_signal += cycle * x_value

            if command == 'noop':
                cycle += 1
                crt_pointer += 1
                crt_pointer %= 40
            else:
                cycle += 1
                crt_pointer += 1
                crt_pointer %= 40

                # Each add command takes 2 cycles, so run start of cycle actions
                if crt_pointer in sprite_locations:
                    crt[cycle//40][crt_pointer] = '#'

                if cycle in [20, 60, 100, 140, 180, 220]:
                    total_signal += cycle * x_value

                _, add_val = command.split(' ')
                x_value += int(add_val)
                sprite_locations = [x_value - 1, x_value, x_value + 1]

                cycle += 1
                crt_pointer += 1
                crt_pointer %= 40

        np.set_printoptions(linewidth=np.inf)
        if file_path == 'input.txt':
            print(crt)

        return total_signal, 0

# Test solution against sample input
sample_results = get_result('sample.txt')
assert sample_results[0] ==  13140, 'Test 1 failed, got: %d' % sample_results[0]
assert sample_results[1] ==  0, 'Test 2 failed, got: %d' % sample_results[1]

input_results = get_result('input.txt')
print('Part 1:', input_results[0])
print('Part 2:', input_results[1])