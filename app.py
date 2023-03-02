import pygame
from player import *
from settings import *
import sys
import random
from pygame import mixer
pygame.init()
pygame.display.set_caption("MATH ESCAPE")
vec = pygame.math.Vector2


class App:

    def __init__(self):
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "start"
        self.cell_width = maze_width // 72
        self.cell_height = maze_height // 72
        self.levels = []
        self.current_level = 1
        self.walls = []
        self.traps = []
        self.win = []
        self.doors = []
        self.tasks = []
        self.hps = []
        self.images()
        self.player_pos = None
        self.load()
        self.player = Player(self, self.player_pos)
        self.timer_sec = 600
        self.timer = pygame.USEREVENT + 1
        self.best_time = 0
        pygame.time.set_timer(self.timer, 1000)
        self.wrong_group = pygame.sprite.Group()
        self.correct_group = pygame.sprite.Group()
        self.play_music()
        self.show_controls = False
        self.show_credits = False
        self.score = 0

    def run(self):
        while self.running:
            if self.state == "start":
                self.start_events()
                self.start_draw()
            elif self.state == "play":
                self.play_draw()
                self.play_update()
                self.play_events()
            elif self.state == "lose":
                self.lose_events()
                self.lose_draw()
            elif self.state == "win":
                self.win_events()
                self.win_draw()
            elif self.state == "level":
                self.level_events()
                self.level_draw()
            else:
                self.running = False
            self.clock.tick(fps)
        pygame.quit()
        sys.exit()

