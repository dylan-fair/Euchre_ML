import tensorflow as tf
import pandas as pd

trump_model = tf.keras.models.load_model('Models/trump_pick_model.keras')
card_model = tf.keras.models.load_model('Models/card_choice_model.keras')
replacement_model = tf.keras.models.load_model('Models/card_replacement_model.keras')

suit_list = ['Hearts', 'Spades', 'Diamonds', 'Clubs']

def load_card_picker_model(hand, position, trump, leading_suit):
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

    new_hand = []
    best_card = ''
    best_suit = ''
    max_value = -1
    if position == 1:
        for leading_suits in suit_list:
            for i, cards in enumerate(hand):
                value = load_model(card_model, hand, cards, position, trump, leading_suits)
                if value > max_value:
                    best_card = cards
                    best_suit = convert_bower([best_card], trump)[0].split(';')[0]
                    max_value = value

    else:
        for cards in hand:
            value = (load_model(card_model, hand, cards, position, trump, leading_suit))
            if value > max_value and len(cards) > 1:
                    best_card = cards
                    best_suit = leading_suit
                    max_value = value
    card_index = hand.index(best_card)
        #returns card to play and the new players hand and leading suit
    hand.remove(best_card)
    hand.append('0')
    return best_card, hand, best_suit

def load_trump_picking_model(hand, ):
    def load_model(model,hand, trump):

        data = parse_data_for_model(hand,trump)

        d = {'card1_suit': [data[0]], 'card1_rank': [data[1]],
                    'card2_suit': [data[2]], 'card2_rank': [data[3]],
                    'card3_suit': [data[4]], 'card3_rank': [data[5]],
                    'card4_suit': [data[6]], 'card4_rank': [data[7]],
                    'card5_suit': [data[8]], 'card5_rank': [data[9]], 'trump': [data[10]]}
        # print(d)
        input_df = pd.DataFrame(data=d)

        prediction = model.predict(input_df)
        return prediction



    def parse_data_for_model(hand, trump):
        rank_dict = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'J2' : 10, '10': 9, '9': 8, '0': 0}
        suit_rank = {'Hearts': 1, 'Diamonds': 2, 'Spades': 3, 'Clubs': 4}
        data = []
        for card in hand:
            card = card.split(';')
            data.append(suit_rank[card[0]])
            data.append(rank_dict[card[1]])
        data.append(suit_rank[trump])
        return data
    max_value = -1
    best_trump = ''
    for trump_suit in suit_list:
        value = load_model(trump_model, hand, trump_suit)
        if value > max_value:
            best_trump = trump_suit
            max_value = value
    #This will return the best trump suit and the value associated so we can determine
    #a threshold to say the hand is good enough
    return best_trump, max_value[0][0]

def load_card_replace_model(hand, new_card):
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
    
    best_card_removed = ''
    max_value = -1
    index = 0
    for i, card_removed in enumerate(hand):
        value = load_model(replacement_model,hand, card_removed, new_card)
        if value > max_value:
            best_card_removed = card_removed
            index = i
            max_value = value
    #This will return the new hand, and the best card to remove, and the old hand
    new_hand = hand.copy()
    new_hand[index] = new_card
    return new_hand, best_card_removed, hand
