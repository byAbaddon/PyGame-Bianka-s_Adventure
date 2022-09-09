import pygame


class Player(pygame.sprite.Sprite):
    energy_power = 100
    player_dead = False
    counter = 0
    SPRITE_ANIMATION_SPEED = 0.2
    PLAYER_SPEED = 4
    JUMP_SPEED = 0.2

    # def __init__(self, pos=(SCREEN_WIDTH - 700, SCREEN_HEIGHT - 80)):
    def __init__(self, x=100, y=470):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = [pygame.image.load(f'../src/assets/images/player/walking/{x}.png') for x in range(1, 7)]
        self.current_sprite = 0
        self.isAnimating = False
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.center = (x, y)
    #   self.position = SCREEN_WIDTH - 700  # player start position
        self.direction = 1  # go right ; -1 go left
        self.is_jump = False
        self.vel_y = 0

    def movie_plyer(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            self.direction = 1
            self.rect.x += self.PLAYER_SPEED
        if key[pygame.K_LEFT]:
            self.direction = -1
            self.rect.x -= self.PLAYER_SPEED
        # jump
        if key[pygame.K_UP] and not self.is_jump:
            self.j()

        if key[pygame.K_DOWN]:
            self.is_jump = False

        # shooting
        if key[pygame.K_SPACE]:
            self.shooting_bullet_position()

        if key[pygame.K_RIGHT] or key[pygame.K_LEFT]:
            self.isAnimating = True

    def j(self): #TODO
        self.vel_y = self.rect.y
        if self.vel_y - 10 < self.rect.y:
            self.rect.y -= 3
        else:
            self.vel_y = self.rect.y


    def sprite_frames(self):
        if self.isAnimating:
            self.current_sprite += self.SPRITE_ANIMATION_SPEED
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 1
            self.image = self.sprites[int(self.current_sprite)]

    def flip_image(self):
        if self.direction == -1 and self.isAnimating:  # go to left
            self.image = pygame.transform.flip(self.image, True, False)
        self.isAnimating = False

    #  shooting bullets
    def shooting_bullet_position(self):
        return self.rect.center

    def update(self):
        pygame.mask.from_surface(self.image)  # create mask image
        self.sprite_frames()
        self.flip_image()
        self.movie_plyer()
        self.j()



