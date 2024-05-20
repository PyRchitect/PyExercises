from enum import Enum
from os import system
from time import sleep

class Constants(Enum):
	DISK_DOT = "O"
	DISK_NOT = "-"
	NAME_DOT = '.'
	SPACING = 5
	SLEEP_TIME = 0.5

class tower_disk():
	def __init__(self,half_length,half_width):
		self.width = half_width*2
		self.image = Constants.DISK_DOT.value*(half_length*2)

	def __str__(self):
		return f"{self.image:{Constants.DISK_NOT.value}^{self.width}}"

class tower_stack():
	def __init__(self,name,height=0,total_height=0):
		self.name = name
		self.total_height = total_height
		self.height = height
		self.disks = [tower_disk(x,height) for x in range(1,height+1)]

	def pop(self):
		disk = self.disks.pop(0)	# pop top disk
		return disk

	def push(self,new_disk):
		self.disks.insert(0,new_disk)

	def render(self):
		image = [f"{self.name}{Constants.NAME_DOT.value*(self.total_height*2-1)}"]

		for x in range(self.total_height - len(self.disks)):
			# first render empty rows if there are any
			image.append(Constants.DISK_NOT.value*self.total_height*2)

		for x in self.disks:
			# then render rows with disks if there are any
			image.append(str(x))

		return image

class board():
	def __init__(self,heading,images):
		self.heading = heading		
		col_break = [" "*Constants.SPACING.value for _ in range(len(images[0]))]

		status = []
		for i in images:
			status.append(i)
			status.append(col_break)
		self.status = list(zip(*status))

	def show(self):
		sleep(Constants.SLEEP_TIME.value)
		system('cls')
		print(f"{self.heading}:\n")
		for s in self.status:
			print(*s)

def hanoi(n,source:'tower_stack',auxiliary:'tower_stack',destination:'tower_stack'):
	if n>0:
		hanoi(n-1,source,destination,auxiliary)		# flip destination and auxiliary

		destination.push(source.pop())				# move top disk source -> destination

		# stacks are different for each iteration, need to sort A,B,C for rendering
		render_list = sorted((source,destination,auxiliary),key=lambda x: x.name)
		board("MOVE",[t.render() for t in render_list]).show()

		hanoi(n-1,auxiliary,source,destination)		# flip source and auxiliary

def game(n):
	towers = 	[
				tower_stack('A',n,n),
				tower_stack('B',0,n),
				tower_stack('C',0,n)
				]
	board("START",[t.render() for t in towers]).show()

	hanoi(n,*towers)

def main():
	new_game = True
	while new_game == True:
		n = input("Unesi n ili [x] za izlaz: ")

		try:
			game(int(n))
		except:
			if n == 'x':
				new_game = False
			else:
				print("Pogresan unos!")

main()