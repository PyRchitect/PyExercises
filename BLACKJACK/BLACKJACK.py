import pandas as pd
import numpy as np
import random as rn
import urwid as uw

class Game():
	max_players = 8
	max_decks = 8
	display_separator = "- "*10

	def __init__(self):

		self.players = self.init_players()
		self.bank = Player("bank","B")

		self.number_of_decks, self.shuffle_after = self.init_decks()

		self.move_count = 0

		self.available_cards = Cards(self.number_of_decks)
			
	def init_players(self):
		print("INICIJALIZACIJA IGRAČA")
		players = []
		
		np_test = False
		while np_test == False:
			try:
				np = int(input("> Broj igraca [#]: "))
				assert np>=1 and np<=Game.max_players
			except:
				print("Pogresan unos!")
			else:
				np_test = True
			finally:
				print(Game.display_separator)
		
		for p in range(np):
			print(f"{p+1}. IGRAČ:")

			pn_test = False
			while pn_test == False:
				try:
					pn = input("> Ime igraca [""]: ")
					assert pn
				except:
					print("Pogresan unos!")
				else:
					pn_test = True
			
			pt_test = False
			while pt_test == False:
				try:
					pt = input("> Tip igraca [H,C]: ")
					assert pt.upper() in ["H","C"]
				except:
					print("Pogresan unos!")
				else:
					pt_test = True

				print(Game.display_separator)

			players.append(Player(pn,pt))

		return players
	
	def init_decks(self):
		print("INICIJALIZACIJA DECKOVA")

		d_test = False
		while d_test == False:
			try:
				d = int(input("> Broj deckova [#]: "))
				assert d>=1 and d<=Game.max_decks
			except:
				print("Pogresan unos!")
			else:
				d_test = True

		s_test = False
		while s_test == False:
			try:
				s = int(input("> Shuffle nakon [#]: "))
				assert s>=1 and s<=d
			except:
				print("Pogresan unos!")
			else:
				d_test = True
			
			print(Game.display_separator)

			return (d,s)

	def deal(self,player):

		# deal 2 cards:
		player.dealt_cards.add_card(self.available_cards.remove_card())
		player.dealt_cards.add_card(self.available_cards.remove_card())
		print(f"> PRVE DVIJE KARTE: {player.dealt_cards.get_cards()}")
		ps = player.dealt_cards.score
		score_display = f"{ps[0]}" + (f"{'/'+str(ps[1]) if ps[1] else ''}")
		print(f"> BROJ BODOVA: {score_display}")

		m_test = False
		while m_test == False:
			ps = player.dealt_cards.score
			if ps[0]==21 or ps[1]==21:
					print(" > BLACKJACK!")
					m_test = True
					continue

			s_test = False
			while s_test == False:
				try:
					move = input("> Stand / Hit? [S,H] ")
					assert move.upper() in ["S","H"]
				except:
					print("Pogrešan unos!")
					s_test = False
				else:
					s_test = True
				finally:
					print(Game.display_separator)
			
			if move == "H":
				player.dealt_cards.add_card(self.available_cards.remove_card())
				print(f"> KARTE: {player.dealt_cards.get_cards()}")
				ps = player.dealt_cards.score
				score_display = f"{ps[0]}" + (f"{'/'+str(ps[1]) if ps[1] else ''}")
				print(f"> BROJ BODOVA: {score_display}",end='')
			
				if ps[0]==21 or ps[1]==21:
					print(" > WIN!")
					m_test = True
				elif ps[0]>21:
					print(" > BUST!")
					m_test = True
				else:
					print(" > UNDER!")

			else:
				m_test = True

	def evaluate(self):
		L = []
		for i,p in enumerate(self.players):
			ps = p.dealt_cards.score
			score = ps[1] if ps[1] else ps[0]
			if score <= 21:
				L.append((i,score))
		
		from operator import itemgetter
		return sorted(L,key=itemgetter(1),reverse=True)

