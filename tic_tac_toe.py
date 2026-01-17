from tkinter import *

root = Tk()
root.geometry("420x621")
root.title("Tic tac toe ")
# setting the main window colour
root.configure(bg="#E6E6fA")
root.resizable(0,0)

frame1 = Frame(root)
frame1.grid()

titleLabel = Label( frame1 , text = "Tic Tac Toe game board", font = ("Algerian",22,"bold" ), bg = "#E6E6fA", fg ="black",padx=4)
titleLabel.grid(row = 0 ,column=0)

optionFrame = Frame(root , bg="grey")
optionFrame.grid()

frame2 = Frame(root,bg="#2F4F4F")
frame2.grid()

# To Store the Entered Element
board = { 1 : " " ,2 : " " ,3 : " ", 
          4 : " " ,5 : " " ,6 : " ",
          7 : " " ,8 : " " ,9 : " " }

turn = "X"
game_end = False
msglabel = None  # Store the label reference here
mode = "singlePlayer"

def changeModeToSinglePlayer(): 
   global mode 
   mode = "singlePlayer"
   singlePlayerButton["bg"] = "#CD5C5C"
   multiPlayerButton["bg"] = "#F5F5DC"

def changeModeToMultiplayer():
   global mode 
   mode = "multiPlayer"
   multiPlayerButton["bg"] = "#CD5C5C"
   singlePlayerButton["bg"] = "#F5F5DC"

def updateBoard():
   for key in board.keys():
      buttons[key-1]["text"] = board[key]

#WINNIN CHECK FUNCTION
def checkForWin(player):
    return (board[1] == board[2] == board[3] == player or
            board[4] == board[5] == board[6] == player or
            board[7] == board[8] == board[9] == player or
            board[1] == board[4] == board[7] == player or
            board[2] == board[5] == board[8] == player or
            board[3] == board[6] == board[9] == player or
            board[1] == board[5] == board[9] == player or
            board[3] == board[5] == board[7] == player)


# CHECK FOR DRAW
def checkfordraw():
   for i in board.keys():
      if board[i]==" ":
          return False
   return True

def RestartGame():
   global game_end, turn, msglabel
   turn = "X"
   game_end = False
   for button in buttons:
      button["text"]=" "
   for i in board.keys():
      board[i]=" "
    # Destroy the outcome label if it exists
   if msglabel is not None:
        msglabel.destroy()
        msglabel = None  # Reset the label reference

def minimax(board , isMaximizing):
    
   if checkForWin("O"):
        return 1 
   if checkForWin("X"):
        return -1
   if checkfordraw():
        return 0
   if isMaximizing: 
      bestScore = -100  #bestScore = -float("inf")   float("inf") represents positive infinity in Python, so -float("inf") is negative infinity.
      for key in board.keys():
         if board[key] == " ":
            board[key] = "O"
            score = minimax(board , False) # minimax
            board[key] = " "
            if score > bestScore : 
               bestScore = score 
        
      return bestScore
    
   else:
      bestScore = 100   #bestScore = -float("inf")
      for key in board.keys():
         if board[key] == " ":
            board[key] = "X"
            score = minimax(board , True) # minimax
            board[key] = " "
            if score < bestScore : 
               bestScore = score 
        
      return bestScore
    
def playComputer():
   bestScore = -100 
   bestMove = 0
   for key in board.keys():
      if board[key] == " ":
         board[key] = "O"
         score = minimax(board , False) # minimax
         board[key] = " "
         if score > bestScore : 
               bestScore = score 
               bestMove = key

   board[bestMove] = "O"  
   buttons[bestMove - 1]["text"] = "O"  # Update the button text to show "O"  

# Function to play
def play(event):
   global turn, game_end, msglabel
   if game_end:
        return
   button = event.widget
   clicked = buttons.index(button) + 1  # Get button index directly and adjust to board position (1-9)

   if button["text"] == " ":  # Proceed only if the spot is unoccupied
        board[clicked] = turn
        button["text"] = turn

        # Check for win condition
        if checkForWin(turn):
            msglabel = Label(frame2, text=f"{turn} wins the game", font=("Comic Sans MS", 25), bg="#00008B", fg="#FFFF00", padx=4, pady=15, width=18)
            msglabel.grid(row=2, column=0, columnspan=3)
            game_end = True

        elif checkfordraw():  # Check for draw condition
            #msglabel = Label(frame2, text="Game Draw", bg="#98FB98",fg = "#006400" ,font=("Comic Sans MS", 26), width=18, padx=4, pady=15)
            msglabel = Label(frame2, text="Game Draw", bg="#DC143C", fg="gold" ,font=("Comic Sans MS", 26), width=18, padx=4, pady=15)
            msglabel.grid(row=2, column=0, columnspan=3)
            game_end = True

        else:
            # Change turn for next player or computer
            turn = "O" if turn == "X" else "X"
            #updateBoard()  # Sync board visually

            # Handle computer's move if in single-player mode
            if turn == "O" and mode == "singlePlayer":
                playComputer()
                if checkForWin(turn):
                  msglabel = Label(frame2, text=f"{turn} wins the game", font=("Comic Sans MS", 26),  bg="#4B0082", fg="#FFD700", width=18, padx=4, pady=15)
                  msglabel.grid(row=2, column=0, columnspan=3)
                  game_end = True
                turn = "X"
                #updateBoard()  # Sync board visually for next turn

   

    # restricting user to place in a box already occupied
