# Five-In-A-Row (Or Gomoku)
# Developed on Python 3.x

import os
import math
import random

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
		self.bg_color = '#AA1337'
		self.cur_player = 'w'
		self.ai = False

		# Main frame.
		self.main_frame = Frame(master)
		self.main_frame.pack()

		# Top frame: Everything but the game.
		self.top_frame = Frame(self.main_frame)
		self.top_frame.pack()

			# Header message (displays turn, winning message, etc.)
		self.header = Message(self.top_frame, width=self.tile_size*13)
		self.header.pack()

		# Bottom frame that contains the game board.
		self.bottom_frame = Frame(self.main_frame)
		self.bottom_frame.pack()

		# Start game
		self.initialize_game()
	def initialize_game(self):
		self.play = True
		frame = self.bottom_frame

		# Makes lines shorter...
		ts = self.tile_size 
		bg_color = self.bg_color

		# White starts first.
		self.player = 'w'
		self.header.config(text='White\'s turn...')

		# Adding the playing board.
		self.board = Canvas(frame, bg=bg_color, height=ts*13, width=ts*13)
		self.board.pack()

		# Adding board tiles.
		for row in range(13):
			for col in range(13):
				tag = tags='r'+str(row)+'c'+str(col)

				self.board.create_rectangle(col*ts, row*ts, col*ts+ts, row*ts+ts, fill=bg_color, outline=bg_color, tags=tag)
				self.board.create_line(col*ts+ts/2, row*ts, col*ts+ts/2, row*ts+ts, fill='gray', tags=tag)
				self.board.create_line(col*ts, row*ts+ts/2, col*ts+ts, row*ts+ts/2, fill='gray', tags=tag)

				# Bind all the items added above to a lambda calling on_click
				self.board.tag_bind(
					tag, '<Button-1>', lambda event, params={'coords':[row, col], 'tag':tag}: self.on_click(event, params)
					)

		# If playing with AI, need to run further logic.
		if self.ai and self.cur_player=='b':
			self.play = False
			self.ai_move()

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
			r = params['coords'][0]
			c = params['coords'][1]
			tag = params['tag']

			if self.player == 'w':
				self.board.create_oval(c*ts+size, r*ts+size, c*ts+ts-size, r*ts+ts-size, fill='white', outline='black', tag='w')
				self.player = 'b'
				self.header.config(text='Black\'s turn...')
			else:
				self.board.create_oval(c*ts+size, r*ts+size, c*ts+ts-size, r*ts+ts-size, fill='black', outline='black', tag='b')
				self.player = 'w'
				self.header.config(text='White\'s turn...')
			# Unbind clicked board with parameters passed in.
			self.board.tag_unbind(tag, '<Button-1>')

			# Check for a win
			if (self.check_win(r, c)):
				self.end_game()	
			elif self.ai:
				# Additional steps for AI.
				self.play = False
				self.ai_move()
		else:
			#root.destroy();
			pass

	def ai_click(self, params):
		"""
		Very similar logic to on_click.
		Putting this as a seperate function to avoid a spaghetti of toggles
		to switch between AI and player turn.
		"""
		size = self.piece_size
		ts = self.tile_size
		r = params['coords'][0]
		c = params['coords'][1]
		tag = params['tag']

		if self.player == 'w':
			self.board.create_oval(c*ts+size, r*ts+size, c*ts+ts-size, r*ts+ts-size, fill='white', outline='black', tag='w')
			self.player = 'b'
			self.header.config(text='Black\'s turn...')
		else:
			self.board.create_oval(c*ts+size, r*ts+size, c*ts+ts-size, r*ts+ts-size, fill='black', outline='black', tag='b')
			self.player = 'w'
			self.header.config(text='White\'s turn...')
		# Unbind clicked board with parameters passed in.
		self.board.tag_unbind(tag, '<Button-1>')

	def end_game(self):
		# 'Disable' all on_clicks and display end message.
		self.play = False
		winner = "White" if self.player == 'b' else 'Black'
		self.header.config(text=winner+' wins!!')

	def check_win(self, r, c):
		oppo = self.player
		p = 'w' if self.player == 'b' else 'b'
		ts = self.tile_size

		# Horizontal
		hor = 1
		for i in range(1, 5):
			try:
				tags = self.board.gettags(self.board.find_closest(c*ts+ts/2-i*ts, r*ts+ts/2))
				if (p in tags):
					hor += 1
				else:
					break
			except IndexError:
				pass
		if (hor >= 5):
			print('hor ' + str(hor))
			return True
		for i in range(1, 5):
			try:
				tags = self.board.gettags(self.board.find_closest(c*ts+ts/2+i*ts, r*ts+ts/2))
				if (p in tags):
					hor += 1
				else:
					break
			except IndexError:
				pass
		if (hor >= 5):
			print('hor ' + str(hor))
			return True

		# Vertical
		ver = 1
		for i in range(1, 5):
			try:
				tags = self.board.gettags(self.board.find_closest(c*ts+ts/2, r*ts+ts/2-i*ts))
				if (p in tags):
					ver += 1
				else:
					break
			except IndexError:
				pass
		if (ver >= 5):
			print('v ' + str(ver))
			return True
		for i in range(1, 5):
			try:
				tags = self.board.gettags(self.board.find_closest(c*ts+ts/2, r*ts+ts/2+i*ts))
				if (p in tags):
					ver += 1
				else:
					break
			except IndexError:
				pass
		if (ver >= 5):
			print('v ' + str(ver))
			return True

		# Forward Diagonal
		diag = 1
		for i in range(1, 5):
			try:
				tags = self.board.gettags(self.board.find_closest(c*ts+ts/2-i*ts, r*ts+ts/2-i*ts))
				if (p in tags):
					diag += 1
				else:
					break
			except IndexError:
				pass
		if (diag >= 5):
			print('d ' + str(diag))
			return True
		for i in range(1, 5):
			try:
				tags = self.board.gettags(self.board.find_closest(c*ts+ts/2+i*ts, r*ts+ts/2+i*ts))
				if (p in tags):
					diag += 1
				else:
					break
			except IndexError:
				pass
		if (diag >= 5):
			print('d ' + str(diag))
			return True

		# Backward Diagonal
		xdiag = 1
		for i in range(1, 5):
			try:
				tags = self.board.gettags(self.board.find_closest(c*ts+ts/2-i*ts, r*ts+ts/2+i*ts))
				if (p in tags):
					xdiag += 1
				else:
					break
			except IndexError:
				pass
		if (xdiag >= 5):
			print('xd ' + str(xdiag))
			return True
		for i in range(1, 5):
			try:
				tags = self.board.gettags(self.board.find_closest(c*ts+ts/2+i*ts, r*ts+ts/2-i*ts))
				if (p in tags):
					xdiag += 1
				else:
					break
			except IndexError:
				pass
		if (xdiag >= 5):
			print('xd ' + str(xdiag))
			return True

	def clear_game(self):
		self.board.delete(ALL)
		self.board.pack_forget()

	def start_game(self):
		self.ai = False
		self.clear_game()
		self.initialize_game()

	def start_ai_game(self):
		self.ai = True
		self.clear_game()
		self.pick_player()

	def set_bg_color(self, bg_color):
		if (bg_color != None):
			self.bg_color = bg_color

	def toggle_ai(self):
		self.ai = not self.ai

	def pick_player(self):		
		self.header.config(text="Pick your color:")

		# Drawing choices
		ts = self.tile_size
		self.board.pack()
		b_button = self.board.create_rectangle(0, 0, ts*13, ts*13/2, fill='black', outline='black')
		w_button = self.board.create_rectangle(0, ts*13/2, ts*13, ts*13, fill='white', outline='white')

		self.board.tag_bind(b_button, '<Button-1>', lambda event: self.set_cur_player('b'))
		self.board.tag_bind(w_button, '<Button-1>', lambda event: self.set_cur_player('w'))

	def set_cur_player(self, color):
		self.cur_player = color
		self.clear_game()
		self.initialize_game()

	def ai_move(self):
		"""
		Logic for CPU implemented here.
		"""
		me = self.cur_player
		ts = self.tile_size

		while True:
			row = random.randint(0, 13)
			col = random.randint(0, 13)
			x = row*ts+ts/2
			y = col*ts+ts/2
			tags = self.board.gettags(self.board.find_closest(x, y))

			if ('b' in tags or 'w' in tags):
				pass
			else:
				break
		tag = 'r'+str(row)+'c'+str(col)
		print(tag)

		self.ai_click({'coords':[row, col], 'tag':tag})
		self.play = True

		# Check for a win. Putting it here so that self.play will be set to False
		if (self.check_win(row, col)):
			print('ai win')
			self.end_game()


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