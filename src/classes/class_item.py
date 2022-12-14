import pygame
from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT_SIZE, key_pressed, BG_SPEED, BG_LOOP_SPEED_INCREASE


class Item(pygame.sprite.Sprite):
    SPRITE_ANIMATION_SPEED = 0.1

    def __init__(self, pic='', x=SCREEN_WIDTH, y=SCREEN_HEIGHT - GROUND_HEIGHT_SIZE, sprite_pic_num=0):
        pygame.sprite.Sprite.__init__(self)
        self.group_name = pic.split('/')[5]
        self.item_name = pic.split('/')[6][:-4]
        self.image = pygame.image.load(pic).convert_alpha()
        self.image_height_size = self.image.get_height()
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.midtop = (x, y - self.image_height_size + 13)
        self.current_sprite = 0
        self.sprite_pic_num = sprite_pic_num
        self.sprites_animate = [pygame.image.load(f'{pic[:-4]}/{x}.png') for x in range(1, self.sprite_pic_num + 1)]
        # print(self.group_name, 'g - i -> ' , self.item_name)

    def movement(self):
        if key_pressed(pygame.K_RIGHT):
            self.rect.x -= BG_SPEED
        # uncomment this and same in Background class to running fast screen illusion /ONLY FOR TEST!!!/
        # if key_pressed(pygame.K_RIGHT) and key_pressed(pygame.K_a):  # developer hack speed
        #     self.rect.x -= BG_SPEED + BG_LOOP_SPEED_INCREASE

    def sprite_frames(self):
        if self.sprite_pic_num > 0:
            self.current_sprite += self.SPRITE_ANIMATION_SPEED  # speed may be changed
            if self.current_sprite >= len(self.sprites_animate):
                self.current_sprite = 1
            self.image = self.sprites_animate[int(self.current_sprite)]

    def prevent_overflow_item_group(self):  # remove old item from item_group if it out of screen
        if self.rect.x < -80 or self.rect.x > SCREEN_WIDTH + 100:
            self.kill()

    def update(self):
        pygame.mask.from_surface(self.image)
        self.movement()
        self.sprite_frames()
        self.prevent_overflow_item_group()
