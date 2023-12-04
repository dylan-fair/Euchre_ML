import tensorflow as tf
import pandas as pd
model = tf.keras.models.load_model('Models/card_replacement_model.keras')

def load_model(model,hand, card_removed, new_card):

    data = parse_data_for_model(hand, card_removed, new_card)

    d = {'card1_suit': [data[0]], 'card1_rank': [data[1]],
                'card2_suit': [data[2]], 'card2_rank': [data[3]],
                'card3_suit': [data[4]], 'card3_rank': [data[5]],
                'card4_suit': [data[6]], 'card4_rank': [data[7]],
                'card5_suit': [data[8]], 'card5_rank': [data[9]],
                'card_removed_suit': [data[10]], 'card_removed_rank': [data[11]],
                'new_card_suit': [data[12]], 'new_card_rank': [data[13]]}
    # print(d)
    input_df = pd.DataFrame(data=d)

    prediction = model.predict(input_df)
    return prediction



def parse_data_for_model(hand, card_removed, new_card):
    rank_dict = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'J2' : 10, '10': 9, '9': 8, '0': 0}
    suit_rank = {'Hearts': 1, 'Diamonds': 2, 'Spades': 3, 'Clubs': 4}
    data = []
    for card in hand:
        card = card.split(';')
        data.append(suit_rank[card[0]])
        data.append(rank_dict[card[1]])

    card_removed = card_removed.split(';')
    data.append(suit_rank[card_removed[0]])
    data.append(rank_dict[card_removed[1]])

    new_card = new_card.split(';')
    data.append(suit_rank[new_card[0]])
    data.append(rank_dict[new_card[1]])

    

    return data

hand = ['Spades;10', 'Clubs;10', 'Clubs;9', 'Clubs;Q', 'Spades;J']
position = 1
pos = 3
trump = 'Hearts'
leading_suit = 'Hearts'
suit_list = ['Hearts', 'Spades', 'Diamonds', 'Clubs']
prediction = []
best_number = -1
new_card = 'Diamonds;9'

for cards in hand:
    prediction.append(load_model(model, hand, cards, new_card)[0][0]) 


print(prediction)
print(max(prediction))
print(hand)