########################################################################################################################

    def draw_text(self, start_message, screen, pos, s, color, name, size=50, centered=False):
        font = pygame.font.SysFont(name, s)
        text = font.render(start_message, False, color)
        transform = (round(text.get_size()[0] / (text.get_size()[1] / round(size))), round(size))
        text = pygame.transform.scale(text, transform)
        if centered:
            screen.blit(text, (pos[0] - transform[0] // 2, pos[1] - transform[1] // 2))
        else:
            screen.blit(text, pos)

    def load(self):
        if self.current_level < 4:
            with open(f"maze/{self.current_level}.txt") as file:
                for y_index, line in enumerate(file):
                    for x_index, char in enumerate(line):
                        if char == "1":
                            self.walls.append(vec(x_index, y_index))
                        if char == "C":
                            self.traps.append(vec(x_index, y_index))
                        if char == "W":
                            self.win.append(vec(x_index, y_index))
                        if char == "P":
                            self.player_pos = vec(x_index, y_index)
                        if char == "D":
                            self.doors.append(vec(x_index, y_index))

    def images(self):
        self.cat_image = pygame.image.load("images/cat.png")
        self.mini_cat_image = pygame.transform.scale(self.cat_image, (42, 50))
        self.dog_image = pygame.image.load("images/dog.png")
        self.mini_dog_image = pygame.transform.scale(self.dog_image, (33, 50))
        self.mouse_image = pygame.image.load("images/mouse.png")
        self.mini_mouse_image = pygame.transform.scale(self.mouse_image, (50, 40))
        self.food_image = pygame.image.load("images/food.png")
        self.mini_food_image = pygame.transform.scale(self.food_image, (50, 33))
        self.bone_image = pygame.image.load("images/bone.png")
        self.mini_bone_image = pygame.transform.scale(self.bone_image, (50, 23))
        self.cheese_image = pygame.image.load("images/cheese.png")
        self.mini_cheese_image = pygame.transform.scale(self.cheese_image, (50, 42))

        self.player_images = [self.cat_image, self.dog_image, self.mouse_image]
        self.award_images = [self.food_image, self.bone_image, self.cheese_image]
        self.mini_player_images = [self.mini_cat_image, self.mini_dog_image, self.mini_mouse_image]
        self.mini_award_images = [self.mini_food_image, self.mini_bone_image, self.mini_cheese_image]

        self.clew_image = pygame.image.load("images/clew.png")
        self.collar_image = pygame.image.load("images/collar.png")
        self.collar_image = pygame.transform.scale(self.collar_image, (37, 20))
        self.mousetrap_image = pygame.image.load("images/mousetrap.png")
        self.mousetrap_image = pygame.transform.scale(self.mousetrap_image, (41, 20))

        self.trap_images = [self.clew_image, self.collar_image, self.mousetrap_image]

        self.controls_image = pygame.image.load("images/controls.png")
        self.controls_image = pygame.transform.scale(self.controls_image, (660, 660))
        self.credits_image = pygame.image.load("images/credits.png")
        self.credits_image = pygame.transform.scale(self.credits_image, (660, 660))
        self.i_image = pygame.image.load("images/i.png")
        self.o_image = pygame.image.load("images/o.png")
        self.start_bg = pygame.image.load("maze/start.jpg")
        self.you_won_bg = pygame.image.load("maze/you_won.jpg")
        self.game_over_bg = pygame.image.load("maze/game_over.jpg")
        self.level1_bg = pygame.image.load("maze/level1.jpg")
        self.level2_bg = pygame.image.load("maze/level2.jpg")
        self.level3_bg = pygame.image.load("maze/level3.jpg")

        self.levels_bg = [self.level1_bg, self.level2_bg, self.level3_bg]

        for num in range(1, 4):
            img = pygame.image.load(f"maze/{num}.jpg")
            win_img = pygame.image.load(f"maze/{num}_win.jpg")
            self.levels.append((img, win_img))

        if self.current_level < 4:
            players = ["cat", "dog", "mouse"]
            for num in range(0, 4):
                img = pygame.image.load(f"hps/{num}hp_{players[self.current_level - 1]}.png")
                self.hps.append(img)

        if self.current_level == 1:
            answers = [1, 1, 4, 3, 3, 3, 4, 3, 4, 2, 2, 2, 3, 2, 2, 3, 4, 1, 2, 1, 3, 4, 4, 1, 3, 2, 3, 2, 2, 1]
            for num in range(0, 10):
                img = pygame.image.load(f"tasks/{num}.png")
                self.tasks.append((img, answers[num]))
        if self.current_level == 2:
            answers = [1, 1, 4, 3, 3, 3, 4, 3, 4, 2, 2, 2, 3, 2, 2, 3, 4, 1, 2, 1, 3, 4, 4, 1, 3, 2, 3, 2, 2, 1]
            for num in range(10, 20):
                img = pygame.image.load(f"tasks/{num}.png")
                self.tasks.append((img, answers[num]))
        if self.current_level == 3:
            answers = [1, 1, 4, 3, 3, 3, 4, 3, 4, 2, 2, 2, 3, 2, 2, 3, 4, 1, 2, 1, 3, 4, 4, 1, 3, 2, 3, 2, 2, 1]
            for num in range(20, 30):
                img = pygame.image.load(f"tasks/{num}.png")
                self.tasks.append((img, answers[num]))

    def play_music(self):
        mixer.music.load("music/music.wav")
        mixer.music.play(-1)
        mixer.music.set_volume(1)
        self.explosion_sound = mixer.Sound("music/explosion.wav")
        self.meow_sound = mixer.Sound("music/meow.wav")
        self.bark_sound = mixer.Sound("music/bark.wav")
        self.squeak_sound = mixer.Sound("music/squeak.wav")
        self.door_sound = mixer.Sound("music/door.wav")
        self.explosion_sound.set_volume(1)
        self.meow_sound.set_volume(1)
        self.bark_sound.set_volume(1)
        self.squeak_sound.set_volume(1)
        self.door_sound.set_volume(1)

        self.player_sounds = [self.meow_sound, self.bark_sound, self.squeak_sound]

        self.music_up = pygame.image.load("music/music_up.png")
        self.music_up = pygame.transform.scale(self.music_up, (50, 50))
        self.music_mute = pygame.image.load("music/music_mute.png")
        self.music_mute = pygame.transform.scale(self.music_mute, (50, 50))
        self.sound_up = pygame.image.load("music/sound_up.png")
        self.sound_up = pygame.transform.scale(self.sound_up, (50, 50))
        self.sound_mute = pygame.image.load("music/sound_mute.png")
        self.sound_mute = pygame.transform.scale(self.sound_mute, (50, 50))
        self.music = [self.music_up]
        self.sound = [self.sound_up]

########################################################################################################################

    def start_events(self):
        self.timer_sec = 600
        self.player = Player(self, self.player_pos)
        self.score = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.rand = random.randint(0, len(self.tasks) - 1)
                self.state = "level"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    if not self.show_controls and not self.show_credits:
                        self.show_controls = True
                    elif self.show_controls:
                        self.show_controls = False
                if event.key == pygame.K_o:
                    if not self.show_credits and not self.show_controls:
                        self.show_credits = True
                    elif self.show_credits:
                        self.show_credits = False
                if event.key == pygame.K_m:
                    if mixer.music.get_volume() == 1:
                        mixer.music.set_volume(0)
                        self.music.clear()
                        self.music = [self.music_mute]
                    elif mixer.music.get_volume() == 0:
                        mixer.music.set_volume(1)
                        self.music.clear()
                        self.music = [self.music_up]
                if event.key == pygame.K_n:
                    if self.explosion_sound.get_volume() == 1:
                        self.explosion_sound.set_volume(0)
                        self.meow_sound.set_volume(0)
                        self.bark_sound.set_volume(0)
                        self.squeak_sound.set_volume(0)
                        self.door_sound.set_volume(0)
                        self.sound.clear()
                        self.sound = [self.sound_mute]
                    elif self.explosion_sound.get_volume() == 0:
                        self.explosion_sound.set_volume(1)
                        self.meow_sound.set_volume(1)
                        self.bark_sound.set_volume(1)
                        self.squeak_sound.set_volume(1)
                        self.door_sound.set_volume(1)
                        self.sound.clear()
                        self.sound = [self.sound_up]

    def start_draw(self):
        self.screen.blit(self.start_bg, (0, 0))
        self.screen.blit(self.sound[0], (1150, 650))
        self.screen.blit(self.music[0], (1210, 650))
        self.screen.blit(self.i_image, (20, 610))
        self.screen.blit(self.o_image, (110, 610))
        if self.show_controls:
            self.screen.blit(self.controls_image, (310, 30))
        if self.show_credits:
            self.screen.blit(self.credits_image, (310, 30))
        pygame.display.update()

    def restart(self):
        self.timer_sec = 600
        self.current_level = 1
        self.hps.clear()
        self.tasks.clear()
        self.traps.clear()
        self.walls.clear()
        self.win.clear()
        self.doors.clear()
        self.load()
        self.player = Player(self, self.player_pos)
        self.images()

########################################################################################################################

    def play_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.restart()
                    self.score = 0
                    self.state = "level"
                if event.key == pygame.K_ESCAPE:
                    self.state = "start"
                    self.restart()
                if event.key == pygame.K_i:
                    if not self.show_controls:
                        self.show_controls = True
                    elif self.show_controls:
                        self.show_controls = False
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))
                if event.key == pygame.K_m:
                    if mixer.music.get_volume() == 1:
                        mixer.music.set_volume(0)
                        self.music.clear()
                        self.music = [self.music_mute]
                    elif mixer.music.get_volume() == 0:
                        mixer.music.set_volume(1)
                        self.music.clear()
                        self.music = [self.music_up]
                if event.key == pygame.K_n:
                    if self.explosion_sound.get_volume() == 1:
                        self.explosion_sound.set_volume(0)
                        self.meow_sound.set_volume(0)
                        self.bark_sound.set_volume(0)
                        self.squeak_sound.set_volume(0)
                        self.door_sound.set_volume(0)
                        self.sound.clear()
                        self.sound = [self.sound_mute]
                    elif self.explosion_sound.get_volume() == 0:
                        self.explosion_sound.set_volume(1)
                        self.meow_sound.set_volume(1)
                        self.bark_sound.set_volume(1)
                        self.squeak_sound.set_volume(1)
                        self.door_sound.set_volume(1)
                        self.sound.clear()
                        self.sound = [self.sound_up]
            if event.type == self.timer:
                if self.timer_sec > 0:
                    self.timer_sec -= 1
                if self.timer_sec == 0 or self.player.life == 0 and not self.wrong_group:
                    self.state = "lose"
                    self.restart()
            if self.player.grid_pos in self.win:
                self.state = "level"
                self.timer_sec = 600
                self.current_level += 1
                self.hps.clear()
                self.traps.clear()
                self.tasks.clear()
                self.walls.clear()
                self.win.clear()
                self.load()
                self.images()
                if self.timer_sec > self.best_time:
                    self.best_time = self.timer_sec
            if self.current_level == 4:
                self.state = "win"
                self.current_level = 1
                self.hps.clear()
                self.tasks.clear()
                self.traps.clear()
                self.walls.clear()
                self.win.clear()
                self.doors.clear()
                self.load()
                self.images()

    def play_update(self):
        self.player.update()

    def play_draw(self):
        correct_answer_animations = [CatAnimation(975, 465), DogAnimation(975, 408), MouseAnimation(1130, 492)]
        keys = pygame.key.get_pressed()
        m, s = divmod(self.timer_sec, 60)
        if self.traps:
            self.screen.blit(self.levels[self.current_level - 1][0], (0, 0))
        if not self.traps:
            self.doors.clear()
            self.screen.blit(self.levels[self.current_level - 1][1], (0, 0))
        if self.player.on_trap():
            self.screen.blit(self.tasks[self.rand][0], (710, 100))
            if self.tasks[self.rand][1] == 1:
                if keys[pygame.K_1]:
                    self.player_sounds[self.current_level - 1].play()
                    self.traps.remove(self.player.grid_pos)
                    self.score += 1
                    self.tasks.pop(self.rand)
                    if self.tasks:
                        self.rand = random.randint(0, len(self.tasks) - 1)
                    correct = correct_answer_animations[self.current_level - 1]
                    self.correct_group.add(correct)
                    if not self.traps:
                        self.door_sound.play()
                elif keys[pygame.K_2] or keys[pygame.K_3] or keys[pygame.K_4]:
                    self.explosion_sound.play()
                    self.traps.remove(self.player.grid_pos)
                    self.player.life -= 1
                    self.tasks.pop(self.rand)
                    if self.tasks:
                        self.rand = random.randint(0, len(self.tasks) - 1)
                    wrong = Wrong(975, 350)
                    self.wrong_group.add(wrong)
                    if not self.traps:
                        self.door_sound.play()
            elif self.tasks[self.rand][1] == 2:
                if keys[pygame.K_2]:
                    self.player_sounds[self.current_level - 1].play()
                    self.traps.remove(self.player.grid_pos)
                    self.score += 1
                    self.tasks.pop(self.rand)
                    if self.tasks:
                        self.rand = random.randint(0, len(self.tasks) - 1)
                    correct = correct_answer_animations[self.current_level - 1]
                    self.correct_group.add(correct)
                    if not self.traps:
                        self.door_sound.play()
                elif keys[pygame.K_1] or keys[pygame.K_3] or keys[pygame.K_4]:
                    self.explosion_sound.play()
                    self.traps.remove(self.player.grid_pos)
                    self.player.life -= 1
                    self.tasks.pop(self.rand)
                    if self.tasks:
                        self.rand = random.randint(0, len(self.tasks) - 1)
                    wrong = Wrong(975, 350)
                    self.wrong_group.add(wrong)
                    if not self.traps:
                        self.door_sound.play()
            elif self.tasks[self.rand][1] == 3:
                if keys[pygame.K_3]:
                    self.player_sounds[self.current_level - 1].play()
                    self.traps.remove(self.player.grid_pos)
                    self.score += 1
                    self.tasks.pop(self.rand)
                    if self.tasks:
                        self.rand = random.randint(0, len(self.tasks) - 1)
                    correct = correct_answer_animations[self.current_level - 1]
                    self.correct_group.add(correct)
                    if not self.traps:
                        self.door_sound.play()
                elif keys[pygame.K_1] or keys[pygame.K_2] or keys[pygame.K_4]:
                    self.explosion_sound.play()
                    self.traps.remove(self.player.grid_pos)
                    self.player.life -= 1
                    self.tasks.pop(self.rand)
                    if self.tasks:
                        self.rand = random.randint(0, len(self.tasks) - 1)
                    wrong = Wrong(975, 350)
                    self.wrong_group.add(wrong)
                    if not self.traps:
                        self.door_sound.play()
            elif self.tasks[self.rand][1] == 4:
                if keys[pygame.K_4]:
                    self.player_sounds[self.current_level - 1].play()
                    self.traps.remove(self.player.grid_pos)
                    self.score += 1
                    self.tasks.pop(self.rand)
                    if self.tasks:
                        self.rand = random.randint(0, len(self.tasks) - 1)
                    correct = correct_answer_animations[self.current_level - 1]
                    self.correct_group.add(correct)
                    if not self.traps:
                        self.door_sound.play()
                elif keys[pygame.K_1] or keys[pygame.K_2] or keys[pygame.K_3]:
                    self.explosion_sound.play()
                    self.traps.remove(self.player.grid_pos)
                    self.player.life -= 1
                    self.tasks.pop(self.rand)
                    if self.tasks:
                        self.rand = random.randint(0, len(self.tasks) - 1)
                    wrong = Wrong(975, 350)
                    self.wrong_group.add(wrong)
                    if not self.traps:
                        self.door_sound.play()
        self.draw_traps()
        self.draw_text(f"{m:02d}:{s:02d}", self.screen, [10, 10],
                       font_size, red, font_name, 40)
        self.screen.blit(self.hps[self.player.life], (570, 5))
        self.screen.blit(self.mini_award_images[self.current_level - 1], (310, 10))
        self.player.draw()
        self.screen.blit(self.sound[0], (1150, 650))
        self.screen.blit(self.music[0], (1210, 650))
        if self.show_controls:
            self.screen.blit(self.controls_image, (5, 55))
        self.wrong_group.draw(self.screen)
        self.wrong_group.update()
        self.correct_group.draw(self.screen)
        self.correct_group.update()
        pygame.display.update()

    def draw_traps(self):
        for trap in self.traps:
            rect = self.trap_images[self.current_level - 1].get_rect()
            rect.center = (trap.x * self.cell_width, trap.y * self.cell_height + 3)
            self.screen.blit(self.trap_images[self.current_level - 1], rect)

