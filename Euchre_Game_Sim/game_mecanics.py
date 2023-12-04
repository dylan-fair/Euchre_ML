import random
import pygame
from load_models import load_card_picker_model, load_card_replace_model, load_trump_picking_model
pygame.init()
WIDTH, HEIGHT = 1000, 700
card_types = ['A', 'K', 'Q', 'J', '10', '9']
card_suits = ['Hearts', 'Spades', 'Clubs', 'Diamonds']

def make_deck():
    deck = []
    for suit in card_suits:
        for card_type in card_types:
            deck.append(f'{suit};{card_type}')
    random.shuffle(deck)
    return deck

def make_hands_and_blind():
    deck = make_deck()
    hands = [[],[], [], []]
    blind = []
    for i in range(20):
        index = i % 4
        hands[index].append(deck.pop(0))
    blind = deck
    return hands, blind
def find_sprint_index(all_cards, card):
    played_card_sprite = None
    for card_sprite in all_cards.sprites():
        if card_sprite.value == card:  
            played_card_sprite = card_sprite
            break
    if played_card_sprite is not None:
        return all_cards.sprites().index(played_card_sprite)
    else:
        print("Played card not found in the sprite group.")
def play_card(hand, position, trump, leading_suit, all_cards, name):
    best_card, hand, best_suit = load_card_picker_model(hand, position, trump, leading_suit)

    print(best_card)
    index = find_sprint_index(all_cards, best_card)
    if type(index )== int:
        if name == 'Player 1':
            all_cards.sprites()[index].rect.x = WIDTH // 2 - 50
            all_cards.sprites()[index].rect.y = HEIGHT // 2 + 75
        if name == 'Player 2':
            all_cards.sprites()[index].rect.x = WIDTH // 2 - 300
            all_cards.sprites()[index].rect.y = HEIGHT // 2
        if name == 'Player 3':
            all_cards.sprites()[index].rect.x = WIDTH // 2 
            all_cards.sprites()[index].rect.y = HEIGHT // 2 - 200
        if name == 'Player 4':
            all_cards.sprites()[index].rect.x = WIDTH // 2 + 225
            all_cards.sprites()[index].rect.y = HEIGHT // 2


    return best_card, hand, best_suit, all_cards

def trump_choice(trump_card, hand):
    if len(trump_card) != 0:
        suit, rank = trump_card.split(';')
        best_trump, value = load_trump_picking_model(hand)
        if best_trump == suit:
            return 1, best_trump
        else:
            return 0, best_trump
    else:
        best_trump, value = load_trump_picking_model(hand)
        if value > .7:
            return 1, best_trump
        else:
            return 0, best_trump
        
def change_dealer_hand(hand, new_card):
    new_hand, best_card_removed, hand = load_card_replace_model(hand, new_card)
    return new_hand