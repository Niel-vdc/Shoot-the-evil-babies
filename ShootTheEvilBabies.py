import pygame
import sys
import random


# Classes
score = 100
high_score = 0
lives = 5
shot_count = 0
class Player(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = screen_width / 2, 900
        self.speed = 1

    def move(self, x_dir, y_dir):
        self.rect.centerx += x_dir * self.speed * 3
        self.rect.centery += y_dir * self.speed * 3

        if self.rect.left <= -20:
            self.rect.left = -20
        if self.rect.right >= screen_width + 20:
            self.rect.right = screen_width + 20
        if self.rect.top <= screen_height - 400:
            self.rect.top = screen_height - 400
        if self.rect.bottom >= screen_height - 50:
            self.rect.bottom = screen_height - 50

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.move(-1, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.move(1, 0)
        if keys[pygame.K_UP] or keys[pygame.K_w]:  
            player.move(0, -1)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.move(0, 1)

    def create_laser(self):
        return Laser(laser_surface, self.rect.centerx, self.rect.centery)

    def create_flame(self):
        flame1 = Flame(flame_surface, self.rect.bottomleft[0] + 32, self.rect.bottomleft[1])
        flame2 = Flame(flame_surface, self.rect.bottomright[0] - 32, self.rect.bottomright[1])

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            return flame2
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            return flame1
        if keys[pygame.K_UP] or keys[pygame.K_w]:  
            flame1 = Flame(flame_surface, self.rect.bottomleft[0] + 32, self.rect.bottomleft[1] + 7)
            flame2 = Flame(flame_surface, self.rect.bottomright[0] - 32, self.rect.bottomright[1] + 7)
            return flame1, flame2
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            flame1 = Flame(flame_surface, self.rect.bottomleft[0] + 32, self.rect.bottomleft[1] -7)
            flame2 = Flame(flame_surface, self.rect.bottomright[0] - 32, self.rect.bottomright[1] -7)
            return flame1, flame2
        else:
            return flame1, flame2

class Laser(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(picture_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)

    def update(self):
        global score
        self.rect.y -= 20

        if self.rect.y <= 0 - 100:
              self.kill()
              score -= 20

class Flame(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(picture_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        pos_x = random.randrange(50, screen_width - 50)
        self.image = pygame.image.load(picture_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, -50)
    
    def update(self, speed):
        global lives
        self.rect.y += speed

        if self.rect.y == screen_height + 50:
            self.kill()
            lives -= 1
            lose.play()

    def collide(self):
        global score
        global lives
        global shot_count 
        for enemy in enemy_group:
            for laser in laser_group:
                if laser.rect.colliderect(enemy):
                    enemy.kill()
                    laser.kill()
                    random.choice(baby_sounds).play()
                    score += 100
                    shot_count += 1
            for player in player_group:
                if player.rect.colliderect(enemy):
                    enemy.kill()
                    lose.play()
                    lives -= 1



# Functions
bg_y_pos = 0
def background(speed):
    global bg_y_pos
    bg_y_pos += speed
    screen.blit(bg_surface, (0, bg_y_pos))
    screen.blit(bg_surface, (0, bg_y_pos - bg_surface.get_height()))
    if bg_y_pos >= bg_surface.get_height():
        bg_y_pos = 0

def life_images():
    life_x_pos = screen_width - 50
    for life in range(lives):
        life_rect = life_surface.get_rect(midright = (life_x_pos, 200))
        screen.blit(life_surface, life_rect)
        life_x_pos -= 50

#Initialize
pygame.init()
clock = pygame.time.Clock()
screen_width = screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
tick = 100

# Game Variables
game_active = False
game_count = 0
bg_surface = pygame.transform.scale2x(pygame.image.load("Media/background.png")).convert()



player_surface = "Media/playerShip2_red.png"
player = Player(player_surface)
player_group = pygame.sprite.Group()
player_group.add(player)

life_surface = pygame.image.load("Media/playerLife2_red.png").convert_alpha()

flame_surface = "Media/fire15.png"
flame_group = pygame.sprite.Group()

laser_surface = "Media/laserBlue01.png"
laser_group = pygame.sprite.Group()

enemy_surface = "Media/Baby.png"
enemy_group = pygame.sprite.Group()
SPAWNENEMY = pygame.USEREVENT
pygame.time.set_timer(SPAWNENEMY, 1000)
enemy_count = 0

arrows_surface = pygame.image.load("Media/Arrows.png").convert_alpha()
spacebar_surface = pygame.image.load("Media/Spacebar.png").convert_alpha()

baby_sound1 = pygame.mixer.Sound("Media/Baby1.wav")
baby_sound2 = pygame.mixer.Sound("Media/Baby2.wav")
baby_sound3 = pygame.mixer.Sound("Media/Baby3.wav")
baby_sound4 = pygame.mixer.Sound("Media/Baby4.wav")
baby_sound5 = pygame.mixer.Sound("Media/Baby5.wav")
baby_sound6 = pygame.mixer.Sound("Media/Baby6.wav")
baby_sound7 = pygame.mixer.Sound("Media/Baby7.wav")
baby_sound8 = pygame.mixer.Sound("Media/Baby8.wav")
baby_sound9 = pygame.mixer.Sound("Media/Baby9.wav")
baby_sound10 = pygame.mixer.Sound("Media/Baby10.wav")
baby_sound11 = pygame.mixer.Sound("Media/Baby11.wav")
baby_sound12 = pygame.mixer.Sound("Media/Baby12.wav")
baby_sound13 = pygame.mixer.Sound("Media/Baby13.wav")
baby_sound14 = pygame.mixer.Sound("Media/Baby14.wav")
baby_sound15 = pygame.mixer.Sound("Media/Baby15.wav")
baby_sounds = [baby_sound1, baby_sound2, baby_sound3, baby_sound4, baby_sound5, baby_sound6, baby_sound7, baby_sound8, baby_sound9, baby_sound10, baby_sound11, baby_sound12, baby_sound13, baby_sound14, baby_sound15]

baby_laugh = pygame.mixer.Sound("Media/Baby_laugh.wav")

laser_sound = pygame.mixer.Sound("Media/sfx_laser1.ogg")
lose = pygame.mixer.Sound("Media/sfx_lose.wav") 

#song = pygame.mixer.Sound("Media/SkyFire.ogg")
#title_song = song.play()

game_font = pygame.font.Font("Media/kenvector_future.ttf", 24)
end_screen_font = pygame.font.Font("Media/kenvector_future.ttf", 30)
end_screen_message_font = pygame.font.Font("Media/kenvector_future.ttf", 40)
message = ""

# Game Loop
while True:
    pygame.display.flip()
    # Events

    if game_active:
        game_active = (score>0)
        enemy = Enemy(enemy_surface)
        enemy.collide()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SPAWNENEMY:
                enemy_group.add(enemy)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    laser_group.add(player.create_laser()) 
                    laser_sound.play()
                if event.key == pygame.K_UP:
                    tick = 140
                if event.key == pygame.K_DOWN:
                    tick = 60
            else:
                tick = 100

        if shot_count >= 30 and game_active == True:
            message = f"You survived... For now"
            game_active = False
        
        if lives <= 0 and game_active == True:
            game_active = False
            message = f"You lose! Baby wins :)"
            #title_song.stop()
            baby_laugh.play()

        if score <= 0  :
            message = "You lose! Baby wins :)"
            #title_song.stop()
            baby_laugh.play()


    # Draw
        pygame.display.flip()

        background(0.4)

        laser_group.draw(screen)
        laser_group.update()

        enemy_group.draw(screen)
        enemy_group.update(2)

        flame_group.empty()
        flame_group.add(player.create_flame())
        flame_group.draw(screen)
        flame_group.update()

        player_group.draw(screen)
        player_group.update()

        shot_count_surface = game_font.render((f"Babies you shot: {int(shot_count)}"), True, (255, 255, 255))
        shot_count_rect = shot_count_surface.get_rect(midright = (screen_width - 50, 50))
        screen.blit(shot_count_surface, shot_count_rect)

        score_surface = game_font.render((f"Score: {int(score)}"), True, (255, 255, 255))
        score_rect = score_surface.get_rect(midright = (screen_width - 50, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render((f"High score: {int(high_score)}"), True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(midright = (screen_width - 50, 150))
        screen.blit(high_score_surface, high_score_rect)

        life_images()
        # lives_surface = game_font.render((f"Lives: {int(lives)}"), True, (255, 255, 255))
        # lives_rect = lives_surface.get_rect(midright = (screen_width - 50, 200))
        # screen.blit(lives_surface, lives_rect)


    else:
        background(0.4)

        if game_count >= 1:
            player_group.empty()
            enemy_group.empty()

            if score >= high_score:
                high_score = score
            if high_score == 0:
                high_score = score

            message_surface = end_screen_message_font.render((message), True, (255, 255, 255))
            message_rect = message_surface.get_rect(midleft = (100, 300))
            screen.blit(message_surface, message_rect)

            shot_count_surface = end_screen_font.render((f"Babies you shot: {int(shot_count)}"), True, (255, 255, 255))
            shot_count_rect = shot_count_surface.get_rect(midleft = (100, 450))
            screen.blit(shot_count_surface, shot_count_rect)

            lives_surface = end_screen_font.render((f"Lives: {int(lives)}"), True, (255, 255, 255))
            lives_rect = lives_surface.get_rect(midleft = (100, 500))
            screen.blit(lives_surface, lives_rect)

            score_surface = end_screen_font.render((f"score: {int(score)}"), True, (255, 255, 255))
            score_rect = score_surface.get_rect(midleft = (100, 550))
            screen.blit(score_surface, score_rect)

            high_score_surface = end_screen_font.render((f"High score: {int(high_score)}"), True, (255, 255, 255))
            high_score_rect = high_score_surface.get_rect(midleft = (100, 600))
            screen.blit(high_score_surface, high_score_rect)

            continue_surface = end_screen_font.render((f"Press Spacebar to begin"), True, (255, 255, 255))
            continue_rect = continue_surface.get_rect(center = (screen_width / 2, screen_height - 100))
            screen.blit(continue_surface, continue_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player = Player(player_surface)
                        score = 100
                        lives = 5
                        shot_count = 0
                        player_group.add(player)
                        game_active = True
                        baby_laugh.stop()
                        #song.set_volume(0.5)
                        #song.play()


        if game_count < 1:
            #title_song
            message_surface = game_font.render("Controls:", True, (255, 255, 255))
            message_rect = message_surface.get_rect(midleft = (100, 100))
            screen.blit(message_surface, message_rect)

            arrows_rect = arrows_surface.get_rect(midleft = (100, 200))
            screen.blit(arrows_surface, arrows_rect)

            spacebar_rect = spacebar_surface.get_rect(midleft = (450, 200))
            screen.blit(spacebar_surface, spacebar_rect)

            message_surface = end_screen_message_font.render("Shoot the evil babies", True, (255, 255, 255))
            message_rect = message_surface.get_rect(center = (screen_width / 2, screen_height / 2))
            screen.blit(message_surface, message_rect)

            continue_surface = end_screen_font.render((f"Press Spacebar to begin"), True, (255, 255, 255))
            continue_rect = continue_surface.get_rect(center = (screen_width / 2, screen_height - 100))
            screen.blit(continue_surface, continue_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        score = 100
                        lives = 5
                        shot_count = 0
                        player_group.add(player)
                        game_active = True
                        game_count += 1
                        #title_song.set_volume(0.5)

        pygame.display.flip()

        pygame.time.wait(1000)


    clock.tick(tick) 
