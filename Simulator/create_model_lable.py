import pandas as pd
import ast

df = pd.read_csv('TrainingData/hands_broken_down.csv')

model_df = pd.DataFrame()

card1 = []
card2 = []
card3 = []
card4 = []
card5 = []
trump = []
position = []
suit_first = []
card_played = []
lable = []

count = 0

df['hand'] = df['hand'].apply(ast.literal_eval)

def separate_card(hand):
    cards = []
    for i in range(5):
        if i < len(hand):
            cards.append(hand[i])
        else:
            cards.append('0')
    return cards

for index, row in df.iterrows():
    if count % 100000 == 0:
        print(count)
    count+=1
    new_hand = separate_card(row['hand'])
    card1.append(new_hand[0])
    card2.append(new_hand[1])
    card3.append(new_hand[2])
    card4.append(new_hand[3])
    card5.append(new_hand[4])

    trump.append(row['trump'])
    position.append(row['position'])
    suit_first.append(row['suit_played_first'])
    card_played.append(row['card_played'])

    if row['didnt_follow_suit'] == 1:
        lable.append(-1)
    else:
        lable.append(row['won_trick'])

model_df['card1'] = card1
model_df['card2'] = card2
model_df['card3'] = card3
model_df['card4'] = card4
model_df['card5'] = card5
model_df['card_played'] = card_played
model_df['trump'] = trump
model_df['position'] = position
model_df['suit_played_first'] = suit_first
model_df['label'] = lable

model_df.to_csv(f'TrainingData/card_choice_training_set.csv')
