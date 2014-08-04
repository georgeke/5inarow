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
		self.ts = 43
		ts = self.ts
		bg_color = '#AA1337'

		frame = Frame(master)
		frame.pack()

		self.player = 'w'
		self.board = Canvas(frame, bg='#EF16B0', height=ts*13, width=ts*13)
		self.board.pack()

		# Adding board tiles
		for col in range(13):
			for row in range(13):
				tag = tags='tile'+str(col)+str(row)

				rec = self.board.create_rectangle(col*ts, row*ts, col*ts+ts, row*ts+ts, fill=bg_color, outline=bg_color, tags=tag)
				l1 = self.board.create_line(col*ts+ts/2, row*ts, col*ts+ts/2, row*ts+ts, fill='gray', tags=tag)
				l2 = self.board.create_line(col*ts, row*ts+ts/2, col*ts+ts, row*ts+ts/2, fill='gray', tags=tag)
				self.board.tag_bind(tag, '<Button-1>', lambda event='<Button-1>', coords=[row, col]: self.on_click('<Button-1>', coords))

	def on_click(self, event, coords):
		print(coords)
		ts = self.ts
		r = coords[0]
		c = coords[1]
		if self.player == 'w':
			self.board.create_oval(c*ts, r*ts, c*ts+ts, r*ts+ts, fill='white', outline='black')
			self.player = 'b'
		else:
			self.board.create_oval(c*ts, r*ts, c*ts+ts, r*ts+ts, fill='black', outline='black')
			self.player = 'w'

root = Tk()
root.title('Five-In-A-Row')

gomoku = Gameboard(root)

root.mainloop()
root.destroy();