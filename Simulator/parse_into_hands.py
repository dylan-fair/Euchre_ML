import pandas as pd
import ast
df = pd.read_csv('TrainingData/euchre_all_hands.csv')

model_df = pd.DataFrame()

current_hand = []
card_played = []
win_trick = []
trump = []
position = []
suit_played = []
not_follow_suit = [] # 1 if we did 0 if we didnt.

tuple_columns = ['hand', 'best_order', 'trick_wons', 'suits_delt']  # Replace 'column1', 'column2', ... with the actual column names

# Convert string representations to actual tuples
for column in tuple_columns:
    df[column] = df[column].apply(ast.literal_eval)

def not_follow_suit_finder(suit_delt, hand, card_played):
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
    if count % 10000 == 0:
        print(count)
    count+=1
    for i in range(5):
        current_hand.append(list(row['hand'])[i:5])
        card_played.append(list(row['best_order'])[i])
        win_trick.append(row['trick_wons'][i])
        trump.append(row['trump'])
        position.append(row['position'])
        suit_played.append(row['suits_delt'][i])
        broke_rules = not_follow_suit_finder(row['suits_delt'][i], list(row['best_order'])[i+1:5], list(row['best_order'])[i])
        not_follow_suit.append(int(broke_rules))

model_df['hand'] = current_hand
model_df['card_played'] = card_played
model_df['won_trick'] = win_trick
model_df['trump'] = trump
model_df['position'] = position
model_df['suit_played_first'] = suit_played
model_df['didnt_follow_suit'] = not_follow_suit


model_df.to_csv(f'TrainingData/hands_broken_down.csv')