import pygame
from classes import Card
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

def load_card_images():
    card_width, card_height = 71, 96
    VALUES = ['A', '9', '10', 'J', 'Q', 'K']
    SUITS = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
    sprite_sheet = pygame.image.load("Euchre_Game_Sim/card_sheet.png")
    base_dist = 568
    card_images = {}
    ace = VALUES.pop(0)

    for i, suit in enumerate(SUITS):
        x = 0
        y = i * card_height
        card_rect = pygame.Rect(x, y, card_width, card_height)
        card_image = sprite_sheet.subsurface(card_rect)
        card_images[f'{suit};{ace}'] = card_image

    for i, suit in enumerate(SUITS):
        for j, value in enumerate(VALUES):
                x = (j * card_width) + base_dist
                y = i * card_height
                card_rect = pygame.Rect(x, y, card_width, card_height)
                card_image = sprite_sheet.subsurface(card_rect)
                card_images[f'{suit};{value}'] = card_image
    return card_images

def group_card_images( hands,):
    card_images = load_card_images()
    WIDTH, HEIGHT = 1000, 700
        # Create a sprite group to hold the cards
    all_cards = pygame.sprite.Group()

    # Create Card objects for each card and add them to the sprite group
    for j in range(4):
        for i in range(len(hands[j])):
            card = hands[j][i]
            if len(card) == 1:
                pass
            else:
                card_image = card_images[card]
                card_sprite = Card(card_image,card)

                # Adjust the card positions based on the player
                if j == 0:  # Player 1
                    card_sprite.rect.x = WIDTH // 2 - 75 + i * 30
                    card_sprite.rect.y = HEIGHT - 160
                elif j == 1:  # Player 2
                    card_sprite.rect.x = 50
                    card_sprite.rect.y = HEIGHT // 2 - 50 + i * 30
                elif j == 2:  # Player 3
                    card_sprite.rect.x = WIDTH // 2 - 75 + i * 30
                    card_sprite.rect.y = 50
                elif j == 3:  # Player 4
                    card_sprite.rect.x = WIDTH - 150
                    card_sprite.rect.y = HEIGHT // 2 - 50 + i * 30

                all_cards.add(card_sprite)
    return all_cards