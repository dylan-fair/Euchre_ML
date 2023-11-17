import tensorflow as tf
import pandas as pd
model = tf.keras.models.load_model('card_choice_model.keras')

def load_model(model,hand, card_played, position, trump, leading_suit):

    data = parse_data_for_model(hand, card_played, position, trump, leading_suit)


    d = {'card1_suit': [data[0]],'card1_rank': [data[1]],'card2_suit': [data[2]],
                    'card2_rank': [data[3]],'card3_suit': [data[4]],'card3_rank': [data[5]],
                    'card4_suit': [data[6]],'card4_rank': [data[7]],'card5_suit': [data[8]],
                    'card5_rank': [data[9]],'card_played_suit': [data[10]],
                    'card_played_rank': [data[11]],'position': [data[12]],'trump': [data[13]],
                    'leading_suit': [data[14]]}
    input_df = pd.DataFrame(data=d)

    prediction = model.predict(input_df)
    return prediction



def parse_data_for_model(hand, card_played, position, trump, leading_suit):
    rank_dict = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, '10': 10, '9': 9, '0': 0}
    suit_rank = {'Hearts': 1, 'Diamonds': 2, 'Spades': 3, 'Clubs': 4}
    data = []

    for card in hand:
        if len(card) == 1:
            data.append(0)
            data.append(0)
        else:
            suit, rank = card.split(';')
            data.append(suit_rank[suit])
            data.append(rank_dict[rank])
    if len(card_played) == 1:
        data.append(0)
        data.append(0)
    else:
        suit, rank = card_played.split(';')
    data.append(suit_rank[suit])
    data.append(rank_dict[rank])
    data.append(position)
    data.append(suit_rank[trump])
    data.append(suit_rank[leading_suit])
    return data

hand = ['Hearts;J', '0', 'Clubs;A', 'Hearts;A', '0']
position = 1
trump = 'Hearts'
leading_suit = 'Spades'
suit_list = ['Hearts', 'Spades', 'Diamonds', 'Clubs']
results = []
for suits in suit_list:
    for cards in hand:
        results.append(load_model(model, hand, cards, position, trump, suits))
        results.append(f'{suits},{cards}')
    
print(results)