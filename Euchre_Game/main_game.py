import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 700
FPS = 30
card_width, card_height = 71, 96

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Card values and suits
VALUES = ['A', '9', '10', 'J', 'Q', 'K']
SUITS = ['Spades', 'Hearts', 'Clubs', 'Diamonds']

class Card(pygame.sprite.Sprite):
    def __init__(self, image, value, suit):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.value = value
        self.suit = suit
class PlayerLabel(pygame.sprite.Sprite):
    def __init__(self, text, x, y):
        super().__init__()
        self.font = pygame.font.Font(None, 36)
        self.image = self.font.render(text, True, BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Function to create a deck
def create_deck():
    return [(value, suit) for value in VALUES for suit in SUITS]

# Function to shuffle the deck
def shuffle_deck(deck):
    random.shuffle(deck)

def load_card_images():
    sprite_sheet = pygame.image.load("Euchre_Game/card_sheet.png")  # Set the width and height of each card in pixels
    base_dist = 568
    card_images = {}
    ace = VALUES.pop(0)

    for i, suit in enumerate(SUITS):
        x = 0
        y = i * card_height
        card_rect = pygame.Rect(x, y, card_width, card_height)
        card_image = sprite_sheet.subsurface(card_rect)
        card_images[(ace, suit)] = card_image

    for i, suit in enumerate(SUITS):
        for j, value in enumerate(VALUES):
                x = (j * card_width) + base_dist
                y = i * card_height
                card_rect = pygame.Rect(x, y, card_width, card_height)
                card_image = sprite_sheet.subsurface(card_rect)
                card_images[(value, suit)] = card_image

    return card_images
def draw_cards(screen, all_cards, player_labels, trump_card, card_images):

    # Draw cards on the screen
    all_cards.draw(screen)

    # Draw player labels
    for label in player_labels:
        screen.blit(label.image, label.rect)

    # Draw trump card in the center
    trump_card_image = card_images[trump_card]
    trump_card_rect = trump_card_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(trump_card_image, trump_card_rect)

    # Update the display
    pygame.display.flip()



# Function to deal cards to players
def deal_cards(deck):
    hands = [[], [], [], []]
    for i in range(5):
        for j in range(4):
            hands[j].append(deck.pop(0))
    return hands, deck

def game():
    # Create and shuffle the deck
    deck = create_deck()
    shuffle_deck(deck)

    # Deal cards to players
    hands, deck = deal_cards(deck)

    # Initialize Pygame screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Euchre")

    clock = pygame.time.Clock()

    card_images = load_card_images()

    # Create a sprite group to hold the cards
    all_cards = pygame.sprite.Group()

    # Create Card objects for each card and add them to the sprite group
    for i in range(5):
        for j in range(4):
            card = hands[j][i]
            card_image = card_images[card]
            card_sprite = Card(card_image, card[0], card[1])

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


    player_labels = [
    PlayerLabel("Player 1 (Dealer)", WIDTH // 2 - 50, HEIGHT - 30),
    PlayerLabel("Player 2", 10, HEIGHT // 2 - 100),
    PlayerLabel("Player 3", WIDTH // 2 - 50, 10),
    PlayerLabel("Player 4", WIDTH - 100, HEIGHT // 2 - 100)
    ]


    # Reveal the trump card
    trump_card = deck.pop(0)
    print(f"Trump card is: {trump_card[0]} of {trump_card[1]}")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Drawing code goes here
        screen.fill((0, 143, 0))

        # Draw cards on the screen
        draw_cards(screen, all_cards, player_labels, trump_card, card_images)

        # Draw player labels
        for label in player_labels:
            screen.blit(label.image, label.rect)

        # Draw trump card in the center
        trump_card_image = card_images[trump_card]
        trump_card_rect = trump_card_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(trump_card_image, trump_card_rect)

        # Update the display
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game()