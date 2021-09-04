from Data_Structures.DLX import DLX
from Data_Structures.Sudoku import Sudoku

four_by_four_solved = '1243341221344321'
four_by_four_unsolved = '1043301021044020'

cover = DLX(four_by_four_unsolved)

def use_solution(node):
    sol_node = node
    cover.solution.append(node)
    while 1:
        sol_node.parent.cover()
        sol_node = sol_node.right
        if sol_node == node:
            break

def to_matrix_index(r, c, n):
    return (r * 16) + (c * 4) + (n % 4)

import matplotlib.pyplot as plt
size = cover.sudoku.size
x1 = []
y1 = []
x2 = []
y2 = []
x3 = []
y3 = []
x4 = []
y4 = []
for i, _ in enumerate(cover.matrix):
    for j, _ in enumerate(cover.matrix[0]):
        if cover.matrix[i][j] != 0:
            current = cover.matrix[i][j]
            if current.col < size ** 2:
                y1.append(size ** 3 - i)
                x1.append(j)
                continue
            if current.col < (size ** 2) * 2:
                y2.append(size ** 3 - i)
                x2.append(j)
                continue
            if current.col < (size ** 2) * 3:
                y3.append(size ** 3 - i)
                x3.append(j)
                continue
            y4.append(size ** 3 - i)
            x4.append(j)
plt.scatter(x1, y1, marker='.', c='black')
plt.scatter(x2, y2, marker='.', c='blue')
plt.scatter(x3, y3, marker='.', c='green')
plt.scatter(x4, y4, marker='.', c='red')
plt.xlabel('x - axis')
plt.ylabel('y - axis')
plt.title('Cover Matrix')
plt.grid()
# plt.show()

if 0:
    use_solution(cover.header.right.down)
    use_solution(cover.header.right.down)
    use_solution(cover.header.right.down)
    use_solution(cover.header.right.down)

    use_solution(cover.header.right.down)
    use_solution(cover.matrix[to_matrix_index(1, 1, 3)][5])
    use_solution(cover.header.right.down)
    use_solution(cover.matrix[to_matrix_index(1, 3, 1)][7])

    use_solution(cover.header.right.down)
    use_solution(cover.header.right.down)
    use_solution(cover.matrix[to_matrix_index(2, 2, 2)][10])
    use_solution(cover.header.right.down)

    use_solution(cover.header.right.down)
    use_solution(cover.matrix[to_matrix_index(3, 1, 2)][13])
    use_solution(cover.header.right.down)
    use_solution(cover.matrix[to_matrix_index(3, 3, 0)][15])

cover.solve()
current = cover.header
while 1:
    print(current)
    inpt = input('u, d, l, r')
    if inpt == 'l':
        current = current.left
        continue
    if inpt == 'r':
        current = current.right
        continue
    if inpt == 'u':
        current = current.up
        continue
    if inpt == 'd':
        current = current.down
        continue
    break



solution = cover.solved
print(solution)
if 0:
    for i, char in enumerate(four_by_four_unsolved):
        if char == '0':
            matrix_row = solution[i].row
            four_by_four_unsolved = four_by_four_unsolved[:i] + str((matrix_row % cover.sudoku.size) + 1) + four_by_four_unsolved[i + 1:]
    print(f'\nTest Solution: {Sudoku(four_by_four_unsolved)}')