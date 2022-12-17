import math
import numpy as np

def check_fall(scan_map: np.ndarray, i: int, j: int) -> bool | None:
    rows, cols = scan_map.shape
    if i >= rows or j < 0 or j >= cols:
        return None
    elif scan_map[i][j] in ['o', '#']:
        return False
    elif scan_map[i][j] == '.':
        return True
    else:
        return False

def simulate_sand(scan_map: np.ndarray, sand_source: [int, int]) -> int:
    scan_map[sand_source[0], sand_source[1]] = '+'
    full = False
    total_sand = 0

    while not full:
        pos = sand_source
        falling = True

        while falling:
            for pos_diff in [[1, 0], [1, -1], [1, 1]]:
                new_i, new_j = np.add(pos, pos_diff)
                fall = check_fall(scan_map, new_i, new_j)

                if fall is None:
                    falling = False
                    full = True
                    break
                elif fall == True:
                    pos = [new_i, new_j]
                    break
                elif fall == False and pos_diff == [1, 1]:
                    if pos == sand_source:
                        scan_map[pos[0], pos[1]] = 'o'
                        total_sand += 1
                        full = True

                    falling = False
                    break

        if not full:
            scan_map[pos[0], pos[1]] = 'o'
            total_sand += 1

    return total_sand

# Return (part_1_answer, part_2_answer)
def get_result(file_path: str) -> (int, int):
    with open(file_path, 'r') as file:
        data = file.read().rstrip('\n')
        lines = data.split('\n')

        rock_formations = []
        col_offset = math.inf
        max_cols = 0
        max_rows = 0

        for line in lines:
            coods = line.split(' -> ')
            formation = []

            for cood in coods:
                x, y = map(int, cood.split(','))
                formation.append([y, x])

                if x < col_offset:
                    col_offset = x
                if x > max_cols:
                    max_cols = x
                if y > max_rows:
                    max_rows = y

            rock_formations.append(formation)

        scan_map = np.full((max_rows + 1, max_cols - col_offset + 1), '.')
        sand_source = [0, 500 - col_offset]

        for formation in rock_formations:
            for i in range(1, len(formation)):
                pos_1 = formation[i - 1]
                pos_2 = formation[i]
                pos_1_row = pos_1[0]
                pos_1_col = pos_1[1] - col_offset
                pos_diff = np.subtract(pos_2, pos_1)

                if pos_diff[0] != 0:
                    row_from, row_to = sorted([pos_1_row, pos_1_row + pos_diff[0]])
                    row_to += 1
                    scan_map[row_from:row_to,pos_1_col] = '#'
                elif pos_diff[1] != 0:
                    col_from, col_to = sorted([pos_1_col, pos_1_col + pos_diff[1]])
                    col_to += 1
                    scan_map[pos_1_row,col_from:col_to] = '#'

        # Part 1
        total_sand = simulate_sand(scan_map.copy(), sand_source)

        # Part 2
        rows, cols = scan_map.shape
        extra_cols = [['.'] * rows for i in range(rows)]
        scan_map_2 = scan_map[:]
        scan_map_2 = np.hstack([extra_cols, scan_map_2, extra_cols])

        rows, cols = scan_map_2.shape
        extra_rows = [['.'] * cols, ['#'] * cols]
        scan_map_2 = np.vstack([scan_map_2, extra_rows])
        np.set_printoptions(linewidth=np.inf)

        sand_source_2 = [0, sand_source[1] + rows]
        total_sand_2 = simulate_sand(scan_map_2, sand_source_2)

        return total_sand, total_sand_2

# Test solution against sample input
sample_results = get_result('sample.txt')
assert sample_results[0] ==  24, 'Test 1 failed, got: %d' % sample_results[0]
assert sample_results[1] ==  93, 'Test 2 failed, got: %d' % sample_results[1]

input_results = get_result('input.txt')
print('Part 1:', input_results[0])
print('Part 2:', input_results[1])