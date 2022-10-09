from settings import *
from classes.class_background import Background
from classes.class_table import Table
from src.classes.class_sound import Sound
from state_classes import Intro, Menu, Legend, Score, LevelStatistic, PlayerDead
from classes.class_player import Player
from classes.class_knight import Knight
from classes.class_ground import Ground
from classes.class_bullet import Bullet
from classes.class_item import Item
from classes.class_enemy import Enemy

# ================================================================= TEST imported classes
# print(dir(Menu))

# ========================================================================== variables

# ======================================================================== create Sprite groups
background_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
knight_group = pygame.sprite.GroupSingle()
ground_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

# add to all_sprite_groups   /items group include enemy/
all_spite_groups_dict = {'player': player_group, 'knight': knight_group, 'bullets': bullets_group,
                         'ground': ground_group, 'items': item_group}

# ======================================================================= initialize  Classes

player = Player(Bullet, all_spite_groups_dict)
knight = Knight(Bullet, all_spite_groups_dict, player)
ground = Ground()


# add to group
# ground2 = Ground('../src/assets/images/cloud/static.png', SCREEN_WIDTH, SCREEN_HEIGHT - 150)
# ground3 = Ground('../src/assets/images/ground/distance.png', 400, SCREEN_HEIGHT - 170)
player_group.add(player)
knight_group.add(knight)
ground_group.add(ground)

# ---------------------------------------------------------------------- create Enemies

# variables
asg = all_spite_groups_dict
S_W = SCREEN_WIDTH
S_H = SCREEN_HEIGHT
G_H_S = GROUND_HEIGHT_SIZE
T_F_S = TOP_FRAME_SIZE
pic_monkey = '../src/assets/images/enemies/monkey/monkey.png'
pic_hedgehog = '../src/assets/images/enemies/hedgehog/hedgehog.png'
pic_raven = '../src/assets/images/enemies/raven/1.png'
pic_boar = '../src/assets/images/enemies/boar/1.png'
pic_bee = '../src/assets/images/enemies/bee/1.png'
pic_mouse = '../src/assets/images/enemies/mouse/1.png'
pic_mole = '../src/assets/images/enemies/mole/mole.png'
pic_raven_bullet = '../src/assets/images/bullets/egg.png'
pic_monkey_bullet = '../src/assets/images/bullets/coconut.png'


