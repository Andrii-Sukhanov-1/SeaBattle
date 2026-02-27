import random
vertical_values=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

    
def neighbors(row, column):
    neighbor_sq = []
    if column + 1 <= 9:
        neighbor = str(row) + str(column + 1)
        neighbor_sq.append(neighbor)
    if column - 1 >= 0:
        neighbor = str(row) + str(column - 1)
        neighbor_sq.append(neighbor)
    if row + 1 <= 9:
        neighbor = str(row + 1) + str(column)
        neighbor_sq.append(neighbor)
    if row - 1 >= 0:
        neighbor = str(row - 1) + str(column)
        neighbor_sq.append(neighbor)
    return neighbor_sq


def kill_ship(m1, n1, m2, n2, board):  #m1 must be <= m2, the same for n's
    
    #Finding a rectangle in which all squares will be shown to the player
    #max and min handle with cases when the ship is on the corner of the map
    m1_limit=max(0, m1-1)
    m2_limit=min(9, m2+1)
    n1_limit=max(0, n1-1)
    n2_limit=min(9, n2+1)

    killed_ones=[]    #The function will also report which cells it killed
                      #via this list
    
    # The very killing
    for a in range(m1_limit, m2_limit + 1):
        for b in range(n1_limit, n2_limit + 1):
            if not '_' in board[a][b]:
                board[a][b]+='_'
                victim = str(a)+str(b)
                killed_ones.append(victim)
    return killed_ones  

def to_sink_or_not_to_sink(m, n, board):  #investigates the state of the ship to which belongs m, n square
                                          #and sinks it if all parts are destroyed
    victims=[]  #squares that will be killed in this function call
                #will be the value function returns
                #this variable is only used to remove water adjacent to ship
                #from list of cells computer perceives as unknown
    
    
    #Now we determine if current target has any dead neighbors
    found_dead_neighbor=False
    found_live_neighbor=False
    for square in neighbors(m, n): 
        m_neighbor=int(square[0])
        n_neighbor=int(square[1])
        neighbor=board[m_neighbor][n_neighbor]
        
        #The case when there is live neighbor
        if neighbor == '1':
            found_live_neighbor=True
            break
        
        #The case where there is dead neighbor
        elif neighbor == '1_':
            found_dead_neighbor=True
            break
     
    #The case when whole ship is one square (it dies)
    single_ship = not found_live_neighbor and not found_dead_neighbor
    if single_ship:
        victims = kill_ship(m, n, m, n, board)
        return victims
    
    #if we found adjacent dead ship piece, we screen the row or column of the ship further
    if found_dead_neighbor:
        live_ship_piece=False
        if m == m_neighbor: #Checking if ship under attack is horizontal
            #Rearranging n values so that n < n-neighbor
            n=min(n, n_neighbor)
            n_neighbor=n+1
                
            #finding lower n end
            #or terminating current move if there are any live squares in the ship left
            while not live_ship_piece:
                
                #if the lower n=0, we assign n=0 to one ship end and prevent going to negative indexes
                #(we don't want python to jump to the last column by having index -1)
                if n==0:
                    n_end1=0
                    m_end1 = m
                    break
                
                n-=1
                cell=board[m][n]
                if cell=='1':
                    live_ship_piece=True
                    
                elif cell=='1_':
                    pass
                else:
                    n_end1 = n+1
                    m_end1 = m
                    break
                    
            #finding upper n end
            #or terminating current move if there are any live squares in the ship left
            while not live_ship_piece:
                #if the upper n=9, we assign n=9 to one ship end and prevent going to negative indexes
                #(we don't want python to jump to the index 10, which doesn't exist)
                if n_neighbor==9:
                    m_end2=m
                    n_end2 = 9
                    break
                
                n_neighbor+=1
                cell=board[m][n_neighbor]
                
                if cell=='1':
                    live_ship_piece=True
                elif cell=='1_':
                    pass
                else:
                    n_end2 = n_neighbor-1
                    m_end2 = m
                    break
                    
            
        else:   #The case when ship is vertical 
            #Rearranging m values so that m < m_neighbor
            m=min(m, m_neighbor)
            m_neighbor=m+1
            
            #finding lower m
            #or terminating current move if there are any live squares in the ship left
            while not live_ship_piece:
                #if the lower m=0, we assign m=0 to one ship end and prevent going to negative indexes
                #(we don't want python to jump to the last row by having index -1)
                if m==0:
                    m_end1=0
                    n_end1 = n
                    break
                
                m-=1
                cell=board[m][n]
                
                if cell=='1':
                    live_ship_piece=True
            
                elif cell=='1_':
                    pass
                else:
                    m_end1 = m+1
                    n_end1 = n
                    break
            
            #finding upper m end
            #or terminating current move if there are any live squares in the ship left
            while not live_ship_piece:
                #if the upper m=9, we assign m=9 to one ship and and prevent going to negative indexes
                #(we don't want python to jump to the index 10, which will cause a error)
                if m_neighbor==9:
                    m_end2=9
                    n_end2 = n
                    break
                
                m_neighbor+=1
                cell=board[m_neighbor][n]
                
                if cell=='1':
                    live_ship_piece=True
                    #break
                elif cell=='1_':
                    pass
                else:
                    m_end2 = m_neighbor-1
                    n_end2 = n
                    break
            
        #Killing the whole ship if it has to be done    
        if not live_ship_piece:
            victims = kill_ship(m_end1, n_end1, m_end2, n_end2, board)
                
    return victims #roporting which cells we killed
                    
            
