import pygame
from openPhase4 import *
from movingPhase4 import *
from time import sleep
import subprocess as sb
 
pygame.init()

screen = pygame.display.set_mode((500, 630))
background_color = (255,228,196)
pygame.display.set_caption("MLYNEK")

#images
boardImg = pygame.image.load('static/board4.jpg')
white = pygame.image.load('static/white1.jpg')
black = pygame.image.load('static/black1.jpg')
highImg = pygame.image.load('static/high.png')
roboImg = pygame.image.load('static/robo1.jpg')
back =pygame.image.load('static/backbutton1.png')

mul = 500/840
coords = {
	0: (70, 720, 120, 770),
	1: (770, 720, 820, 770),
	2: (180, 610, 230, 660),
	3: (660, 610, 710, 660),
	4: (300, 490, 350, 540),
	5: (540, 490, 590, 540),
	6: (70, 375, 120, 425),
	7: (180, 375, 230, 425),
	8: (300, 375, 350, 425),
	9: (540, 375, 590, 425),
	10: (660, 375, 710, 425),
	11: (770, 375, 820, 425),
	12: (300, 260, 350, 310),
	13: (420, 260, 470, 310),
	14: (540, 260, 590, 310),
	15: (180, 140, 230, 190),
	16: (420, 140, 470, 190),
	17: (660, 140, 710, 190),  
	18: (70, 30, 120, 80),
	19: (420, 30, 470, 80),
	20: (770, 30, 820, 80),
	21: (420, 490, 470, 540),
	22: (420, 610, 470, 660),
	23: (420, 720, 470, 770),
	24: (370, 375, 420, 425),
	25: (420, 310, 470, 360),
	26: (480, 375, 520, 425),
	27: (420, 430, 470, 480),
	28: (370, 310, 420, 360),
	29: (480, 310, 520, 360),
	30: (480, 430, 520, 480),
	31: (370, 430, 420, 480)
}

back_co = {
	0: (225,580,226,581)
}

clickables = [pygame.Rect(mul*c[0], mul*c[1], 35, 35) for c in coords.values()]
clickss = [pygame.Rect(c[0], c[1], 50, 30) for c in back_co.values()]

