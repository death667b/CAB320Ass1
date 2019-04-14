
'''

Sanity check script to test your submission 'mySokobanSolver.py'


A similar script (with different inputs) will be used for marking your code.

Make sure that your code runs without errors with this script.


'''


from sokoban import Warehouse

from mySokobanSolver import my_team, taboo_cells, SokobanPuzzle, check_action_seq
from mySokobanSolver import solve_sokoban_elem, can_go_there, solve_sokoban_macro 

#from fredSokobanSolver import my_team, taboo_cells, SokobanPuzzle, check_action_seq
#from fredSokobanSolver import solve_sokoban_elem, can_go_there, solve_sokoban_macro 


    
def test_taboo_cells():
    wh = Warehouse()
    wh.load_warehouse("./warehouses/warehouse_01.txt")
    expected_answer = '####  \n#X #  \n#  ###\n#   X#\n#   X#\n#XX###\n####  '
    answer = taboo_cells(wh)
    fcn = test_taboo_cells    
    print('<<  Testing {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
        


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



def test_solve_sokoban_elem():
    puzzle_t1 ='#######\n#@ $. #\n#######'
    wh = Warehouse()    
    wh.extract_locations(puzzle_t1.split(sep='\n'))
    # first test
    answer = solve_sokoban_elem(wh)
    expected_answer = ['Right', 'Right']
    fcn = test_solve_sokoban_elem
    print('<<  First test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
    # second test
    puzzle_t2 ='#######\n#@ $ #.#\n#######'
    wh = Warehouse()    
    wh.extract_locations(puzzle_t2.split(sep='\n'))
    answer = solve_sokoban_elem(wh)
    expected_answer = ['Impossible']
    print('<<  Second test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
#     third test
    wh = Warehouse()
    wh.load_warehouse("./warehouses/warehouse_01.txt")
    answer = solve_sokoban_elem(wh)
    expected_answer = ['Down', 'Left', 'Up', 'Right', 'Right', 'Right', 'Down', 'Left', 'Up', 'Left', 'Left', 'Down', 'Down', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down', 'Down', 'Right', 'Right', 'Up', 'Left', 'Down', 'Left', 'Up', 'Up']

    fcn = test_solve_sokoban_elem
    print('<<  First test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
        
#     4 test
    wh = Warehouse()
    wh.load_warehouse("./warehouses/warehouse_03.txt")
    answer = solve_sokoban_elem(wh)
    expected_answer = ['Right', 'Up', 'Up', 'Left', 'Left', 'Left', 'Up', \
                       'Left', 'Down', 'Right', 'Right', 'Right', 'Right', \
                       'Down', 'Down', 'Left', 'Up', 'Right', 'Up', 'Left', \
                       'Left', 'Left', 'Down', 'Down', 'Left', 'Left', 'Left', \
                       'Up', 'Up', 'Right', 'Right', 'Down', 'Right', 'Down', \
                       'Left', 'Up', 'Up', 'Up', 'Right', 'Down', 'Down']
    
    fcn = test_solve_sokoban_elem
    print('<<  First test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
        print('Number of moves: ', len(expected_answer))
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ('+str(len(expected_answer))+' moves)');print(expected_answer)
        print('But, received  ('+str(len(answer))+' moves)');print(answer)
        
    wh = Warehouse()
    wh.load_warehouse("./warehouses/warehouse_47.txt")
    answer = solve_sokoban_elem(wh)
    expected_answer = ['Right', 'Right', 'Right', 'Up', 'Up', 'Up', 'Left', \
                       'Left', 'Down', 'Right', 'Right', 'Down', 'Down', 'Left', \
                       'Left', 'Left', 'Left', 'Up', 'Up', 'Right', 'Right', \
                       'Right', 'Up', 'Right', 'Down', 'Down', 'Up', 'Left', \
                       'Left', 'Left', 'Left', 'Down', 'Down', 'Right', 'Right', \
                       'Right', 'Right', 'Right', 'Right', 'Down', 'Right', \
                       'Right', 'Up', 'Left', 'Left', 'Left', 'Left', 'Left', \
                       'Left', 'Right', 'Right', 'Up', 'Up', 'Up', 'Right', \
                       'Right', 'Down', 'Left', 'Up', 'Left', 'Down', 'Down', \
                       'Up', 'Left', 'Left', 'Left', 'Left', 'Down', 'Down', \
                       'Down', 'Right', 'Right', 'Up', 'Right', 'Right', 'Left', \
                       'Left', 'Down', 'Left', 'Left', 'Up', 'Right', 'Right']
    
    fcn = test_solve_sokoban_elem
    print('<<  First test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
        print('Number of moves: ', len(expected_answer))
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ('+str(len(expected_answer))+' moves)');print(expected_answer)
        print('But, received  ('+str(len(answer))+' moves)');print(answer)
        
    wh = Warehouse()
    wh.load_warehouse("./warehouses/warehouse_147.txt")
    answer = solve_sokoban_elem(wh)
    expected_answer = ['Left', 'Left', 'Left', 'Left', 'Left', 'Left', 'Down', \
                       'Down', 'Down', 'Right', 'Right', 'Up', 'Left', 'Down', \
                       'Left', 'Up', 'Up', 'Left', 'Up', 'Right', 'Right', \
                       'Right', 'Right', 'Right', 'Right', 'Down', 'Right', 'Right', \
                       'Right', 'Up', 'Up', 'Left', 'Left', 'Down', 'Left', \
                       'Left', 'Left', 'Left', 'Left', 'Left', 'Down', 'Down', \
                       'Right', 'Right', 'Right', 'Down', 'Right', 'Down', 'Down', \
                       'Left', 'Up', 'Right', 'Up', 'Left', 'Left', 'Left', 'Right', \
                       'Right', 'Down', 'Down', 'Down', 'Left', 'Left', 'Up', \
                       'Up', 'Left', 'Up', 'Up', 'Up', 'Left', 'Up', 'Right', \
                       'Right', 'Right', 'Right', 'Right', 'Right', 'Left', 'Left', \
                       'Left', 'Left', 'Left', 'Down', 'Down', 'Right', 'Right', \
                       'Down', 'Left', 'Down', 'Left', 'Up', 'Up', 'Up', 'Left', \
                       'Up', 'Right', 'Right', 'Right', 'Right', 'Right', 'Down', \
                       'Right', 'Down', 'Right', 'Right', 'Up', 'Left', 'Right', \
                       'Right', 'Up', 'Up', 'Left', 'Left', 'Down', 'Left', 'Left', \
                       'Left', 'Left', 'Left', 'Left', 'Right', 'Right', 'Right', \
                       'Right', 'Right', 'Right', 'Up', 'Right', 'Right', 'Down', \
                       'Down', 'Left', 'Down', 'Left', 'Left', 'Up', 'Right', 'Up', \
                       'Left', 'Left', 'Down', 'Right', 'Right', 'Right', 'Down',\
                       'Right', 'Up']
    
    fcn = test_solve_sokoban_elem
    print('<<  First test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
        print('Number of moves: ', len(expected_answer))
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ('+str(len(expected_answer))+' moves)');print(expected_answer)
        print('But, received  ('+str(len(answer))+' moves)');print(answer)

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

  
def test_solve_sokoban_macro():
#    puzzle_t2 ='#######\n#@ $ .#\n#######'
#    wh = Warehouse()    
#    wh.extract_locations(puzzle_t2.split(sep='\n'))
#    # first test
#    answer=solve_sokoban_macro(wh)
#    expected_answer = [((1, 3), 'Right'), ((1, 4), 'Right')]
#    fcn = test_solve_sokoban_macro
#    print('<<  First test of {} >>'.format(fcn.__name__))
#    if answer==expected_answer:
#        print(fcn.__name__, ' passed!  :-)\n')
#    else:
#        print(fcn.__name__, ' failed!  :-(\n')
#        print('Expected ');print(expected_answer)
#        print('But, received ');print(answer)
    # second test
#    wh = Warehouse()
#    wh.load_warehouse("./warehouses/warehouse_01.txt")
#    answer=solve_sokoban_macro(wh)
#    expected_answer = [((1, 3), 'Right'), ((1, 4), 'Right')]
#    fcn = test_solve_sokoban_macro
#    print('<<  First test of {} >>'.format(fcn.__name__))
#    if answer==expected_answer:
#        print(fcn.__name__, ' passed!  :-)\n')
#    else:
#        print(fcn.__name__, ' failed!  :-(\n')
#        print('Expected ');print(expected_answer)
#        print('But, received ');print(answer)
    
#    wh = Warehouse()
#    wh.load_warehouse("./warehouses/warehouse_03.txt")
#    answer=solve_sokoban_macro(wh)
#    expected_answer = [((2, 6), 'Left'), ((2, 5), 'Left'), ((2, 4), 'Left'), ((2, 3), 'Down'),\
#                       ((3, 6), 'Up'), ((2, 6), 'Left'), ((2, 5), 'Left'), ((2, 4), 'Left'), \
#                       ((2, 3), 'Right'), ((3, 3), 'Down'), ((4, 3), 'Left'), ((2, 4), 'Down'), ((3, 4), 'Down')]
#    
#    fcn = test_solve_sokoban_macro
#    print('<<  First test of {} >>'.format(fcn.__name__))
#    if answer==expected_answer:
#        print(fcn.__name__, ' passed!  :-)\n')
#        print('Number of moves: ', len(expected_answer))
#    else:
#        print(fcn.__name__, ' failed!  :-(\n')
#        print('Expected ('+str(len(expected_answer))+' moves)');print(expected_answer)
#        print('But, received  ('+str(len(answer))+' moves)');print(answer)

    wh = Warehouse()
    wh.load_warehouse("./warehouses/warehouse_47.txt")
    answer=solve_sokoban_macro(wh)
    expected_answer = [((2, 4), 'Right'), ((2, 5), 'Right'), ((2, 2), 'Right'), \
                       ((2, 3), 'Right'), ((2, 6), 'Left'), ((2, 5), 'Down'), \
                       ((3, 5), 'Down'), ((4, 5), 'Right'), ((2, 4), 'Right'), \
                       ((2, 5), 'Down'), ((4, 6), 'Right'), ((4, 7), 'Right'), \
                       ((4, 8), 'Left'), ((4, 7), 'Left'), ((4, 6), 'Left'), \
                       ((4, 5), 'Left'), ((4, 4), 'Left'), ((4, 3), 'Left'), \
                       ((3, 5), 'Down'), ((4, 5), 'Right'), ((4, 2), 'Right'), \
                       ((4, 3), 'Right')]
    
    fcn = test_solve_sokoban_macro
    print('<<  First test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
        print('Number of moves: ', len(expected_answer))
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ('+str(len(expected_answer))+' moves)');print(expected_answer)
        print('But, received  ('+str(len(answer))+' moves)');print(answer)
    

if __name__ == "__main__":
    pass    
#    print(my_team())  # should print your team

    test_solve_sokoban_macro()   
    test_solve_sokoban_elem()
#    test_check_elem_action_seq()
#    test_taboo_cells()
#    test_can_go_there()
