alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ_.,"


def build_matrix(keyword):
    to_insert = keyword + alphabet
    was = set()
    matrix = []
    for i in range(6):
        cur_row = []
        for j in range(6):
            while to_insert[0] in was:
                to_insert = to_insert[1:]
            cur_row.append(to_insert[0])
            was.add(to_insert[0])
            to_insert = to_insert[1:]
        matrix.append(cur_row)

    # print("Matrix:")
    # for row in matrix:
    #     print(row)
    return matrix


def find_position(matrix, char):
    for row_idx, row in enumerate(matrix):
        if char in row:
            return row_idx, row.index(char)
    return None


def prepare_message(message):
    prepared = []
    i = 0
    while i < len(message):
        prepared.append(message[i])
        if i + 1 < len(message) and message[i] == message[i + 1]:
            prepared.append("Ъ")
        i += 1
    if len(prepared) % 2 != 0:
        prepared.append("Ъ")
    return prepared


def playfair(message, key, mode="encode"):
    """
    Шифрует или расшифровывает сообщение с использованием Playfair шифра.
    mode="encode" - шифровка
    mode="decode" - расшифровка
    """
    matrix = build_matrix(key)
    if mode == "encode":
        message_pairs = prepare_message(message)
    elif mode == "decode":
        message_pairs = list(message)
    else:
        raise ValueError("Режим должен быть 'encode' или 'decode'")

    # print("Message pairs:", message_pairs)
    processed_message = []
    shift = 1 if mode == "encode" else -1

    for i in range(0, len(message_pairs), 2):
        char1, char2 = message_pairs[i], message_pairs[i + 1]
        row1, col1 = find_position(matrix, char1)
        row2, col2 = find_position(matrix, char2)

        if row1 == row2:  # Одинаковая строка
            processed_message.append(matrix[row1][(col1 + shift) % 6])
            processed_message.append(matrix[row2][(col2 + shift) % 6])
        elif col1 == col2:  # Одинаковый столбец
            processed_message.append(matrix[(row1 + shift) % 6][col1])
            processed_message.append(matrix[(row2 + shift) % 6][col2])
        else:  # Прямоугольник
            if mode == "encode":
                if (row2 - row1) * (col2 - col1) < 0:
                    processed_message.append(matrix[row2][col1])

                    processed_message.append(matrix[row1][col2])
                else:
                    processed_message.append(matrix[row1][col2])
                    processed_message.append(matrix[row2][col1])

            else:
                if (row2 - row1) * (col2 - col1) > 0:
                    processed_message.append(matrix[row2][col1])

                    processed_message.append(matrix[row1][col2])
                else:
                    processed_message.append(matrix[row1][col2])
                    processed_message.append(matrix[row2][col1])

    return "".join(processed_message)


# # Пример использования
# key = "МОРКОВЬ"
# # ЗАКОНОДАТЕЛЬНЫЙ_УРОВЕНЬ_ЗАЩИТЫ_ИНФОРМАЦИИ
# # Шифровка
# message_to_encrypt = "РКДБЖЙЖБЖШЬЗЖЁ_.ЖБШЙПГЯЙХЛРКАЖЖШЛШ"
# message_to_encrypt += "Ъ" * (len(message_to_encrypt) % 2)
# encrypted_message = playfair(message_to_encrypt, key, mode="encode")
# print(f"Зашифрованное сообщение: {encrypted_message}")

# # Расшифровка
# message_to_decrypt = encrypted_message
# decrypted_message = playfair(message_to_encrypt, key, mode="decode")
# print(f"Расшифрованное сообщение: {decrypted_message.replace("Ъ", "")}")


def main():
    print("Выберите действие:")
    print("1 - Зашифровать сообщение")
    print("2 - Расшифровать сообщение")
    choice = input("Введите номер действия: ")

    if choice not in ["1", "2"]:
        print("Некорректный выбор. Попробуйте снова.")
        return

    message = input("Введите сообщение (только символы из алфавита): ").upper()
    key = input("Введите ключ (только символы из алфавита): ").upper()

    if choice == "1":
        result = playfair(message, key, mode="encode")
        print(f"Зашифрованное сообщение: {result}")
    elif choice == "2":
        result = playfair(message, key, mode="decode")
        print(f"Расшифрованное сообщение: {result.replace('Ъ', '')}")


if __name__ == "__main__":
    main()
