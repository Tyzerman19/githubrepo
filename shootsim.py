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
    "Egg":1,
    "Shark":4,
    "Box":1,
    "Tay":5,
    "Duo":2,
    "Dino":3,
    "Narv":1,
    "Beat":2,
    "Jee":3,
    "Mint":4,
    "Vent":5,
    "Ang":1,
    "Bank":2,
    "Cal":3,
    "Smoke":4,
    "Rob":5,
    "Wild":5,
    "Felix":1,
    "Flow":5,
    "Bug":1
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

def play_match(match_id, number_of_rounds, shots_per_round, p1name, p1skill, p2name, p2skill):
    # function to complete a match by playing multiple rounds
    # intakes the number of rounds/games per round and the skill of each player

    # create a blank match score
    match_result = [0,0,0]
    # store the result of each individual match
    match_list = []

    # for the number of rounds requested play a round
    for i in range(number_of_rounds):

        # play the round
        round_result = play_round(p1skill, p2skill, shots_per_round)

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
    outcome = [match_id,
               result,
               [winner,
                    max(player1_score, player2_score)],
               [loser,
                    min(player1_score, player2_score)],
               match_result,
               p1name,
               p2name]

    # return match results
    return outcome

def run_event(number_of_matches, number_of_rounds, shots_per_round, list_of_players, event_id):
    # run an event with many matches
    # accept number of matches, number of rounds per match, shots per round, player list, and event id number
    # output the event table

    match_log = []

    # run the matches
    for i in range(number_of_matches):
        match_id= i

        # pick 2 random players for the match
        player1 = random.choice(list_of_players)
        while True:
            player2 = random.choice(list_of_players)
            if player2 != player1:
                break

        # get the player skill levels
        player1_skill = player_dict.get(player1)
        player2_skill = player_dict.get(player2)

        # play their match
        outcome = play_match(match_id,
                             number_of_rounds,
                             shots_per_round,
                             player1,
                             player1_skill,
                             player2,
                             player2_skill)

        match_log.append(outcome)

    # organize the match logs into summary tables
    match_df = pd.DataFrame(match_log, columns=["match_id", "Result Type", "Winner", "Loser", "Score", "P1 Name", "P2 Name"])

    match_df[["Winner Name", "Winner Points"]] = match_df["Winner"].apply(pd.Series)
    match_df[["Loser Name", "Loser Points"]] = match_df["Loser"].apply(pd.Series)

    del match_df["Winner"]
    del match_df["Loser"]

    win_counts = match_df["Winner Name"].value_counts().reset_index()
    win_counts.columns = ["Name", "Wins"]

    loss_counts = match_df["Loser Name"].value_counts().reset_index()
    loss_counts.columns = ["Name", "Losses"]

    tie_counts = match_df[["Result Type", "P1 Name", "P2 Name"]]
    tie_counts = tie_counts[tie_counts["Result Type"] == "Tie"]
    tie_counts = pd.concat([tie_counts["P1 Name"], tie_counts["P2 Name"]])
    tie_counts = tie_counts.value_counts().reset_index()
    tie_counts.columns = ["Name", "Ties"]

    event_df = pd.merge(win_counts, loss_counts, on="Name", how="outer")
    event_df = pd.merge(event_df, tie_counts, on="Name", how="outer")
    event_df.drop(event_df[event_df["Name"] == "None"].index, inplace=True)
    event_df.fillna(0,inplace=True)
    event_df[["Wins", "Losses", "Ties"]] = event_df[["Wins", "Losses", "Ties"]].astype(int)
    event_df["Matches"] = event_df[["Wins", "Losses", "Ties"]].sum(axis=1)
    event_df["Win Pct"] = (event_df["Wins"] / (event_df["Wins"] + event_df["Losses"]) * 100).round(1)
    event_df["event_id"] = event_id
    event_df = event_df[["Name", "Matches", "Wins", "Losses", "Ties", "event_id"]]

    return event_df

def run_season(number_of_events):
    season_results = pd.DataFrame()

    for i in range(number_of_events):
        event_result = run_event(18, 3, 3, player_list, i)
        season_results = pd.concat([season_results, event_result], ignore_index=True)

    season_results = season_results.groupby("Name").sum()
    season_results["Win Pct"] = (season_results["Wins"] /
                                 (season_results["Wins"] + season_results["Losses"]) * 100).round(1)
    season_results = season_results.sort_values(by="Wins", ascending=False)
    print(season_results)

run_season(12)