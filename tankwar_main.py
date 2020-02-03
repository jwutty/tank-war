import pygame,time,random
from pygame.sprite import Sprite
#tank war
_display = pygame.display
COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_RED = pygame.Color(255, 0, 0)

class Main():
    #Display window
    window = None
    SCREEN_HEIGHT = 500
    SCREEN_WIDTH = 800
    #Initialize player tank
    TANK_P1 = None
    #Enemy tanks
    EnemyTank_list = []
    EnemyTank_count = 5

    Bullet_list = []
    Enemy_bullet_list = []
    Explosion_list = []
    Wall_list = []
    def __init__(self):
        pass

    def startGame(self):
        _display.init()

        Main.window = _display.set_mode([Main.SCREEN_WIDTH,Main.SCREEN_HEIGHT])
        self.creatMyTank()
        self.creatEnemyTank()
        self.creatWalls()
        _display.set_caption("Tank War")
        #main loop
        while True:
            if len(Main.EnemyTank_list)==0:
                Main.window.blit(self.getTextSurface("You win!"), (200, 200))
                time.sleep(2)
                exit()
            time.sleep(0.02)
            Main.window.fill(COLOR_BLACK)
            self.getEvent()
            Main.window.blit(self.getTextSurface("%d Enemy Remaining"%len(Main.EnemyTank_list)),(10,10))
            self.blitWalls()
            if Main.TANK_P1 and Main.TANK_P1.alive:
                Main.TANK_P1.displayTank()
            else:
                del Main.TANK_P1
                Main.TANK_P1 = None

            self.blitEnemyTank()
            if Main.TANK_P1 and not Main.TANK_P1.stop:
                Main.TANK_P1.move()
                Main.TANK_P1.hitWalls()
                Main.TANK_P1.hitEnemyTank()
            self.blitBullet()
            self.blitEnemyBullet()
            self.displayExplosions()
            if Main.TANK_P1 and Main.TANK_P1.alive:
                if not Main.TANK_P1.stop:
                    Main.TANK_P1.move()
                    Main.TANK_P1.hitWalls()
                    Main.TANK_P1.hitEnemyTank()
            time.sleep(0.02)
            #refresh
            _display.update()



    def creatMyTank(self):
        Main.TANK_P1 = MyTank(400, 300)
        music = Music('img/start.wav')
        music.play()

    def creatEnemyTank(self):
        top = 100
        for i in range(Main.EnemyTank_count):
            speed = random.randint(1,6)
            left = random.randint(0, 600)
            enemy = EnemyTank(left,top,speed)
            Main.EnemyTank_list.append(enemy)

    def creatWalls(self):
        for i in range(6):
            wall = Wall(130*i,240)
            Main.Wall_list.append(wall)
    def blitWalls(self):
        for wall in Main.Wall_list:
            if wall.alive:
                wall.displayWall()
            else:
                Main.Wall_list.remove(wall)
    #display enemy tanks
    def blitEnemyTank(self):
        for enemy in Main.EnemyTank_list:
            if enemy.alive:
                enemy.displayTank()
                #randomly move
                enemy.randMove()
                enemy.hitWalls()
                enemy.hitMyTank()
                eBullet = enemy.fire()
                if eBullet:
                    Main.Enemy_bullet_list.append(eBullet)
            else:
                Main.EnemyTank_list.remove(enemy)

    #display player tank's bullet
    def blitBullet(self):
        for bullet in Main.Bullet_list:
            if bullet.alive:
                bullet.displayBullet()
                bullet.bulletMove()
                bullet.hitEnemyTank()
                bullet.hitWalls()
            else:
                Main.Bullet_list.remove(bullet)

    #display enemy tanks' bullets
    def blitEnemyBullet(self):
        for eBullet in Main.Enemy_bullet_list:
            if eBullet.alive:
                eBullet.displayBullet()
                eBullet.bulletMove()
                eBullet.hitWalls()
                if Main.TANK_P1 and Main.TANK_P1.alive:
                    eBullet.hitMyTank()
            else:
                Main.Enemy_bullet_list.remove(eBullet)

    #display explosions
    def displayExplosions(self):
        for Explosion in Main.Explosion_list:
            if Explosion.alive:
                Explosion.displayExplosion()
            else:
                Main.Explosion_list.remove(Explosion)

    #get keyboard events
    def getEvent(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                self.endGame()
            if event.type == pygame.KEYDOWN:
                #Respawn tank by pressing ESC
                if event.key == pygame.K_ESCAPE and not Main.TANK_P1:
                    self.creatMyTank()
                if Main.TANK_P1 and Main.TANK_P1.alive:
                    # Other key events
                    if event.key == pygame.K_LEFT:
                        print("Moving left")
                        Main.TANK_P1.direction = 'L'
                        Main.TANK_P1.stop = False
                    elif event.key == pygame.K_RIGHT:
                        print("Moving right")
                        Main.TANK_P1.direction = 'R'
                        Main.TANK_P1.stop = False
                    elif event.key == pygame.K_UP:
                        print("Moving up")
                        Main.TANK_P1.direction = 'U'
                        Main.TANK_P1.stop = False
                    elif event.key == pygame.K_DOWN:
                        print("Moving down")
                        Main.TANK_P1.direction = 'D'
                        Main.TANK_P1.stop = False
                    elif event.key == pygame.K_SPACE:
                        print("FIRE!")
                        if len(Main.Bullet_list) < 3:
                            m = Bullet(Main.TANK_P1)
                            Main.Bullet_list.append(m)
                            music = Music('img/fire.wav')
                            music.play()
                        else:
                            print("Not enough ammo")
                        print("Ammo left:%d" % (3-len(Main.Bullet_list)))
            #End game
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    if Main.TANK_P1 and Main.TANK_P1.alive:
                        Main.TANK_P1.stop = True
    #display text
    def getTextSurface(self,text):
        pygame.font.init()
        font = pygame.font.SysFont('Arial',18)
        textSurface = font.render(text,True,COLOR_RED)
        return textSurface
    def endGame(self):
        print("GG")
        exit()
class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
class Tank(BaseItem):
    def __init__(self,left,top):
        #display direction of tank's movement
        self.images = {
            'U':pygame.image.load('img/p1tankU.gif'),
            'D':pygame.image.load('img/p1tankD.gif'),
            'L':pygame.image.load('img/p1tankL.gif'),
            'R':pygame.image.load('img/p1tankR.gif')
        }
        self.direction = 'U'
        self.image = self.images[self.direction]
        #get tank's position
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top

        self.speed = 5
        #stop accounts whether a tnak can move
        self.stop = True
        #alive accounts whether a tank is alive
        self.alive = True
        #records the tank's position if needs to reposition to the last position
        self.lastLeft = self.rect.left
        self.lastTop = self.rect.top

    #Move the tanks
    def move(self):
        #move the last position to the current position
        self.lastLeft = self.rect.left
        self.lastTop = self.rect.top
        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left + self.rect.height < Main.SCREEN_WIDTH:
                self.rect.left += self.speed
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < Main.SCREEN_HEIGHT:
                self.rect.top += self.speed

    #stay at the currrent position
    def stay(self):
        self.rect.left = self.lastLeft
        self.rect.top = self.lastTop

    #stay in place if moves to a wall
    def hitWalls(self):
       for wall in Main.Wall_list:
           if pygame.sprite.collide_rect(wall,self):
               self.stay()

    def fire(self):
        return Bullet(self)

    def displayTank(self):
        self.image = self.images[self.direction]
        Main.window.blit(self.image,self.rect)
class MyTank(Tank):
    def __init__(self,left,top):
        super(MyTank, self).__init__(left,top)
    def hitEnemyTank(self):
        for tank in Main.EnemyTank_list:
            if pygame.sprite.collide_rect(tank,self):
                self.stay()

class EnemyTank(Tank):
    def __init__(self,left,top,speed):
        super(EnemyTank, self).__init__(left,top)
        # self.alive = True
        self.images = {
            'U': pygame.image.load('img/enemy1U.gif'),
            'D': pygame.image.load('img/enemy1D.gif'),
            'L': pygame.image.load('img/enemy1L.gif'),
            'R': pygame.image.load('img/enemy1R.gif')
        }
        self.direction = self.randDirection()
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = speed
        self.stop = True
        self.step = 30

    def randDirection(self):
        num = random.randint(1,4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        elif num == 4:
            return 'R'

    def randMove(self):
        if self.step <= 0:
            self.direction = self.randDirection()
            self.step = 50
        else:
            self.move()
            self.step -= 1
    def fire(self):
        num = random.randint(1,1000)
        if num  <= 20:
            return Bullet(self)
    def hitMyTank(self):
        if Main.TANK_P1 and Main.TANK_P1.alive:
            if pygame.sprite.collide_rect(self, Main.TANK_P1):
                self.stay()

class Bullet(BaseItem):
    def __init__(self,tank):

        self.image = pygame.image.load('img/enemymissile.gif')

        self.direction = tank.direction
        #positioning
        self.rect = self.image.get_rect()
        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width/2 - self.rect.width/2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2

        self.speed = 7
        self.alive = True

    #Move the bullet
    def bulletMove(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.alive = False
        elif self.direction == 'D':
            if self.rect.top < Main.SCREEN_HEIGHT - self.rect.height:
                self.rect.top += self.speed
            else:
                self.alive = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.alive = False
        elif self.direction == 'R':
            if self.rect.left < Main.SCREEN_WIDTH - self.rect.width:
                self.rect.left += self.speed
            else:
                self.alive = False

    def displayBullet(self):
        Main.window.blit(self.image,self.rect)

    def hitEnemyTank(self):
        for enemy in Main.EnemyTank_list:
            if pygame.sprite.collide_rect(enemy,self):
                #create an explosion
                explosion = Explosion(enemy)
                Main.Explosion_list.append(explosion)
                self.alive = False
                enemy.alive = False

    def hitMyTank(self):
        if pygame.sprite.collide_rect(self,Main.TANK_P1):
            explosion = Explosion(Main.TANK_P1)
            Main.Explosion_list.append(explosion)
            self.alive = False
            Main.TANK_P1.alive = False

    def hitWalls(self):
        for wall in Main.Wall_list:
            if pygame.sprite.collide_rect(wall,self):
                self.alive = False
                wall.hp -= 1
                if wall.hp <= 0:
                    wall.alive = False

class Explosion():
    def __init__(self,tank):
        self.rect = tank.rect
        self.step = 0
        self.images = [
            pygame.image.load('img/blast0.gif'),
            pygame.image.load('img/blast1.gif'),
            pygame.image.load('img/blast2.gif'),
            pygame.image.load('img/blast3.gif'),
            pygame.image.load('img/blast4.gif')
        ]
        self.image = self.images[self.step]
        self.alive = True

    def displayExplosion(self):
        if self.step < len(self.images):
            Main.window.blit(self.image, self.rect)
            self.image = self.images[self.step]
            self.step += 1
        else:
            self.alive = False
            self.step = 0

class Wall():
    def __init__(self,left,top):
        self.image = pygame.image.load('img/steels.gif')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.alive = True
        #number of hits to destroy
        self.hp = 3

    def displayWall(self):
        Main.window.blit(self.image,self.rect)

class Music():
    def __init__(self,fileName):
        self.fileName = fileName
        pygame.mixer.init()
        pygame.mixer.music.load(self.fileName)

    def play(self):
        pygame.mixer.music.play()

Main().startGame()
