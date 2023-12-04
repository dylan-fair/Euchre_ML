from itertools import permutations, combinations
import pandas as pd
import random
import ast

from helper_functions import win_trick

card_types = ['A', 'K', 'Q', 'J', '10', '9']
card_suits = ['Hearts', 'Spades', 'Clubs', 'Diamonds']
pos_dict ={0: 1, 1:4, 2:3, 3:2}
model_df = pd.DataFrame()
df = pd.read_csv('TrainingData/best_hand_orders.csv')
list_columns = ['hand', 'best_order', 'trick_wons']  # Replace 'column1', 'column2', ... with the actual column names

# Convert string representations to actual tuples
for column in list_columns:
    df[column] = df[column].apply(ast.literal_eval)

def make_deck():
    deck = []
    for suit in card_suits:
        for card_type in card_types:
            deck.append(f'{suit};{card_type}')
    return deck

def remaining_cards(deck, hand):
    return [card for card in deck if card not in hand]

hand_list = []
new_card = []
card_removed = []
label = []
counter = 0
for index, row in df.iterrows():
    if row['position'] == 1 and row['trump'] == 'Hearts':
        if counter % 10000 == 0:
            print(counter)
        counter +=1
        hand = row['hand']
        order = row['best_order']
        for i in range(5):
            remaining_deck = remaining_cards(make_deck(), hand)
            random.shuffle(remaining_deck)
            
            # Select the remaining hands
            hand2 = remaining_deck[:5]
            hand3 = remaining_deck[5:10]
            hand4 = remaining_deck[10:15]
            trump_card = remaining_deck[15]
            trump = trump_card.split(';')[0]
            hand_list.append(hand)
            new_card.append(trump_card)
            card_removed.append(hand[i])
            inde = order.index(hand[i])
            order[inde] = trump_card
            tricks_won = 0
            for j in range(5):
                current_hand = {'player1': order[j], 'player2': hand2[j], 'player3': hand3[j], 'player4': hand4[j]}
                winner, delt_suit = win_trick(current_hand, trump, 1)
                if winner == 'player1':
                    tricks_won +=1
            if sum(row['trick_wons']) <= tricks_won:
                label.append(1)
            else:
                label.append(0)

model_df['hand'] = hand_list
model_df['card_removed'] = card_removed
model_df['new_card'] = new_card
model_df['label'] = label

model_df.to_csv(f'TrainingData/card_replacement_data.csv')