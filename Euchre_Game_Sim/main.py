import pygame
from classes import PlayerLabel, Score
import sys

from game_mecanics import make_hands_and_blind, play_card, trump_choice, change_dealer_hand
from euchre_helper_functions import load_card_images, win_trick, group_card_images
pygame.init()
WIDTH, HEIGHT = 1000, 700
FPS = 30
def change_play_order(player_list, winner, team_labels,  team_1_points, team_2_points):
    used_list = player_list.copy()
    used_label = team_labels.copy()
    team_1 = team_1_points
    team_2 = team_2_points
    if winner == 'Player 1':
        order_list = [1, 2, 3, 4]
        team_1 +=1
        used_label[0].setPoints(team_1)
        for i, players in enumerate(used_list):
            players.setPosition(order_list[i])
    if winner == 'Player 2':
        team_2 +=1
        used_label[1].setPoints(team_2)
        order_list = [4, 1, 2, 3]
        for i, players in enumerate(used_list):
            players.setPosition(order_list[i])
    if winner == 'Player 3':
        team_1 +=1
        used_label[0].setPoints(team_1)
        order_list = [3, 4, 1, 2]
        for i, players in enumerate(used_list):
            players.setPosition(order_list[i])
    if winner == 'Player 4':
        team_2 +=1
        used_label[1].setPoints(team_2)
        order_list = [2, 3, 4, 1]
        for i, players in enumerate(used_list):
            players.setPosition(order_list[i])
    return used_list, used_label, team_1, team_2


def draw_cards(screen, all_cards, player_labels, trump_card, card_images, team_labels):

    # Fill the screen with a background color
    screen.fill((0, 143, 0))

    # Draw cards on the screen
    all_cards.draw(screen)
    # Draw player labels
    for label in player_labels:
        screen.blit(label.image, label.rect)
    for label in team_labels:
        screen.blit(label.image, label.rect)

    # Draw trump card in the center
    if len(trump_card) > 1:
        trump_card_image = card_images[trump_card]
        trump_card_rect = trump_card_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(trump_card_image, trump_card_rect)
    # Update the display
    pygame.display.flip()

def remove_cards_after_play(all_cards, cards_played):
    for i, cards in enumerate(all_cards):
        if cards.value in cards_played:
            cards.kill()
    return all_cards

def game():

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Euchre Simulation")

    hand, blind = make_hands_and_blind()
    card_images = load_card_images()
    all_cards = group_card_images(hand)

    running = True

    trump_card = blind[0]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # Drawing code goes here
        team_1_points = 0
        team_2_points = 0
        hand = []

        hand, blind = make_hands_and_blind()
        card_images = load_card_images()
        all_cards = group_card_images(hand)

        running = True
        player_labels = [
        PlayerLabel("Player 1", WIDTH // 2 - 50, HEIGHT - 30, hand[0], 4, 1),
        PlayerLabel("Player 2", 10, HEIGHT // 2 - 100, hand[1], 1, 0),
        PlayerLabel("Player 3", WIDTH // 2 - 50, 10, hand[2], 2, 0),
        PlayerLabel("Player 4", WIDTH - 100, HEIGHT // 2 - 100, hand[3], 3, 0)
        ]
        team_labels = [
            Score('Team 1 Points: ', 20, 10, 0),
            Score('Team 2 Points: ',WIDTH -200, 10, 0)
        ]
        trump_card = blind[0]
        screen.fill((0, 143, 0))

        # Draw cards on the screen
        draw_cards(screen, all_cards, player_labels, trump_card, card_images, team_labels)

        # Draw player labels
        for label in player_labels:
            screen.blit(label.image, label.rect)

        # Draw trump card in the center
        trump_card_image = card_images[trump_card]
        trump_card_rect = trump_card_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(trump_card_image, trump_card_rect)

        # Update the display
        pygame.display.flip()
        pygame.time.delay(10000)
        trump_pick_order = sorted(player_labels, key=lambda x: x.position)
        trump = 0
        player_trump = ''
        for player in trump_pick_order:
            if player.isDealer:
                new_hand = change_dealer_hand(player.getHand(), trump_card)
                value, suit = trump_choice(trump_card, new_hand)
                if value == 1: 
                    player.setHand(new_hand)
                    trump = trump_card.split(';')[0]
                    player_trump = player.getText()
                    break
            else:
                value, suit = trump_choice(trump_card, player.getHand())
            if value == 1:
                trump = trump_card.split(';')[0]
                player_trump = player.getText()
                for player in trump_pick_order:
                    if player.isDealer:
                        new_hand = change_dealer_hand(player.getHand(), trump_card)
                        player.setHand(new_hand)

                break
        if trump == 0:
            for player in trump_pick_order:
                if player.isDealer:
                    value, trump = trump_choice('', player.getHand())
                    player_trump = player.getText()
                else:
                    value, trump = trump_choice('', player.getHand())
                    player_trump = player.getText()
                    if value == 1:
                        break

        print(f'Trump Is {trump}')
        team_labels.append(Score(f'Trump is: {trump} by {player_trump}', WIDTH //2 - 175, HEIGHT //2, ''))
        hand = []
        for players in player_labels:
            hand.append(players.getHand())
        all_cards = group_card_images(hand)
        draw_cards(screen, all_cards, player_labels, '', card_images, team_labels )
        for j in range(5):
            suit_played = ''
            hand_played = []
            play_order = sorted(player_labels, key=lambda x: x.position)
            for i, players in enumerate(play_order):
                print(i)
                pygame.time.delay(3000)
                if i == 0:
                    card, hand1, best_suit, all_cards = play_card(players.getHand(), players.getPosition(), trump, 'Hearts', all_cards, players.getText())
                    suit_played = best_suit
                    players.setHand(hand1)
                    hand_played.append(card)
                else:
                    print(suit_played)
                    card, hand1, best_suit, all_cards = play_card(players.getHand(), players.getPosition(), trump, suit_played, all_cards, players.getText())
                    players.setHand(hand1)
                    hand_played.append(card)
                draw_cards(screen, all_cards, player_labels, '', card_images, team_labels)
            hand_dict = {}
            for i, player in enumerate(play_order):
                hand_dict[player.getText()] = hand_played[i]
                if player.getPosition() == 1:
                    position = int(player.getText().split(' ')[1]) -1
            print(position)
            winner, suit = win_trick(hand_dict, trump, position)
            player_labels, team_labels, team_1_points, team_2_points = change_play_order(player_labels, winner, team_labels, team_1_points, team_2_points)
            pygame.time.delay(5000)
            all_cards = remove_cards_after_play(all_cards, hand_played)
            draw_cards(screen, all_cards, player_labels, '', card_images, team_labels)
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game()

