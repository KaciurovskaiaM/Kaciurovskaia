import pygame
import sys
from pygame.locals import *

DISPLAYWIDTH = 640
DISPLAYHEIGHT = 480

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
ORANGE = (255, 128, 0)

BGCOLOR = BLACK
BLOCKGAP = 2
BLOCKWIDTH = 62
BLOCKHEIGHT = 25
ARRAYWIDTH = 10
ARRAYHEIGHT = 5
PADDLEWIDTH = 100
PADDLEHEIGHT = 10
BALLRADIUS = 20
BALLCOLOR = WHITE
BLOCK = 'block'
BALL = 'ball'
PADDLE = 'paddle'
BUTTON = 'button'
BALLSPEED = [0.1, 0.2, 0.4, 0.75, 1, 1.5]
SPEEDSTR = ['0', '1', '2', '3', '4', '5']
BUTTONWIDTH = 200
BUTTONHEIGHT = 100


class Block(pygame.sprite.Sprite):

	def __init__(self):
		self.blockWidth = BLOCKWIDTH
		self.blockHeight = BLOCKHEIGHT
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((self.blockWidth, self.blockHeight))
		self.image.fill(WHITE)
		self.rect = self.image.get_rect()
		self.name = BLOCK


class Ball(pygame.sprite.Sprite):
	def __init__(self, displaySurf):
		pygame.sprite.Sprite.__init__(self)
		self.name = BALL
		self.moving = False
		self.image = pygame.Surface((16, 16))
		# self.image.fill(ORANGE)
		pygame.draw.circle(self.image,ORANGE , (8,8), 8)
		self.rect = self.image.get_rect()
		#self.rect = self.image.get_circle()
		self.speed = 2
		self.vectorx = BALLSPEED[self.speed]
		self.vectory = BALLSPEED[self.speed] * -1
		self.x = self.rect.x
		self.y = self.rect.y
		print(self.vectorx, self.vectory)
		self.score = 0

	def update(self, mousex, blocks, paddle, *args):
		if self.moving == False:
			self.rect.centerx = mousex
			self.x = self.rect.x
			self.y = self.rect.y

		else:
			print(self.x, self.y)
			print(self.vectorx, self.vectory)
			self.y += self.vectory

			hitGroup = pygame.sprite.Group(paddle, blocks)

			spriteHitList = pygame.sprite.spritecollide(self, hitGroup, False)
			if len(spriteHitList) > 0:
				for sprite in spriteHitList:
					if sprite.name == BLOCK:
						sprite.kill()
						self.score += 1
				self.vectory *= -1
				self.y = self.rect.y
				self.y += self.vectory

			self.x += self.vectorx

			blockHitList = pygame.sprite.spritecollide(self, blocks, True)

			if len(blockHitList) > 0:
				self.vectorx *= -1
				self.score += 1

			if self.rect.right > DISPLAYWIDTH:
				self.vectorx *= -1
				self.x = DISPLAYWIDTH - self.rect.w

			if self.rect.left < 0:
				self.vectorx *= -1
				self.x = self.rect.w

			if self.rect.top < 0:
				self.vectory *= -1
				self.rect.top = 0
				self.y = self.rect.y

			self.rect.x = self.x
			self.rect.y = self.y

	def sign(self, x):
		return 1 if x > 0 else -1

	def change_speed(self, sign):
		self.speed += sign
		if self.speed >= len(BALLSPEED):
			self.speed = len(BALLSPEED) - 1
		if self.speed < 0:
			self.speed = 0

		self.vectorx = BALLSPEED[self.speed] * self.sign(self.vectorx)
		self.vectory = BALLSPEED[self.speed] * self.sign(self.vectory)
		


