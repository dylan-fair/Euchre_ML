import pandas as pd
import ast
import random
df = pd.read_csv('TrainingData/best_hand_orders.csv')

model_df = pd.DataFrame()

current_hand = []
card_played = []
win_trick = []
trump = []
position = []
suit_played = []
not_follow_suit = [] # 1 if we did 0 if we didnt.

list_columns = ['hand', 'best_order', 'trick_wons', 'suits_delt']  # Replace 'column1', 'column2', ... with the actual column names

# Convert string representations to actual tuples
for column in list_columns:
    df[column] = df[column].apply(ast.literal_eval)

def convert_bower(hand, trump):
    new_hand = []
    for cards in hand:
        if trump == 'Hearts' and cards == 'Diamonds;J':
            new_hand.append('Hearts;J2')
        elif trump == 'Diamonds' and cards == 'Hearts;J':
            new_hand.append('Diamonds;J2')
        elif trump == 'Clubs' and cards == 'Spades;J':
            new_hand.append('Clubs;J2')
        elif trump == 'Spades' and cards == 'Clubs;J':
            new_hand.append('Spades;J2')
        else:
            new_hand.append(cards)
    return new_hand


def not_follow_suit_finder(suit_delt, hand, card_played, trump):
    broke_rules = False

    if card_played.split(';')[0] == suit_delt:
        return False
    for cards in hand:
        suit = cards.split(';')[0]
        if suit == suit_delt:
            broke_rules = True
    return broke_rules

count = 0
for index, row in df.iterrows():
    hand = convert_bower(row['hand'], row['trump'])
    best_order = convert_bower(row['best_order'], row['trump'])
    if count % 10000 == 0:
        print(count)
    count+=1
    for i in range(5):
        current_hand.append(hand.copy())
        current_card = best_order[i]
        hand.remove(current_card)
        card_played.append(current_card)
        win_trick.append(row['trick_wons'][i])
        trump.append(row['trump'])
        position.append(row['position'])
        if row['position'] == 1:
            card_split = current_card.split(';')
            suit_played.append(card_split[0])
            suit_play = card_split[0]
        else:     
            suit_played.append(row['suits_delt'][i])
            suit_play = row['suits_delt'][i]
        broke_rules = not_follow_suit_finder(suit_play, hand.copy(), current_card, row['trump'])
        not_follow_suit.append(int(broke_rules))

model_df['hand'] = current_hand
model_df['card_played'] = card_played
model_df['won_trick'] = win_trick
model_df['trump'] = trump
model_df['position'] = position
model_df['suit_played_first'] = suit_played
model_df['didnt_follow_suit'] = not_follow_suit


model_df.to_csv(f'TrainingData/hands_broken_down.csv')