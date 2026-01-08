import sys
from time import sleep
import pygame
from settings import Settings
from gamestats import GameStats
from ships import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard
class AlienInvasion:
    """manage the resource"""
    def __init__(self):
        pygame.init()
        self.clock=pygame.time.Clock()
        self.settings=Settings()
        self.screen=pygame.display.set_mode(
            (self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Alien_invasion")
        self.ship=Ship(self)
        self.bullets = pygame.sprite.Group()
        self.alien = pygame.sprite.Group()
        self.stats = GameStats(self)
        self._create_fleet()
        self.game_active = False
        self.play_button = Button(self,"Play")
        self.sb = Scoreboard(self)

    def run_game(self):
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                print(len(self.bullets))
            
            self._update_screen()
            self.clock.tick(60)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.alien, True, True
        )#return an dict of all bullets and aliens that have collided,bool reflicts whether to delete the bullet/alien
        if not self.alien:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
     
    def _check_play_button(self,mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.sb.prep_level()
            self.sb.prep_ships()
            self.settings.initialize_dynamic_settings()
            pygame.mouse.set_visible(False)
            self.stats.reset_stats()
            self.sb.prep_score()
            self.game_active = True
            self.alien.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)                         
                                                            
    def _check_keyup_events(self,event):
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.alien.draw(self.screen)
        self.sb.show_score()
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.alien.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break                                   

    def _create_alien(self, current_x,current_y):
        new_alien = Alien(self)
        new_alien.x = current_x
        new_alien.rect.x = new_alien.x
        new_alien.rect.y = current_y
        self.alien.add(new_alien)

    def _create_fleet(self):
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        current_x,current_y =alien_width,alien_height
        while current_y < (self.settings.screen_height - 3*alien_height):
            while current_x < (self.settings.screen_width - alien_width):
                self._create_alien(current_x,current_y)
                current_x += alien_width * 2
            current_x = alien_width
            current_y += alien_height * 2

    def _check_fleet_edges(self):
        for alien in self.alien.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.alien.sprites():
            alien.rect.y  += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        self._check_fleet_edges()
        self.alien.update()#use one def update for all aliens in the group
        if pygame.sprite.spritecollideany(self.ship,self.alien):
            self._ship_hit()
        self._check_aliens_bottom()

    def _ship_hit(self):
            if self.stats.ships_left > 0:
                self.stats.ships_left -= 1
                self.sb.prep_ships()
                self.alien.empty()
                self.bullets.empty()
                self._create_fleet()
                self.ship.center_ship()
                sleep(0.5)
            else:
                self.game_active = False
                pygame.mouse.set_visible(True)
                                                                       
if __name__ == '__main__':
    ai=AlienInvasion()
    ai.run_game()
