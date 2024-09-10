import copy
from a1_partc import Queue

def get_overflow_list(grid):
    """
    Identifies cells in the grid that are overflowing.
    
    A cell is considered overflowing if its absolute value is greater than
    the number of its neighbors. Edge and corner cells have fewer neighbors.
    
    Args:
    grid (List[List[int]]): The 2D grid to check for overflowing cells.
    
    Returns:
    List[Tuple[int, int]] or None: A list of (row, column) coordinates of overflowing cells,
                                   or None if no cells are overflowing.
    """
    coords = []
    for row_i, row in enumerate(grid):
        max_nbs = 2 if row_i in (0, len(grid) - 1) else 3
        for col_i, value in enumerate(row):
            tmp_max = max_nbs - 1 if col_i in (0, len(row) - 1) else max_nbs
            if abs(value) > tmp_max:
                coords.append((row_i, col_i))
    return coords or None

def overflow(grid, a_queue, grids_added=0):
    """
    Simulates the overflow process on the grid.
    
    This function recursively handles overflows until the grid stabilizes
    or all cells have the same sign.
    
    Args:
    grid (List[List[int]]): The initial grid state.
    a_queue (Queue): A queue to store each new grid state.
    grids_added (int): The number of grids added to the queue (default is 0).
    
    Returns:
    int: The number of grids added to the queue during the process.
    """
    # Get the list of overflowing cells
    overflow_cells = get_overflow_list(grid)
    
    # Check if there are overflowing cells and if the grid has different signs
    if overflow_cells and not all_same_sign(grid):
        signs = []  # Parallel list of the signs of overflowing cells
        for y, x in overflow_cells:
            signs.append(grid[y][x] // abs(grid[y][x]))
            grid[y][x] = 0

        # Update the neighbors of each overflowing cell
        for i, (row, col) in enumerate(overflow_cells):
            for y, x in neighbors(row, col):
                if valid_coord(grid, y, x):
                    grid[y][x] = (abs(grid[y][x]) + 1) * signs[i]
        
        # Enqueue the new grid state
        a_queue.enqueue(copy.deepcopy(grid))
        grids_added += 1
        
        # Recursively handle the next overflow
        if get_overflow_list(grid):
            grids_added += overflow(grid, a_queue)
    
    return grids_added

def neighbors(row, col):
    """
    Returns the coordinates of the neighboring cells.
    
    Args:
    row (int): The row index of the cell.
    col (int): The column index of the cell.
    
    Returns:
    List[Tuple[int, int]]: A list of (row, column) coordinates of neighboring cells.
    """
    return [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

def valid_coord(grid, row, col):
    """
    Checks if the given coordinates are within the grid bounds.
    
    Args:
    grid (List[List[int]]): The 2D grid.
    row (int): The row index to check.
    col (int): The column index to check.
    
    Returns:
    bool: True if the coordinates are valid, False otherwise.
    """
    row_max = len(grid) - 1
    col_max = len(grid[0]) - 1
    return 0 <= row <= row_max and 0 <= col <= col_max

def all_same_sign(grid):
    """
    Checks if all non-zero values in the grid have the same sign.
    
    Args:
    grid (List[List[int]]): The 2D grid to check.
    
    Returns:
    bool: True if all non-zero values have the same sign, False otherwise.
    """
    sign = None
    all_same = True
    for row in grid:
        for val in row:
            if val != 0:
                if sign is None:
                    sign = val // abs(val)
                elif sign != val // abs(val):
                    all_same = False
    return all_same