# Game State
class GameState(Sound, ):
    COOLDOWN = 3000  # milliseconds
    start_timer = pygame.time.get_ticks()
    count_visit = 0
    enemy_list = ['enemy_raven', 'enemy_monkey', 'enemy_hedgehog', 'enemy_static_hedgehog', 'enemy_boar', 'enemy_bee',
                  'enemy_mouse', 'enemy_static_mole']

    def __init__(self, player_data, knight_data):
        self.state = 'intro'
        self.current_music = Sound.intro_music(self)
        self.is_music_play = False
        self.background = None
        self.is_bg_created = False
        self.area = 2
        self.level = 1
        self.boss_number = 1
        self.level_reader_row = 1
        self.player_data = player_data
        self.knight_data = knight_data
        self.bonus_pts = 0
        self.is_add_bonus = False
        self.is_start_new_game = False

    def start_game(self):
        # =============================================== RESET ALL DATA IF START NEW GAME
        if self.is_start_new_game:  # reset all old data
            self.is_start_new_game = False
            Sound.stop_all_sounds()
            self.player_data.reset_all_player_data_for_new_game()  # reset all player data
            item_group.empty()
            self.is_music_play = False
            self.background = None
            self.is_bg_created = False
            self.area = 1
            self.level = 1
            self.boss_number = 1
            self.level_reader_row = 1
            self.bonus_pts = 0
            self.is_add_bonus = False
        # -----------------------------------------------
        self.bonus_pts = 0  # reset pts
        player.is_boos_level = False  # set player walking border to 1/3 S_W
        # top display frame
        table.update()

        # developer utils
        text_creator(f'FPS {int(CLOCK.get_fps())}', 'white', 10, 5, 25)
        # text_creator(f'Direction: x= {int(player.direction.x)} y= {int(player.direction.y)}', 'white', 90, 15, 22)
        # text_creator(f'Pos: x= {int(player.pos.x)} y= {int(player.pos.y)}', 'white', 86, 33, 22)
        # text_creator(f'Vel: x= {player.velocity.x:.2f} y= {player.velocity.y:.2f} ', 'white', 90, 50, 22)
        # text_creator(f'Acc: x= {player.acceleration.x:.2f} y= {player.acceleration.y:.2f}', 'white', 90, 70, 22)

        # ================================ create enemy classes
        def enemy_creator(enemy_name):
            if enemy_name == 'enemy_bee':
                b1 = Enemy(Bullet, asg, pic_bee, S_W, S_H - (G_H_S + player.image.get_height() // 2), 2,
                           True, False, pic_bee, 0, 4)
                b2 = Enemy(Bullet, asg, pic_bee, S_W + 40, S_H - (G_H_S + player.image.get_height() // 2 - 40), 2,
                           True, False, pic_bee, 0, 4)
                return b1, b2
            if enemy_name == 'enemy_raven':
                return Enemy(Bullet, asg, pic_raven, S_W, T_F_S + 100, 3, True, True, pic_raven_bullet, 1.4, 5)
            if enemy_name == 'enemy_monkey':
                return Enemy(Bullet, asg, pic_monkey, S_W, 150, 5, True, True, pic_monkey_bullet, 1)
            if enemy_name == 'enemy_hedgehog':
                return Enemy(Bullet, asg, pic_hedgehog, S_W, S_H - G_H_S - 5, 1)
            if enemy_name == 'enemy_static_hedgehog':
                return Enemy(Bullet, asg, pic_hedgehog, S_W, S_H - G_H_S - 5, 0)
            if enemy_name == 'enemy_boar':
                return Enemy(Bullet, asg, pic_boar, S_W, S_H - G_H_S - 32, 3, True, False, pic_boar, 0, 8)
            if enemy_name == 'enemy_mouse':
                return Enemy(Bullet, asg, pic_mouse, S_W, S_H - G_H_S - 2, 5, True, False, '', 0, 3)
            if enemy_name == 'enemy_static_mole':
                return Enemy(Bullet, asg, pic_mole, S_W, S_H - G_H_S - 2, 0, True)

        # ================================ create cloud platform classes
        # def cloud_platform_creator(cloud_type):
        #     # if cloud_type == 'cloud_static':
        #     return Ground('../src/assets/images/cloud/static.png', 200 + self.background.distance_mt, S_H - 170)

        # function sprite creator
        def sprite_creator(dictionary, input_class=None, group_class=None):
            # time_now = pygame.time.get_ticks()
            # ---------create
            for k, v in dictionary.items():  # t: 'item pic'
                if k == int(self.background.distance_mt):
                    # if time_now - self.START_TIMER > 0:  # timer prevent 300ms create double item in group
                    #     self.START_TIMER = time_now
                    if v in self.enemy_list:  # check is class
                        # create new class from enemy_name
                        new_enemy_class = enemy_creator(enemy_name=v)
                        # add to item group
                        group_class.add(new_enemy_class)
                    elif v.split('/')[0] == 'cloud':  # ----------- create ground platform cloud
                        # create new class from cloud platform
                        # new_cloud_class = cloud_platform_creator(cloud_type=v)
                        new_cloud_class = input_class(f'../src/assets/images/{v}.png', S_W, 470)
                        # add to item group
                        group_class.add(new_cloud_class)
                    else:
                        new_item_class = input_class(f'../src/assets/images/{v}.png')  # create item class
                        group_class.add(new_item_class)  # add new class to item_group
                    self.background.distance_mt += 1  # prevent create double sp if player stay in same position

        def distance_counter(*args):
            match int(self.background.distance_mt):
                case 25:
                    Sound.sign_go(self)
                    # self.state = 'level_statistic'
                    self.background.distance_mt += 1  # prevent play double sound if player stay in same position
                case 550:
                    Sound.sign_middle(self)
                    self.background.distance_mt += 1  # prevent ...
                case 1080:  # Finished level
                    Sound.sign_finish(self)
                    self.level_reader_row += 1  # read row level from txt
                    self.background.distance_mt = 0  # prevent ...
                    self.is_music_play = False
                    Sound.stop_all_sounds()
                    Sound.statistic_music(self)
                    self.state = 'level_statistic'  # switch to statistic state

        def area_label():  # Info Table label when Start new Area/Level
            if self.background.distance_mt < 10:
                image = pygame.image.load('../src/assets/images/frames/level_frame.png')
                SCREEN.blit(image, [SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 32])
                text_creator(f'Area {self.area} - {self.level}', 'white', SCREEN_WIDTH // 2 - 54,
                             SCREEN_HEIGHT // 2, 36)

        # ==================== # check is player ALIVE
        if self.player_data.is_player_dead:
            Sound.stop_all_sounds()
            if self.player_data.lives > 0:
                Sound.player_lost_live_music(self)
                self.player_data.reset_current_player_data()    # reset player data for current game
                all_spite_groups_dict['items'].empty()   # clear item group
                self.knight_data.reset_knife_data()
                self.state = 'player_dead'
            if self.player_data.lives == 0:
                Sound.player_dead_funeral_march(self)
                self.state = 'funeral_agency'   # - Game Over

        # ============== level manipulator
        if self.level > 4:
            if self.level == 5:
                self.state = 'boss'
                if self.knight_data.is_boss_level_complete:   #todo:
                    self.level -= 1
            else:
                self.level = 1
                self.area += 1

        # ========================================== START GAME  with Area 1; Level 1
        if self.area == 1:
            if not self.is_music_play:
                self.current_music = Sound.forest_music_area_one(self)
                self.is_music_play = True

            if not self.is_bg_created:
                # resize image
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_level_1.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True)
                self.is_bg_created = True

            # ============== create level: items, enemy, and more
            items_dict = eval(file_operation('levels/levels_data.txt', 'r', self.level_reader_row))
            sprite_creator(items_dict, Item, item_group)

            # ============= level counter
            distance_counter()
            # print(len(item_group))

            # =================================================== UPDATE
            # update BG
            self.background.update()
            # --------------------------- draw sprite group
            # ground_group.draw(SCREEN)  # hide under bg
            bullets_group.draw(SCREEN)
            player_group.draw(SCREEN)
            item_group.draw(SCREEN)

            # --------------------------- update sprite group
            ground_group.update()
            player_group.update()
            bullets_group.update()
            item_group.update()

            # ============== draw current area/level labels
            area_label()

        # ========================================== START GAME  with Area 2; Level 1
        if self.area == 2:
            table.update()
            # top display frames

            if not self.is_music_play:
                # self.current_music = Sound.sea_music_area_two(self)
                self.is_music_play = True

            if not self.is_bg_created:
                # resize image
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_sea.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, True, player.velocity.x, True)
                # add rock ground
                ground_group.empty()
                ground_rock = Ground('../src/assets/images/ground/dock2.png', False, 0, S_H - 100)
                ground_group.add(ground_rock)
                self.is_bg_created = True

            # ============== create level: items, enemy, and more
            items_dict = eval(file_operation('levels/levels_data.txt', 'r', self.level_reader_row))
            sprite_creator(items_dict, Item, item_group)

            # ============= level counter
            distance_counter()

            # =================================================== UPDATE
            # update BG
            self.background.update()
            # --------------------------- draw sprite group
            ground_group.draw(SCREEN)  # hide under bg
            bullets_group.draw(SCREEN)
            player_group.draw(SCREEN)
            item_group.draw(SCREEN)

            # --------------------------- update sprite group
            ground_group.update()
            player_group.update()
            bullets_group.update()
            item_group.update()

            # ============== draw current area/level labels
            area_label()

            # print('AREA 2 ; Level 1')

    def boss(self):
        player.is_boos_level = True  # set player walking border to all SCREEN_WIDTH

        # top display frames
        table.update()
        if self.boss_number == 1:
            text_creator(f'FPS {int(CLOCK.get_fps())}', 'white', 10, 10, 25)
            if not self.is_music_play:
                # Sound.boss_music_area_one(self)
                self.is_music_play = True

            if self.is_bg_created:  # todo remove not  only for test
                # resize image
                scaled_img = scale_image('../src/assets/images/backgrounds/bg_boss/bg_area_one_forest_boss.png', 800, 510)
                self.background = Background(scaled_img, 0, 90, False, player.velocity.x, True)
                self.is_bg_created = False  # todo must be False

            if self.player_data.is_player_kill_boss:
                self.state = 'level_statistic'
            if self.player_data.is_player_dead:
                self.state = 'player_dead'

            # # # =================================================== UPDATE
            # update BG
            self.background.update()
            # # # --------------------------- draw sprite group
            bullets_group.draw(SCREEN)
            player_group.draw(SCREEN)
            knight_group.draw(SCREEN)
            # # # --------------------------- update sprite group
            player_group.update()
            knight_group.update()
            bullets_group.update()

    def intro(self,):
        Intro()
        Intro.event(self)

    def menu(self):
        Menu()
        Menu.event(self)

    def legend(self):
        Legend()
        Legend.event(self)

    def score(self):
        Score()
        Score.event(self)

    def player_dead(self):
        # reset part of game_state data
        self.is_music_play = False
        self.background = None
        self.is_bg_created = False
        PlayerDead(self.player_data, self.area, self.level)
        PlayerDead.event(self)

    def funeral_agency(self):
        background_image('../src/assets/images/player/dead/bg/rip.png', 0, 0)
        if key_pressed(pygame.K_RETURN):
            self.is_start_new_game = True  # for reset old game
            self.state = 'intro'

    def level_statistic(self):
        # reset part of game state
        self.is_music_play = False
        self.background = None
        self.is_bg_created = False
        # ---------------------------------------------
        table.update()

        if screen_transition_animation() >= 0:  # clear screen
            LevelStatistic(self.bonus_pts, self.player_data, self.level).update()
            LevelStatistic(self.bonus_pts, self.player_data, self.level).event(self)

            if self.player_data.energy_power > 0:  # add bonus points to score
                Sound.add_point(self)
                self.player_data.energy_power -= 1
                self.bonus_pts += 30  # 3000 pts
                player.points += round(self.player_data.energy_power % 10 + 25.5)
            elif not self.is_add_bonus and player.energy_power == 0 and\
                    (player.bonus_coins or player.bonus_statuette or player.is_player_kill_boss):
                Sound.grab_coin(self)
                if player.bonus_coins:
                    player.points += 1000 * player.bonus_coins
                if player.bonus_statuette:
                    player.points += 3000
                if player.is_player_kill_boss:
                    player.points += 5000
                self.is_add_bonus = True

    # ========================================= state manager
    def state_manager(self):
        # print(self.state)
        if self.state == 'intro':
            self.intro()
        if self.state == 'menu':
            self.menu()
        if self.state == 'legend':
            self.legend()
        if self.state == 'start_game':
            self.start_game()
        if self.state == 'level_statistic':
            self.level_statistic()
        if self.state == 'boss':
            self.boss()
        if self.state == 'player_dead':
            self.player_dead()
        if self.state == 'funeral_agency':
            self.funeral_agency()


#  ================================ create new GameState
game_state = GameState(player, knight)

# ================================================================ create top Table for: score , energy and more
table = Table(game_state, player, knight)

# ============= Starting Game loo
while True:
    SCREEN.fill(pygame.Color('black'))
    game_state.state_manager()
    pygame.display.update()
    CLOCK.tick(FPS)
    exit_game()
