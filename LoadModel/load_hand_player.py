import tensorflow as tf
import pandas as pd
model = tf.keras.models.load_model('Models/card_choice_model.keras')
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

def load_model(model,hand, card_played, position, trump, leading_suit):

    data = parse_data_for_model(hand, card_played, position, trump, leading_suit)

    d = {'card1_suit': [data[0]], 'card1_rank': [data[1]],
                'card2_suit': [data[2]], 'card2_rank': [data[3]],
                'card3_suit': [data[4]], 'card3_rank': [data[5]],
                'card4_suit': [data[6]], 'card4_rank': [data[7]],
                'card5_suit': [data[8]], 'card5_rank': [data[9]],
                'card_played_suit' : [data[10]], 'card_played_rank': [data[11]],
                'position': [data[12]], 'trump': [data[13]], 'leading_suit': [data[14]]}
    # print(d)
    input_df = pd.DataFrame(data=d)

    prediction = model.predict(input_df)
    return prediction



def parse_data_for_model(hand, card_played, position, trump, leading_suit):
    rank_dict = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'J2' : 10, '10': 9, '9': 8, '0': 0}
    suit_rank = {'Hearts': 1, 'Diamonds': 2, 'Spades': 3, 'Clubs': 4}
    data = []
    hand = convert_bower(hand, trump)
    card_played = convert_bower([card_played], trump)[0]
    for card in hand:
        if len(card) == 1:
            data.append(0)
            data.append(0)
        else:
            card = card.split(';')
            data.append(suit_rank[card[0]])
            data.append(rank_dict[card[1]])
    if len(card_played) == 1:
        data.append(0)
        data.append(0)
    else:
        card_played = card_played.split(';')
        data.append(suit_rank[card_played[0]])
        data.append(rank_dict[card_played[1]])
    data.append(position)
    data.append(suit_rank[trump])
    data.append(suit_rank[leading_suit])
    return data

hand = ['Spades;A', 'Clubs;J', '0', 'Diamonds;J', 'Spades;J']
# hand = sorted(hand, key=lambda x: (x == '0', x))
position = 1
pos = 3
trump = 'Hearts'
leading_suit = 'Hearts'
suit_list = ['Hearts', 'Spades', 'Diamonds', 'Clubs']
prediction = []
best_card = ''
best_suit = ''
best_number = -1
card_list = []
# for suit in suit_list:
#     for card_played in hand:
#         predict = load_model(model, hand, card_played, position, trump, suit)[0][0]
#         if predict > best_number:
#             best_card = card_played
#             best_number = predict
#             best_suit = suit

for cards in hand:
    prediction.append(load_model(model, hand, cards, pos, trump, leading_suit)[0][0])
    card_list.append(cards)

print(best_card)
print(best_suit)

print(prediction)
print(max(prediction))
print(card_list)