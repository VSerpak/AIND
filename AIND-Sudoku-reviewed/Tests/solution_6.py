
# coding: utf-8

# In[2]:

assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'


# In[3]:

def cross(A, B):
    """ Cross product of elements in A and elements in B. """
    cross_prod = [x+y for x in A for y in B]
    return cross_prod


# In[4]:

# Define boxes of a sudoku
boxes = cross(rows, cols)
# Define row units of a sudoku
row_units = [cross(r, cols) for r in rows]
# Define column units of a sudoku
column_units = [cross(rows, c) for c in cols]
# Define square units of a sudoku
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# Define diagonal units of a sudoku
diagonal_units = [[x+y for x, y in zip(rows, cols)], [x+y for x, y in zip(rows, cols[::-1])]]
# Create a list of all units of a sudoku
unitlist = row_units + column_units + square_units + diagonal_units
# Create a dictionary of peers of each box
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


# In[5]:

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


# In[6]:

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        values(dict): the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    naked_twin_dict = {}
    for unit in unitlist:
        # Build a dictionary/hash map to identify a naked twin pair
        vdict = {}
        for box in unit:
            # Identify box containing only 2 possibilities
            # as a candidate for a naked twin
            if len(values[box]) == 2:
                if not values[box] in vdict:
                    vdict[values[box]] = [box]
                else:
                    vdict[values[box]].append(box)
        # Examine the dictionary to validate the candidates present as
        # naked twin pairs
        for key in vdict:
            # Condition for the candidate to be a naked twin pair
            if len(vdict[key]) == 2:
                if not key in naked_twin_dict:
                    naked_twin_dict[key] = [unit]
                else:
                    naked_twin_dict[key].append(unit)

    # Eliminate the naked twins as possibilities for their peers
    for key in naked_twin_dict:
        for unit in naked_twin_dict[key]:
            for box in unit:
                if values[box] != key:
                    assign_value(values, box, values[box].replace(key[0], ''))
                    assign_value(values, box, values[box].replace(key[1], ''))
    return values


# In[7]:

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    sudoku_grid = {}
    for val, key in zip(grid, boxes):
        if val == '.':
            sudoku_grid[key] = '123456789'
        else:
            sudoku_grid[key] = val
    return sudoku_grid


# In[8]:

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print


# In[9]:

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Args:
        values(dict): A sudoku in dictionary form.
    Returns:
        evalues(dict): The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values,peer,values[peer].replace(digit,''))
            #values[peer] = values[peer].replace(digit,'')
    return values


# In[10]:

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values,dplaces[0],digit)
                #values[dplaces[0]] = digit
    return values


# In[11]:

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


# In[12]:

def search(values):
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier in reduce_puzzle
    if all(len(values[s]) == 1 for s in values): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in values if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        assign_value(new_sudoku,s,value)
        #new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


# In[ ]:

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = reduce_puzzle(values)
    values = search(values)
    values = naked_twins(values)
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(solve(diag_sudoku_grid))
    
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')


# In[ ]:


