import pygame
from src.settings import SCREEN, SCREEN_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT_SIZE, vec, randrange
from src.classes.class_sound import Sound


class Knight(pygame.sprite.Sprite, Sound,):
    SPRITE_ANIMATION_SPEED = 0.3
    COOLDOWN = 1000  # milliseconds
    COOLDOWN_ATTACK = {'run': 600, 'attack': 800, 'dead': 1000}  # milliseconds
    WALK_LEFT_SCREEN_BORDER = 20  # is knight w_size
    WALK_RIGHT_SCREEN_BORDER = SCREEN_WIDTH - 20
    WALK_SPEED = 3
    JUMP_HEIGHT = -6
    energy_power = 4
    is_walk = False
    is_run = False
    is_jump = False
    is_attack = False
    is_dead = False
    is_sound = False

    def __init__(self, class_bullet, all_sprite_groups_dict, player):
        pygame.sprite.Sprite.__init__(self)
        self.class_bullet = class_bullet
        self.all_sprite_groups_dict = all_sprite_groups_dict
        self.player = player
        self.image = pygame.image.load('../src/assets/images/boss_knight/idle/1.png')
        self.sprites_knight = [pygame.image.load(f'../src/assets/images/boss_knight/idle/{x}.png') for x in range(1, 11)]
        self.current_sprite = 0
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.midbottom = (SCREEN_WIDTH - 100, SCREEN_HEIGHT - GROUND_HEIGHT_SIZE + 4)
        self.direction = vec(-1, 1)  # stay/idle 0

    def knight_movie(self):
        if self.is_walk and not self.is_dead:
            # ---------------------------------------- firs knight scream sound
            if not self.is_sound:
                Sound.knight_scream(self)
                # change list ot pic sprite USING scope BOOLEAN SOUND TO PREVENT falling FPS
                self.sprites_knight = [pygame.image.load(f'../src/assets/images/boss_knight/walk/{x}.png') for x in range(1, 11)]
                self.is_sound = True

            # ---------------------------------------- go left
            if self.direction.x == -1:
                self.rect.x -= self.WALK_SPEED
                if self.rect.x <= 150:
                    self.direction.x = 1
            # --------------------------------------- go right
            if self.direction.x == 1:
                self.rect.x += self.WALK_SPEED
                if self.rect.x >= randrange(500, SCREEN_WIDTH):
                    self.direction.x = -1

    def knight_dead(self):
        if not self.is_dead:
            self.energy_power = 0
            Sound.knight_dead(self)
            # add amulets number to player list
            self.player.boss_taken_amulets += 1
            self.is_dead = True
        self.image = pygame.image.load('../src/assets/images/boss_knight/dead/9.png')
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT_SIZE - self.image.get_height() // 2

        # create amulet after knight dead
        amulet = pygame.image.load(f'../src/assets/images/amulets/small/{self.player.boss_taken_amulets}.png')
        img_rect = amulet.get_bounding_rect(min_alpha=1)
        img_rect.center = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20]
        SCREEN.blit(amulet, img_rect.center)

        # check collide player and amulet
        get_amulet = self.player.rect.colliderect(img_rect)
        if get_amulet:
            Sound.grab_amulets(self)
            self.player.is_player_kill_boss = True  # return info to player if boss death and take amulet








    def sprite_frames(self):
        if self.direction.y == 1:
            self.current_sprite += self.SPRITE_ANIMATION_SPEED
            if self.current_sprite >= len(self.sprites_knight):
                self.current_sprite = 1
            self.image = self.sprites_knight[int(self.current_sprite)]

    def check_players_bullet_collide(self):
        bullets_group = self.all_sprite_groups_dict['bullets']
        sprite = pygame.sprite.spritecollide(self, bullets_group, True, pygame.sprite.collide_mask)
        if sprite:
            for hit_point in sprite:
                if 400 <= hit_point.rect.topleft[1] <= 442:  # head shoot
                    self.is_walk = True
                    Sound.bullet_player_hit_knight_face(self)
                    self.energy_power -= self.player.WEAPONS_DICT[self.player.current_weapon_name]['power']
                else:
                    Sound.bullet_player_hit_knight_armor(self)  # body soot

    def update(self,):
        self.sprite_frames()
        self.knight_movie()
        self.check_players_bullet_collide()
        if self.energy_power <= 0:
            self.knight_dead()

