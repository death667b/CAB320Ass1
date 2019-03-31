from sokoban import Warehouse

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

def test_taboo_cells1():
    wh = Warehouse()
    wh.load_warehouse("./warehouses/warehouse_01.txt")
    expected_answer = '####  \n#X #  \n#  ###\n#   X#\n#   X#\n#XX###\n####  '
    answer = taboo_cells(wh)
#    fcn = test_taboo_cells1    
#    print('<<  Testing {} >>'.format(fcn.__name__))
#    if answer==expected_answer:
#        print(fcn.__name__, ' passed!  :-)\n')
#    else:
#        print(fcn.__name__, ' failed!  :-(\n')
#        print('Expected ');print(expected_answer)
#        print('But, received ');print(answer)

def test_taboo_cells2():
    wh = Warehouse()
    wh.load_warehouse("./warehouses/warehouse_87.txt")
    expected_answer = '####  \n#X #  \n#  ###\n#   X#\n#   X#\n#XX###\n####  '
    answer = taboo_cells(wh)
#    fcn = test_taboo_cells2    
#    print('<<  Testing {} >>'.format(fcn.__name__))
#    if answer==expected_answer:
#        print(fcn.__name__, ' passed!  :-)\n')
#    else:
#        print(fcn.__name__, ' failed!  :-(\n')
#        print('Expected ');print(expected_answer)
#        print('But, received ');print(answer)
        
test_taboo_cells2()