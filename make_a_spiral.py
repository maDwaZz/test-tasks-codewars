# Make a spiral
# https://www.codewars.com/kata/534e01fbbb17187c7e0000c6/train/python

def spiralize(size):
    spiral = [[0 for _ in range(size)] for _ in range(size)]

    spiral[0][0] = 1
    x, y = 0, 0
    length = size - 1
    indent = 0

    while indent <= size // 2:
        while x < length - indent:
            x += 1
            spiral[y][x] = 1
        while y < length - indent:
            y += 1
            spiral[y][x] = 1
        while x > indent:
            x -= 1
            spiral[y][x] = 1
        indent += 2
        while y > indent:
            y -= 1
            spiral[y][x] = 1

    if spiral[y][x + 1] + spiral[y + 1][x] + spiral[y][x - 1] + spiral[y - 1][x] == 2:
        spiral[y][x] = 0  # убираем лишний заворот спирали для случаев, когда size является четным числом

    return spiral