def endgame(winner):
    #after the game has ended
    #not killed ships of computer board are rendered visible           
    for x in range(10):
        for y in range(10):
            if computer_board[x][y] == '1':
                computer_board[x][y]='_1_'
    #The winner is announced and fully opened boards are displayed
    print(winner, 'is the winner! Congratulations!')
    output(player_board, computer_board)
    quit()                    
                    

def game_board():
    game_board=[ ['0' for i in range(10)] for i in range(10)]
    ship_orientation=['hozirontal', 'vertical']
    for size in range(4,0,-1):
        ship_number=0
        while ship_number < 5 - size:                       #creates different number of ships of differnt size
            orientation=random.choice(ship_orientation)
            
            #unavailable_squares is used to check if one ship overlaps with others:
            # '0' in game_board means water, '1' means ship
            unavailable_squares=0
            
            if orientation=='hozirontal':
                
                #Generating potential ship ends
                m = random.randint(0, 9)
                n1 = random.randint(0, 10-size)
                n2=n1+(size-1)
                
                #Finding a rectangle in which all squares should be empty for ship to spawn
                #max and min handle with cases when the ship is on the corner of the map
                m_limit1=max(0, m-1)
                m_limit2=min(9, m+1)
                n1_limit=max(0, n1-1)
                n2_limit=min(9, n2+1)
                
                #checking if coordinates are OK
                for row in range(m_limit1, m_limit2 + 1):
                    for x in range(n1_limit, n2_limit + 1):
                        if game_board[row][x] == '1':
                            unavailable_squares+=1
                            
                #spawning the ship if possible
                if unavailable_squares==0:
                    for y in range(n1, n2+1):
                        game_board[m][y]='1'
                    ship_number+=1
                    
                    
            if orientation=='vertical':
                
                #Generating potential ship ends
                m1 = random.randint(0, 10-size)
                n = random.randint(0, 9)
                m2=m1+(size-1)
                
                #Finding a rectangle in which all squares should be empty for ship to spawn
                #max and min handle with cases when the ship is on the corner of the map
                m1_limit=max(0, m1-1)
                m2_limit=min(9, m2+1)
                n_limit1=max(0, n-1)
                n_limit2=min(9, n+1)
                
                #checking if coordinates are OK
                for column in range(n_limit1, n_limit2 + 1):
                    for p in range(m1_limit, m2_limit + 1):
                        if game_board[p][column] == '1':
                            unavailable_squares+=1
                            
                #spawning the ship if possible
                if unavailable_squares==0:
                    for q in range(m1, m2+1):
                        game_board[q][n]='1'
                    ship_number+=1
                    
    return game_board


    
