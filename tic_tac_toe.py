from tkinter import *
import tkinter.messagebox

btn_width = 5
btn_height = 2
btn_padx = 5
btn_pady = 5

#list of 9 buttons created
btns = []
#list of buttons that were clicked
checked_btns = []
#list X and O based on buttons clicked
win =['', '', '', '', '', '', '', '', '']
#to count the number of moves, max is 9
turn = 0

#sets player1 as the first player
player_1_turn = True

def label_widget():
	#shows which player has which sign X or O
	player1 = Label(TTT, text='Player 1 is X\nPlayer 2 is O', font='BOLD', 
					bg=my_bg_color2)
	player1.grid(row=0, column=3, padx=20)

#changes rgb tuple (integers) to tkinter color
def get_color(color_code):
    return "#%02x%02x%02x" % color_code   
#insert the rgb tuple of the desired color
my_bg_color1 = get_color((98, 144, 182)) 
my_bg_color2 = get_color((98, 144, 100)) 

def create_table():
	i=0
	for r in range(0, 3):
		for c in range(0, 3):
			btns.append(Button(TTT, text='', width=btn_width, 
									height=btn_height, padx=btn_padx, 
									pady=btn_pady, font='BOLD',
									bg=my_bg_color1))
			btns[i].grid(row=r, column=c)
			i += 1

def onclick(event):
	#player_1_turn set as global so it can be called outside of the function
	global player_1_turn
	global turn

	#x returns x position relative to main window in pixels
	x = event.x_root - TTT.winfo_rootx() 
	#y returns y position relative to main window in pixels
	y = event.y_root - TTT.winfo_rooty() 
	#grid_position returns the (row, column) position of the clicked grid
	grid_position = TTT.grid_location(x, y)
	
	#sets the sign to be displayed when a player clicked
	if player_1_turn == True:
		symbol = 'X'
	else:
		symbol = 'O'

	#if the button was clicked for the first time, it is appended to btns
	if (grid_position not in checked_btns):
		checked_btns.append(grid_position)
		#we get the row and column number of the last clicked button which
		#was added to the checked_btns list
		r = checked_btns[-1][1]
		c = checked_btns[-1][0]
		
		#change the text of the clicked button. No change if clicked on grid
		#outside of the playing zone
		if (r < 3) and (c <3):
			if r == 0:
				btns[(r+c)].config(text=symbol)
				cell = r + c
			elif r == 1:
				btns[(r+c+2)].config(text=symbol)
				cell = r + c + 2
			elif r == 2:
				btns[(r+c+4)].config(text=symbol)
				cell = r + c + 4
			
			#add the symbol X or Y to the win list for the button that was
			#clicked
			win[cell] = symbol
	
		turn += 1

		#check for winner vertical and horizontal
		for i in range (0,3):
			if (win[i] == symbol and win[i+3] == symbol and win[i+6] == symbol):
				show_winner(symbol)
				TTT.quit()
			elif (win[i*3] == symbol and win[(i*3)+1] == symbol \
				and win[(i*3)+2] == symbol):
				show_winner(symbol)
				TTT.quit()
		#check for winer diagonal
		if win[0] == symbol and win[4] == symbol and win[8] == symbol:
			show_winner(symbol)
			TTT.quit()
		elif win[2] == symbol and win[4] == symbol and win[6] == symbol:
			show_winner(symbol)
			TTT.quit()

		#after the 9th move if there is no winner, this message box pops-up
		if (turn == 9) and (show_winner.has_been_called == False):
			tkinter.messagebox.showinfo('Game over!', 'Sorry guys, no winner!')
			TTT.quit()

		#change the turn to the other player
		player_1_turn = not(player_1_turn)

#messagebox shows the winner at the end of the game
#show_winner.has_been_called is set to False. When the show_winner function is
#called, this attribute changes to True. If the attribute is False after the
#9th move, there is no winner
def show_winner(symbol):
	show_winner.has_been_called = True
	tkinter.messagebox.showinfo('Game over!', 'The winner is Player ' + symbol)
show_winner.has_been_called = False

TTT = Tk()
TTT.title('Tic Tac Toe')
TTT.geometry('350x250')
TTT.iconbitmap('ttt.ico')
TTT.configure(bg=my_bg_color2)

create_table()
label_widget()
TTT.bind('<Button-1>', onclick)

TTT.mainloop()