board = list('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

turn = 2
v = 0

running = True
mill = False
played = False
moveLoc = None

MAX = 50000

Game = MiniMaxOpening(9, turn)

Font = pygame.font.SysFont('Roboto Mono',  30)
roboFont = pygame.font.SysFont('Roboto Mono',  25)

openingText = Font.render("AI=W     Human=B", False, (0,0,0))
waitText = roboFont.render(" : My turn, let me think . . . .", False, (0,0,0))
millText = roboFont.render(" : Ah! Mill! Go ahead and remove my piece", False, (0,0,0))
openingRobo = roboFont.render(" : Place a piece on any empty vertice", False, (0,0,0))
middleRobo = roboFont.render(" : Click on your piece and move to an adjacent spot", False, (0,0,0))
endGameRobo = roboFont.render(" : Click on your piece and move to any spot", False, (0,0,0))
overRobo1 = roboFont.render(" : Game Over. Press R to restart", False, (0,0,0))


text_rect = openingText.get_rect(center=(250, 510))

selectMove = False
availableShifts = []
endGame = False
gameComplete = 0


fps = 20
clock = pygame.time.Clock()

def checkEndgame():
	global endGame
	endGame = False
	cnt , cnt1=0,0
	for b in board:
		if b == 'B':
			cnt += 1
		if b == 'W':
			cnt1 += 1
	if cnt == 3 or cnt1==3:
		endGame = True

def checkGameComplete():
	global gameComplete

	if turn > 18:
		cnt1, cnt2 = 0, 0
		for b in board:
			if b == 'B':
				cnt1 += 1
			if b == 'W':
				cnt2 += 1
		if cnt2 < 3:
			gameComplete = -1 
		if cnt1 < 3:
			gameComplete = 1

		Game = MiniMaxGame(3)
		
		if Game.GenerateMovesMidgameEndgame(board, True) == []:
			gameComplete = -1
		if Game.GenerateMovesMidgameEndgame(board) == []:
			gameComplete = 1


def drawBoard():
	global availableShifts, mill, moveLoc
	if selectMove:
		if endGame:
			availableShifts = []
			for loc in range(len(board)):
				if board[loc] == 'x':
					availableShifts.append(loc)
					x = mul*coords[loc][0] - 5
					y = mul*coords[loc][1] - 5
					screen.blit(highImg,(x, y))

		else:
			n = Game.neighbors[moveLoc]
			availableShifts = []
			for j in n:
				if board[j] == 'x':
					availableShifts.append(j)
					x = mul*coords[j][0] - 5
					y = mul*coords[j][1] - 5
					screen.blit(highImg,(x, y))		


	if mill:
		cnt = 0
		for loc in range(len(board)):
			if board[loc] == 'W':
				if not Game.closeMill(loc, board):
					x = mul*coords[loc][0] - 5
					y = mul*coords[loc][1] - 5
					screen.blit(highImg,(x, y))
					cnt += 1
		if cnt == 0:
			moveLoc = None
			mill = False

	
	for loc in range(len(board)):
		if board[loc] == 'W':
			x = mul*coords[loc][0]
			y = mul*coords[loc][1]
			screen.blit(white,(x, y))
		if board[loc] == 'B':
			x = mul*coords[loc][0]
			y = mul*coords[loc][1]
			screen.blit(black,(x, y))


def drawText():
	screen.blit(roboImg, (10, 540))
	screen.blit(openingText,text_rect)
	
	if gameComplete == 1:
		screen.blit(overRobo1, (50, 550))
	if gameComplete == -1:
		screen.blit(overRobo1, (50, 550))

	else:
		if played and (not mill):
			screen.blit(waitText, (50, 550))

		elif mill:
			screen.blit(millText, (50, 550))

		else:
			if turn <= 18:
				screen.blit(openingRobo, (50, 550))
			elif endGame:
				screen.blit(endGameRobo, (50, 550))
			elif not gameComplete:
				screen.blit(middleRobo, (50, 550))


while running:
	screen.fill(background_color)
	screen.blit(boardImg, (0, 0))
	screen.blit(back,(225,580))
	checkEndgame()
	checkGameComplete()
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1: 
				for i, area in enumerate(clickss):
					if area.collidepoint(event.pos):
						sb.Popen(["python", "UI.py"])
						# pygame.quit()
						event.type=pygame.QUIT
						running = False
						break
						# print(clickss[i])

		# opening
		if (not mill) and turn <= 18 and event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				for i, area in enumerate(clickables):
					if area.collidepoint(event.pos):
						board[i] = 'B'
						played = True
						moveLoc = i
		
		# midgame
		if selectMove and turn > 18 and event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				for i, area in enumerate(clickables):
					if area.collidepoint(event.pos):
						if i in availableShifts:
							board[i] = 'B'
							board[moveLoc] = 'x'
							played = True
							turn += 2
							moveLoc = i
							selectMove = False


		if (not played) and (not mill) and turn > 18 and event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				for i, area in enumerate(clickables):
					if area.collidepoint(event.pos):
						if board[i] == 'B':
							turn += 2
							moveLoc = i
							selectMove = True
		
		
		# mill logic
		if mill and event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				for i, area in enumerate(clickables):
					if area.collidepoint(event.pos):
						if board[i] == 'W':
							board[i] = 'x'
							mill = False
							moveLoc = None

		# restart logic
		if gameComplete != 0 and event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				sb.Popen(["python", "UI.py"])
				pygame.quit()

	drawBoard()
	drawText()
	
	pygame.display.update()
	clock.tick(fps)


	if played and (not mill) and (not selectMove):
		if moveLoc and Game.closeMill(moveLoc, board):
			mill = True
			continue

	if turn <= 18 and (not mill) and played:
		Game = MiniMaxOpening(7, turn)


		root = Node(board, turn)
		v = Game.MaxMin(root, -MAX, MAX)
		board = Game.bestResponse
		played = False
		turn += 2

	if turn >= 18 and (not mill) and (not selectMove) and played:
		if endGame:
			Game = MiniMaxGame(4)
		else:
			Game = MiniMaxGame(5)
		
		root = Node(board, 0)
		v = Game.MaxMin(root, -MAX, MAX)
		
		if v == float('inf'):
			Game = MiniMaxGame(3)
			root = Node(board, 0)
			v = Game.MaxMin(root, -MAX, MAX)
		
		board = Game.bestResponse
		played = False
		turn += 2



