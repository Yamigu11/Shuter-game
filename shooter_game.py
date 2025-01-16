from pygame import *
from random import randint
from time import sleep
window = display.set_mode((700, 500))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (780, 508))
win_width = 700
win_height= 500
lost = 0
img_bullet = 'bullet.png'


game = True
finish = False

clock = time.Clock()
FPS = 60
mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.3)
mixer.music.play()
fire_music = mixer.Sound('fire.ogg') 
lost = 0

class GameSprite(sprite.Sprite):
	def __init__(self, player_image, player_x, player_y, x_size , y_size, player_speed):
		super().__init__()
		self.image = transform.scale(image.load(player_image), (x_size, y_size))
		self.speed = player_speed
		self.rect = self.image.get_rect()
		self.rect.x = player_x
		self.rect.y = player_y
	def reset(self):
		window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet( GameSprite): 
	def update( self ): 
		self.rect.y += self.speed
		global lost
		if self.rect.y < 0 :
			self.kill()

class Player(GameSprite):
	def update(self):
		keys = key.get_pressed()
		if  keys[K_LEFT] and self.rect.x >5:
			self.rect.x -= self.speed
		if  keys[K_RIGHT] and self.rect.x < win_width - 80:
			self.rect.x += self.speed
	def fire(self):
		bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 20 , 15, -20 )
		bullets.add(bullet)


class Enemy( GameSprite): 
	def update( self ): 
		self.rect.y += self.speed
		global lost
		if self.rect.y > win_height-15 :
			self.rect.x = randint(80 , win_width - 80)
			self.rect.y = 0
			sleep(0.03)	
			lost +=1

class Asteroid( GameSprite): 
	def update( self ): 
		self.rect.y += self.speed
		if self.rect.y > win_height-15 :
			self.rect.x = randint(80 , win_width - 80)

number = 0
num_monsters = 6
num_asteroids = 3
life = 3
img_enemy = 'ufo.png'
img_asteroid = 'asteroid.png'
monsters = sprite.Group()
for i in range(1,num_monsters):
	monster = Enemy(img_enemy,randint(80 , win_width - 80), -40 , 80, 50, randint(1,num_monsters - 1))
	monsters.add(monster)
asteroids = sprite.Group()
for i in range(1,num_asteroids):
	asteroid = Asteroid(img_asteroid,randint(80 , win_width - 80), -40 , 80, 50, randint(1,num_asteroids - 1))
	asteroids.add(asteroid)
bullets = sprite.Group()

font.init()
font1 = font.SysFont('Arial', 36)
font = font.SysFont('Arial', 70)

player  = Player("rocket.png", 320, win_height - 80 ,65, 65, 4)

while game:
	window.blit(background, (0,0))
	player.reset()
	player.update()
	text_lose = font1.render('Пропущено: '+ str(lost),1, (100,100,100))
	text_win = font1.render('Счёт:'+ str(number),1, (100,100,100))
#	text_life = font1.render('Жизни:'+ str(life),1, (100,100,100))
	window.blit(text_lose,(20, 20))
	window.blit(text_win, (20,50))
#	window.blit(text_life, (20,80))
	monsters.update()
	monsters.draw(window)
	asteroids.update()
	asteroids.draw(window)
	bullets.update()
	bullets.draw(window)
	colides = sprite.groupcollide(monsters, bullets, True, True)
	sprites_list = sprite.spritecollide(player,monsters,False)
	spriteas = sprite.spritecollide(player,asteroids,False) 
	collides = sprite.groupcollide(asteroids, bullets, False, True)
	for e in event.get():
		if e.type == QUIT:
			game = False
		elif e.type == KEYDOWN:
			if e.key == K_SPACE:
				player.fire()
				fire_music.play() 
	if lost >= 5:
		LOSE = font.render('Ты проиграл!' , True , (255, 0, 0))
		window.blit(LOSE,(200,200))
		game = False
	elif number >= 7:
		WIN = font.render('Ты выиграл!' , True , (0, 250, 0))
		window.blit(WIN,(200,200))
		game = False
	for c in colides:
		number +=1
		monster = Enemy(img_enemy,randint(80 , win_width - 80), -40 , 80, 50, randint(1,num_monsters - 1))
		monsters.add(monster)
	for s in sprites_list:
		LOSE = font.render('Ты проиграл!' , True , (255, 0, 0))
		window.blit(LOSE,(200,200))
		game = False	
	for sp in spriteas:
		LOSE = font.render('Ты проиграл!' , True , (255, 0, 0))
		window.blit(LOSE,(200,200))
		game = False

	display.update()
	clock.tick(FPS)
sleep(1.5)