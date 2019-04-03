
'''

    2019 CAB320 Sokoban assignment

The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

You are not allowed to change the defined interfaces.
That is, changing the formal parameters of a function will break the 
interface and triggers to a fail for the test of your code.
 
# by default does not allow push of boxes on taboo cells
SokobanPuzzle.allow_taboo_push = False 

# use elementary actions if self.macro == False
SokobanPuzzle.macro = False 

'''

# you have to use the 'search.py' file provided
# as your code will be tested with this specific file
import search

import sokoban



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ 
        (0000000, 'Alexandra', 'Koppon'),
        (5372828, 'Ian', 'Daniel'), 
        (0000000, 'Jordon', 'Ramsay')
    ]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A cell inside a warehouse is 
    called 'taboo' if whenever a box get pushed on such a cell then the puzzle 
    becomes unsolvable.  
    When determining the taboo cells, you must ignore all the existing boxes, 
    simply consider the walls and the target cells.  
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner inside the warehouse and not a target, 
             then it is a taboo cell.
     Rule 2: all the cells between two corners inside the warehouse along a 
             wall are taboo if none of these cells is a target.
    
    @param warehouse: a Warehouse object

    @return
       A string representing the puzzle with only the wall cells marked with 
       an '#' and the taboo cells marked with an 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''

    
    def inWarehouse(houseLines, inside, x, y):
        # protect agains negitive array elements
        lastX = 0 if x <= 1 else x - 1
        lineLength = len(houseLines[0])
        
        if houseLines[y][lastX] == '#' and \
            (houseLines[y][x] == ' ' or houseLines[y][x] == '.'):
            for idx in range(x, lineLength):
                if houseLines[y][idx] == '#':
                    inside = 1
        elif houseLines[y][x] == '#':
            inside = 0
        
        return inside
    
    def popLeft(arr):
        return (arr[:1][0], arr[1:])
    
    def drawHorizontalLine(houseLines, y):
        newLine = '-1'
        indices = [i for i, x in enumerate(houseLines[y]) if x == "X"]
        if len(indices) > 1: 
            popped, indices = popLeft(indices)
            counter = 0
            for x in range(popped+1, indices[0]):
                if houseLines[y][x] == ' ' and (houseLines[y-1][x] == '#' or houseLines[y+1][x] == '#'):
                    counter += 1
                else:
                    counter = 0
                    break
                
            if counter > 0:
                newLine = houseLines[y][:popped+1]+('X'*counter)+houseLines[y][indices[0]:]
        return newLine
    
    # Prepair houseLines leaving the targets in place for now
    houseLines = str(warehouse) \
        .replace('@', ' ') \
        .replace('$', ' ') \
        .replace('*', '.') \
        .split('\n')
    
    # Calculates corner cells and horizontal taboo lines
    for y in range(1, len(houseLines)-1):
        inside= 0
        for x in range(len(houseLines[y])):
            inside = inWarehouse(houseLines, inside, x, y)
            
            if inside == 1 and houseLines[y][x] != '.':
                # Check top left corner
                if houseLines[y-1][x] == '#' and houseLines[y][x-1] == '#':
                    houseLines[y] = houseLines[y][:x] + 'X' + houseLines[y][x+1:]
                # Check top right corner
                if houseLines[y-1][x] == '#' and houseLines[y][x+1] == '#':
                    houseLines[y] = houseLines[y][:x] + 'X' + houseLines[y][x+1:]
                # Check bottom left corner
                if houseLines[y+1][x] == '#' and houseLines[y][x-1] == '#':
                    houseLines[y] = houseLines[y][:x] + 'X' + houseLines[y][x+1:]
                # Check bottom right corner
                if houseLines[y+1][x] == '#' and houseLines[y][x+1] == '#':
                    houseLines[y] = houseLines[y][:x] + 'X' + houseLines[y][x+1:]
          
         
        newLine = drawHorizontalLine(houseLines, y)
        if newLine != '-1':
            houseLines[y] = newLine
            
    # Calculates vertical taboo lines (needs all corners computed)
    for y in range(1, len(houseLines)-1):
        for x in range(1, len(houseLines[y])-1):
            if houseLines[y][x] == 'X':
                # Start checking downward
                counter = 0
                for yy in range(y+1, len(houseLines)-1):
                    if houseLines[yy][x] == ' ' and (houseLines[yy][x-1] == '#' or houseLines[yy][x+1] == '#'):
                        counter += 1
                    elif houseLines[yy][x] == 'X' and (houseLines[yy][x-1] == '#' or houseLines[yy][x+1] == '#'):
                        # Line ends here
                        break
                    else:
                        # Fails the rules
                        counter = 0
                        break
                if counter > 0:
                    # apply found taboo
                    for yy in range(y+1, counter+y+2):
                        houseLines[yy] = houseLines[yy][:x]+'X'+houseLines[yy][x+1:]
    
    returnStr = '\n'.join(houseLines).replace('.', ' ')
    
    #print ('\n'+returnStr)

    return returnStr

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    Each instance should have at least the following attributes
    - self.allow_taboo_push
    - self.macro
    
    When self.allow_taboo_push is set to True, the 'actions' function should 
    return all possible legal moves including those that move a box on a taboo 
    cell. If self.allow_taboo_push is set to False, those moves should not be
    included in the returned list of actions.
    
    If self.macro is set True, the 'actions' function should return 
    macro actions. If self.macro is set False, the 'actions' function should 
    return elementary actions.
    
    
    '''
    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' function is needed
    #     to satisfy the interface of 'search.Problem'.

    
    def __init__(self, warehouse):
        raise NotImplementedError()

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        raise NotImplementedError

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Failure', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_elem(warehouse):
    '''    
    This function should solve using elementary actions 
    the puzzle defined in a file.
    
    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return the string 'Impossible'
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,column) 
    without pushing any box.
    
    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''
    
    def heuristic(node):
        # Using Manhattan Distance for heuristics
        nodeState = node.state
        
        aSquared = (nodeState[0] - dst[0]) ** 2
        bSquared = (nodeState[1] - dst[1]) ** 2
        manhattanDistance = (aSquared + bSquared) ** 0.5
        
        return manhattanDistance
    
    worker = warehouse.worker
    node = search.astar_graph_search(Pathing(worker, warehouse, dst), heuristic)
           
    return node is not None

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_macro(warehouse):
    '''    
    Solve using macro actions the puzzle defined in the warehouse passed as
    a parameter. A sequence of macro actions should be 
    represented by a list M of the form
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ] 
    means that the worker first goes the box at row 3 and column 4 and pushes it left,
    then goes to the box at row 5 and column 2 and pushes it up, and finally
    goes the box at row 12 and column 4 and pushes it down.
    
    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return the string 'Impossible'
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class Pathing(search.Problem):
    '''
    Really need to write something here
    '''
    def __init__(self, initial, warehouse, goal=None):
        self.initial = initial
        self.warehouse = warehouse
        # Need to reverse the row(y) and col(x) 
        # from a (y,x) pair to (x,y) pair
        self.goal = (goal[1], goal[0])
        
    def value(self, state):
        # All moves have a cost of 1
        # This works with heuristics so they are admissible
        moveCost = 1
        return moveCost
    
    def result(self, state, action):
        newX = state[0] + action[0]
        newY = state[1] + action[1]
        
        return newX, newY 
    
    def actions(self, state):
        myTaboos = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        
        for wallOrBox in myTaboos:
            stateWithWallBox = state[0] + wallOrBox[0], state[1] + wallOrBox[1]
            
            if stateWithWallBox not in self.warehouse.boxes and stateWithWallBox not in self.warehouse.walls:
                yield wallOrBox
                
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -