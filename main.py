import random
import copy
import sys
from Data_Structures.DLX import DLX

# helper function to check if a string can be converted to int
def valid_integer(string):
    try:
        int(string)
        return True
    except ValueError:
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
def check_sudoku(puzzle_str):
    cover = DLX(puzzle_str)
    cover.solve()
    return cover.at_least_one_solution and not cover.multiple_solutions

# function to create a filled puzzle
def generate_puzzle():
    # initalizes empty puzzle with a tile counter set to 0
    new_puzzle = {
        'puzzle': [[0 for i in range(9)] for j in range(9)],
        'current_space': 0
    }

    # recursive function to build upon above puzzle
    def build_sudoku():
        space = new_puzzle['current_space']
        # the counter being at 81 indicates that the puzzle is full
        if space == 81:
            return
        # creates coordinates of current tile from counter
        coord = [int(space//9), space % 9]

        # shuffled list of nums 1-9
        num_list = list(range(1, 10))
        random.shuffle(num_list)

        # tries nums 1-9 in random order at current tile
        for num in num_list:
            if new_puzzle['current_space'] == 81:
                return
            if check_valid_num(new_puzzle['puzzle'], num, coord):
                new_puzzle['puzzle'][coord[0]][coord[1]] = num
                new_puzzle['current_space'] += 1
                build_sudoku()

        # when the puzzle is full there is no need for resets as the function unwinds
        if new_puzzle['current_space'] == 81:
            return

        # sets current tile back to 0 and rewinds counter before backtracking
        new_puzzle['puzzle'][coord[0]][coord[1]] = 0
        new_puzzle['current_space'] -= 1
        return
    
    build_sudoku()
    return ''.join([''.join([str(n) for n in m]) for m in new_puzzle['puzzle']])

# function to create a sudoku with missing tiles that is solvable
def generate_sudoku():
    solved_puzzle = generate_puzzle()
    puzzle = '0' * 81

    # Makes sure there are at least twenty filled tiles
    counter = 0
    while counter < 21:
        cell = random.randint(0, 80)
        cell_digit = int(puzzle[cell:cell + 1])

        if cell_digit != 0:
            continue

        puzzle = puzzle[0:cell] + solved_puzzle[cell:cell + 1] + puzzle[cell + 1:]
        counter += 1

    # Fills tiles until the puzzle is solvable
    while not check_sudoku(puzzle):
        cell = random.randint(0, 80)
        cell_digit = int(puzzle[cell:cell + 1])

        if cell_digit != 0:
            continue

        puzzle = puzzle[0:cell] + solved_puzzle[cell:cell + 1] + puzzle[cell + 1:]
    
    return puzzle, solved_puzzle

# function to print a nice looking sudoku puzzle
def print_sudoku(sudoku_str):
    sudoku = [[s for s in sudoku_str[n:n + 9]] for n in range(0, 81, 9)]
    row_strings = []
    for row in sudoku:
        # each row will start with a pipe
        row_string = '|'

        for i, num in enumerate(row):
            # the pipe for col 9 comes later
            if i == 8:
                row_string += num
            # each col that isn't 3, 6, 9 will be followed by a space
            elif (i + 1) % 3 != 0:
                row_string += num + ' '
            # col 3 and 6 are followed by a pipe
            else:
                row_string += num + '|'

        row_strings.append(row_string.replace('0', ' '))
    
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
    new_sudoku, new_sudoku_solved = generate_sudoku()
    playing = True

    while playing:
        print_sudoku(new_sudoku)

        # gathers input from user
        arg = input('Enter an answer for a tile. (e.g. "r3c2 4"): ')
        # arg must be at least 6 chars and char 2, 4, and 6 must be valid integers
        while len(arg) < 6 or not valid_integer(arg[1]) or not valid_integer(arg[3]) or not valid_integer(arg[5]):
            arg = input('Enter an answer for a tile. (e.g. "r3c2 4"): ')

        row = int(arg[1])
        col = int(arg[3])
        cell = (row - 1) * 9 + col - 1
        cell_num = int(new_sudoku_solved[cell:cell + 1])
        num = int(arg[5])

        # if the arg is correct, add it to the working puzzle
        if cell_num == num:
            new_sudoku = new_sudoku[0:cell] + str(cell_num) + new_sudoku[cell + 1:]

            # if the puzzle is filled ask if they want to keep playing
            if new_sudoku.find('0') == -1:
                print('Congrats, you finished the puzzle!')
                print_sudoku(new_sudoku)
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
                    print('Generating puzzle...')
                    play()
                else:
                    playing = False
                    continue

            print('Got it, keep going!')
        else:
            print('Oops, That wasn\'t right!')

    # kills program if playing is set to False
    print('Thanks for playing!')
    sys.exit()

# program start
if __name__ == '__main__':
    print('Generating puzzle...')
    play()