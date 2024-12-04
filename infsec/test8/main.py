def table_decryption(string, width, height):
    table = [[''] * width for _ in range(height)]
    line = []
    i = j = f = 0
    end = len(string) % width

    for k in range(len(string)):
        table[i][j] = string[k]
        i += 1
        if i == height:
            i = 0
            j += 1
        if j == end and f == 0:
            height -= 1
            f = 1

    height += 1
    for i in range(height):
        for j in range(width):
            if table[i][j]:
                line.append(table[i][j])

    return ''.join(line)


def table_encryption(string, width, height):
    table = [[''] * width for _ in range(height)]
    line = []
    i = j = 0
    k = 0

    while k < len(string):
        table[i][j] = string[k]
        k += 1
        j += 1
        if j == width:
            j = 0
            i += 1

    for i in range(width):
        for j in range(height):
            if table[j][i]:
                line.append(table[j][i])

    return ''.join(line)
