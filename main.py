import random

def check_valid_num(puzzle, num, coord):
    # determine starting points for the sudoku square
    square_y = coord[0] - (coord[0] % 3)
    square_x = coord[1] - (coord[1] % 3)

    # check validity in row
    if puzzle[coord[0]].count(num) != 0:
        return False
    # check validity in column
    if [row[coord[1]] for row in puzzle].count(num) != 0:
        return False
    # check validity in square
    for i in range(3):
        for j in range(3):
            if puzzle[square_y + i][square_x + j] == num:
                return False

    return True

# example solvable sudoku
puzzle1 = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
          [6, 0, 0, 1, 9, 5, 0, 0, 0],
          [0, 9, 8, 0, 0, 0, 0, 6, 0],
          [8, 0, 0, 0, 6, 0, 0, 0, 3],
          [4, 0, 0, 8, 0, 3, 0, 0, 1],
          [7, 0, 0, 0, 2, 0, 0, 0, 6],
          [0, 6, 0, 0, 0, 0, 2, 8, 0],
          [0, 0, 0, 4, 1, 9, 0, 0, 5],
          [0, 0, 0, 0, 8, 0, 0, 7, 9]]

# example unsolvable sudoku
puzzle2 = [[5, 3, 2, 0, 7, 0, 0, 0, 0],
           [6, 0, 0, 1, 9, 5, 4, 0, 0],
           [0, 9, 8, 0, 0, 0, 1, 6, 0],
           [8, 0, 0, 0, 6, 0, 0, 0, 3],
           [4, 0, 0, 8, 0, 3, 0, 0, 1],
           [7, 0, 3, 0, 2, 0, 0, 0, 6],
           [0, 6, 0, 0, 0, 0, 2, 8, 0],
           [0, 0, 0, 4, 1, 9, 6, 0, 5],
           [0, 0, 0, 0, 8, 0, 0, 7, 9]]

# example sudoku with more than one solution
puzzle3 = [[0, 0, 0, 0, 7, 0, 0, 0, 0],
           [6, 0, 0, 0, 9, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 6, 0],
           [8, 0, 0, 0, 6, 0, 0, 0, 3],
           [0, 0, 0, 8, 0, 3, 0, 0, 1],
           [0, 0, 3, 0, 2, 0, 0, 0, 6],
           [0, 0, 0, 0, 0, 0, 0, 8, 0],
           [0, 0, 0, 0, 1, 0, 0, 0, 0],
           [0, 0, 0, 0, 8, 0, 0, 0, 0]]

# example object to pass into check_sudoku func
sudoku_object = {
    'puzzle': puzzle3,
}

# checks if a sudoku is solvable
def check_sudoku(puzzle_object):
    # copy of object to prevent mutations
    object_copy = {
        **puzzle_object,
        'solved': False,
        'multiple_solutions': False
    }

    # locates the nearest empty sudoku space
    def find_empty_space(puzzle):
        for i in range(0, 9):
            for j in range(0, 9):
                if puzzle[i][j] == 0:
                    return [i, j]
        return False

    # solves a sudoku and returns a boolean for its solvability
    def solve_sudoku(coord):
        # if the puzzle is filled, mark it as solved
        if not find_empty_space(object_copy['puzzle']):
            # if the puzzle has already been completed, mark it as having multiple solutions
            if object_copy['solved']:
                object_copy['multiple_solutions'] = True

            print(object_copy['puzzle'])
            object_copy['solved'] = True

        # for numbers 1 through 9
        # if there is an empty space, check for validity
        for num in range(1, 10):
            # if the puzzle is already marked for mult solutions, avoid unecessary computation
            if object_copy['multiple_solutions']:
                return 

            if coord:
                if check_valid_num(object_copy['puzzle'], num, coord):
                    object_copy['puzzle'][coord[0]][coord[1]] = num
                    solve_sudoku(find_empty_space(object_copy['puzzle']))
            else:
                return

        # before backtracking, reset the puzzle-space to 0
        object_copy['puzzle'][coord[0]][coord[1]] = 0
        return

    solve_sudoku(find_empty_space(object_copy['puzzle']))
    # print(object_copy['puzzle'])
    return object_copy['solved'] and not object_copy['multiple_solutions']

def generate_puzzle():
    # initalizes empty puzzle with a tile counter set to 0
    empty_puzzle = {
        'puzzle': [[0 for i in range(9)] for j in range(9)],
        'current_space': 0
    }

    # recursive function to build upon above puzzle
    def build_sudoku():
        space = empty_puzzle['current_space']
        # the counter being at 81 indicates that the puzzle is full
        if space == 81:
            return
        # creates coordinates of current tile from counter
        coord = [int((space - (space % 9))/9), space % 9]

        # shuffled list of nums 1-9
        num_list = list(range(1, 10))
        random.shuffle(num_list)

        # tries nums 1-9 in random order at current tile
        for num in num_list:
            if empty_puzzle['current_space'] == 81:
                return
            if check_valid_num(empty_puzzle['puzzle'], num, coord):
                empty_puzzle['puzzle'][coord[0]][coord[1]] = num
                empty_puzzle['current_space'] += 1
                build_sudoku()

        # when the puzzle is full there is no need for resets as the function unwinds
        if empty_puzzle['current_space'] == 81:
            return

        # sets current tile back to 0 and rewinds counter before backtracking
        empty_puzzle['puzzle'][coord[0]][coord[1]] = 0
        empty_puzzle['current_space'] -= 1
        return
    
    build_sudoku()
    return empty_puzzle['puzzle']

new_sudoku = generate_puzzle()
for row in new_sudoku:
    print(row)