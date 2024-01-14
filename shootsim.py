from time import sleep
import random
import numpy as np
import matplotlib.pyplot as plt

# skill can be from 1 to 5


def shoot(skill):

    # base score given for performing the shot
    base_score = random.randint(1,(10 + skill)) - random.randint(1,(6 - skill))

    # # create an error score to subtract
    # error = ((7 * random.random() / skill))

    # calculate the shot result
    result = (base_score)

    if result < 0:
        result = 0

    result = round(result, 1)

    return result
    # result = 10 if shot_calc > 10 else result

    scores.append(result)



# for i in range(1,6):
#     scores = []
#     for j in range(100000):
#         scores.append(shoot(i))
#     print(f"Skill: " + str(i))
#     print(f"Min: " + str(np.min(scores)))
#     print(f"Max: " + str(np.max(scores)))
#     print(f"Mean: " + str(np.mean(scores)))
#     print(f"std: " + str(np.std(scores)))
#     print("")

    # plt.hist(scores, bins=100)
    # plt.show()


def play_round(p1skill, p2skill, games):
    round_result = [0,0,0]
    game_counter = 0
    for i in range(games):
        game_counter += 1
        p1score = shoot(p1skill)
        p2score = shoot(p2skill)
        if p1score > p2score:
            round_result[0] += 1
        if p1score < p2score:
            round_result[1] += 1
        if p1score == p2score:
            round_result[2] += 1

    return round_result


def play_match(number_of_rounds, games_per_round, p1skill, p2skill):
    match_result = [0,0,0]
    match_list = []
    outcome = "Tie"
    for i in range(number_of_rounds):
        round_result = play_round(p1skill, p2skill, games_per_round)
        match_list.append(round_result)
        if round_result[0] > round_result[1] and round_result[0] > round_result[2]:
            match_result[0] += 1
        elif round_result[1] > round_result[0] and round_result[1] > round_result[2]:
            match_result[1] += 1
        elif round_result[2] > round_result[0] and round_result[2] > round_result[1]:
            match_result[2] += 1
    if match_result[0] > match_result[1]:
        outcome = "Player 1 wins"
    if match_result[1] > match_result[0]:
        outcome = "Player 2 wins"
    print(outcome)
    print(match_result)
    print(match_list)

play_match(100,4,5,5)