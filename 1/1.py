with open('input.txt', 'r') as file:
    data = file.read().rstrip('\n')
    elves = data.split('\n\n')

    all_calories = []

    for elf in elves:
        str_calories = elf.split('\n')
        calories = map(int, str_calories)
        total = sum(calories)
        all_calories.append(total)
        
    # Part 1
    max_calories = max(all_calories)
    print(max_calories)

    # Part 2
    all_calories.sort(reverse=True)
    print(sum(all_calories[:3]))