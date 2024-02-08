import sys

class Node:
	def __init__(self, board, depth):
		self.position = board
		self.depth = depth
		self.code = ''.join(board)

class MiniMaxGame:
	def __init__(self, maxDepth):
		self.evaluatedPositions = 0
		self.bestResponse = None
		self.maxDepth = maxDepth
 
		self.neighbors = {
			0: [2,6,23],
			1: [3,11,23],
			2: [0,4,7,22],
			3: [1,5,10,22],
			4: [2,8,21,31],
			5: [3,9,21,30],
			6: [0, 7, 18],
			7: [2, 6, 8, 15],
			8: [4, 7, 12,24],
			9: [5, 10, 14,26],
			10: [3, 9, 11, 17],
			11: [1, 10, 20],
			12: [8,13,15,28],
			13: [12, 14, 16,25],
			14: [9, 13,17,29],
			15: [7, 16, 18,12],
			16: [13, 15, 17, 19],
			17: [10, 16, 20,14],
			18: [6, 19, 15],
			19: [16, 18, 20],
			20: [11, 19, 17],
			21: [4,5,22,27],
			22: [2,3,21,23],
			23: [0,1,22],
			24: [28,31,8],
			25: [28,29,13],
			26: [9,29,30],
			27: [30,31,21],
			28: [24,25,12],
			29: [25,26,14],
			30: [5,27,26],
			31: [24,27,4]
		}

		self.checkMillMap = {
			0: [[6,18],[2,4,31],[1,23]],
			1: [[11,20],[0,23],[3,5,30]],
			2: [[7,15],[0,4,31],[3,22]],
			3: [[10,17],[2,22],[1,5,30]],
			4: [[0,2,31],[8,12],[5,21]],
			5: [[9,14],[4,21],[1,3,30]],
			6: [[0,18],[7,8,24]],
			7: [[6,8,24],[2,15]],
			8: [[6,7,24],[4,12]],
			9: [[5,14],[10,11,26]],
			10: [[9,11,26],[3,17]],
			11: [[9,10,26],[1,20]],
			12: [[8,4],[13,14],[15,18,28]],
			13: [[12,14],[16,19,25]],
			14: [[5,9],[12,13],[17,20,29]],
			15: [[2,7],[16,17],[12,18,28]],
			16: [[15,17],[13,19,25]],
			17: [[15,16],[10,3],[14,20,29]],
			18: [[0,6],[19,20],[12,15,28]],
			19: [[13,16,25],[18,20]],
			20: [[18,19],[11,1],[14,17,29]],
			21: [[23,22,27],[4,5]],
			22: [[2,3],[21,23,27]],
			23: [[0,1],[21,22,27]],
			24: [[28,31],[6,7,8]],
			25: [[28,29],[13,16,19]],
			26: [[29,30],[9,10,11]],
			27: [[30,31], [21,22,23]],
			28: [[24,31],[25,29],[12,15,18]],
			29: [[25,28],[26,30],[14,17,20]],
			30: [[27,31],[26,29],[1,3,5]],
			31: [[24,28],[27,30],[0,2,4]]
		}


		
	def closeMill(self, j, b):
		
		for millNeighbors in self.checkMillMap[j]:
			if len(millNeighbors)==2:
				if (b[millNeighbors[0]] == b[j]) and (b[millNeighbors[1]] == b[j]):
					return True
			elif len(millNeighbors)==3:
				if (b[millNeighbors[0]] == b[j]) and (b[millNeighbors[1]] == b[j]) and (b[millNeighbors[2]] == b[j]):
					return True
		return False


	def possibleMill(self, j, b):
		for millNeighbors in self.checkMillMap[j]:
			if len(millNeighbors)==2:
				if (b[millNeighbors[0]] == b[j]) and (b[millNeighbors[1]] == 'x'):
					return True
				if (b[millNeighbors[0]] == 'x') and (b[millNeighbors[1]] == b[j]):
					return True
			elif len(millNeighbors)==3:
				if (b[millNeighbors[0]] == 'x') and (b[millNeighbors[1]] == b[j]) and (b[millNeighbors[2]] == b[j]):
					return True
				if (b[millNeighbors[0]] == b[j]) and (b[millNeighbors[1]] == 'x') and (b[millNeighbors[2]] == b[j]):
					return True
				if (b[millNeighbors[0]] == b[j]) and (b[millNeighbors[1]] == b[j]) and (b[millNeighbors[2]] == 'x'):
					return True
		return False


	def countMills(self, board):
		numBlackCloseMills = 0
		numWhiteCloseMills = 0
		numPotBlackCloseMills = 0
		numPotWhiteCloseMills = 0

		for loc in range(len(board)):
			if board[loc] == 'W':
				if self.closeMill(loc, board):
					numWhiteCloseMills += 1
				if self.possibleMill(loc, board):
					numPotWhiteCloseMills += 1
			if board[loc] == 'B':
				if self.closeMill(loc, board):
					numBlackCloseMills += 1
				if self.possibleMill(loc, board):
					numPotBlackCloseMills += 1
		
		return numWhiteCloseMills, numBlackCloseMills, \
			numPotWhiteCloseMills, numPotBlackCloseMills


	def countPieces(self, board):
		numWhitePieces = 0
		numBlackPieces = 0

		for b in board:
			if b=='W':
				numWhitePieces += 1
			if b=='B':
				numBlackPieces += 1

		return numWhitePieces, numBlackPieces

	def checkBlocked(self, board, loc):
		res = True
		n = self.neighbors[loc]
		for ni in n:
			if board[ni] == 'x':
				res = False
		return res

	def blocked(self, board):
		whiteBlocked = 0
		blackBlocked = 0

		for loc in range(len(board)):
			if board[loc] == 'W':
				if self.checkBlocked(board, loc):
					whiteBlocked += 1
			if board[loc] == 'B':
				if self.checkBlocked(board, loc):
					blackBlocked += 1
		
		return whiteBlocked - blackBlocked	

	def static(self, board):
		numWhitePieces = 0
		numBlackPieces = 0
		for b in board:
			if b=='W':
				numWhitePieces += 1
			if b=='B':
				numBlackPieces += 1

		numBlackMoves = len(self.GenerateMovesMidgameEndgame(board, True))

		numWhiteCloseMills, numBlackCloseMills, \
		numPotWhiteCloseMills, numPotBlackCloseMills = self.countMills(board)

		if numBlackPieces <= 2:
			return 10000
		elif numWhitePieces <= 2:
			return -10000
		elif numBlackMoves == 0:
			return 10000
		else:
			return 100 * ((numWhitePieces - numBlackPieces) + \
				3*(numWhiteCloseMills - numBlackCloseMills) + \
				2*(numPotWhiteCloseMills - numPotBlackCloseMills) + \
				self.blocked(board)) - numBlackMoves


	def MinMax(self, x, alpha, beta):
		depth = x.depth
		if self.maxDepth == depth:
			self.evaluatedPositions += 1
			return self.static(x.position)

		
		v = 50000 - depth
		children = self.GenerateMovesMidgameEndgame(x.position, switchColor=True)

		for y in children:
			node_y = Node(y, depth+1)
			v = min(v, self.MaxMin(node_y, alpha, beta))
			
			if v <= alpha:
				return v
			else:
				beta = min(v,beta)
		return v


	def MaxMin(self, x, alpha, beta):
		depth = x.depth
		if self.maxDepth == depth:
			self.evaluatedPositions += 1
			return self.static(x.position)
		
		v = -50000 + depth
		children = self.GenerateMovesMidgameEndgame(x.position)

		for y in children:
			node_y = Node(y, depth+1)
			tmpV = v
			v = max(v, self.MinMax(node_y, alpha, beta))
			
			if v > tmpV and node_y.depth==1:
					self.bestResponse = y
			
			if v >= beta:
				return v
			else:
				alpha = max(v,alpha)

		return v


	def switchColors(self, board):
		for i in range(len(board)):
			if type(board[i]) == list:
				for j in range(len(board[i])):
					if board[i][j] == 'W':
						board[i][j] = 'B'
					elif board[i][j] == 'B':
						board[i][j] = 'W'

			else:
				if board[i] == 'W':
					board[i] = 'B'
				elif board[i] == 'B':
					board[i] = 'W'
		return board



	def GenerateRemove(self, board, L):
		numPositions = 0

		for loc in range(len(board)):
			if board[loc] == 'B':
				if not self.closeMill(loc, board):
					b = board.copy()
					b[loc] = 'x'
					L.append(b)
					numPositions += 1

		if numPositions == 0:
			L.append(board.copy())


	def GenerateAdd(self, board):
		L = []

		for loc in range(len(board)):
			if board[loc] == 'x':
				b = board.copy()
				b[loc] = 'W'
				if self.closeMill(loc, b):
					self.GenerateRemove(b, L)
				else:
					L.append(b)
		
		return L



	def GenerateFlying(self, board):
		L = []
		for loc1 in range(len(board)):
			if board[loc1] == 'W':
				for loc2 in range(len(board)):
					if board[loc2] == 'x':
						b = board.copy()
						b[loc1] = 'x'
						b[loc2] = 'W'
						if self.closeMill(loc2, b):
							self.GenerateRemove(b, L)
						else:
							L.append(b)
		return L


	def GenerateMove(self, board):
		L = []
		for loc in range(len(board)):
			if board[loc] == 'W':
				n = self.neighbors[loc]
				for j in n:
					if board[j] == 'x':
						b = board.copy()
						b[loc] = 'x'
						b[j] = 'W'
						if self.closeMill(j,b):
							self.GenerateRemove(b, L)
						else:
							L.append(b)
		return L


	def GenerateMovesMidgameEndgame(self, board, switchColor=False):
		if switchColor:
			board = self.switchColors(board)

		numWhitePieces = 0
		for b in board:
			if b=='W':
				numWhitePieces += 1

		if numWhitePieces == 3:
			L = self.GenerateFlying(board)
		else:
			L = self.GenerateMove(board)

		if switchColor:
			board = self.switchColors(board)
			L = self.switchColors(L)
		
		return L
