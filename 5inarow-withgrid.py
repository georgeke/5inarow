# Five-In-A-Row (Or Gomoku)
# Developed on Python 3.x

import os
import math
import random
import time

try:
	# Python2
	from Tkinter import *
	from tkColorChooser import askcolor
except ImportError:
	# Python3
	from tkinter import *
	from tkinter.colorchooser import *

class Gameboard():
	def __init__(self, master):
		self.tile_size = 43
		self.piece_size = 2
		self.board_len = 15
		self.bg_color = '#AA1337'
		self.cur_player = 'w'
		self.ai = False
		self.grid = self.create_grid()

		# Main frame.
		self.main_frame = Frame(master)
		self.main_frame.pack()

		# Top frame: Everything but the game.
		self.top_frame = Frame(self.main_frame)
		self.top_frame.pack()

			# Header message (displays turn, winning message, etc.)
		self.header = Message(self.top_frame, width=self.tile_size*self.board_len)
		self.header.pack()

		# Bottom frame that contains the game board.
		self.bottom_frame = Frame(self.main_frame)
		self.bottom_frame.pack()

		# Start game
		self.initialize_game()
	def initialize_game(self):
		"""
		Shows game board and assigns on clicks.
		"""
		self.play = True
		frame = self.bottom_frame
		b_len = self.board_len

		# Makes lines shorter...
		ts = self.tile_size 
		bg_color = self.bg_color

		# Black starts first.
		self.player = 'b'
		self.header.config(text='Black\'s turn...')

		# Adding the playing board.
		self.board = Canvas(frame, bg=bg_color, height=ts*b_len, width=ts*b_len)
		self.board.pack()

		# Adding board tiles.
		for row in range(b_len):
			for col in range(b_len):
				tag = tags='r'+str(row)+'c'+str(col)

				self.board.create_rectangle(col*ts, row*ts, col*ts+ts, row*ts+ts, fill=bg_color, outline=bg_color, tags=tag)
				self.board.create_line(col*ts+ts/2, row*ts, col*ts+ts/2, row*ts+ts, fill='gray', tags=tag)
				self.board.create_line(col*ts, row*ts+ts/2, col*ts+ts, row*ts+ts/2, fill='gray', tags=tag)

				# Bind all the items added above to a lambda calling on click
				self.board.tag_bind(
					tag, '<Button-1>', lambda event, params={'coords':{'r':row, 'c':col}, 'tag':tag}: self.on_click(event, params)
					)

		# If playing with AI, need to run further logic.
		if self.ai and self.cur_player=='w':
			self.play = False
			self.ai_move()
		if self.ai:
			# Set up a grid tracking areas on the board that are worth checking by the AI.
			self.target_grid = [row[:] for row in self.grid]

	def on_click(self, event, params):
		"""
		Draws a player piece at the tile it was clicked at. 
		Toggles between black and white player tiles.
		If AI is on, it will play right after you play.
		"""
		# Either it's your turn and AI isn't moving, or it isn't your turn and AI is moving.
		if self.play:
			size = self.piece_size
			ts = self.tile_size
			r = params['coords']['r']
			c = params['coords']['c']
			tag = params['tag']

			if self.player == 'w':
				self.board.create_oval(c*ts+size, r*ts+size, c*ts+ts-size, r*ts+ts-size, fill='white', outline='black', tag='w')
				self.header.config(text='Black\'s turn...')
			else:
				self.board.create_oval(c*ts+size, r*ts+size, c*ts+ts-size, r*ts+ts-size, fill='black', outline='black', tag='b')				
				self.header.config(text='White\'s turn...')
			self.grid[c][r] = self.player
			self.player = 'w' if self.player == 'b' else 'b'
			# Unbind clicked board with parameters passed in.
			self.board.tag_unbind(tag, '<Button-1>')

			# Check for a win
			if (self.check_xinarow(5, self.grid, {'r':r, 'c':c}, 'b' if self.player=='w' else 'w') >= 0):
				self.end_game()
			elif self.ai:
				# Update 'worth checking' grid with spaces around placed piece.
				self.add_target(self.target_grid, {'r':r, 'c':c})
				# AI goes after you go.
				self.play = False
				self.ai_move()
		else:
			#root.destroy();
			pass

	def ai_click(self, params):
		"""
		Very similar logic to on click.
		Putting this as a seperate function to avoid a spaghetti of toggles
		to switch between AI and player turn.
		"""
		size = self.piece_size
		ts = self.tile_size
		r = params['coords']['r']
		c = params['coords']['c']
		tag = params['tag']

		if self.player == 'w':
			self.board.create_oval(c*ts+size, r*ts+size, c*ts+ts-size, r*ts+ts-size, fill='white', outline='black', tag='w')
			self.header.config(text='Black\'s turn...')
		else:
			self.board.create_oval(c*ts+size, r*ts+size, c*ts+ts-size, r*ts+ts-size, fill='black', outline='black', tag='b')
			self.header.config(text='White\'s turn...')
		self.add_target(self.target_grid, {'r':r, 'c':c})
		self.grid[c][r] = self.player
		self.player = 'w' if self.player == 'b' else 'b'
		# Unbind clicked board with parameters passed in.
		self.board.tag_unbind(tag, '<Button-1>')

	def end_game(self):
		"""
		'Disable' all on clicks and display end message.
		"""
		self.play = False
		winner = "White" if self.player == 'b' else 'Black'
		self.header.config(text=winner+' wins!!')

	def check_xinarow(self, x, grid, coords, p):
		"""
		Check the grid for x in a row pieces based on p, the player.
		If there are x in a row, returns the number of sides blocked.
		Else, returns -1.
		"""
		hor = self.check_xdir(x, grid, coords, {'mc':1, 'mr':0}, p)
		if hor>=0:
			return hor

		ver = self.check_xdir(x, grid, coords, {'mc':0, 'mr':1}, p)
		if ver>=0:
			return ver

		diag = self.check_xdir(x, grid, coords, {'mc':1, 'mr':-1}, p)
		if diag>=0:
			return diag

		xdiag = self.check_xdir(x, grid, coords, {'mc':1, 'mr':1}, p)
		if xdiag>=0:
			return xdiag

		return -1

	def check_2x4inarow(self, grid, coords, p):
		"""
		Checks if the pieces plays by coords will create at least a double 4 in a row
		with each 4 in a row having only 1 side blocked.
		"""
		results = [
			self.check_xdir(4, grid, coords, {'mc':1, 'mr':0}, p),
			self.check_xdir(4, grid, coords, {'mc':0, 'mr':1}, p),
			self.check_xdir(4, grid, coords, {'mc':1, 'mr':-1}, p),
			self.check_xdir(4, grid, coords, {'mc':1, 'mr':1}, p)
		]
		num_4inarow = 0

		# Checking number of 4inarows with 1 side blocked.
		for i in range(4):
			if results[i] == 1:
				num_4inarow += 1
		if num_4inarow>=2:
			return True
		else:
			return False

	def check_2x3inarow(self, grid, coords, p):
		"""
		Checks if the pieces plays by coords will create at least a double 3 in a row
		with each 3 in a row having no sides blocked.
		"""
		results = [
			self.check_xdir(3, grid, coords, {'mc':1, 'mr':0}, p),
			self.check_xdir(3, grid, coords, {'mc':0, 'mr':1}, p),
			self.check_xdir(3, grid, coords, {'mc':1, 'mr':-1}, p),
			self.check_xdir(3, grid, coords, {'mc':1, 'mr':1}, p)
		]
		num_3inarow = 0

		for i in range(4):
			if results[i] == 0:
				num_3inarow += 1
		if num_3inarow>=2:
			return True
		else:
			return False

	def check_3and4inarow(self, grid, coords, p):
		"""
		Checks if the pieces plays by coords will create at least one 4inarow with
		one side blocked, and at least one 3inarow with no sides blocked.
		"""
		results_4 = [
			self.check_xdir(4, grid, coords, {'mc':1, 'mr':0}, p),
			self.check_xdir(4, grid, coords, {'mc':0, 'mr':1}, p),
			self.check_xdir(4, grid, coords, {'mc':1, 'mr':-1}, p),
			self.check_xdir(4, grid, coords, {'mc':1, 'mr':1}, p)
		]
		results_3 = [
			self.check_xdir(3, grid, coords, {'mc':1, 'mr':0}, p),
			self.check_xdir(3, grid, coords, {'mc':0, 'mr':1}, p),
			self.check_xdir(3, grid, coords, {'mc':1, 'mr':-1}, p),
			self.check_xdir(3, grid, coords, {'mc':1, 'mr':1}, p)
		]
		num_3inarow = 0
		num_4inarow = 0

		for i in range(4):
			if results_3[i] == 0:
				num_3inarow += 1
			if results_4[i] == 1:
				num_4inarow += 1
		if num_3inarow>=1 and num_4inarow>=1:
			return True
		else:
			return False

	def check_xdir(self, x, grid, coords, modifiers, p):
		"""
		Checks a certain direction for x in a row based on modifiers.
		Returns the number of sides blocked if x in a row, else -1.
		"""
		count = 1
		c = coords['c']
		r = coords['r']
		mc = modifiers['mc']
		mr = modifiers['mr']
		# These represent the pieces that are the bounds of the x in a row line
		end_upper = {'c':c+mc, 'r':r+mr}
		end_lower = {'c':c-mc, 'r':r-mr}
		for i in range(1, x):
			try:
				if c+i*mc<0 or r+i*mr<0:
					break
				if (grid[c+i*mc][r+i*mr] == p):
					end_upper['c'], end_upper['r'] = c+i*mc+mc, r+i*mr+mr
					count += 1
				else:
					break
			except IndexError:
				pass
		if (count >= x):
			return self.num_blocks(end_upper, end_lower)
		for i in range(1, x):
			try:
				if c-i*mc<0 or r-i*mr<0:
					break
				if (grid[c-i*mc][r-i*mr] == p):
					end_lower['c'], end_lower['r'] = c-i*mc-mc, r-i*mr-mr
					count += 1
				else:
					break
			except IndexError:
				pass
		if (count >= x):
			return self.num_blocks(end_upper, end_lower)

		return -1

	def num_blocks(self, upper, lower):
		"""
		Returns the number of blockages based on end points of x in a row.
		"""
		block = 0;
		try:
			if upper['c'] < 0 or upper['r'] < 0:
				block += 1
			elif self.grid[upper['c']][upper['r']] != '-':
				block += 1
		except IndexError:
			pass
		try:
			if lower['c'] < 0 or lower['r'] < 0:
				block += 1
			elif self.grid[lower['c']][lower['r']] != '-':
				block += 1
		except IndexError:
			pass
		return block

	def clear_game(self):
		"""
		Clears grid state, all pieces, and game board.
		"""
		self.grid = self.create_grid()
		if self.ai:
			self.target_grid = [row[:] for row in self.grid]
		self.board.delete(ALL)
		self.board.pack_forget()

	def start_game(self):
		"""
		Start a game between two players.
		"""
		self.ai = False
		self.clear_game()
		self.initialize_game()

	def start_ai_game(self):
		"""
		Start a game with an AI
		"""
		self.ai = True
		self.clear_game()
		self.pick_player()

	def set_bg_color(self, bg_color):
		"""
		Change the background color. Will apply after New Game.
		"""
		if (bg_color != None):
			self.bg_color = bg_color

	def pick_player(self):
		"""
		Load the screen for user to choose player color 
		for gameplay against AI.
		"""	
		b_len = self.board_len
		self.header.config(text="Pick your color:")

		# Drawing choices
		ts = self.tile_size
		self.board.pack()
		b_button = self.board.create_rectangle(0, 0, ts*b_len, ts*b_len/2, fill='black', outline='black')
		w_button = self.board.create_rectangle(0, ts*b_len/2, ts*b_len, ts*b_len, fill='white', outline='white')

		self.board.tag_bind(b_button, '<Button-1>', lambda event: self.set_cur_player('b'))
		self.board.tag_bind(w_button, '<Button-1>', lambda event: self.set_cur_player('w'))

	def set_cur_player(self, color):
		"""
		OnClick for choosing player color. Starts the game after.
		"""
		self.cur_player = color
		self.clear_game()
		self.initialize_game()

	def ai_move(self):
		"""
		Logic for CPU implemented here.
		"""
		#time.sleep(1.5)
		ts = self.tile_size

		# Random placement.
		"""
		while True:
			row = random.randint(0, self.board_len-1)
			col = random.randint(0, self.board_len-1)
			if (self.grid[col][row] == '-'):
				break
		"""

		# Minimax algorithm.
		test = [row[:] for row in self.grid]
		result = self.minimax(0, 3, {'c':0, 'r':0}, test, True)
		row = result['coords']['r']
		col = result['coords']['c']
		print('Score: ' + str(result['score']))

		tag = 'r'+str(row)+'c'+str(col)
		self.ai_click({'coords':{'c':col, 'r':row}, 'tag':tag})
		self.play = True

		#self.print_grid(self.target_grid)

		# Check for a win. Putting it here so that self.play will be set to False
		if (self.check_xinarow(5, self.grid, {'r':row, 'c':col}, 'b' if self.player=='w' else 'w') >= 0):
			self.end_game()

	def create_grid(self):
		"""
		Creates a NxN array initialized with '-'.
		This grid is used to store the game state.
		"""
		grid = []
		for r in range(self.board_len):
			grid.append([])
			for c in range(self.board_len):
				grid[r].append('-')
		return grid

	def add_target(self, grid, coords):
		"""
		Changes grid contents of every space in a 1 grid radius around coords
		into 'X' for AI use.
		"""
		r = coords['r']
		c = coords['c']

		for i in range(-1, 2):
			for j in range(-1, 2):
				try:
					if (c+i>=0 and r+j>=0):
						grid[c+i][r+j] = 'X'
				except IndexError:
					pass

	def minimax(self, depth, max_depth, coords, grid, do_max):
		"""
		Minimax function. Returns the best (min or max) score as well as
		the coordinates of the placement.
		"""
		human = self.cur_player
		ai = self.player
		best = float('-inf') if do_max else float('inf')
		middle= math.floor(self.board_len/2)
		best_coords = {'r':middle, 'c':middle}
		if depth <= max_depth:
			for i in range(self.board_len):
				for j in range(self.board_len):
					if grid[i][j]=='-' and self.target_grid[i][j]=='X':
						test = [row[:] for row in grid]
						test[i][j] = ai if do_max else human

						result = self.minimax(depth+1, max_depth, {'c':i, 'r':j}, test, not do_max)
						score = result['score']
						# Updating best scores based on min/maxing.
						if do_max and score > best:
							best = score
							#print(str(result['coords']['c']) + " " + str(result['coords']['r']) + " " + str(score))
							best_coords = {'r':j, 'c':i}
						if not do_max and score < best:
							best = score
							best_coords = {'r':j, 'c':i}
		else:
			r = coords['r']
			c = coords['c']
			# If at leaf, return evaluation of score.
			score = 0;		
			result = {'score':score, 'coords':{'c':c, 'r':r}}
			check = [row[:] for row in grid]
			# 'me' represents the person playing the piece. 'you' represents their opponent.
			# This is based on do_max because if this node is maximizing, the parent node
			# will be minimizing. Since the minimizer is the human, the logic is that way.
			me = human if do_max else ai
			you = ai if do_max else human

			win_5inarow = self.check_xinarow(5, grid, {'r':r, 'c':c}, me)
			if win_5inarow>=0:
				# If win is next turn, it is the highest priority
				score += 10000
				return score			
			block_5inarow = self.check_xinarow(5, grid, {'r':r, 'c':c}, you)
			if block_5inarow>=0:
				score += -9000
				return score

			win_2x4inarow = self.check_2x4inarow(grid, {'r':r, 'c':c}, me)
			if win_2x4inarow:
				score += 8000
				return score				
			block_2x4inarow = self.check_2x4inarow(grid, {'r':r, 'c':c}, you)
			if block_2x4inarow:
				score += -7000
				return score

			win_4inarow = self.check_xinarow(4, grid, {'r':r, 'c':c}, me)
			if win_4inarow==0:
				score += 6000
				return score
			block_4inarow = self.check_xinarow(4, grid, {'r':r, 'c':c}, you)
			if block_4inarow==0:
				score += -5000
				return score
				
			win_3and4inarow = self.check_3and4inarow(grid, {'r':r, 'c':c}, me)
			if win_3and4inarow:
				score += 4000
				return score				
			block_3and4inarow = self.check_3and4inarow(grid, {'r':r, 'c':c}, you)
			if block_3and4inarow:
				score += -3000
				return score
				
			win_2x3inarow = self.check_2x3inarow(grid, {'r':r, 'c':c}, me)
			if win_2x3inarow:
				score += 2000
				return score				
			block_2x3inarow = self.check_2x3inarow(grid, {'r':r, 'c':c}, you)
			if block_2x3inarow:
				score += -1000
				return score

			# If no return check each setup possiblity as well as their corresponding block
			# opportunity and sum them.
			set_4inarow = self.check_xinarow(4, grid, {'r':r, 'c':c}, me)
			if set_4inarow==1:
				score += 4
			block_set_4inarow = self.check_xinarow(4, grid, {'r':r, 'c':c}, you)
			if block_set_4inarow==1:
				score += 5

			set_3inarow = self.check_xinarow(3, grid, {'r':r, 'c':c}, me)
			if set_3inarow==0:
				score += 10
			elif set_3inarow==1:
				score += 4
			block_set_3inarow = self.check_xinarow(3, grid, {'r':r, 'c':c}, you)
			if block_set_3inarow==0:
				score += 8
			elif block_set_3inarow==1:
				score += 3

			set_2inarow = self.check_xinarow(2, grid, {'r':r, 'c':c}, me)
			if set_2inarow==0:
				score += 2
			elif set_2inarow==1:
				score += 1
			block_set_2inarow = self.check_xinarow(2, grid, {'r':r, 'c':c}, you)
			if block_set_2inarow==0:
				score += 2
			elif block_set_2inarow==1:
				score += 0.5

			result['score'] = score

			return result
			
		return {'score':best, 'coords':best_coords}

	def print_grid(self, grid):
		"""
		Used for testing. Prints grid contents for checking augmentation.
		""" 
		for i in range(len(grid)):
			for j in range(len(grid[i])):
				print(grid[i][j] + " ", end="")
			print("\n") 

class Node():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.score = 0
		self.children = []

	def add(self, child):
		self.children.append(child)


def get_color():
    color = askcolor()
    return color

def get_hex(output):
	return output[1]

root = Tk()
root.title('Five-In-A-Row')
gomoku = Gameboard(root)

menubar = Menu(root)
menubar.add_command(label="New Game", command=gomoku.start_game)
menubar.add_command(label="New Game with Computer", command=lambda: gomoku.start_ai_game())
	# Change background
menubar.add_command(
	label="Change Background", command=lambda: gomoku.set_bg_color(get_hex(get_color()))
	)
# Show menu
root.config(menu=menubar)


root.mainloop()
print('Good bye!')
#root.destroy();