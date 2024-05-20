import math
import operator

class TTTBoard():
	empty = '-'
	num_players = 2
	board_size = 3

	def __init__(self):
		self.status = [[TTTBoard.empty for x in range(3)] for y in range(3)]

	def display(self):
		board_display = ''

		for i in range(3):
			board_display+='\n| '
			for j in range(3):
				board_display+=f'{self.status[i][j]} | '

		print(board_display[1:])

	def update(self,row,col,player):
		if self.status[row][col]==TTTBoard.empty:
			self.status[row][col]=Player.marks[player.player_index]
		else:
			raise TypeError

	def is_moves_left(self):
		for i in range(3):
			for j in range(3):
				if (self.status[i][j] == TTTBoard.empty):
					return True
		return False

	def evaluate(self):

		walk_direction = 	[				# [move_r, move_c]
								[-1,1],		# diag - up
								[0,1],		# right
								[1,1],		# diag - down
								[1,0]		# down
							]
		test_directions = 	[									# test dir. per cell
								[[1,2,3],	[3],	[3]],		# [r,dd,d],	[d],	[d]
								[[1],		[],		[]],		# [r],		[],		[]
								[[0,1],		[],		[]]			# [r,du],	[],		[]
							]									# walk_direction[d]

		def do_test(self,r,c):
			if test_directions[r][c]:
				for d in test_directions[r][c]:
					if board_walk(self,r,c,walk_direction[d]):
						return True
			return False

		def board_walk(self,r,c,d):
			if (self.status[r][c] == self.status[r+1*d[0]][c+1*d[1]]) and (
				self.status[r][c] == self.status[r+2*d[0]][c+2*d[1]]):
				return True
			return False

		for r in range(3):
			for c in range(3):
				if self.status[r][c] != TTTBoard.empty:		# if cell not empty
					if do_test(self,r,c):
						if self.status[r][c] == Player.marks[0]:
							return 1
						return -1
		return 0

class Player():
	marks = ['X','O']
	minimax_setting = ['max','min']

	def __init__(self,player_index,player_type=None,player_name=None):
		self.player_type = player_type
		self.player_name = player_name
		self.player_index = player_index

	@staticmethod
	def switch_player(index):
		return 1 if index == 0 else 0

def minimax(board,player_turn):

	score = board.evaluate()
	if (score != 0):
		return score # netko je pobijedio
	if (not board.is_moves_left()):
		return 0 # nema više poteza i nitko nije pobijedio > neriješeno

	if Player.minimax_setting[player_turn] == 'max': # Ako je Maximizer na potezu
		best = -math.inf
		best_func = max
	else: # Ako je Minimizer na potezu
		best = math.inf
		best_func = min

	for i in range(3):
		for j in range(3):
			if board.status[i][j] == TTTBoard.empty: # ćelija prazna?
				board.status[i][j] = Player.marks[player_turn] # napravi potez
				best = best_func(best,minimax(board,Player.switch_player(player_turn)))
				board.status[i][j] = TTTBoard.empty # vrati potez nakon testa

	return best

def find_best_move(board,player_turn):
	# vraća najbolji potez prema minimax algoritmu
	if Player.minimax_setting[player_turn] == 'max':
		best_score = -math.inf
		compare = operator.gt
	elif Player.minimax_setting[player_turn] == 'min':
		best_score = math.inf
		compare = operator.lt

	best_move = None
	# evaluate minimax function za sve prazne ćelije, vrati optimalnu
	for i in range(3):
		for j in range(3):
			if board.status[i][j] == TTTBoard.empty: # ćelija prazna?
				board.status[i][j] = Player.marks[player_turn] # napravi potez
				score = minimax(board,Player.switch_player(player_turn))
				board.status[i][j] = TTTBoard.empty	# vrati potez nakon testa
				if compare(score,best_score):	# ažuriraj ako je potez bolji
					best_move = (i, j)
					best_score = score

	return best_move

def play(players):

	def move_check(move,board):

		def board_check(x,y):
			return (x in [0,1,2] and y in [0,1,2])

		try:
			row = int(move.split(' ')[0])
			col = int(move.split(' ')[1])
		except ValueError:
			return (False, "Pogrešan unos!")

		if (not board_check(row,col)):
			return (False, "Potez van ploče!")

		if board.status[row][col]!=TTTBoard.empty:
			return (False, "Polje nije prazno!")

		return (True,(row,col))

	def move_display(move,board,player):
		(row,col) = move
		board.update(row,col,player)
		board.display()
		score = board.evaluate()

		if score != 0:
			return (True,board,f"pobjeda {player.player_name}!")

		if board.is_moves_left():
			return (False,board,"slijedeci potez ...")

		return (True,board,"izjednaceno!")

	player_turn = 0
	move_count = 1

	board = TTTBoard()
	board.display()

	print("\nUPUTA: potez se unosi u obliku (red, [0-2]) (stupac, [0-2]).")

	win_flag = False

	while not win_flag:
		print(f"\n> {move_count}. potez ({players[player_turn].player_name}): ",end='')

		if players[player_turn].player_type == 'H':
			(move_test,move) = move_check(input(),board)
			if not move_test:
				print(move)		# neuspješno unesen potez
				continue
		else:
			print()
			# TO DO: ako je kompjuter na redu, randomiziraj 1. potez
			(move_test,move) = (True,find_best_move(board,player_turn))

		(win_flag,board,poruka) = move_display(move,board,players[player_turn])
		print(poruka)

		if win_flag:
			# TO DO: dodaj running score [.,.] (return umjesto break)
			# +1 onom koji je igrao zadnji ako je pobjeda, inače 0
			break

		player_turn = Player.switch_player(player_turn)
		move_count += 1

def assign_value(msg_input,expected_type,check_list,msg_error):

	parameter = None
	while not parameter:
		parameter = expected_type(input(msg_input))

		if (len(parameter) == 0) or (check_list and (not parameter in check_list)):
			parameter = None
			print(msg_error)
			continue

	return parameter.upper()

def main():

	new_players = True
	new_game = True

	def initialize_players():
		players = [Player(x) for x in range(TTTBoard.num_players)]

		for (index,player) in enumerate(players):
			player.player_type = assign_value(
				f"Igrac ({index+1}): (H)uman or (C)omputer? ",str,['h','H','c','C'],"Pogresan unos!")
			player.player_name = assign_value(
				"Ime igraca? ",str,[],"Igrac mora imati ime!")

		return players

	while new_game:

		if new_players:
			players = initialize_players()

		print(f"\n{players[0].player_name} VS {players[1].player_name}\n")

		play(players)

		new_game = assign_value("\n> nova igra? (Y/N) ",str,['y','Y','n','N'],"Pogrešan unos!")

		if new_game in ['n','N']:
			new_game = False
			continue

		new_players = assign_value("\n> novi igraci? (Y/N) ",str,['y','Y','n','N'],"Pogrešan unos!")

		if new_players in ['n','N']:
			new_players = False

main()
