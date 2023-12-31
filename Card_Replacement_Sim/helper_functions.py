import random

card_types = ['A', 'K', 'Q', 'J', '10', '9']
card_suits = ['Hearts', 'Spades', 'Clubs', 'Diamonds']
trump_rank = {'J': 1, 'A': 3, 'K': 4, 'Q': 5, '10': 6, '9': 7}
regular_rank = {'A': 8, 'K': 9, 'Q': 10, 'J': 11, '10': 12, '9': 13}
#Euchre only uses the cards Ace - 9, and the suit matters because of what is trump
def make_deck():
    deck = []
    for suit in card_suits:
        for type in card_types:
            deck.append(f'{suit};{type}')
    return deck 

def is_trump(card, trump):
    card_split = card.split(';')
    if card_split[0] == trump:
        return True
    else:
        if trump == 'Hearts' and card == 'Diamonds;J':
            return True
        elif trump == 'Diamonds' and card == 'Hearts;J':
            return True
        elif trump == 'Clubs' and card == 'Spades;J':
            return True
        elif trump == 'Spades' and card == 'Clubs;J':
            return True
        else:
            return False
#This will rank all the cards based on the current trump card and what was delt
def get_card_ranks(trump, delt_suit):
    deck = make_deck()
    rank_dict = {}
    for cards in deck:
        card = cards.split(';')
        if is_trump(cards, trump):
            #This would be if it was the little brother or the jack of the same color as trump
            if card[0] != trump:
                rank_dict[cards] = trump_rank[card[1]] + 1
            else: 
                rank_dict[cards] = trump_rank[card[1]]
        else:
            if card[0] != delt_suit:
                rank_dict[cards] = regular_rank[card[1]] + 10
            else:
                rank_dict[cards] = regular_rank[card[1]]
    return rank_dict

# A hand will be a dictionary where the key is the player number and the value is their card.
#We will assume for opur sake player 1 started the hand, trump is what suit is currently trump
def win_trick(hand, trump, pos):
    #Keep track of the winning card to return the winning player at the end
    # Set this card to the first players card to see if anyone beats it.
    counter = 0
    winning_player = list(hand.keys())[pos]
    winner_card = hand[winning_player]
    delt_suit = winner_card.split(';')[0]
    rank = get_card_ranks(trump,delt_suit)
    for card in hand.values():
        if card == winner_card:
            pass
        else:
            if rank[card] < rank[winner_card]:
                winner_card = card
                winning_player = list(hand.keys())[counter]
        counter +=1 
    return winning_player, delt_suit

def is_bower(card, trump):
    if trump == 'Hearts' and card == 'Diamonds;J':
        return True
    elif trump == 'Diamonds' and card == 'Hearts;J':
        return True
    elif trump == 'Clubs' and card == 'Spades;J':
        return True
    elif trump == 'Spades' and card == 'Clubs;J':
        return True
    else:
        return False
    
def not_follow_suit_finder(suit_delt, hand, card_played, trump):
    broke_rules = False
    if trump == 'Hearts' and card_played == 'Diamonds;J' and suit_delt == 'Hearts':
        return broke_rules
    if trump == 'Dimaonds' and card_played == 'Hearts;J' and suit_delt == 'Diamonds':
        return broke_rules
    if trump == 'Clubs' and card_played == 'Spades;J' and suit_delt == 'Clubs':
        return broke_rules
    if trump == 'Spades' and card_played == 'Clubs;J' and suit_delt == 'Spades':
        return broke_rules

    if card_played.split(';')[0] == suit_delt:
        return False
    for cards in hand:
        suit = cards.split(';')[0]
        if suit == suit_delt:
            broke_rules = True
    return broke_rules
