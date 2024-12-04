def decrypt(message, rows, cols):
    """
    Расшифровывает сообщение по заданным количеству строк и столбцов.

    :param message: Зашифрованное сообщение.
    :param rows: Количество строк.
    :param cols: Количество столбцов.
    :return: Расшифрованное сообщение.
    """
    # Создаём таблицу для расшифровки
    table = [['' for _ in range(cols)] for _ in range(rows)]
    debt = rows * cols - len(message)

    # Заполняем таблицу пустыми ячейками ("Z"), если сообщение короче
    for col in range(cols - 1, -1, -1):
        for row in range(rows - 1, -1, -1):
            if debt > 0:
                table[row][col] = "Z"
                debt -= 1
            else:
                break
        if debt <= 0:
            break

    # Заполняем таблицу символами из сообщения
    indx = 0
    for row in range(rows):
        for col in range(cols):
            if indx < len(message) and table[row][col] != "Z":
                table[row][col] = message[indx]
                indx += 1

    # Читаем сообщение из таблицы
    res = ""
    for col in range(cols):
        for row in range(rows):
            res += table[row][col]
    
    return res.replace("Z", '')

def encrypt(message, rows, cols):
    """
    Шифрует сообщение по заданным количеству строк и столбцов.

    :param message: Исходное сообщение.
    :param rows: Количество строк.
    :param cols: Количество столбцов.
    :return: Зашифрованное сообщение.
    """
    # Создаём таблицу для шифрования
    table = [['' for _ in range(cols)] for _ in range(rows)]
    idx = 0

    # Заполняем таблицу по столбцам
    for col in range(cols):
        for row in range(rows):
            if len(message) > idx:
                table[row][col] = message[idx]
                idx += 1

    # Читаем таблицу по строкам
    encrypted_message = ""
    for row in range(rows):
        encrypted_message += ''.join(table[row])
    
    return encrypted_message

# Основной сценарий работы
if __name__ == "__main__":
    print("Выберите действие: 1 - Зашифровать, 2 - Расшифровать")
    choice = input("Введите номер действия: ")

    if choice == "1":
        message = input("Введите сообщение для шифровки: ")
        rows = int(input("Введите количество строк: "))
        cols = int(input("Введите количество столбцов: "))
        encrypted_message = encrypt(message, rows, cols)
        print(f"Зашифрованное сообщение: {encrypted_message}")

    elif choice == "2":
        message = input("Введите зашифрованное сообщение: ")
        rows = int(input("Введите количество строк: "))
        cols = int(input("Введите количество столбцов: "))
        decrypted_message = decrypt(message, rows, cols)
        print(f"Расшифрованное сообщение: {decrypted_message}")

    else:
        print("Некорректный выбор действия. Перезапустите программу.")
