import pygame
# Colors
pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
class PlayerLabel(pygame.sprite.Sprite):
    def __init__(self, text, x, y, hand, position, isDealer):
        super().__init__()
        self.font = pygame.font.Font(None, 36)
        self.text = text
        self.isDealer = isDealer
        self.name = self.changeText()
        self.image = self.font.render(self.name, True, BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hand = hand
        self.position = position
    def getHand(self):
        return self.hand
    def setPosition(self, pos):
        self.position = pos
    def getPosition(self):
        return self.position
    def getHandAndPosition(self):
        return self.hand, self.position
    def setDealer(self, isDealer):
        self.isDealer = isDealer
    def getDealer(self):
        return self.isDealer
    def changeText(self):
        if self.isDealer:
            name = self.text + ' Dealer'
        else:
            name = self.text
        return name
    def getText(self):
        return self.text
    def setHand(self, hand):
        self.hand = hand
    def getPosition(self):
        return self.position
    
class Score(pygame.sprite.Sprite):
    def __init__(self, text, x, y, points):
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.points = points
        self.name = self.makeTitle()
        self.updateImage()  # Initialize the image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def makeTitle(self):
        return self.text + str(self.points)

    def setPoints(self, points):
        self.points = points
        self.updateImage()  # Update the image when points change

    def getPoints(self):
        return self.points

    def getText(self):
        return self.text

    def updateImage(self):
        self.image = self.font.render(self.makeTitle(), True, BLACK)

class Card(pygame.sprite.Sprite):
    def __init__(self, image, value):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.value = value