########################################################################################################################

    def lose_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = "start"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    if mixer.music.get_volume() == 1:
                        mixer.music.set_volume(0)
                        self.music.clear()
                        self.music = [self.music_mute]
                    elif mixer.music.get_volume() == 0:
                        mixer.music.set_volume(1)
                        self.music.clear()
                        self.music = [self.music_up]
                if event.key == pygame.K_n:
                    if self.explosion_sound.get_volume() == 1:
                        self.explosion_sound.set_volume(0)
                        self.meow_sound.set_volume(0)
                        self.bark_sound.set_volume(0)
                        self.squeak_sound.set_volume(0)
                        self.door_sound.set_volume(0)
                        self.sound.clear()
                        self.sound = [self.sound_mute]
                    elif self.explosion_sound.get_volume() == 0:
                        self.explosion_sound.set_volume(1)
                        self.meow_sound.set_volume(1)
                        self.bark_sound.set_volume(1)
                        self.squeak_sound.set_volume(1)
                        self.door_sound.set_volume(1)
                        self.sound.clear()
                        self.sound = [self.sound_up]

    def lose_draw(self):
        self.screen.blit(self.game_over_bg, (0, 0))
        self.screen.blit(self.sound[0], (1150, 650))
        self.screen.blit(self.music[0], (1210, 650))
        pygame.display.update()

