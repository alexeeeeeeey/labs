def find_caesar_key(plaintext, ciphertext, alphabet):
    # Найти разницу между индексами первой пары символов
    p_index = alphabet.index(plaintext[0])
    c_index = alphabet.index(ciphertext[0])
    # Рассчитать ключ, учитывая циклический сдвиг
    key = (c_index - p_index) % len(alphabet)
    return key


def decrypt_caesar(ciphertext, key, alphabet):
    decrypted_message = ""
    for char in ciphertext:
        if char in alphabet:
            # Найти индекс символа в алфавите
            index = alphabet.index(char)
            # Сдвиг влево на ключ
            new_index = (index - key) % len(alphabet)
            decrypted_message += alphabet[new_index]
        else:
            # Если символа нет в алфавите, оставить как есть
            decrypted_message += char
    return decrypted_message


def main():
    # Алфавит
    alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

    print("Выберите действие:")
    print("1. Определить ключ шифра Цезаря по паре текст-шифротекст")
    print("2. Расшифровать сообщение")
    choice = input("Ваш выбор (1/2): ").strip()

    if choice == "1":
        # Определение ключа
        plaintext = input("Введите открытый текст: ").upper()
        ciphertext = input("Введите шифротекст: ").upper()

        if len(plaintext) != len(ciphertext):
            print("Ошибка: длины открытого текста и шифротекста не совпадают!")
            return

        key = find_caesar_key(plaintext, ciphertext, alphabet)
        print(f"Ключ шифра Цезаря: {key}")

    elif choice == "2":
        # Расшифровка сообщения
        ciphertext = input("Введите зашифрованное сообщение: ").upper()

        print("Перебираем все возможные ключи...")
        for key in range(1, len(alphabet)):  # 0 < n < 33
            decrypted_message = decrypt_caesar(ciphertext, key, alphabet)
            print(f"{decrypted_message}: Ключ {key}")
        print("Ответ на задание - ключ исходного слова")
    else:
        print("Неверный выбор.")


if __name__ == "__main__":
    main()