def output(board_plr, board_comp):
    #creating basic output symbols
    white_square = '\033[37m\u2588\033[0m'*2
    blue_square = '\033[34m\u2588\033[0m'*2
    black_square = '\033[30m\u2588\033[0m'*2
    green_square = '\033[32m\u2588\033[0m'*2
    magenta_square = '\033[35m\u2588\033[0m'*2
    
    #creaing dictionaries for translation of cell state into how it should look like
    output_comp_board= {
        '0'  :  white_square,
        '1'  :  white_square,
        '0_' :  blue_square,
        '1_' :  black_square,
        '_1_' : magenta_square
        }
    
    output_plr_board= {
        '0'  :  white_square,
        '1'  :  green_square,
        '0_' :  blue_square,
        '1_' :  black_square,
        }
    
    #Building the output
    print('  A B C D E F G H I J', ' ' * 11 + '  A B C D E F G H I J')
    for m in range(10):
        line_player_board = ' ' + str(m+1) 
        line_computer_board = ' ' + str(m+1)
        if m+1 == 10:
            line_player_board=line_player_board.lstrip()
            line_computer_board=line_computer_board.lstrip()
        for n in range(10):
            cell_player_board=board_plr[m][n]
            cell_computer_board=board_comp[m][n]
            line_player_board = line_player_board + output_plr_board[cell_player_board]
            line_computer_board = line_computer_board + output_comp_board[cell_computer_board]
        m_line = line_player_board + ' '*11 + line_computer_board
        print(m_line)
       
    
    
    
#Creating game boards
computer_board=game_board()
player_board=game_board()

#Defining numbers of successful moves 
computer_kills=0
player_kills=0

#Creating a memory for computer
unknown_squares=[]
squares_to_attack=[]
for a in range(0, 10):
    for b in range(0, 10):
        unknown=str(a)+str(b)
        unknown_squares.append(unknown)


    