########################################################################################################################

    def win_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = "start"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    if mixer.music.get_volume() == 1:
                        mixer.music.set_volume(0)
                        self.music.clear()
                        self.music = [self.music_mute]
                    elif mixer.music.get_volume() == 0:
                        mixer.music.set_volume(1)
                        self.music.clear()
                        self.music = [self.music_up]
                if event.key == pygame.K_n:
                    if self.explosion_sound.get_volume() == 1:
                        self.explosion_sound.set_volume(0)
                        self.meow_sound.set_volume(0)
                        self.bark_sound.set_volume(0)
                        self.squeak_sound.set_volume(0)
                        self.door_sound.set_volume(0)
                        self.sound.clear()
                        self.sound = [self.sound_mute]
                    elif self.explosion_sound.get_volume() == 0:
                        self.explosion_sound.set_volume(1)
                        self.meow_sound.set_volume(1)
                        self.bark_sound.set_volume(1)
                        self.squeak_sound.set_volume(1)
                        self.door_sound.set_volume(1)
                        self.sound.clear()
                        self.sound = [self.sound_up]

    def win_draw(self):
        self.screen.blit(self.you_won_bg, (0, 0))
        self.screen.blit(self.sound[0], (1150, 650))
        self.screen.blit(self.music[0], (1210, 650))
        pygame.display.update()

