
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
        (9741232, 'Jordon', 'Ramsay')
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
    
    allow_taboo_push = False
    macro = False
    # if marco true - return [ ((3,4), 'Left'), ((5,2), 'Right')]
    # if marco false - return [ 'Left', 'Right' ]
    
    
    def createGoal(self, warehouse):
        houseLines = str(warehouse) \
            .replace('@', ' ') \
            .replace('$', ' ') \
            .replace('.', '*')
        return houseLines
    
    def __init__(self, origWarehouse, goal=None):
        
        self.initial = str(origWarehouse)
        if goal is None:
            self.goal = self.createGoal(self.initial)
        else:
            self.goal = goal

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        # These are in (y, x) format
        moveLeft = (-1, 0)
        moveRight = (1, 0)
        moveUp= (0, -1)
        moveDown = (0, 1) 
        possibleMoves = [moveLeft, moveRight, moveUp, moveDown]
        
        nodeAsString = state.split('\n')
        warehouseObject = sokoban.Warehouse()
        warehouseObject.extract_locations(nodeAsString)
        justTabooCells = taboo_cells(warehouseObject)
        tabooCells = list(sokoban.find_2D_iterator(justTabooCells.split('\n'), 'X')) \
            if not self.allow_taboo_push else []
        
        currentWalls = warehouseObject.walls
        currentBoxes = warehouseObject.boxes
        currentWorker = warehouseObject.worker
        
        if self.macro:
            for box in currentBoxes:
                for move in possibleMoves:
                    testNewBoxPosition = box[0]+move[0], box[1]+move[1]
                    # Need to reverse the tuple to be in a (x,y) format
                    testNewPlayerPosition = box[1]+(move[1]*-1), box[0]+(move[0]*-1)
                    canIGetThere = can_go_there(warehouseObject, testNewPlayerPosition)
                    
                    if canIGetThere and testNewBoxPosition not in currentWalls \
                            and testNewBoxPosition not in currentBoxes \
                            and testNewBoxPosition not in tabooCells:
                        revBox = box[1], box[0]
                        if move == moveLeft:
                            yield(revBox, "Left")
                        elif move == moveRight:
                            yield(revBox, "Right")
                        elif move == moveUp:
                            yield(revBox, "Up")
                        elif move == moveDown:
                            yield(revBox, "Down")
        else:
            for move in possibleMoves:
                # Need to reverse the tuple to be in a (x,y) format
                testNewPlayerPosition = currentWorker[0]+move[0], currentWorker[1]+move[1]
                if testNewPlayerPosition not in currentWalls:
                    if testNewPlayerPosition not in currentBoxes:
                        if move == moveLeft:
                            yield("Left")
                        elif move == moveRight:
                            yield("Right")
                        elif move == moveUp:
                            yield("Up")
                        elif move == moveDown:
                            yield("Down")
                    else:
                        # If there is a box in the way, make sure the box can legally be moved
                        newBoxPosition = testNewPlayerPosition[0]+move[0], testNewPlayerPosition[1]+move[1]
                        if newBoxPosition not in currentWalls and \
                                newBoxPosition not in currentBoxes and \
                                newBoxPosition not in tabooCells:
                            if move == moveLeft:
                                yield("Left")
                            elif move == moveRight:
                                yield("Right")
                            elif move == moveUp:
                                yield("Up")
                            elif move == moveDown:
                                yield("Down")
        
    def result(self, state, action):
        # NO TESTING - YOU ALREADY KNOW THAT THIS IS A VALID MOVE!!!
        stateArray = state.split('\n')       
        warehouseObject = sokoban.Warehouse()
        warehouseObject.extract_locations(stateArray)       
        workerPos = warehouseObject.worker
        
        # These are in (y, x) format
        moveLeft = ((-1, 0), 'Left')
        moveRight = ((1, 0), 'Right')
        moveUp= ((0, -1), 'Up')
        moveDown = ((0, 1), 'Down') 
        possibleMoves = [moveLeft, moveRight, moveUp, moveDown]
        if type(action) == tuple:
            actionString = action[1]
            moveFrom = action[0][1], action[0][0]
        else:
            actionString = action
        for movePair in possibleMoves:
            if movePair[1] == actionString:
                move = movePair[0]
                break
        
        # if marco true - action = [ ((3,4), 'Left'), ((5,2), 'Right')]
        if self.macro:
            boxArrayPosition = warehouseObject.boxes.index(moveFrom)
            newBoxPosition = moveFrom[0] + move[0], moveFrom[1] + move[1]
            warehouseObject.boxes[boxArrayPosition] = newBoxPosition
            warehouseObject.worker = moveFrom
            return str(warehouseObject)
        
        # if marco false - action = [ 'Left', 'Right' ]
        else:
            newWorkerPosition = workerPos[0] + move[0], workerPos[1] + move[1]
            testPos = stateArray[newWorkerPosition[1]][newWorkerPosition[0]]
            if testPos == ' ' or testPos == '.':
                # nothing more to do, just update state with worker = testPos
                warehouseObject.worker = newWorkerPosition
                return str(warehouseObject)
            elif testPos == '$' or testPos == '*':
                # need to shift box before moving worker to this location
                assert newWorkerPosition in warehouseObject.boxes
                boxArrayPosition = warehouseObject.boxes.index(newWorkerPosition)
                newBoxPosition = newWorkerPosition[0] + move[0], newWorkerPosition[1] + move[1]
                warehouseObject.boxes[boxArrayPosition] = newBoxPosition
                warehouseObject.worker = newWorkerPosition[0], newWorkerPosition[1]
                return str(warehouseObject)
        
        # The code should never EVER get here!
        print("STOP!!!!!!, you should never see this...")
        print("The possible actions failed to correctly find the actions available")
        assert False
    
    def goal_test(self, state):
        playerlessState = state.replace('@', ' ')
        return self.goal == playerlessState
    
    def value(self, state):
        return 1
    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def warehouse_deepcopy(warehouse):
    result = sokoban.Warehouse()
    result.worker = (warehouse.worker[0],warehouse.worker[1])
    
    boxesInternal = []
    for i in warehouse.boxes:
        boxesInternal.append((i[0], i[1]))
    
    
    result.boxes = boxesInternal
    result.targets = warehouse.targets
    result.walls = warehouse.walls
    return result

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
    whTemp = warehouse_deepcopy(warehouse)
    
    # These are in (y, x) format
    moveLeft = (-1, 0)
    moveRight = (1, 0)
    moveUp= (0, -1)
    moveDown = (0, 1)
    
    def wallsAndBoxesCheck(whh, action):
        workLocation = whh.worker
        whWalls = whh.walls
        whBoxes = whh.boxes
        
        testLocation = workLocation[0] + action[0], workLocation[1] + action[1] 
        if testLocation not in whWalls:
            if testLocation in whBoxes:
                # NewLocation is a possible box location
                # Testing to see if it will be in a wall OR another box
                newLocation = testLocation[0] + action[0], testLocation[1] + action[1] 
                if newLocation in whWalls or newLocation in whBoxes:
                    return "Failure"
                # Move the box
                boxIdx = whBoxes.index(testLocation)
                whBoxes[boxIdx] = newLocation
            newWorker = testLocation
        else:
            return "Failure"
            
        return whh.copy(worker = newWorker, boxes = whBoxes)
        
    
    for action in action_seq:
        if action == 'Left':
            whTemp = wallsAndBoxesCheck(whTemp, moveLeft)
            if not isinstance(whTemp, sokoban.Warehouse):
                break
        elif action == 'Right':
            whTemp = wallsAndBoxesCheck(whTemp, moveRight)
            if not isinstance(whTemp, sokoban.Warehouse):
                break
        elif action == 'Up':
            whTemp = wallsAndBoxesCheck(whTemp, moveUp)
            if not isinstance(whTemp, sokoban.Warehouse):
                break
        elif action == 'Down':
            whTemp = wallsAndBoxesCheck(whTemp, moveDown)
            if not isinstance(whTemp, sokoban.Warehouse):
                break
    
    return str(whTemp)


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
    
    def heuristic(node):
        # Using Manhattan Distance for heuristics
        nodeState = node.state
        
        warehouseFromNode = sokoban.Warehouse()
        warehouseFromNode.extract_locations(nodeState)
        
        warehouseTargets = warehouseFromNode.targets
        warehouseTargetsCount = len(warehouseTargets)
        warehouseBoxes = warehouseFromNode.boxes
        warehouseWorker = warehouseFromNode.worker
        heuristicValue = 0
        
        for warehouseBox in warehouseBoxes:
            totalBoxDistance = 0
            
            aSquared = abs(warehouseBox[0] - warehouseWorker[0])
            bSquared = abs(warehouseBox[1] - warehouseWorker[1])
            workerDistanceToBox = (aSquared + bSquared) ** 0.5 
            
            for warehouseTarget in warehouseTargets:
                aSquared = abs(warehouseBox[0] - warehouseTarget[0])
                bSquared = abs(warehouseBox[1] - warehouseTarget[1])
                
                manhattanDistanceSingleBox = (aSquared + bSquared) ** 0.5 
                totalBoxDistance += manhattanDistanceSingleBox
            
            heuristicValue += (totalBoxDistance / warehouseTargetsCount) + (workerDistanceToBox*warehouseTargetsCount)
        
        return heuristicValue
    
    puzzle = SokobanPuzzle(warehouse)
    puzzle.macro = False
        
    searchResult = search.best_first_graph_search(puzzle, heuristic)
    
    if searchResult is None:
        return ['Impossible']
    
    result = []
    for node in searchResult.path():
        if node.action is not None:
            result.append(node.action)
    
    return result

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
    
    def heuristic(node):
        # Using Manhattan Distance for heuristics
        nodeState = node.state
        
        warehouseFromNode = sokoban.Warehouse()
        warehouseFromNode.extract_locations(nodeState)
        
        warehouseTargets = warehouseFromNode.targets
        warehouseTargetsCount = len(warehouseTargets)
        warehouseBoxes = warehouseFromNode.boxes
        warehouseWorker = warehouseFromNode.worker
        heuristicValue = 0
        
        for warehouseBox in warehouseBoxes:
            totalBoxDistance = 0
            
            aSquared = abs(warehouseBox[0] - warehouseWorker[0])
            bSquared = abs(warehouseBox[1] - warehouseWorker[1])
            workerDistanceToBox = (aSquared + bSquared) ** 0.5 
            
            for warehouseTarget in warehouseTargets:
                aSquared = abs(warehouseBox[0] - warehouseTarget[0])
                bSquared = abs(warehouseBox[1] - warehouseTarget[1])
                
                manhattanDistanceSingleBox = (aSquared + bSquared) ** 0.5 
                totalBoxDistance += manhattanDistanceSingleBox
            
            
            heuristicValue += (totalBoxDistance / warehouseTargetsCount) * workerDistanceToBox
        
        return heuristicValue
    
    puzzle = SokobanPuzzle(warehouse)
    puzzle.macro = True
        
    searchResult = search.best_first_graph_search(puzzle, heuristic)
    
    if searchResult is None:
        return ['Impossible']
    
    result = []
    for node in searchResult.path():
        if node.action is not None:
            result.append(node.action)
    
    return result

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
class Pathing(search.Problem):
    '''
    Tests to see if it is possible to get from A to B
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