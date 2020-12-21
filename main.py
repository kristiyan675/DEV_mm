var = input()
# rows
N = int(var.split(' ')[0])
# columns
M = int(var.split(' ')[1])

# Assessment - The validations that the numbers are even and the area of the first layer is larger that 2x2
while True:
    if N % 2 != 0 or M % 2 != 0:
        print('Please enter even numbers for the rows and columns')
        var = input()
        # rows
        N = int(var.split(' ')[0])
        # columns
        M = int(var.split(' ')[1])
    elif not 1 < N < 100 or not 2 < M < 100:
        print('Please enter numbers larger than 2 and smaller than 100 for the rows and columns')
        var = input()
        # rows
        N = int(var.split(' ')[0])
        # columns
        M = int(var.split(' ')[1])
    else:
        break

# instantiating the matrix
matrix = []
# dict for the numbers that are put horizontally
horizontals = {}
# dict for the numbers that are put vertically
verticals = {}

# filling in the matrix with the numbers
for i in range(N):
    matrix.append([int(x) for x in input().split()])

    # Assessment - Check if the user is submitting empty rows or rows that are with different numbers of columns
    if len(matrix[-1]) != M:
        print('Validate input has exactly same number of rows and columns')
        exit()

# loop over the matrix for analyse
for row in range(len(matrix)):
    for col in range(len(matrix[0])):
        if col + 1 < len(matrix[0]):
            # filling the horizontals dict
            if matrix[row][col] == matrix[row][col + 1]:
                temp = {matrix[row][col]: ((row, col), (row, col + 1))}
                horizontals.update(temp)
                # Assessment - Validate there are no bricks spanning 3 rows/ columns.
                try:
                    matrix[row][col + 2]
                    if matrix[row][col] == matrix[row][col + 2]:
                        print('There can be no bricks spanning 3 rows or columns.')
                        exit()
                except(IndexError):
                    continue

        if row + 1 < len(matrix):
            # filling the verticals dict
            if matrix[row][col] == matrix[row + 1][col]:
                temp = {matrix[row][col]: ((row, col), (row + 1, col))}
                verticals.update(temp)
                # Assessment - Validate there are no bricks spanning 3 rows/ columns.
                try:
                    matrix[row + 2][col]
                    if matrix[row][col] == matrix[row + 2][col]:
                        print('There can be no bricks spanning 3 rows or columns.')
                        exit()
                except(IndexError):
                    continue

# Assessment - If the matrix has two consecutive vertical bricks in the beginning or end, it has no solution
first_col = 0
second_col = 1
last_col = len(matrix[0]) - 1
before_last_col = len(matrix[0]) - 2
for row in range(0, len(matrix), 2):
    if matrix[row][first_col] == matrix[row + 1][first_col] and matrix[row][second_col] == matrix[row + 1][second_col]:
        exit(-1)
    elif matrix[row][before_last_col] == matrix[row + 1][before_last_col] and matrix[row][last_col] == matrix[row][
        last_col]:
        exit(-1)

# current row
row = 0
# current column
col = 0
# numbers of columns
length_of_a_row = len(matrix[0])

# loop over the matrix for creating the seconds layer
while row < len(matrix):
    while col < len(matrix[0]):
        # bool regarding the result from the check if there exist vertical bricks
        only_horizontals = True
        # check what is the current brick (horizontal or vertical)
        if matrix[row][col] == matrix[row][col + 1]:

            # check if there exist vertical bricks
            for x in range(col, len(matrix[0])):
                if matrix[row][x] in verticals.keys():
                    only_horizontals = False

            # solution if the row starts with a horizontal brick there are only horizontal bricks
            if only_horizontals:
                matrix[row + 1][col] = matrix[row][col]
                matrix[row][len(matrix[0]) - 1] = matrix[row + 1][len(matrix[0]) - 1]
                for temp in range(col + 1, len(matrix[0]) - 1, 2):
                    matrix[row][temp] = matrix[row][temp + 1]
                    matrix[row + 1][temp + 1] = matrix[row + 1][temp]
                row += 2
                break

            # solution if the row starts with a horizontal brick and there are also vertical bricks
            else:
                for var in verticals.keys():
                    coordinates_of_vertical = verticals[var]
                    matrix[row][col] = var
                    matrix[row + 1][col] = var
                    verticals.pop(var)
                    var = coordinates_of_vertical[0][1]
                    break
                for temp in range(col + 1, var + 1, 2):
                    matrix[row][temp + 1] = matrix[row][temp]
                    matrix[row + 1][temp + 1] = matrix[row + 1][temp]
                col = var + 1

                try:
                    matrix[row][col + 1]

                except(IndexError):
                    row += 2
                    col = 0
                    break

        # solution if the row starts with a vertical brick
        elif matrix[row][col] == matrix[row + 1][col]:
            # solution if the row starts with a vertical brick and there are NO more vertical bricks
            if len(verticals) == 1:
                matrix[row][len(matrix[0]) - 1] = matrix[row][col]
                matrix[row + 1][len(matrix[0]) - 1] = matrix[row + 1][col]
                for i in range(col + 1, len(matrix[0]), 2):
                    matrix[row][i - 1] = matrix[row][i]
                    matrix[row + 1][i - 1] = matrix[row + 1][i]

                col = 0
                row += 2
                break
            # solution if the row starts with a vertical brick and there are more vertical bricks
            else:
                counter = 0
                keys_to_remove = []

                for check in verticals.keys():
                    counter += 1
                    keys_to_remove.append(check)
                    if counter == 2:
                        needed_var = int(verticals[check][0][1])
                        break

                matrix[row][col + 1] = matrix[row][col]
                matrix[row + 1][col] = check
                matrix[row + 1][col + 1] = check

                for i in range(col + 2, needed_var, 2):
                    matrix[row][i + 1] = matrix[row][i]
                    matrix[row + 1][i + 1] = matrix[row + 1][i]

                for x in keys_to_remove:
                    verticals.pop(x)

                col = needed_var + 1
                try:
                    matrix[row][col]

                except(IndexError):
                    col = 0
                    row += 2
                    break

horizontals.clear()
verticals.clear()

for row in range(len(matrix)):
    for col in range(len(matrix[0])):
        if col + 1 < len(matrix[0]):
            # filling the horizontals dict
            if matrix[row][col] == matrix[row][col + 1]:
                temp = {matrix[row][col]: ((row, col), (row, col + 1))}
                horizontals.update(temp)
        if row + 1 < len(matrix):
            # filling the verticals dict
            if matrix[row][col] == matrix[row + 1][col]:
                temp = {matrix[row][col]: ((row, col), (row + 1, col))}
                verticals.update(temp)


# for x in matrix:
#     for y in x:
#         print(f"{y}\t", end='')
#     print()

# Print the second layer
# first nested loop
s = [[str(e) for e in row] for row in matrix]
# get max length
lens = [max(map(len, col)) for col in zip(*s)]
# format the new layer
fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
# fill in the values
table = [fmt.format(*row) for row in s]

print('\n'.join(table))


# end-------------------
# Thank you :)