########################################################################################################################

    def level_events(self):
        self.player = Player(self, self.player_pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = "play"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    if mixer.music.get_volume() == 1:
                        mixer.music.set_volume(0)
                        self.music.clear()
                        self.music = [self.music_mute]
                    elif mixer.music.get_volume() == 0:
                        mixer.music.set_volume(1)
                        self.music.clear()
                        self.music = [self.music_up]
                if event.key == pygame.K_n:
                    if self.explosion_sound.get_volume() == 1:
                        self.explosion_sound.set_volume(0)
                        self.meow_sound.set_volume(0)
                        self.bark_sound.set_volume(0)
                        self.squeak_sound.set_volume(0)
                        self.door_sound.set_volume(0)
                        self.sound.clear()
                        self.sound = [self.sound_mute]
                    elif self.explosion_sound.get_volume() == 0:
                        self.explosion_sound.set_volume(1)
                        self.meow_sound.set_volume(1)
                        self.bark_sound.set_volume(1)
                        self.squeak_sound.set_volume(1)
                        self.door_sound.set_volume(1)
                        self.sound.clear()
                        self.sound = [self.sound_up]

    def level_draw(self):
        self.screen.blit(self.levels_bg[self.current_level - 1], (0, 0))
        player_rect = self.player_images[self.current_level - 1].get_rect()
        player_rect.center = [width // 6, height - height // 4]
        self.screen.blit(self.player_images[self.current_level - 1], player_rect)
        award_rect = self.award_images[self.current_level - 1].get_rect()
        award_rect.center = [width - width // 6, height - height // 4]
        self.screen.blit(self.award_images[self.current_level - 1], award_rect)
        self.screen.blit(self.sound[0], (1150, 650))
        self.screen.blit(self.music[0], (1210, 650))
        pygame.display.update()

########################################################################################################################


class Wrong(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 41):
            img = pygame.image.load(f"wrong/exp{num}.png")
            img = pygame.transform.scale(img, (750, 750))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        wrong_speed = 1
        self.counter += 1
        if self.counter >= wrong_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        if self.index >= len(self.images) - 1 and self.counter >= wrong_speed:
            self.kill()


class CatAnimation(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 18):
            img = pygame.image.load(f"correct/cat_{num}.png")
            img = pygame.transform.scale(img, (400, 309))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        correct_speed = 4
        self.counter += 1
        if self.counter >= correct_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        if self.index >= len(self.images) - 1 and self.counter >= correct_speed:
            self.kill()


class DogAnimation(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 18):
            img = pygame.image.load(f"correct/dog_{num}.png")
            img = pygame.transform.scale(img, (400, 423))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        correct_speed = 4
        self.counter += 1
        if self.counter >= correct_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        if self.index >= len(self.images) - 1 and self.counter >= correct_speed:
            self.kill()


class MouseAnimation(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 18):
            img = pygame.image.load(f"correct/mouse_{num}.png")
            img = pygame.transform.scale(img, (200, 255))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        correct_speed = 4
        self.counter += 1
        if self.counter >= correct_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        if self.index >= len(self.images) - 1 and self.counter >= correct_speed:
            self.kill()