#The Game
a1_style_move_comp="None yet"
n_moves=0
while True:
    
    #Player's move
    let_another_move_player=True
    while let_another_move_player:
        
        player_move=input("What square will you attack? (in form 'a1') ")  
        print('-'*100)
        
        #Used in bug fixing
        if player_move=='quit':
            quit(1)
            
        try:
            m, n =  int(player_move[1:]) - 1 , player_move[0]
            n=vertical_values.index(n)
            computer_board[m][n]
        except:
            print("Are you sure there's such a square? Try again")
            continue
        if '_' in computer_board[m][n]:
            print("Captain, didn't we attack this place already?")
            continue
        
        
        computer_board[m][n]+='_'      #Adding _ means the square content is now known for player  
        if computer_board[m][n]=='1_':  #Checking if we damaged any ship
            print('You have damaged the ship! Try again!')
            a1_style_move_comp='Skip'
            
            player_kills+=1
            to_sink_or_not_to_sink(m, n, computer_board)
            #Checking if the player won
            if player_kills==20:
                print('-'*100)
                print('My move: ' + a1_style_move_comp + ' ' * 24 + "Your move:" + player_move)
                endgame('Player')
            
            print('My move: ' + a1_style_move_comp + ' ' * 24 + "Your move:" + player_move)
            output(player_board, computer_board)
        #Preventing the player from attacking again if they haven't damaged ship        
        else:
            let_another_move_player=False
            
        
           
        
    print('-'*100)
        
        
    #Computer's move             
    let_another_move_computer=True        
    while let_another_move_computer:
        to_delete_from_memory=[]  #Used to control computer memory
        if squares_to_attack:
            comp_move=random.choice(squares_to_attack)
            
        else:
            comp_move=random.choice(unknown_squares)
        m, n = int(comp_move[0]), int(comp_move[1])
        a1_style_move_comp=vertical_values[n] + str(m+1)
        unknown_squares.remove(comp_move)
        
       
        
        current_cell=player_board[m][n]
        current_cell+='_'                    #Adding _ means the square content is now known
        player_board[m][n]=current_cell
        if current_cell=='1_': #Checking if we damaged any ship
            print('I have damaged the ship! You better give up!')
            player_move='Skip'
            computer_kills+=1
            #Checking if the computer won
            if computer_kills==20:
                print('-'*100)
                print('My move: ' + a1_style_move_comp + ' ' * 24 + "Your move:" + player_move)
                endgame('Computer')
                
            
            
            to_delete_from_memory = to_sink_or_not_to_sink(m, n, player_board) # if the ship sunk
                                                                               #A list is filled with coordinates of water adjacent to it
            #if the full ship is to sink, we notify computer that water adjacent to it is no longer a target
            for cell in to_delete_from_memory:
                if cell in unknown_squares:
                    unknown_squares.remove(cell)
                
            #This block modifies list of squares that will be in priority
            #for computer's next move
                
            # if current move sunk a ship, there is no use in current content of
            #squares_to attack: computer should just attack random cells
            if to_delete_from_memory:
                squares_to_attack=[]
                
            #else if  before we didn't have any potential targets,
            #then unknown neighbors of current move should be attacked next time
            elif not squares_to_attack: 
                for neighbor in neighbors(m, n):
                    m, n = int(neighbor[0]), int(neighbor[1])
                    if not '_' in player_board[m][n]:
                        squares_to_attack.append(neighbor)
                        
            #the case when we had potential targets this move           
            else:
                squares_to_attack=[]  #we will fully rewrite next targets list
                if previous_kill_m == m:  #checking if the ship is horizontal
                    #Finding n's of 2 last targets (so that n1 < n2)
                    n1_dead=min(n, previous_kill_n)
                    n2_dead=n1_dead+1
                    
                    while True:
                        if n1_dead != 0:
                            #we check the eligibility of squares where the rest of ship may hide
                            #eligibility = the square is not outside the board and still unknown
                            #if it is ok, we store them in squares_to_attack
                            if not '_' in player_board[m][n1_dead-1]:
                                target=str(m) + str(n1_dead-1)
                                if target in unknown_squares:
                                    squares_to_attack.append(target)
                                break
                            #if the square is dead ship, we go forward to check eligibility of its neighbor    
                            elif player_board[m][n1_dead-1] == '1_':
                                n1_dead-=1
                            #if the square is '0_', we stop    
                            else:
                                break
                        
                    while True:
                        if n2_dead != 9:
                            #we check the eligibility of squares where the rest of ship may hide
                            #eligibility = the square is not outside the board and still unknown
                            #if it is ok, we store them in squares_to_attack
                            if not '_' in player_board[m][n2_dead+1]:
                                target=str(m) + str(n2_dead+1)
                                if target in unknown_squares:
                                    squares_to_attack.append(target)
                                break
                            #if the square is dead ship, we go forward to check eligibility of its neighbor    
                            elif player_board[m][n2_dead+1] == '1_':
                                n2_dead+=1
                            #if the square is '0_', we stop    
                            else:
                                break
                        
                    for cell in squares_to_attack:
                        if cell[0] != m:
                            squares_to_attack.remove(cell)
                            
                #the same screening logic is applied as in horizontal ship case
                if previous_kill_n == n:  #checking if the ship is vertical
                    #Finding m's of 2 last targets (so that m1 < m2)
                    m1_dead=min(m, previous_kill_m)
                    m2_dead=m1_dead+1
                    #we check the eligibility of squares where the rest of ship may hide
                    #eligibility = the square is not outside the board and still unknown
                    #if it is ok, we store them in squares_to_attack
                    while True:
                        if m1_dead != 0:
                            if not '_' in player_board[m1_dead-1][n]:
                                target=str(m1_dead-1) + str(n)
                                if target in unknown_squares:
                                    squares_to_attack.append(target)
                                break
                        elif player_board[m1_dead-1][n] == '1_':
                            m1_dead-=1
                        else:
                            break
                        
                    while True:
                        if m2_dead != 9:
                            if not '_' in player_board[m2_dead+1][n]:
                                target=str(m2_dead+1) + str(n)
                                if target in unknown_squares:
                                    squares_to_attack.append(target)
                                break
                            elif player_board[m2_dead+1][n] == '1_':
                                m2_dead+=1
                            else:
                                break
                            
                            
                    for cell in squares_to_attack:
                        if cell[1] != n:
                            squares_to_attack.remove(cell)
                    
            #storing last target
            previous_kill_m = m
            previous_kill_n = n
            
                
                
         
            print('My move: ' + a1_style_move_comp + ' ' * 24 + "Your move:" + player_move)
            output(player_board, computer_board)
              
        #Preventing the computer from attacking again if it hasn't damaged ship         
        else:
            let_another_move_computer=False
            print('My move: ' + a1_style_move_comp + ' ' * 24 + "Your move:" + player_move)
            output(player_board, computer_board)
            
    if comp_move in squares_to_attack:
                squares_to_attack.remove(comp_move)
             
    print('-'*100)
    n_moves+=1



        
        
        
    
        
    
        
        
            
                              