# this is console version of the game 2048 with the same logic as in the pygame version
# controls: r - right, l - left, u - up, d - down
# to start the game, run this file
# to exit the game, press ctrl+c
# to make a move, press one of the keys above and press enter


from random import randint, choice


def generateRandom():
    global matrix, fieldSize
    i = randint(0, fieldSize - 1)
    j = randint(0, fieldSize - 1)
    while matrix[i][j] != 0:
        i = randint(0, fieldSize - 1)
        j = randint(0, fieldSize - 1)
    matrix[i][j] = choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])


def has_zero():
    global matrix
    for row in matrix:
        if 0 in row:
            return True
    return False


def has_same_neighbors():
    global matrix, fieldSize
    for i in range(fieldSize):
        for j in range(fieldSize):
            current = matrix[i][j]
            if current == 0:
                continue
            if i != fieldSize - 1:
                if matrix[i + 1][j] == current:
                    return True
            if j != fieldSize - 1:
                if matrix[i][j + 1] == current:
                    return True
    return False


def right():
    global matrix, fieldSize
    moved = False
    combined = [[False for _ in range(fieldSize)] for __ in range(fieldSize)]
    for row in matrix:
        for j in range(fieldSize - 1, -1, -1):
            if row[j] == 0:
                continue
            if j > 0 and row[j - 1] == row[j] and not combined[j][j - 1]:
                row[j - 1] *= 2
                row[j] = 0
                combined[j][j - 1] = True
                moved = True
            elif j < fieldSize - 1 and not combined[j][j + 1]:
                row[j + 1] = row[j]
                row[j] = 0
                moved = True
    if moved:
        generateRandom()


def left():
    global matrix, fieldSize
    moved = False
    combined = [[False for _ in range(fieldSize)] for __ in range(fieldSize)]
    for row in matrix:
        for j in range(1, fieldSize):
            if row[j] == 0:
                continue
            if j < fieldSize - 1 and row[j + 1] == row[j] and not combined[j][j + 1]:
                row[j + 1] *= 2
                row[j] = 0
                combined[j][j + 1] = True
                moved = True
            elif j > 0 and not combined[j][j - 1]:
                row[j - 1] = row[j]
                row[j] = 0
                moved = True
    if moved:
        generateRandom()


def up():
    global matrix, fieldSize
    moved = False
    combined = [[False for _ in range(fieldSize)] for __ in range(fieldSize)]
    for i in range(1, fieldSize):
        for j in range(fieldSize):
            if matrix[i][j] == 0:
                continue
            if i < fieldSize - 1 and matrix[i + 1][j] == matrix[i][j] and not combined[i + 1][j]:
                matrix[i + 1][j] *= 2
                matrix[i][j] = 0
                combined[i + 1][j] = True
                moved = True
            elif i > 0 and not combined[i - 1][j]:
                matrix[i - 1][j] = matrix[i][j]
                matrix[i][j] = 0
                moved = True
    if moved:
        generateRandom()


def down():
    global matrix, fieldSize
    moved = False
    combined = [[False for _ in range(fieldSize)] for __ in range(fieldSize)]
    for i in range(fieldSize - 2, -1, -1):
        for j in range(fieldSize):
            if matrix[i][j] == 0:
                continue
            if i > 0 and matrix[i - 1][j] == matrix[i][j] and not combined[i - 1][j]:
                matrix[i - 1][j] *= 2
                matrix[i][j] = 0
                combined[i - 1][j] = True
                moved = True
            elif i < fieldSize - 1 and not combined[i + 1][j]:
                matrix[i + 1][j] = matrix[i][j]
                matrix[i][j] = 0
                moved = True
    if moved:
        generateRandom()


if __name__ == '__main__':
    fieldSize = 4
    matrix = [[0 for _ in range(fieldSize)] for __ in range(fieldSize)]
    matrix[0][0] = 2
    matrix[0][1] = 2
    matrix[0][2] = 4
    matrix[0][3] = 4
    generateRandom()
    generateRandom()
    while has_zero() or has_same_neighbors():
        for x in matrix:
            print(x)
        print()
        act = input()
        if act:
            if act == 'r':
                right()
            elif act == 'l':
                left()
            elif act == 'u':
                up()
            elif act == 'd':
                down()
            else:
                continue