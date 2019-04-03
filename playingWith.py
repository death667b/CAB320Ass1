from sokoban import Warehouse
import search

class Pathing(search.Problem):
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
        return state[0] + action[0], state[1] + action[1]
    
    def actions(self, state):
        myTaboos = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        
        for wallOrBox in myTaboos:
            stateWithWallBox = state[0] + wallOrBox[0], state[1] + wallOrBox[1]
            
            if stateWithWallBox not in self.warehouse.boxes and stateWithWallBox not in self.warehouse.walls:
                yield wallOrBox

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

def test_can_go_there():
    puzzle_t1 ='#######\n#@ $. #\n#######'
    wh = Warehouse()    
    wh.extract_locations(puzzle_t1.split(sep='\n'))
    # first test
    answer = can_go_there(wh,(1,2))
    expected_answer = True
    fcn = test_can_go_there
    print('<<  First test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
    # second test
    answer = can_go_there(wh,(1,5))
    expected_answer = False
    print('<<  Second test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
        
test_can_go_there()