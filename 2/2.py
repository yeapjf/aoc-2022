# A = X = 1 = Rock
# B = Y = 2 = Paper
# C = Z = 3 = Scissors
play_score = {
    'X': 1,
    'Y': 2,
    'Z': 3
}

outcome_score = {
    'X': {
        'A': 3,
        'B': 0,
        'C': 6
    },
    'Y': {
        'A': 6,
        'B': 3,
        'C': 0
    },
    'Z': {
        'A': 0,
        'B': 6,
        'C': 3
    }
}

outcome_score_2 = {
    'X': 0,
    'Y': 3,
    'Z': 6
}

play_score_2 = {
    'A': {
        'X': 3,
        'Y': 1,
        'Z': 2
    },
    'B': {
        'X': 1,
        'Y': 2,
        'Z': 3
    },
    'C': {
        'X': 2,
        'Y': 3,
        'Z': 1
    }
}

with open('input.txt', 'r') as file:
    data = file.read().rstrip('\n')
    plays = data.split('\n')

    # Part 1
    total_score = 0
    for play in plays:
        opp, you = play.split(' ')
        total_score += play_score[you] + outcome_score[you][opp]

    print(total_score)

    # Part 2
    total_score_2 = 0
    for play in plays:
        opp, outcome = play.split(' ')
        total_score_2 += outcome_score_2[outcome] + play_score_2[opp][outcome]

    print(total_score_2)
