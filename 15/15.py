import re

def get_interval(coods: [(str, str)], y: int, x_max: int | None = None) -> [int | None, int | None]:
    s_x, s_y = map(int, list(coods[0]))
    b_x, b_y = map(int, list(coods[1]))
    s_interval = abs(b_x - s_x) + abs(b_y - s_y)
    row_interval = s_interval - abs(y - s_y)

    if row_interval < 0:
        return [None, None]

    row_start = s_x - row_interval
    row_start = 0 if (x_max is not None and row_start < 0) else row_start
    row_end = s_x + row_interval
    row_end = x_max if (x_max is not None and row_end > x_max) else row_end
    return [row_start, row_end + 1]

def get_merged_interval(sensors: [dict], y: int, x_max: int | None = None) -> [list]:
    intervals = []
    
    for sensor in sensors:
        row_interval = get_interval(sensor, y)
        if row_interval != [None, None]:
            intervals.append(get_interval(sensor, y, x_max))

    intervals.sort(key=lambda interval: interval[0])
    merged = [intervals[0]]
    row_total = 0

    for current in intervals:
        previous = merged[-1]
        if current[0] <= previous[1]:
            previous[1] = max(previous[1], current[1])
        else:
            merged.append(current)

    return merged

# Return a list of (part_1_answer, part_2_answer)
def get_result(file_path: str) -> (int, int):
    with open(file_path, 'r') as file:
        data = file.read().rstrip('\n')
        lines = data.split('\n')

        sensors = []
        y_beacons = {}

        for line in lines:
            coods = re.findall(r'x=([-\d]+), y=([-\d]+)', line)
            b_x, b_y = map(int, list(coods[1]))
            sensors.append(coods)
            y_beacons.setdefault(b_y, set()).add(b_x)
        
        # Part 1
        y = 10 if file_path == 'sample.txt' else 2000000
        merged_interval = get_merged_interval(sensors, y)
        row_total = 0
            
        for interval in merged_interval:
            row_total += interval[1] - interval[0]

        row_total -= len(y_beacons[y])

        # Part 2
        x_max = 20 if file_path == 'sample.txt' else 4000000
        y_max = 20 if file_path == 'sample.txt' else 4000000
        tuning_value = None

        for i in range(y_max + 1):
            row_merged_interval = get_merged_interval(sensors, i, x_max)

            if row_merged_interval[0] != [0, x_max + 1]:
                tuning_value = row_merged_interval[0][1] * 4000000 + i
                break

        return row_total, tuning_value

# Test solution against sample input
sample_results = get_result('sample.txt')
assert sample_results[0] ==  26, 'Test 1 failed, got: %d' % sample_results[0]
assert sample_results[1] ==  56000011, 'Test 2 failed, got: %d' % sample_results[1]

input_results = get_result('input.txt')
print('Part 1:', input_results[0])
print('Part 2:', input_results[1])