class Cards():
	suits = list(range(1,4+1))
	sd = ["C","D","H","S"]
	# clubs, diamonds, hearts, spades
		
	ranks = list(range(1,13+1))
	# ranks basic range npr. za indeksiranje ili ako će trebati
	rd_al = ["A"] + [str(x) for x in range(2,11)] + ["J","Q","K"]
	# ranks display: aces low > A=1, 2-10, J=11, Q=12, K=13
	rd_ah = [str(x) for x in range(2,11)] + ["J","Q","K","A"]
	# ranks display: aces high > 2-10, J=10, Q=11, K=12, A=13
	rp_al = list(range(1,11)) + [10]*3
	# ranks points: aces low > A=1, 2-10, J,Q,K=10
	rp_ah = list(range(2,11)) + [10]*4
	# ranks points: aces high > 2-10, J,Q,K,A=10

	def __init__(self,decks,input_data=None,aces=0):
		# if no input data (for set games) init to number of decks in all positions
		input_data = input_data or [[decks for _ in Cards.ranks] for _ in Cards.suits]
		# aces flag: 0 - low, 1 - high
		if aces not in [0,1]:
			raise ValueError("Aces flag - pogresan unos! [0,1]")
		elif aces == 0:
			cols=Cards.rd_al
		elif aces == 1:
			cols=Cards.rd_ah
		self.aces_lh = aces

		self.status = pd.DataFrame.from_records(data=input_data,columns=cols,index=Cards.sd)
		pd.set_option('display.max_columns',13)
		pd.set_option('display.max_rows',4)

		self.score = 0
	
	def init_shuffle(self,decks):
		return [[decks for _ in Cards.ranks] for _ in Cards.suits]
	
	def aces_lh_switch(self):
		col = self.status.pop("A")

		if self.aces_lh == 0:
			self.status.insert(len(self.status.columns),col.name,col) # move to end
			self.aces_lh = 1
		else:			
			self.status.insert(0,col.name,col) # move to beginning
			self.aces_lh = 0
	
	def number_of_cards_in_deck(self):
		return np.sum(self.status.values)

	def calculate_points(self):
		# aces flag: 0 - low, 1 - high
		if self.aces_lh == 1:
			self.aces_lh_switch()
		cols=Cards.rp_al

		status_points = pd.DataFrame.from_records(data=self.status.values,columns=cols,index=Cards.sd)

		# first calculate the hard hand:
		sum_hard = 0
		for i in range(status_points.shape[1]):
			c = status_points.iloc[:,i]
			sum_hard+=c.name*sum(c.values)
		
		# then, if there are aces, try to calculate soft hands:
		sum_soft = sum_hard+10 if self.status["A"].sum()>0 and sum_hard+10<=21 else None
		
		return (sum_hard,sum_soft)

	def add_card(self,new_card):
		self.status.loc[new_card[0],new_card[1]] += 1
		self.score = self.calculate_points()

	def remove_card(self,position=None):
		card_list = []
		for r in range(self.status.shape[0]):
			for c in range(self.status.shape[1]):
				num_cards = self.status.values[r][c]
				if num_cards > 0:
					row_name = self.status.index[r]
					col_name = self.status.columns[c]
					card_list.append([row_name,col_name])
		
		if position == None:
			drawn_card = card_list[rn.randint(0,len(card_list)-1)]
		else:
			if position >= 0 and position < len(card_list):
				drawn_card = card_list[position]
			else:
				raise IndexError("Pozicija izvan liste!")

		self.status.loc[drawn_card[0],drawn_card[1]] -= 1

		return drawn_card

	def get_cards(self):
		card_list = []
		for r in range(self.status.shape[0]):
			for c in range(self.status.shape[1]):
				num_cards = self.status.values[r][c]
				if num_cards > 0:
					row_name = self.status.index[r]
					col_name = self.status.columns[c]
					for _ in range(num_cards):
						card_list.append([row_name,col_name])
		
		return card_list

class Player():
	def __init__(self,player_name,player_type):
		self.name = player_name
		self.type = player_type

		self.dealt_cards = Cards(decks=0)	# player has no decks

def play(new_game):

	print("\nIGRA")
	
	for i,p in enumerate(new_game.players):
		print(f"\n{i+1}. IGRAC:")
		new_game.deal(p)
	
	print("\nREZULTATI")
	print(Game.display_separator)
	ranking = new_game.evaluate()
	print(f"RANG LISTA:")
	if ranking:
		best = ranking[0][1]
		print(f"POBJEDNICI [SCORE = {best}]:",end=' ')
		i = 0
		while ranking[i][1]==best:
			print(new_game.players[ranking[i][0]].name, sep=', ',end=' ')
			i += 1
			if i==len(ranking):
				break
	else:
		print(f"NEMA POBJEDNIKA!")
	print()

def main():
	print("BLACKJACK")

	while True:
		print("\nGLAVNI MENU")
		print(Game.display_separator)
		print("[0] - izlaz")
		print("[1] - igra")
		
		c_test = False
		while c_test == False:
			try:
				c = int(input("Odabir [0,1] "))
				assert c in [0,1]
			except:
				print("Pogrešan unos!")
				c_test = False
			else:
				c_test = True
			finally:
				print(Game.display_separator)

		if c == 0:
			print("Hvala i doviđenja.")
			break

		if c == 1:	
			print("INICIJALIZACIJA")
			print(Game.display_separator)
			new_game = Game()

			play(new_game)

		# elif odabir == ...

main()