# Таблица замен для шифрования
CIPHER_TABLE = {
    "А": [123, 231, 321, 213],
    "Б": [456, 564],
    "В": [789, 897, 987],
    "Г": [234, 342],
    "Д": [876, 768],
    "Е": [345, 453, 543, 435],
    "Ё": [567, 675, 765],
    "Ж": [976, 769],
    "З": [134, 341],
    "И": [965, 659, 569],
    "Й": [145, 451],
    "К": [954, 549, 459],
    "Л": [156, 561, 651],
    "М": [943, 439, 349],
    "Н": [167, 671, 761, 617],
    "О": [932, 329, 239, 392, 923, 293],
    "П": [178, 781, 871],
    "Р": [912, 129, 219],
    "С": [189, 891, 981, 819],
    "Т": [975, 759, 579, 795],
    "У": [135, 351],
    "Ф": [964],
    "Х": [146, 461],
    "Ц": [953],
    "Ч": [157, 571],
    "Ш": [942, 429],
    "Щ": [168, 681],
    "Ъ": [931],
    "Ы": [179],
    "Ь": [952],
    "Э": [158, 581],
    "Ю": [941, 419],
    "Я": [169, 691, 961],
    "_": [930, 309, 39, 390, 903, 93],
}

# Индексы для отслеживания текущего положения в списке кодов для каждого символа
current_indices = {char: 0 for char in CIPHER_TABLE}

# Переворот таблицы для дешифровки
REVERSE_TABLE = {}
for char, codes in CIPHER_TABLE.items():
    for code in codes:
        REVERSE_TABLE[f"{code:03}"] = char


def encrypt_message(message):
    encrypted_message = []
    for char in message:
        if char in CIPHER_TABLE:
            # Получаем текущий индекс для символа
            current_index = current_indices[char]
            # Получаем код из таблицы по текущему индексу
            code = CIPHER_TABLE[char][current_index]
            # Добавляем код в результат
            encrypted_message.append(f"{code:03}")
            # Обновляем индекс для символа (циклический переход)
            current_indices[char] = (current_index + 1) % len(
                CIPHER_TABLE[char]
            )
        else:
            raise ValueError(f"Символ '{char}' отсутствует в таблице замен.")
    return "".join(encrypted_message)


def decrypt_message(encrypted):
    decrypted_message = []
    if len(encrypted) % 3 != 0:
        raise ValueError("Неверный формат зашифрованного сообщения.")

    for i in range(0, len(encrypted), 3):
        code = encrypted[i : i + 3]
        if code in REVERSE_TABLE:
            decrypted_message.append(REVERSE_TABLE[code])
        else:
            raise ValueError(f"Код '{code}' отсутствует в таблице замен.")

    return "".join(decrypted_message)


def main():
    print("Выберите действие:")
    print("1. Зашифровать сообщение")
    print("2. Расшифровать сообщение")
    choice = input("Ваш выбор (1/2): ").strip()

    if choice == "1":
        message = input("Введите сообщение для шифрования: ").upper()
        try:
            encrypted = encrypt_message(message)
            print(f"Зашифрованное сообщение: {encrypted}")
        except ValueError as e:
            print(e)
    elif choice == "2":
        encrypted = input("Введите зашифрованное сообщение: ").strip()
        try:
            decrypted = decrypt_message(encrypted)
            print(f"Расшифрованное сообщение: {decrypted}")
        except ValueError as e:
            print(e)
    else:
        print("Неверный выбор.")


if __name__ == "__main__":
    main()
