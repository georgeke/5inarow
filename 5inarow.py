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
		ts = 43
		bg_color = "#AA1337"

		frame = Frame(master)
		frame.pack()

		self.board = Canvas(frame, bg='#EF16B0', height=ts*13, width=ts*13)
		self.board.pack()

		# Adding board tiles
		for col in range(13):
			for row in range(13):
				tag = tags="tile"+col+row

				rec =self.board.create_rectangle(col*ts, row*ts, col*ts+ts, row*ts+ts, fill=bg_color, outline=bg_color, tags=tag)
				l1 =self.board.create_line(col*ts+ts/2, row*ts, col*ts+ts/2, row*ts+ts, fill="gray", tags=tag)
				l2 =self.board.create_line(col*ts, row*ts+ts/2, col*ts+ts, row*ts+ts/2, fill="gray", tags=tag)

				rec.bind("<Button-1>", #add binding here)

	def on_click(self, button, toggle=[True]):
		if toggle[0]:
			button.config(image=self.board_b)
			toggle[0] = False
		else:
			button.config(image=self.board_clr)
			toggle[0] = True

root = Tk()
root.title("Five-In-A-Row")

gomoku = Gameboard(root)

root.mainloop()
root.destroy();