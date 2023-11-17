import pandas as pd
import ast

rank_dict = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, '10': 10, '9': 9, '0': 0}
suit_rank = {'Hearts': 1, 'Diamonds': 2, 'Spades': 3, 'Clubs': 4}

df = pd.read_csv('TrainingData/card_choice_training_set.csv')

model_df = pd.DataFrame()


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
trump = []
positon = []
suit_played_first = []
label = []
counter = 0


for index, row in df.iterrows():
    if counter % 50000 == 0:
        print(counter)
    counter+=1

    suit, rank = row['card1'].split(';')
    card1_suit.append(suit_rank[suit])
    card1_rank.append(rank_dict[rank])
    if len(row['card2']) == 1:
        card2_suit.append(0)
        card2_rank.append(0)
    else:
        suit, rank = row['card2'].split(';')
        card2_suit.append(suit_rank[suit])
        card2_rank.append(rank_dict[rank])
    if len(row['card3']) == 1:
        card3_suit.append(0)
        card3_rank.append(0)
    else:
        suit, rank = row['card3'].split(';')
        card3_suit.append(suit_rank[suit])
        card3_rank.append(rank_dict[rank])
    if len(row['card4']) == 1:
        card4_suit.append(0)
        card4_rank.append(0)
    else:
        suit, rank = row['card4'].split(';')
        card4_suit.append(suit_rank[suit])
        card4_rank.append(rank_dict[rank])
    if len(row['card5']) == 1:
        card5_suit.append(0)
        card5_rank.append(0)
    else:
        suit, rank = row['card5'].split(';')
        card5_suit.append(suit_rank[suit])
        card5_rank.append(rank_dict[rank])
    suit, rank = row['card_played'].split(';')
    card_played_suit.append(suit_rank[suit])
    card_played_rank.append(rank_dict[rank])
    positon.append(row['position'])
    trump.append(suit_rank[row['trump']])
    suit_played_first.append(suit_rank[row['suit_played_first']])
    label.append(row['label'])


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
model_df['position'] = positon
model_df['trump'] = trump
model_df['leading_suit'] = suit_played_first
model_df['label'] = label


model_df.to_csv(f'TrainingData/final_training_set.csv')