'''
    Here is how the data will be stored
    dict {(position[0], trump[1], Unique_hand[2:]): [best hand [0], number of tricks it won[1]]}
    then each row will recieve the trump card, put into a csv file
'''

from win_trick import win_trick
from itertools import permutations, combinations

import numpy as np
import pandas as pd
import random

card_types = ['A', 'K', 'Q', 'J', '10', '9']
card_suits = ['Hearts', 'Spades', 'Clubs', 'Diamonds']
pos_dict ={0: 1, 1:4, 2:3, 3:2}
model_df = pd.DataFrame()

def make_deck():
    deck = []
    for suit in card_suits:
        for card_type in card_types:
            deck.append(f'{suit};{card_type}')
    return deck

def make_unique_hands():
    all_unique_hands = list(combinations(make_deck(), 5))
    sorted_hands = [tuple(sorted(hand)) for hand in all_unique_hands]
    final_list = []
    for hands in sorted_hands:
        for i in range(4):
            for j in range(4):  
                value = (j, card_suits[i],) + hands
                final_list.append(value)
    dict_of_hands = dict(zip(final_list, [[0, [], 0]] * len(final_list)))
    return dict_of_hands

unique_hands = make_unique_hands()
print(len(unique_hands))

def remaining_cards(deck, hand):
    return [card for card in deck if card not in hand]

def check_unique_hands():
    count = 0
    non_zero_count = 0
    for values in unique_hands.values():
        if values[1] >= 2:
            count +=1
        if values[1] != 0:
            non_zero_count +=1
    print(f'finished numbers = {count}')
    print(f'Hands with non zero tricks {non_zero_count}')
    return count == len(unique_hands)
count = 0

for hands in unique_hands.keys():
    if count %100 ==0:
        print(count)
        # check_unique_hands()
    count += 1
    # Iterate through all permutations of the current hand to find the best order
    trump = hands[1]
    pos = int(hands[0])
    hand = hands[2:]
    for hand1 in permutations(hand):
        remaining_deck = remaining_cards(make_deck(), hand1)
        random.shuffle(remaining_deck)
        
        # Select the remaining hands
        hand2 = remaining_deck[:5]
        hand3 = remaining_deck[5:10]
        hand4 = remaining_deck[10:15]
        # Simulate the game and count tricks won
        tricks_won= [0,0,0,0,0]
        suits_delt = []
        for j in range(5):
            current_hand = {'player1': hand1[j], 'player2': hand2[j], 'player3': hand3[j], 'player4': hand4[j]}
            winner, delt_suit = win_trick(current_hand, trump, pos)
            suits_delt.append(delt_suit)
            if winner == 'player1':
                tricks_won[j] = 1
        best_trick1 = unique_hands[hands][1]
        # Update best performance for the current order
        if sum(tricks_won) >= sum(best_trick1):
            best_performance = tricks_won
            best_order = hand1
            unique_hands[hands] = [best_order, best_performance, suits_delt]
            if sum(tricks_won) >= 3:
                break
hand = []
best_hand = []
tricks_won = []
trump = []
position = []
suits_delt_list = []
for values in unique_hands.values():
    best_hand.append(values[0])
    tricks_won.append(values[1])
    suits_delt_list.append(values[2])
for keys in unique_hands.keys():
    key = list(keys)
    trump.append(key[1])
    position.append(pos_dict[key[0]])
    hand.append(tuple(key[2:]))

model_df['hand'] = hand
model_df['trump'] = trump
model_df['best_order'] = best_hand
model_df['trick_wons'] = tricks_won
model_df['position'] = position
model_df['suits_delt'] = suits_delt_list

model_df.to_csv(f'TrainingData/euchre_all_hands.csv')