class Paddle(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((PADDLEWIDTH, PADDLEHEIGHT))
		self.image.fill(WHITE)
		self.rect = self.image.get_rect()
		self.name = PADDLE

	def update(self, mousex, *args):
		if self.rect.x >= 0 and self.rect.right <= DISPLAYWIDTH:
			self.rect.centerx = mousex

		if self.rect.x < 0:
			self.rect.x = 0

		elif self.rect.right > DISPLAYWIDTH:
			self.rect.right = DISPLAYWIDTH


class Score(object):
	def __init__(self):
		self.score = 0
		self.font = pygame.font.SysFont('Helvetica', 25)
		self.render = self.font.render('Score: ' + str(self.score), True, WHITE, BLACK)
		self.rect = self.render.get_rect()
		self.rect.x = 0
		self.rect.bottom = DISPLAYHEIGHT

class Speed(object):
	def __init__(self):
		self.speed = 0
		self.font = pygame.font.SysFont('Helvetica', 25)
		self.render = self.font.render('Speed: ' + str(SPEEDSTR[self.speed]), True, WHITE, BLACK)
		self.rect = self.render.get_rect()
		self.rect.right = DISPLAYWIDTH
		self.rect.bottom = DISPLAYHEIGHT

class App(object):
	def __init__(self):
		pygame.init()
		self.displaySurf, self.displayRect = self.makeScreen()
		self.mousex = 0
		self.blocks = self.createBlocks()
		self.paddle = self.createPaddle()
		self.ball = self.createBall()
		self.score = Score()
		self.speed = Speed()

		self.allSprites = pygame.sprite.Group(self.blocks, self.paddle, self.ball)

	def updateSpeed(self):
		self.speed.score = self.ball.speed
		self.speed.render = self.speed.font.render('Speed: ' + str(self.speed.speed), True, WHITE, BLACK)
		self.speed.rect = self.speed.render.get_rect()
		self.speed.rect.right = DISPLAYWIDTH - 10
		self.speed.rect.bottom = DISPLAYHEIGHT
	
	def updateScore(self):
		self.score.score = self.ball.score
		self.score.render = self.score.font.render('Score: ' + str(self.score.score), True, WHITE, BLACK)
		self.score.rect = self.score.render.get_rect()
		self.score.rect.x = 0
		self.score.rect.bottom = DISPLAYHEIGHT

	def makeScreen(self):
		pygame.display.set_caption('Arkanoid')
		displaySurf = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT))
		displayRect = displaySurf.get_rect()
		displaySurf.fill(BGCOLOR)
		displaySurf.convert()

		return displaySurf, displayRect

	def createBall(self):
		ball = Ball(self.displaySurf)
		ball.rect.centerx = self.paddle.rect.centerx
		ball.rect.bottom = self.paddle.rect.top

		return ball

	def createPaddle(self):
		paddle = Paddle()
		paddle.rect.centerx = self.displayRect.centerx
		paddle.rect.bottom = self.displayRect.bottom

		return paddle

	def createBlocks(self):
		blocks = pygame.sprite.Group()

		for row in range(ARRAYHEIGHT):
			for i in range(ARRAYWIDTH):
				block = Block()
				block.rect.x = i * (BLOCKWIDTH + BLOCKGAP)
				block.rect.y = row * (BLOCKHEIGHT + BLOCKGAP)
				block.color = self.setBlockColor(block, row, i)
				block.image.fill(block.color)
				blocks.add(block)

		return blocks

	def setBlockColor(self, block, row, column):
		if (row % 2 == 0 and column % 2 ==0) or (row % 2 != 0 and column % 2 !=0):
			return YELLOW
		else:
			return RED

	def checkInput(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.terminate()

			if event.type == MOUSEMOTION:
				self.mousex = event.pos[0]

			elif event.type == KEYUP:
				if event.key == K_SPACE:
					self.ball.moving = True
				elif event.key == K_RETURN:
					self.__init__()
				elif event.key == K_q:
					self.terminate()
				elif event.key == K_PLUS:
					self.ball.change_speed(1)
				elif event.key == K_EQUALS:
					self.ball.change_speed(1)
				elif event.key == K_MINUS:
					self.ball.change_speed(-1)
				self.speed.speed = self.ball.speed
				self.updateSpeed()

	def terminate(self):
		pygame.quit()
		sys.exit()


	def mainLoop(self):
		while True:
			self.displaySurf.fill(BGCOLOR)
			self.updateScore()
			self.updateSpeed()
			self.displaySurf.blit(self.score.render, self.score.rect)
			self.displaySurf.blit(self.speed.render, self.speed.rect)
			self.allSprites.update(self.mousex, self.blocks, self.paddle)
			self.allSprites.draw(self.displaySurf)
			pygame.display.update()
			self.checkInput()


runGame = App()
runGame.mainLoop()
