import random
from tabulate import tabulate

class GameBoard:
    #Gameboard parameters
    SHIP_MAX_SIZE  = 4
    HEIGHT = 10
    WIDTH = 10
    
    #formula defining number of n-sized ship as f(x)
    @classmethod
    def ship_number_by_size(cls, ship_size):
        return (cls.SHIP_MAX_SIZE + 1) - ship_size
    

    @classmethod
    def number_of_ship_and_cells(cls):
        #Finding number of ships and cells belonging to them
        pieces = 0
        ship = 0
        for size in range(1, cls.SHIP_MAX_SIZE + 1):
            this_size_number = cls.ship_number_by_size(size)
            pieces += size * this_size_number
            ship += this_size_number
        return ship, pieces
    
    



     
    
    @classmethod
    #defines what in what direction a ship can grow given one end coordinate
    #so that its second end is within a board
    #directions are in format (horizontal change, vertical change)
    def growth_directions(cls, m, n, size):
        directions = []
        d_coord = size - 1   #the difference in either m or n between ship ends 
        if (m + d_coord) <= (cls.HEIGHT - 1):
            directions.append((0, 1))
        if (m - d_coord) >= 0:
            directions.append((0, -1))
        if (n + d_coord) <= (cls.WIDTH - 1):
            directions.append((1, 0))
        if (n - d_coord) >= 0:
            directions.append((-1, 0))
        return directions


    @staticmethod
    def sort_2_ends(m1, n1, m2, n2):
        #making m2 >= m1, n2 >= n1
        m1, m2 = min(m1, m2), max(m1, m2)
        n1, n2 = min(n1, n2), max(n1, n2)
        return (m1, n1, m2, n2)
    

    @classmethod
    def ship_zone(cls, m1, n1, m2, n2): # m1 should be <= m2, n1 <= n2
        #Finding a rectangle of squares belonging to ship + its adjacent water
        #max and min handle with cases when the ship is on the corner of the map
        m1_limit = max(0, m1-1)
        m2_limit = min(cls.HEIGHT - 1, m2+1)
        n1_limit = max(0, n1-1)
        n2_limit = min(cls.WIDTH - 1, n2+1)

        return (m1_limit, n1_limit, m2_limit, n2_limit)
    

    
    #Used to check if there are any overlaps between currently generated ship and 
    #already existing ones
    def can_spawn(self, m1, n1, m2, n2):
        m1_limit, n1_limit, m2_limit, n2_limit = GameBoard.ship_zone(m1, n1, m2, n2)
                    
        #checking if coordinates are OK
        for m in range(m1_limit, m2_limit + 1):
            for n in range(n1_limit, n2_limit + 1):
                if self.board[m][n] == '1':
                        return False
        return True

    def __init__(self):
        self.quantity_by_size  = {}
        self.last_update = None #later the most recent kill will be stored here

        game_board=[ ['0' for _ in range(GameBoard.WIDTH)] for _ in range(GameBoard.HEIGHT)]
        self.board  = game_board

        for size in range(GameBoard.SHIP_MAX_SIZE, 0, -1):
            needed_ship_number = GameBoard.ship_number_by_size(size)
            ship_number=0
            fruitless_iterations = 0 
            while ship_number < needed_ship_number:                   #creates different number of ships of differnt size

                #Handle too tightly filled boards
                if fruitless_iterations > 1000:
                    raise ValueError(f'''
                    {fruitless_iterations} fruitless iterations while making size {size} ships were made.
                    Seems that there is not enough space on the {GameBoard.HEIGHT} by {GameBoard.WIDTH} board to spawn so many ships.
                    Decrease maximum ship size (now {GameBoard.SHIP_MAX_SIZE}) or spawn less ships.
                    Alternatively, increase board size.''')
                
                #generate one ship end
                m1 = random.randint(0, GameBoard.HEIGHT - 1)
                n1 = random.randint(0, GameBoard.WIDTH -1)
                
                #choose in which direction to 'grow' ship
                direction_vectors = GameBoard.growth_directions(m1, n1, size = size)
                growth_direction = random.choice(direction_vectors)
                dn, dm = growth_direction

                #generating second end
                m2 = m1 + dm * (size - 1)
                n2 = n1 + dn * (size - 1)
                
                #making m2 >= m1, n2 >= n1
                m1, n1, m2, n2 = GameBoard.sort_2_ends(m1, n1, m2, n2)

                #spawning the ship if possible
                if self.can_spawn(m1, n1, m2, n2):
                    for m in range(m1, m2 + 1):
                        for n in range(n1, n2 + 1):
                            self.board[m][n] = '1'
                    ship_number += 1
                else:
                    fruitless_iterations += 1
            self.quantity_by_size[size] = ship_number


    #For simple debug 
    def __str__(self):
        white_square = '\033[30m\u2588\033[0m'*2
        blue_square = '\033[34m\u2588\033[0m'*2
        board = tabulate(self.board)
        board = board.replace('0', white_square).replace('1', blue_square).replace(' ', '')
        return board

    #Allow indexing and assigning
    def __getitem__(self, row):
        return self.board[row]
    

    @classmethod
    def neighbors(cls, row, column):
        neighbor_sq = []
        if column + 1 <= cls.WIDTH - 1:
            neighbor = row, column + 1
            neighbor_sq.append(neighbor)
        if column - 1 >= 0:
            neighbor = row, column - 1
            neighbor_sq.append(neighbor)
        if row + 1 <= cls.HEIGHT - 1:
            neighbor = row + 1, column
            neighbor_sq.append(neighbor)
        if row - 1 >= 0:
            neighbor = row - 1, column
            neighbor_sq.append(neighbor)
        return neighbor_sq


    def kill_ship(self, m1, n1, m2, n2):  #m1 must be <= m2, the same for n's
    
        m1_limit, n1_limit, m2_limit, n2_limit = GameBoard.ship_zone(m1, n1, m2, n2)

        killed_ones=[]    #The function will also report which cells it killed
                        #via this list
        
        # The very killing
        for a in range(m1_limit, m2_limit + 1):
            for b in range(n1_limit, n2_limit + 1):
                if not '_' in self.board[a][b]:
                    self.board[a][b] += '_'
                    victim = a, b
                    killed_ones.append(victim)
        #Storing the last update (last kill) of a board         
        self.last_update = killed_ones
    

    #looks for an end of a ship from point(m, n) in direction (dm, dn),
    #and returns its coordinates
    #if ship is still alive, empty tuple is returned and scan is prematurely stopped
    def scan(self, m, n, dm, dn, depth = None) -> tuple:
        if depth == None:
            depth = GameBoard.SHIP_MAX_SIZE
       
        for _ in range(depth):
            #Jumping to the next point
            m += dm
            n += dn
        
            valid_m =  (0 <= m <= GameBoard.HEIGHT - 1)
            valid_n =  (0 <= n <= GameBoard.WIDTH - 1)
            square_inside_the_board = valid_m and valid_n

            #if the scan reached the end of the board without finding a live ship piece,
            #it should report that previous square if a ship end
            if not square_inside_the_board:
                return (m - dm, n - dn)
            
            cell = self.board[m][n]
            if cell=='1':
                #Report there is no need to sink a ship if live piece is found
                return ()
                
            elif cell=='1_':
                #Continue scan if current cell is dead ship
                pass
            else:
                #Current square is water, previous one is the ship end
                return (m - dm, n - dn)
            

    def kill_ship_if_needed(self, m, n): #investigates the state of the ship to which belongs m, n square
                                         #and sinks it if all parts are destroyed
                                         #updates the most recent 
     
        #now we determine if current target has any dead neighbors
        found_dead_neighbor = False
        found_live_neighbor = False
        for square in GameBoard.neighbors(m, n): 
            m_neighbor = square[0]
            n_neighbor = square[1]
            neighbor = self.board[m_neighbor][n_neighbor]
            
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
            self.kill_ship(m, n, m, n)
            return
            
        #if we found adjacent dead ship piece, we screen the row or column of the ship further
        if found_dead_neighbor:

            #Finding a direction vector (dm, dn) for scanning a ship's row/column
            dm, dn = abs(m - m_neighbor), abs(n - n_neighbor)

            ship_end1 = self.scan(m, n, -dm, -dn) #scan in negative direction
            if ship_end1:
                ship_end2 = self.scan(m, n, dm, dn) #scan in positive direction
                if ship_end2:
                    #No live neighbors found in both directions
                    #Killing the ship
                    m1, n1 = ship_end1
                    m2, n2 = ship_end2
                    self.kill_ship(m1, n1, m2, n2)
                    return
        
        
