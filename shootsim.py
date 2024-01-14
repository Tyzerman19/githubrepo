# import help libraries for later

from time import sleep
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# project description
# a simulation of an arbitrary 'shooting' game
# higher 'skill' rating should lead to better scores in the shooting game
# assume skill level range will be from 1 to 5

# dict of players - ("Name" : "Skill")
player_dict = {
    "Mike":5,
    "Jill":4,
    "Puppy":3,
    "Brent":2,
    "Egg":1
}

player_list = list(player_dict.keys())

# pick 2 players for the game
player1 = random.choice(player_list)
player2 = random.choice(player_list)

player1_skill = player_dict.get(player1)
player2_skill = player_dict.get(player2)


def shoot(skill):
    # function to calculate the score of the shot attempt
    # intake numeric skill level for the shooter
    # output the numeric score of the attempt

    # base calculation of a score for the attempt
    # score is random with the skill level being used to increase the score (more skilled person will do better)
    base_score = random.randint(1,(10 + skill)) - random.randint(1,(6 - skill))

    # calculate the shot result (right now it is simply the base score
    result = (base_score)

    # a score of under 0 will be considered a 'miss' and set to 0
    if result < 0:
        result = 0

    # round for an integer score
    result = round(result, 1)

    # return the result
    return result

def play_round(p1skill, p2skill, shots_per_round):
    # function to perform multiple shot attempts that make up a round
    # intakes the skill for both players and the number of attempts per round
    # outputs the result of the round as a list
    # for each attempt the scores for each player are compared with the higher score getting a point (unless they tie)

    # create blank round score counter ([p1 win, p2 win, tie])
    round_result = [0,0,0]

    # loop for the number of shots requested
    for i in range(shots_per_round):

        # each player performs a shot
        p1score = shoot(p1skill)
        p2score = shoot(p2skill)

        # compare scores to determine winner and assign a point to column in round result
        if p1score > p2score:
            round_result[0] += 1
        if p1score < p2score:
            round_result[1] += 1
        if p1score == p2score:
            round_result[2] += 1

    # return the result of the round
    return round_result

def play_match(game_id, number_of_rounds, games_per_round, p1name, p1skill, p2name, p2skill):
    # function to complete a match by playing multiple rounds
    # intakes the number of rounds/games per round and the skill of each player

    # create a blank match score
    match_result = [0,0,0]
    # store the result of each individual match
    match_list = []

    # for the number of rounds requested play a round
    for i in range(number_of_rounds):

        # play the round
        round_result = play_round(p1skill, p2skill, games_per_round)

        # add round result to the list
        match_list.append(round_result)

        # add the round result to the match score
        if round_result[0] > round_result[1] and round_result[0] > round_result[2]:
            match_result[0] += 1
        elif round_result[1] > round_result[0] and round_result[1] > round_result[2]:
            match_result[1] += 1
        elif round_result[0] == round_result[1]:
            match_result[2] += 1

    # determine the winner
    if match_result[0] > match_result[1]:
        result = "Winner"
        winner = p1name
        winner_skill = p1skill
        loser = p2name
        loser_skill = p2skill
    elif match_result[1] > match_result[0]:
        result = "Winner"
        winner = p2name
        winner_skill = p2skill
        loser = p1name
        loser_skill = p1skill
    else:
        result = "Tie"
        winner = "None"
        winner_skill = "N/A"
        loser = "None"
        loser_skill = "N/A"

    player1_score = match_result[0]
    player2_score = match_result[1]

    # package the outcome to return
    outcome = [game_id,
                result,
                [winner, winner_skill,
                    max(player1_score, player2_score)],
                [loser, loser_skill,
                    min(player1_score, player2_score)],
                match_result]

    # return match results
    return outcome


# run a season

def run_season(number_of_matches, number_of_rounds, games_per_round, list_of_players):

    match_log = []

    for i in range(number_of_matches):
        game_id = i

        # pick 2 players for the game

        player1 = random.choice(list_of_players)
        while True:
            player2 = random.choice(list_of_players)
            if player2 != player1:
                break
        player1_skill = player_dict.get(player1)
        player2_skill = player_dict.get(player2)

        outcome = play_match(game_id,
                   number_of_rounds,
                   games_per_round,
                   player1,
                   player1_skill,
                   player2,
                   player2_skill)

        match_log.append(outcome)
    for i in match_log:
        print(i)

run_season(100, 5, 7, player_list)