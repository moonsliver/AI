from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
unitlist.append([rows[index] + cols[index] for index in range(9)])
unitlist.append([rows[index] + cols[9-index-1] for index in range(9)])

# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    # TODO: Implement this function!
    if(values == None or values == False):
        return False
    
    digitLen = '123456789'
    tempResult =  values.copy()
    for unit in unitlist:
        tmpArr = [box for box in unit if len(tempResult[box]) == 2]
        if(len(tmpArr) <= 1):
            continue
            
        dictObj = {}
        for item in tmpArr:
            if(tempResult[item] not in dictObj.keys()):
                dictObj[tempResult[item]] = [item]
            else:
                dictObj[tempResult[item]].append(item)
        
        for (k,v) in dictObj.items():
            if(len(v) != 2):
                continue

            for item in unit:
                if(item in v):
                    continue

                for digit in k:
                    tempResult[item] = tempResult[item].replace(digit,'')
                    
    return tempResult


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function
    tmpResult = values.copy()
    for (k,v) in values.items():
        if(len(v) > 1):
            continue
            
        for item in peers[k]:
            tmpResult[item] = tmpResult[item].replace(v,'')
    return tmpResult


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    # TODO: Copy your code from the classroom to complete this function
    digits = '123456789'
    tmpResult = values.copy()
    for unit in unitlist:
        for digit in digits:        
            totalDigitInBoxs = [box for box in unit if digit in values[box]]
            if(len(totalDigitInBoxs)!=1):
                continue;
            
            tmpResult[totalDigitInBoxs[0]] = digit
    return tmpResult


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    # TODO: Copy your code from the classroom and modify it to complete this function
    '''
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    '''
    stop = False
    finalResult = values.copy()
    while not stop:
        valueAfter = only_choice(eliminate(finalResult))
        if len([box for box in valueAfter.keys() if len(valueAfter[box]) == 0]):
            return False
            
        confirmedValueBefore = len([ k for (k,v) in finalResult.items() if len(v) == 1])
        confirmedValueAfter = len([ k for (k,v) in valueAfter.items() if len(v) == 1])
        
        if(confirmedValueBefore != confirmedValueAfter):
            finalResult = valueAfter
        else:
            stop = True
            
    return finalResult
    

def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # TODO: Copy your code from the classroom to complete this function
    
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    if(values == False):
        return False

    if (len([box for box in values if len(values[box])==1]) == 81):
        return values
    display(values)
    values = naked_twins(values)
    
    boxLen, box = min([(len(values[box]),box) for box in values if(len(values[box])>1)])
    for num in values[box]:
        tmpValues = values.copy()
        tmpValues[box] = num
        result = search(tmpValues)
        if(result):
            return result

def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '......8.68.........7..863.....8............8..8.5.9...1.8..............8.....8.4.'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    
    if(result == None or result == False):
        print("There is no solution for this SUDO")
    else:
        display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
