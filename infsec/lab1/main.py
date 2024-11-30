import math
import os
import json

ENCRYPT = 1
DECRYPT = 2


def encrypt(text: str, column_key: list, row_key: list):
    columns = len(column_key)
    rows = len(row_key)
    encrypted_text = [[] for i in range(columns * rows)]
    for i in range(len(text)):
        ri = (i // columns) % rows
        sj = i % columns
        k = columns * (row_key[ri] - 1) + column_key[sj] - 1
        encrypted_text[k].append(text[i])
    return encrypted_text


def decrypt(encrypted_text: list[list],
            column_key: list,
            row_key: list):
    text = ""
    symbol_count = sum([len(i) for i in encrypted_text])
    columns = len(column_key)
    rows = len(row_key)
    try:
        for i in range(symbol_count):
            ri = (i // columns) % rows
            sj = i % columns
            k = columns * (int(row_key[ri]) - 1) + int(column_key[sj]) - 1
            text += encrypted_text[k][0]
            encrypted_text[k].pop(0)
        return text
    except IndexError:
        return "Ошибка расшифровки. Ключ подобран неверно."


def input_operation():
    operation = input(
        f"{ENCRYPT} - зашифровать\n"
        f"{DECRYPT} - расшифровать\n"
        "Выберите операцию: "
    )
    if not operation.isdigit():
        return None
    if int(operation) not in (ENCRYPT, DECRYPT):
        return None
    return int(operation)


def key_formatter(key_str: str):
    return list(map(int, key_str.split()))


def main():
    while True:
        op = input_operation()
        if op is None:
            print("Что-то пошло не так, попробуйте ещё раз")
            continue

        if op == ENCRYPT:
            text = input("Введите текст для шифрования или путь к файлу:\n")
            if os.path.isfile(text):
                with open(text, "r", encoding="UTF-8") as f:
                    text = f.read()
                    print("Файл прочитан")

            blocks = int(input("Введите количество блоков: "))

            columns = int(input("Введите количество столбцов: "))
            rows = math.ceil(blocks / columns)

            while True:
                column_key = key_formatter(
                    input(f"Введите ключ столбцов длинной {columns}\n"
                          "(Например для длины 4 - 4 1 3 2): ")
                )
                if set(column_key) == set([i + 1 for i in range(columns)]):
                    break
                print("Неверный ключ! Попробуйте ещё раз: ")

            while True:
                row_key = key_formatter(
                    input(f"Введите ключ строк длинной {rows}\n"
                          "(Например для длины 2 - 2 1): ")
                )
                if set(column_key) == set([i + 1 for i in range(columns)]):
                    break
                print("Неверный ключ! Попробуйте ещё раз: ")

            encrypted_text = encrypt(
                text,
                column_key,
                row_key,
            )

            print(json.dumps(encrypted_text, ensure_ascii=False))
        if op == DECRYPT:
            text = json.loads(
                input("Введите текст для расшифровки в формате json:")
            )
            column_key = key_formatter(input("Введите ключ столбцов: "))
            row_key = key_formatter(input("Введите ключ строк: "))

            decrypted_text = decrypt(
                text,
                column_key,
                row_key,
            )
            print(decrypted_text)


if __name__ == "__main__":
    main()
