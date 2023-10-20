from customtkinter import *
from tkinter import *
#Created by Macpickle, 2023 
#Connect 4 game, made with tkinter, and customtkinter

class Connect4(): 
#initializes the board to tkinter
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.board = self.textBoard()
        self.player = 0

    #draws the board on screen
    def drawBoard(self):    
        for i in range(self.columns):
            for j in range(self.rows):
                canvas.create_rectangle(i*125+500, j*125+150, (i+1)*125+500, (j+1)*125+150, outline='white')
        canvas.pack(fill=BOTH, expand=YES)

    #creates a 2d array of the board for checking win conditions, and current board state
    def textBoard(self):
        board = []
        for i in range(self.rows):
            board.append([])
            for j in range(self.columns):
                board[i].append(" ")  
        return board  
    
    #gets position of mouse cursor, then draws on screen what collumn is selected
    def getPos(self, x):
        match(x):
            case x if x >= 500 and x < 625:
                canvas.create_rectangle(500, 145, 625, 150, fill='green', tags="selected")
                return 0

            case x if x >= 625 and x < 750:
                canvas.create_rectangle(625, 145, 750, 150, fill='green', tags="selected")
                return 1

            case x if x >= 750 and x < 875:
                canvas.create_rectangle(750, 145, 875, 150, fill='green', tags="selected")
                return 2

            case x if x >= 875 and x < 1000:
                canvas.create_rectangle(875, 145, 1000, 150, fill='green', tags="selected")
                return 3

            case x if x >= 1000 and x < 1125:
                canvas.create_rectangle(1000, 145, 1125, 150, fill='green', tags="selected")
                return 4

            case x if x >= 1125 and x < 1250:
                canvas.create_rectangle(1125, 145, 1250, 150, fill='green', tags="selected")
                return 5

            case x if x >= 1250 and x < 1375:
                canvas.create_rectangle(1250, 145, 1375, 150, fill='green', tags="selected")
                return 6

            case _:
                canvas.delete("selected")

    #gets the y position of the piece, checks lowest position
    def placeOnBoard(self, x):
        if gameRunning: 
            for i in range(self.rows-1):
                #checks each row to check if empty, and if the next is empty. will fill with player if found
                if (self.board[i+1][x] != " "):
                    if (self.board[i][x] == " "):
                        self.board[i][x] = self.currentPlayer()
                        return i

                    #technically error, but fix later- still works
                    return None

            #base case, responsible for first input in column
            self.board[self.rows-1][x] = self.currentPlayer()
            return len(self.board)-1
    
    #gets x position, draws on screen where piece will be placed, when pressed
    def motion(self, event):
        x, y = event.x, event.y
        canvas.delete("selected")
        self.getPos(x)
    
    #gets x position, shows what player is currently playing, and draws piece on screen
    def motionOnClick(self, event):
        if gameRunning:
            #updates player on screen
            if self.player == 1:
                colour = "Red"

            elif self.player == 0:
                colour = "Yellow"

            showPlayer.configure(text = "Current Player: " + colour, text_color = colour, font = ("Arial", 40))

            #gets x position of mouse, then gets the column to be drawn in
            x = event.x
            x = board.getPos(x)
            #gets the column the piece is placed in
            y = board.placeOnBoard(x)

            #draws the piece on screen
            newPiece = Pieces(100 + (x*125) + 410, (y*125)+160, 200 + (x*125) + 415, (y*125)+265, self.player)
            newPiece.drawPiece()

            #checks if player has won
            self.checkWin(self.player)

    def currentPlayer(self):
        #swaps player, returns for drawing piece and updating board
        if self.player == 0:
            self.player = 1
            return "X"
        else:
            self.player = 0
            return "O"
            
    #checks if current player has won
    def checkWin(self, player):
        #checks horizontal
        for x in range(self.rows):
            for j in range(self.columns-3):
                if self.board[x][j] != " ":
                    if self.board[x][j] == self.board[x][j+1] == self.board[x][j+2] == self.board[x][j+3]:
                        restart(player)

        #checks vertical
        for x in range(self.rows-3):
            for j in range(self.columns):
                if self.board[x][j] != " ":
                    if self.board[x][j] == self.board[x+1][j] == self.board[x+2][j] == self.board[x+3][j]:
                        restart(player)

        #checks diagonal DOWNWARDS
        for x in range(self.rows-3):
            for j in range(self.columns-3):
                if self.board[x][j] != " ":
                    if self.board[x][j] == self.board[x+1][j+1] == self.board[x+2][j+2] == self.board[x+3][j+3]:
                        restart(player)

        #checks diagonal UPWARDS
        for x in range(self.rows-3):
            for j in range(3, self.columns):
                if self.board[x][j] != " ":
                    if self.board[x][j] == self.board[x+1][j-1] == self.board[x+2][j-2] == self.board[x+3][j-3]:
                        restart(player)
                        
class Pieces():
    #responsible for creating, and moving the pieces
    def __init__(self, x0, y0, x1, y1, colour):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

        self.colour = getColour(colour)

    def drawPiece(self):
        canvas.create_oval(self.x0, self.y0, self.x1, self.y1, fill=self.colour)
        canvas.pack(fill=BOTH, expand=YES)
def getColour(player):
    if player == 1:
        return "Red"
    else:
        return "Yellow"
    
def restartGame():
    #resets GUI and variables for new game
    canvas.destroy()
    showPlayer.destroy()
    restartBtn.destroy()
    winnerLabel.destroy()
    board.board= None
    startGame()

def restart(player):
    global restartBtn, winnerLabel, gameRunning
    #promts restart
    gameRunning = False

    winnerLabel = CTkLabel(window, text = str(getColour(player)) + " has won!", text_color = "green", font = ("Arial", 40))
    restartBtn = CTkButton(window, text = "Restart? ", command = restartGame)
    restartBtn.place(relx = .45, y=150)
    winnerLabel.place(relx=.4, y=100)

def startGame():
    global canvas, board, showPlayer, gameRunning
    gameRunning = True
    #shows player on screen
    showPlayer = CTkLabel(window, text = "Current Player: Red", text_color = "red", font = ("Arial", 40))
    showPlayer.pack(padx = 5, pady = 10)
    board = Connect4(6,7)
    canvas = Canvas(window, bg=window.cget('bg'), highlightthickness=0)
    board.drawBoard()
    board.player = 0

    #credit
    credit = CTkLabel(window, text = "Created by Macpickle, 2023", text_color = "white", font = ("Arial", 10))
    credit.place(relx = .01, rely = 0.95)
    
    #tracks mouse movement and click
    window.bind('<Motion>', board.motion)
    window.bind('<Button-1>', board.motionOnClick)
    window.mainloop()

def main():
    #initializes screen
    global window
    window = CTk()
    window.title("Connect 4")
    
    #get screen width and height
    SCwidth= window.winfo_screenwidth()               
    SCheight= window.winfo_screenheight()               
    
    #fullscreen with title bar
    window.geometry("%dx%d" % (SCwidth, SCheight))
    window.after(0, lambda:window.state("zoomed"))

    startGame()

if __name__ == '__main__':
    main()
