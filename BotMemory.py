from GameBoard import GameBoard
class BotMemory:
    def __init__(self):
        #Creating a memory for computer
        unknown_squares=[]
        for m in range(0, GameBoard.HEIGHT - 1):
            for n in range(0, GameBoard.WIDTH - 1):
                unknown = (m, n)
                unknown_squares.append(unknown)

        self.unknown_squares = unknown_squares
        self.preferred_squares=[]
    

    