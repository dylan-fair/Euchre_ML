import pandas as pd
import ast
import random

df = pd.read_csv('TrainingData/best_hand_orders.csv')
rank_dict = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'J2' : 10, '10': 9, '9': 8, '0': 0}
suit_rank = {'Hearts': 1, 'Diamonds': 2, 'Spades': 3, 'Clubs': 4}
card1_rank = []
card1_suit = []
card2_rank = []
card2_suit = []
card3_rank = []
card3_suit = []
card4_rank = []
card4_suit = []
card5_rank = []
card5_suit = []
trump = []
label = []

list_columns = ['hand','trick_wons']  # Replace 'column1', 'column2', ... with the actual column names

# Convert string representations to actual tuples
for column in list_columns:
    df[column] = df[column].apply(ast.literal_eval)


counter = 0
for index, row in df.iterrows():
    if counter % 10000 == 0:
        print(counter)
    counter +=1
    tricks_won = sum(row['trick_wons'])
    cards = []
    hand = row['hand']
    random.shuffle(hand)
    for card in hand:
        cards.append(card.split(';'))

    card1_suit.append(suit_rank[cards[0][0]])
    card1_rank.append(rank_dict[cards[0][1]])

    card2_suit.append(suit_rank[cards[1][0]])
    card2_rank.append(rank_dict[cards[1][1]])

    card3_suit.append(suit_rank[cards[2][0]])
    card3_rank.append(rank_dict[cards[2][1]])

    card4_suit.append(suit_rank[cards[3][0]])
    card4_rank.append(rank_dict[cards[3][1]])

    card5_suit.append(suit_rank[cards[4][0]])
    card5_rank.append(rank_dict[cards[4][1]])
    trump.append(suit_rank[row['trump']])
    if tricks_won < 3:
        label.append(0)
    else:
        label.append(1)

model_df = pd.DataFrame()
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
model_df['trump'] = trump
model_df['label'] = label

model_df.to_csv(f'TrainingData/trump_choice_training_data.csv')