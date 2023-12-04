import pandas as pd
import ast
import random
df = pd.read_csv('TrainingData/card_replacement_data.csv')
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
card_removed_suit = []
card_removed_rank = []
new_card_suit = []
new_card_rank = []
label = []
#Helper data
counter =0

df['hand'] = df['hand'].apply(ast.literal_eval)

for index, row in df.iterrows():
    if counter % 100000 == 0:
        print(counter)
    counter+=1
    hand = row['hand']  
    random.shuffle(hand)

    card1 = hand[0].split(';')
    card1_suit.append(suit_rank[card1[0]])
    card1_rank.append(rank_dict[card1[1]])

    card2 = hand[1].split(';')
    card2_suit.append(suit_rank[card2[0]])
    card2_rank.append(rank_dict[card2[1]])

    card3 = hand[2].split(';')
    card3_suit.append(suit_rank[card3[0]])
    card3_rank.append(rank_dict[card3[1]])

    card4 = hand[3].split(';')
    card4_suit.append(suit_rank[card4[0]])
    card4_rank.append(rank_dict[card4[1]])

    card5 = hand[4].split(';')
    card5_suit.append(suit_rank[card5[0]])
    card5_rank.append(rank_dict[card5[1]])

    card_removed = row['card_removed'].split(';')
    card_removed_suit.append(suit_rank[card_removed[0]])
    card_removed_rank.append(rank_dict[card_removed[1]])
    new_card = row['new_card'].split(';')
    new_card_suit.append(suit_rank[new_card[0]])
    new_card_rank.append(rank_dict[new_card[1]])
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
model_df['card_removed_suit'] = card_removed_suit
model_df['card_removed_rank'] = card_removed_rank
model_df['new_card_suit'] = new_card_suit
model_df['new_card_rank'] = new_card_rank
model_df['label'] = label


model_df.to_csv(f'TrainingData/card_replacement_training_data.csv')