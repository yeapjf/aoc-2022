def calculate_priority(item: str) -> int:
    if item.islower():
        return ord(item) - 96
    else:
        return ord(item) - 38

with open('input.txt', 'r') as file:
    data = file.read().rstrip('\n')
    rucksacks = data.split('\n')

    # Part 1
    total_priority = 0

    for rucksack in rucksacks:
        compartment_1, compartment_2 = rucksack[:len(rucksack)//2], rucksack[len(rucksack)//2:]
        common_item = list(set(compartment_1).intersection(compartment_2))[0]
        total_priority += calculate_priority(common_item)
    
    print(total_priority)

    # Part 2
    total_priority_2 = 0
    elf_group = []

    for rucksack in rucksacks:
        elf_group.append(rucksack)

        if len(elf_group) == 3:
            common_item = list(set(elf_group[0]).intersection(elf_group[1]).intersection(elf_group[2]))[0]
            total_priority_2 += calculate_priority(common_item)
            elf_group = []

    print(total_priority_2)