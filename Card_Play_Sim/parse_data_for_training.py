import pandas as pd
import ast
df = pd.read_csv('TrainingData/hands_broken_down.csv')
rank_dict = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'J2' : 10, '10': 9, '9': 8, '0': 0}
suit_rank = {'Hearts': 1, 'Diamonds': 2, 'Spades': 3, 'Clubs': 4}

model_df = pd.DataFrame()
# Data needed to train model
card1_suit = []
card1_rank = []
card2_suit = []
card2_rank = []
card3_suit = []
card3_rank = []
card4_suit = []
card4_rank = []
card5_suit = []
card5_rank = []
card_played_suit = []
card_played_rank = []
position = []
trump = []
leading_suit = []
label = []
#Helper data
counter =0

df['hand'] = df['hand'].apply(ast.literal_eval)

for index, row in df.iterrows():
    if counter % 100000 == 0:
        print(counter)
    counter+=1
    card1 = row['hand'][0].split(';')
    card1_suit.append(suit_rank[card1[0]])
    card1_rank.append(rank_dict[card1[1]])
    if len(row['hand']) < 2:
        card2_suit.append(0)
        card2_rank.append(0)
    else:
        card2 = row['hand'][1].split(';')
        card2_suit.append(suit_rank[card2[0]])
        card2_rank.append(rank_dict[card2[1]])
    if len(row['hand']) < 3:
        card3_suit.append(0)
        card3_rank.append(0)
    else:
        card3 = row['hand'][2].split(';')
        card3_suit.append(suit_rank[card3[0]])
        card3_rank.append(rank_dict[card3[1]])
    if len(row['hand']) < 4:
        card4_suit.append(0)
        card4_rank.append(0)
    else:
        card4 = row['hand'][3].split(';')
        card4_suit.append(suit_rank[card4[0]])
        card4_rank.append(rank_dict[card4[1]])
    if len(row['hand']) < 5:
        card5_suit.append(0)
        card5_rank.append(0)
    else:
        card5 = row['hand'][4].split(';')
        card5_suit.append(suit_rank[card5[0]])
        card5_rank.append(rank_dict[card5[1]])
    card_played = row['card_played'].split(';')
    card_played_suit.append(suit_rank[card_played[0]])
    card_played_rank.append(rank_dict[card_played[1]])
    position.append(row['position'])
    trump.append(suit_rank[row['trump']])
    leading_suit.append(suit_rank[row['suit_played_first']])
    if row['didnt_follow_suit'] == 1:
        label.append(-1)
    else:
        label.append(row['won_trick'])

model_df['card1_suit'] = card1_suit
model_df['card1_rank'] = card1_rank
model_df['card2_suit'] = card2_suit
model_df['card2_rank'] = card2_rank
model_df['card3_suit'] = card3_suit
model_df['card3_rank'] = card3_rank
model_df['card4_suit'] = card4_suit
model_df['card4_rank'] = card4_rank
model_df['card5_suit'] = card5_suit
model_df['card5_rank'] = card5_rank
model_df['card_played_suit'] = card_played_suit
model_df['card_played_rank'] = card_played_rank
model_df['position'] = position
model_df['trump'] = trump
model_df['leading_suit'] = leading_suit
model_df['label'] = label


model_df.to_csv(f'TrainingData/final_training_set.csv')