# mazetest2 with mazegen
import mazegen
import pygame
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_p,
    K_n,
    K_SPACE,
    K_a,
    K_s,
    K_d,
    K_w,
)

# screen width and height
SCREEN_WIDTH = 670
SCREEN_HEIGHT = 700
# Create the screen
screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])

# walls
class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Wall,self).__init__()
        self.surf = pygame.Surface((25,25))
        self.surf.fill((84,38,17))
        self.rect = self.surf.get_rect(center=(10+x*25,10+y*25))
        #print('hi')
    def remove_wall(self):
        self.kill()

walls = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# enemies
class Enemy(pygame.sprite.Sprite):
    def __init__(self, r):
        super(Enemy, self).__init__()
        """
        self.surf = pygame.Surface((20,20))
        self.surf.fill((170, 25, 25))
        """
        self.surf = pygame.image.load("test_ball_enemy.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        #picture
        self.startroom = mazegen.room_location[r]-1
        self.randomx=random.randint(-2,2)
        self.randomy=random.randint(-2,2)
        self.rect = self.surf.get_rect(center=(85+(self.startroom%3*250)+(self.randomy*25),85+(self.startroom//3*250)+(self.randomx*25)))
        self.last_move = 5
        self.possible_moves = [0,1,2,3]
    def defeat_enemy(self):
        self.kill()
    def update(self):
        r_choice = 6
        while True:
            if r_choice == self.last_move:
                break
            if len(self.possible_moves)==0: self.possible_moves.append(self.last_move)
            r_choice = random.choice(self.possible_moves)
            #print(self.possible_moves)
            r_choicex = [0,1,0,-1]
            r_choicey = [1,0,-1,0]
            self.rect.move_ip(r_choicex[r_choice]*25, r_choicey[r_choice]*25)
            temp = pygame.sprite.spritecollide(self, enemies, False)
            if pygame.sprite.spritecollideany(self, walls) or len(temp) > 1:
                self.rect.move_ip(r_choicex[r_choice]*(-25), r_choicey[r_choice]*(-25))
            else:
                break
            self.possible_moves.remove(r_choice)
        self.possible_moves = [0,1,2,3]
        self.last_move = (r_choice+2)%4
        self.possible_moves.remove((r_choice+2)%4)
enemies = pygame.sprite.Group()
# key
class Key(pygame.sprite.Sprite):
    def __init__(self):
        super(Key, self).__init__()
        """
        self.surf = pygame.Surface((20,20))
        self.surf.fill((255, 237, 158))
        """
        self.surf = pygame.image.load("test_key_2.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        #picture
        self.startroom = mazegen.room_location[1]-1
        self.randomx=random.randint(-2,2)
        self.randomy=random.randint(-2,2)
        self.rect = self.surf.get_rect(center=(85+(self.startroom%3*250)+(self.randomy*25),85+(self.startroom//3*250)+(self.randomx*25)))
keys = pygame.sprite.Group()
# door
class Door(pygame.sprite.Sprite):
    def __init__(self):
        super(Door, self).__init__()
        """
        self.surf = pygame.Surface((20,20))
        self.surf.fill((200, 200, 200))
        """
        self.surf = pygame.image.load("test_door_2.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        #picture
        self.startroom = mazegen.room_location[0]-1
        self.randomx=random.randint(-2,2)
        self.randomy=random.randint(-2,2)
        self.rect = self.surf.get_rect(center=(85+(self.startroom%3*250)+(self.randomy*25),85+(self.startroom//3*250)+(self.randomx*25)))
doors = pygame.sprite.Group()
# bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super(Bullet, self).__init__()
        self.surf = pygame.Surface ((10,10))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect(center=(y+10,x+10))
    def shoot_up(self):
        global bullet_dir
        self.rect.move_ip(0, -25)
        if pygame.sprite.spritecollide(self, enemies, True):
            bullet_dir = [0,0,0,0]
            self.kill()
        if pygame.sprite.spritecollideany(self,walls):
            bullet_dir = [0,0,0,0]
            self.kill()
    def shoot_down(self):
        global bullet_dir
        self.rect.move_ip(0, 25)
        if pygame.sprite.spritecollide(self, enemies, True):
            bullet_dir = [0,0,0,0]
            self.kill()
        if pygame.sprite.spritecollideany(self,walls):
            bullet_dir = [0,0,0,0]
            self.kill()
    def shoot_left(self):
        global bullet_dir
        self.rect.move_ip(-25, 0)
        if pygame.sprite.spritecollide(self, enemies, True):
            bullet_dir = [0,0,0,0]
            self.kill()
        if pygame.sprite.spritecollideany(self,walls):
            bullet_dir = [0,0,0,0]
            self.kill()
    def shoot_right(self):
        global bullet_dir
        self.rect.move_ip(25, 0)
        if pygame.sprite.spritecollide(self, enemies, True):
            bullet_dir = [0,0,0,0]
            self.kill()
        if pygame.sprite.spritecollideany(self,walls):
            bullet_dir = [0,0,0,0]
            self.kill()
bullet_num = 0
bullets = pygame.sprite.Group()
        
# when starting game
def restart():
    for d in doors:
        d.kill()
    for k in keys:
        k.kill()
    for w in walls:
        w.remove_wall()
    for e in enemies:
        e.defeat_enemy()
    mazegen.goodmaze()
    key = Key()
    keys.add(key)
    all_sprites.add(key)
    door = Door()
    doors.add(door)
    all_sprites.add(door)
    for i in range(27):
        for j in range(27):
            if not mazegen.maze[i][j]:
                wall = Wall(j,i)
                walls.add(wall)
                all_sprites.add(wall)
    for i in range(len(mazegen.room_location)-1):
        enemy = Enemy(i+1)
        enemies.add(enemy)
        all_sprites.add(enemy)
restart()

playerimage = [pygame.image.load("test_oddish_2.png").convert_alpha(),pygame.image.load("test_oddish_2b.png").convert_alpha()]
framework = 0
curframe = 0
# player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        """
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((86, 229, 245))
        """
        self.surf = pygame.image.load("test_ball.png").convert_alpha()
        #self.surf = playerimage[0]
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        #picture
        self.startroom = mazegen.room_location[0]-1
        self.randomx=random.randint(-2,2)
        self.randomy=random.randint(-2,2)
        self.rect = self.surf.get_rect(center=(85+(self.startroom%3*250)+(self.randomy*25),85+(self.startroom//3*250)+(self.randomx*25)))
    def update(self,pressed_keys):
        global game_over
        global steps_taken
        global next_enemy
        #sprite animate
        global framework
        global curframe
        if framework%10 == 0:
            self.surf = playerimage[curframe%2]
            curframe = curframe + 1
        framework=framework+1
        has_moved = 0
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -25)
            if pygame.sprite.spritecollideany(player,walls):
                self.rect.move_ip(0, 25)
            else:
                pygame.event.post(MOVE)
                has_moved = 1
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 25)
            if pygame.sprite.spritecollideany(player,walls):
                self.rect.move_ip(0, -25)
            else:
                pygame.event.post(MOVE)
                has_moved = 1
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-25, 0)
            if pygame.sprite.spritecollideany(player,walls):
                self.rect.move_ip(25, 0)
            else:
                pygame.event.post(MOVE)
                has_moved = 1
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(25, 0)
            if pygame.sprite.spritecollideany(player,walls):
                self.rect.move_ip(-25, 0)
            else:
                pygame.event.post(MOVE)
                has_moved = 1
        if pressed_keys[K_SPACE]:
            pygame.event.post(MOVE)
            has_moved = 1
        if has_moved:
            if steps_taken>=next_enemy:
                pygame.event.post(ADD_E)
                steps_taken = 0
                next_enemy = random.randint(1,100)
            steps_taken += 1
        if pygame.sprite.spritecollideany(player, enemies):
            game_over = 1
    def restart(self):
        self.startroom = mazegen.room_location[0]-1
        self.randomx=random.randint(-2,2)
        self.randomy=random.randint(-2,2)
        self.rect = self.surf.get_rect(center=(85+(self.startroom%3*250)+(self.randomy*25),85+(self.startroom//3*250)+(self.randomx*25)))

player = Player()
#print(player.startroom)
all_sprites.add(player)
# clock stuff
clock = pygame.time.Clock()
MOVE_ENEMY = pygame.USEREVENT + 1
ADD_ENEMY = pygame.USEREVENT + 2
ADD_E = pygame.event.Event(ADD_ENEMY)
MOVE = pygame.event.Event(MOVE_ENEMY)
# initialize game
pygame.init()
pygame.font.init()

# font test
myfont = pygame.font.SysFont('Impact', 150)
myfont2 = pygame.font.SysFont('Verdant', 35)
myfont3 = pygame.font.SysFont('Times', 50)
textsurface = myfont.render('GAME OVER', False, (200, 0, 0))

# run the code
running = True
game_over = False
steps_taken = 0
next_enemy = random.randint(5,30)
has_key=0
LEVEL = 1
bullet_dir = [0,0,0,0]
bullet_num = 3
while running:
    #print(steps_taken)
    # mouse
    mouse = pygame.mouse.get_pos()
    # /mouse
    for event in  pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if game_over == 1 and 195+300 > mouse[0] > 195 and 480+100 > mouse[1] > 480:
                restart()
                player.restart()
                game_over = 0
                has_key = 0
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_p:
                mazegen.mazeprint()
            if event.key == K_n:
                #print (len(walls))
                restart()
                player.restart()
                game_over = 0
                has_key = 0
            #print (player.rect[0])
            #print(len(bullets))
            if event.key == K_a and bullet_num > 0:
                #print ('hi')
                if len(bullets) == 0:
                    bullet_num-=1
                    bullet = Bullet(player.rect[1],player.rect[0])
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    bullet_dir[3] = 1
            if event.key == K_w and bullet_num > 0:
                if len(bullets) == 0:
                    bullet_num-=1
                    bullet = Bullet(player.rect[1],player.rect[0])
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    bullet_dir[0] = 1
            if event.key == K_s and bullet_num > 0:
                if len(bullets) == 0:
                    bullet_num-=1
                    bullet = Bullet(player.rect[1],player.rect[0])
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    bullet_dir[2] = 1
            if event.key == K_d and bullet_num > 0:
                #print('hi')
                if len(bullets) == 0:
                    bullet_num-=1
                    bullet = Bullet(player.rect[1],player.rect[0])
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    bullet_dir[1] = 1
        elif event.type == MOVE_ENEMY:
            for e in enemies:
                e.update()
        elif event.type == ADD_ENEMY:
            for i in range(10):
                if len(enemies) < 22:
                    m_choice = random.randint(0,len(mazegen.room_location)-1)
                    #print(mazegen.room_location, m_choice)
                    new_enemy = Enemy(m_choice)
                    if not pygame.sprite.spritecollideany(new_enemy, enemies):
                        enemies.add(new_enemy)
                        all_sprites.add(new_enemy)
                        this_random_variable = 1 # whether or not the new enemy spawns close to the player
                        if player.rect[0]-30 < new_enemy.rect[0] < player.rect[0]+30 and player.rect[1]-30 < new_enemy.rect[1] < player.rect[1]+30:
                            this_random_variable = 0
                        if (not pygame.sprite.spritecollideany(player, enemies)) and this_random_variable:
                            break
                        else:
                            new_enemy.kill()
    if pygame.sprite.spritecollideany(player, enemies):
        game_over = 1
    if pygame.sprite.spritecollideany(player,keys):
        has_key = 1
        for k in keys:
            k.kill()
    if pygame.sprite.spritecollideany(player,doors) and has_key:
        LEVEL+=1
        restart()
        player.restart()
        has_key = 0
    screen.fill((179,97,59))
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    if bullet_dir[0]:
        for thing in bullets:
            thing.shoot_up()
    if bullet_dir[1]:
        for thing in bullets:
            thing.shoot_right()
    if bullet_dir[2]:
        for thing in bullets:
            thing.shoot_down()
    if bullet_dir[3]:
        for thing in bullets:
            thing.shoot_left()
    for entity in all_sprites:
        screen.blit(entity.surf,entity.rect)
    surf = pygame.Surface((670,30))
    surf.fill((0,0,0))
    rect = surf.get_rect()
    screen.blit(surf,(0,670))
    textsurface2 = myfont2.render('LEVEL: %d          Bullets: %d'%(LEVEL,bullet_num), False, (255, 255, 255))
    #print(textsurface2)
    #print('LEVEL: %d'%(LEVEL))
    screen.blit(textsurface2,(275,675))
    if game_over:
        bullet_num = 3
        screen.fill((0,0,0))
        # button
        textsurface3 = myfont3.render('RESET', False, (240, 255, 220))
        b_surf = pygame.Surface((300,100))
        if 195+300 > mouse[0] > 195 and 480+100 > mouse[1] > 480:
            b_surf.fill((18,30,115))
        else:
            b_surf.fill((47, 112, 200))
        b_rect = b_surf.get_rect()
        screen.blit(b_surf,(195,480))
        # /button
        screen.blit(textsurface3,(270,500))
        screen.blit(textsurface,(5,100))
        LEVEL = 1
    pygame.display.flip()
    clock.tick(15)
# quit everything
pygame.quit()
