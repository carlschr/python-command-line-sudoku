import random
import copy
import sys

# helper function to check if a string can be converted to int
def valid_integer(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

# locates the nearest empty sudoku space
def find_empty_space(puzzle):
    for i in range(0, 9):
        for j in range(0, 9):
            if puzzle[i][j] == 0:
                return [i, j]
    return False

# function to check sudoku rules for an input
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

# checks if a sudoku is solvable
def check_sudoku(puzzle_object):
    # copy of object to prevent mutations
    object_copy = copy.deepcopy(puzzle_object)

    # solves a sudoku and returns a boolean for its solvability
    def solve_sudoku(coord):
        # if the puzzle is filled, mark it as solved
        if not find_empty_space(object_copy['puzzle']):
            # if the puzzle has already been completed, mark it as having multiple solutions
            if object_copy['solved']:
                object_copy['multiple_solutions'] = True

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

# function to create a filled puzzle
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

# function to create a sudoku with missing tiles that is solvable
def generate_sudoku():
    new_puzzle = generate_puzzle()

    puzzle_obj = {
        'solved_puzzle': new_puzzle,
        'puzzle': [[0 for i in range(9)] for j in range(9)],
        'solved': False,
        'multiple_solutions': False
    }

    # Makes sure there are at least twenty filled tiles
    counter = 0
    while counter < 21:
        row = random.randint(0, 8)
        col = random.randint(0, 8)

        if puzzle_obj['puzzle'][row][col] != 0:
            continue

        puzzle_obj['puzzle'][row][col] = puzzle_obj['solved_puzzle'][row][col]
        counter += 1

    # Fills tiles until the puzzle is solvable
    while not check_sudoku(puzzle_obj):
        row = random.randint(0, 8)
        col = random.randint(0, 8)

        if puzzle_obj['puzzle'][row][col] != 0:
            continue

        puzzle_obj['puzzle'][row][col] = puzzle_obj['solved_puzzle'][row][col]

    return puzzle_obj

# function to print a nice looking sudoku puzzle
def print_sudoku(sudoku):
    row_strings = []
    for row in sudoku:
        # each row will start with a pipe
        row_string = '|'

        for i, num in enumerate(row):
            # the pipe for col 9 comes later
            if i == 8:
                row_string += str(num)
            # each col that isn't 3, 6, 9 will be followed by a space
            elif (i + 1) % 3 != 0:
                row_string += str(num) + ' '
            # col 3 and 6 are followed by a pipe
            else:
                row_string += str(num) + '|'

        row_strings.append(row_string)
    
    # top line
    print(' _________________')

    # rows are printed with a pipe on the end
    for i, row_string in enumerate(row_strings):
        # rows 3, 6 and 9 are underlined
        if not (i + 1) % 3:
            print("\u0332".join(row_string) + '|')
        else:
            print(f'{row_string}|')

# function to start the application
def play():
    new_sudoku = generate_sudoku()
    playing = True

    while playing:
        print_sudoku(new_sudoku['puzzle'])

        # gathers input from user
        arg = input('Enter an answer for a tile. (e.g. "r3c2 4"): ')
        # arg must be at least 6 chars and char 2, 4, and 6 must be valid integers
        while len(arg) < 6 or not valid_integer(arg[1]) or not valid_integer(arg[3]) or not valid_integer(arg[5]):
            arg = input('Enter an answer for a tile. (e.g. "r3c2 4"): ')

        row = int(arg[1])
        col = int(arg[3])
        num = int(arg[5])

        # if the arg is correct, add it to the working puzzle
        if new_sudoku['solved_puzzle'][row - 1][col - 1] == num:
            new_sudoku['puzzle'][row - 1][col - 1] = num

            # if the puzzle is filled ask if they want to keep playing
            if not find_empty_space(new_sudoku['puzzle']):
                print('Congrats, you finished the puzzle!')
                keep_playing = input('Keep playing? Y/N: ')

                # switch statement function
                def switch(argument):
                    switch_options = {
                        'Y': True,
                        'N': False
                    }
                    return switch_options.get(argument, False)

                response = switch(keep_playing.upper())
                if response:
                    play()
                else:
                    playing = False

            print('Got it, keep going!')
        else:
            print('Oops, That wasn\'t right!')

    # kills program if playing is set to False
    sys.exit()

# program start
play()