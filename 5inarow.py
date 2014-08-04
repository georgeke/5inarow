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
		self.play = True

		# Size of a tile.
		self.ts = 43
		ts = self.ts
		bg_color = '#AA1337'

		frame = Frame(master)
		frame.pack()

		self.player = 'w'
		self.board = Canvas(frame, bg='#EF16B0', height=ts*13, width=ts*13)
		self.board.pack()

		# Adding board tiles
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
		size = 2
		ts = self.ts
		r = params['coords'][0]
		c = params['coords'][1]
		tag = params['tag']

		if self.player == 'w':
			self.board.create_oval(c*ts+size, r*ts+size, c*ts+ts-size, r*ts+ts-size, fill='white', outline='black', tag='w')
			self.player = 'b'
		else:
			self.board.create_oval(c*ts+size, r*ts+size, c*ts+ts-size, r*ts+ts-size, fill='black', outline='black', tag='b')
			self.player = 'w'
		# Unbind clicked board with parameters passed in.
		self.board.tag_unbind(tag, '<Button-1>')

		# Check for a win
		if (self.check_win(r, c)):
			# Disable all on_clicks and display end message.
			self.board.tag_unbind('alla', '<Button-1>')
			pass

	def check_win(self, r, c):
		oppo = self.player
		p = 'w' if self.player == 'b' else 'b'
		ts = self.ts

		# Horizontal
		hor = 5
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

	def play():
		return self.play

root = Tk()
root.title('Five-In-A-Row')
gomoku = Gameboard(root)

root.mainloop()
root.destroy();