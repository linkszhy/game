import pygame
from pygame.sprite import Sprite
from PIL import Image
from scoreboard import Scoreboard
class Alien(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        img = Image.open("images/alien.jpeg")
        img = img.resize((50,50))
        img_rgb = img.convert("RGB")
        img_rgb.save("images/alien.bmp","BMP")
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.settings = ai_game.settings   

    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True








