from sokoban import Warehouse
import search

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
    whTemp = warehouse.copy()   
    
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
            if not isinstance(whTemp, Warehouse):
                break
        elif action == 'Right':
            whTemp = wallsAndBoxesCheck(whTemp, moveRight)
            if not isinstance(whTemp, Warehouse):
                break
        elif action == 'Up':
            whTemp = wallsAndBoxesCheck(whTemp, moveUp)
            if not isinstance(whTemp, Warehouse):
                break
        elif action == 'Down':
            whTemp = wallsAndBoxesCheck(whTemp, moveDown)
            if not isinstance(whTemp, Warehouse):
                break
    
    return str(whTemp)

def test_check_elem_action_seq():
    wh = Warehouse()
    wh.load_warehouse("./warehouses/warehouse_01.txt")
    # first test
    answer = check_action_seq(wh, ['Right', 'Right','Down'])
    expected_answer = '####  \n# .#  \n#  ###\n#*   #\n#  $@#\n#  ###\n####  '
    fcn = test_check_elem_action_seq    
    print('<<  First test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
    # second test
    answer = check_action_seq(wh, ['Right', 'Right','Right'])
    expected_answer = 'Failure'
    fcn = test_check_elem_action_seq    
    print('<<  Second test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
    # third test - push a box
    answer = check_action_seq(wh, ['Right', 'Right','Down','Left'])
    expected_answer = '####  \n# .#  \n#  ###\n#*   #\n# $@ #\n#  ###\n####  '
    fcn = test_check_elem_action_seq    
    print('<<  Third test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
    # fourth test - push a box into a wall
    answer = check_action_seq(wh, ['Right', 'Down'])
    expected_answer = 'Failure'
    fcn = test_check_elem_action_seq    
    print('<<  Fourth test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
        
test_check_elem_action_seq()