# ------ UI --------

# Change Mode options 

singlePlayerButton = Button(optionFrame , text="SinglePlayer" , width=13 , height=1 , font=("Arial" , 15) , bg="#F5F5DC" , relief=RAISED , borderwidth=5 , command=changeModeToSinglePlayer)
singlePlayerButton.grid(row=0 , column=0 , columnspan=1 , sticky=NW)

multiPlayerButton = Button(optionFrame , text="Multiplayer" , width=13 , height=1 , font=("Arial" , 15) , bg="#F5F5DC" , relief=RAISED , borderwidth=5 , command=changeModeToMultiplayer )
multiPlayerButton.grid(row=0 , column=1 , columnspan=1 , sticky=NW)

# Tic Tac Toe Board 
#       
#FIRST ROW

button1 = Button(frame2 , text = " ",width = 4 , height = 2,font=("Cooper Black",30),bg="#AFEEEE",fg = "#191970",relief=GROOVE,borderwidth=8)
button1.grid(row = 1 , column = 0, padx=5, pady=5)
button1.bind("<Button-1>",play)

button2 = Button(frame2 , text = " ",width = 4 , height = 2,font=("Cooper Black",30),bg="#AFEEEE",fg = "#191970",relief=GROOVE,borderwidth=8)  
button2.grid(row = 1 , column = 1, padx=5, pady=5)
button2.bind("<Button-1>",play)

button3 = Button(frame2 , text = " ",width = 4 , height = 2,font=("Cooper Black",30),bg="#AFEEEE",fg = "#191970",relief=GROOVE,borderwidth=8)  
button3.grid(row = 1 , column = 2, padx=5, pady=5)
button3.bind("<Button-1>",play)

#SECOND ROW

button4 = Button(frame2 , text = " ",width = 4 , height = 2,font=("Cooper Black",30),bg="#AFEEEE",fg = "#191970",relief=GROOVE,borderwidth=8)   
button4.grid(row = 2 , column = 0, padx=5, pady=5)
button4.bind("<Button-1>",play)

button5 = Button(frame2 , text = " ",width = 4 , height = 2,font=("Cooper Black",30),bg="#AFEEEE",fg = "#191970",relief=GROOVE,borderwidth=8) 
button5.grid(row = 2 , column = 1, padx=5, pady=5)
button5.bind("<Button-1>",play)

button6 = Button(frame2 , text = " ",width = 4 , height = 2,font=("Cooper Black",30),bg="#AFEEEE",fg = "#191970",relief=GROOVE,borderwidth=8) 
button6.grid(row = 2 , column = 2, padx=5, pady=5)
button6.bind("<Button-1>",play)

#THIRD ROW

button7 = Button(frame2 , text = " ",width = 4 , height = 2,font=("Cooper Black",30),bg="#AFEEEE",fg = "#191970",relief=GROOVE,borderwidth=8) 
button7.grid(row = 3 , column = 0, padx=5, pady=5)
button7.bind("<Button-1>",play)

button8 = Button(frame2 , text = " ",width = 4 , height = 2,font=("Cooper Black",30),bg="#AFEEEE",fg = "#191970",relief=GROOVE,borderwidth=8) 
button8.grid(row = 3 , column = 1, padx=5, pady=5)
button8.bind("<Button-1>",play)

button9 = Button(frame2 , text = " ",width = 4 , height = 2,font=("Cooper Black",30),bg="#AFEEEE",fg = "#191970",relief=GROOVE,borderwidth=8)
button9.grid(row = 3 , column = 2, padx=5, pady=5)
button9.bind("<Button-1>",play)


restartButton = Button(frame2 , text="Restart Game",width=10,height=3,font=("helvetica",10,"bold"),bg="#32CD32",fg = "black",relief=RAISED,borderwidth=20,command=RestartGame) 
restartButton.grid(row = 6, column=0,)

quitButton = Button(frame2, text="Quit Game", width=10, height=3, font=("helvetica",10,"bold"), bg="#DC143C", fg="black", relief=RAISED, borderwidth=20, command=root.destroy) #FF4500
quitButton.grid(row=6, column=2)

buttons = [ button1 , button2 , button3 , button4 , button5 , button6 , button7 , button8 , button9 ]

root.mainloop()
