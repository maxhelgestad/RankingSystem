#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 09:11:49 2020

@author: maxhelgestad
"""
import numpy as np
import csv

filename = "mcb2019CSV.csv"
with open(filename) as file:
    reader = csv.reader(file)    
    winners = []
    losers = []
    scoreDifference = []
    totalGames = 0
    for row in reader:
        winners.append(row[1])
        scoreDifference.append(int(row[2]) - int(row[4]))
        losers.append(row[3])
        totalGames += 1

#Strip the beginning '@' from the team if it is present
for i in range(len(winners)):
    if winners[i].startswith('@'):
        winners[i] = winners[i].strip('@')
for i in range(len(losers)):
    if losers[i].startswith('@'):
        losers[i] = losers[i].strip('@')
       
#Create an array of all distinct teams
distinctTeams = []
for i in range(len(winners)):
    if winners[i] not in distinctTeams:
        distinctTeams.append(winners[i])
for i in range(len(losers)):
    if losers[i] not in distinctTeams:
        distinctTeams.append(losers[i])
        
#create a matrix for winner and loser of each game
#strength of win/loss
X = np.zeros((totalGames, len(distinctTeams)))
for i in range(totalGames):
    winner = winners[i]
    loser = losers[i]
    dif = scoreDifference[i]
    if dif > 30:
        X[i][distinctTeams.index(winner)] = 1.4
        X[i][distinctTeams.index(loser)] = -1.4
    elif dif > 15:
        X[i][distinctTeams.index(winner)] = 1.2
        X[i][distinctTeams.index(loser)] = -1.2
    else:
        X[i][distinctTeams.index(winner)] = 1
        X[i][distinctTeams.index(loser)] = -1
#create matrix for score differences of each game    
y = np.matrix(scoreDifference).transpose()

#Begin to solve
Xt = X.transpose()
M = np.matmul(Xt, X)
p = np.matmul(Xt, y)

#set bottom row to all 1's
for i in range(len(distinctTeams)):
    M[len(distinctTeams) - 1][i] = 1
#set last entry to zero
p[len(distinctTeams) - 1][0] = 0
#solve for final ratings matrix and convert to list
Mi = np.linalg.inv(M)
r = np.matmul(Mi, p).tolist()

#create ratings dictionary to hold each team's rating
ratings = {}
for i in range(len(distinctTeams)):
    ratings[r[i][0]] = distinctTeams[i]

#print top 25
count = 1
for key, value in reversed(sorted(ratings.items())):
    if count > 25:
        break
    else:
        print(f"\n{count}. {value} | Rating: {key}")
        count += 1

    



