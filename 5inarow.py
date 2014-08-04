# Five-In-A-Row (Or Gomoku)
# Developed on Python 3.x

import os

try:
	# Python2
	from Tkinter import *
except ImportError:
	# Python3
	from tkinter import *

class Gameboard():
	def __init__(self, master):
		self.tile_size = 43
		self.piece_size = 2
		self.bg_color = '#AA1337'

		# Main frame.
		self.main_frame = Frame(master)
		self.main_frame.pack()

		# Top frame: Everything but the game.
		self.top_frame = Frame(self.main_frame)
		self.top_frame.pack()

			# Header message (displays turn, winning message, etc.)
		self.header = Message(self.top_frame, text='White\'s turn...', width=self.tile_size*13)
		self.header.pack()

		# Bottom frame that contains the game board.
		self.bottom_frame = Frame(self.main_frame)
		self.bottom_frame.pack()

		# Start game.
		self.initialize_game()

	def initialize_game(self):
		self.play = True
		frame = self.bottom_frame

		# Making lines shorter...
		ts = self.tile_size 
		bg_color = self.bg_color

		# White starts first.
		self.player = 'w'

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

	def on_click(self, event, params):
		"""
		Draws a player piece at the tile it was clicked at. 
		Toggles between black and white player tiles.
		"""
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
				# 'Disable' all on_clicks and display end message.
				self.play = False

				winner = "White" if self.player == 'b' else 'Black'
				self.header.config(text=winner+' wins!!')
				
		else:
			#root.destroy();
			pass

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
			return True

	def clear_game(self):
		self.board.delete(ALL)
		self.board.pack_forget()

	def restart_game(self):
		self.clear_game()
		self.initialize_game()

root = Tk()
root.title('Five-In-A-Row')
gomoku = Gameboard(root)

# create a toplevel menu
menubar = Menu(root)
menubar.add_command(label="Restart", command=gomoku.restart_game)

# display the menu
root.config(menu=menubar)

root.mainloop()

print('Good bye!')
#root.destroy();