def generate_key_sequence(message, key, alphabet):
    """
    Создаёт повторяющуюся последовательность ключа для сообщения.

    :param message: Исходное сообщение.
    :param key: Ключ для шифрования/дешифрования.
    :param alphabet: Алфавит.
    :return: Последовательность чисел для ключа.
    """
    key_numbers = [alphabet.index(char) for char in key]
    return (key_numbers * (len(message) // len(key_numbers) + 1))[:len(message)]


def gamma_cipher(message, key, alphabet, decrypt=False):
    """
    Шифрует или расшифровывает сообщение методом гаммирования.

    :param message: Исходное сообщение.
    :param key: Ключ.
    :param alphabet: Исходный алфавит.
    :param decrypt: Флаг для расшифровки (по умолчанию False).
    :return: Зашифрованное или расшифрованное сообщение.
    """
    alphabet_dict = {char: i for i, char in enumerate(alphabet)}
    reverse_dict = {i: char for char, i in alphabet_dict.items()}
    alphabet_length = len(alphabet)

    key_sequence = generate_key_sequence(message, key, alphabet)
    result = []

    for i, char in enumerate(message):
        if char not in alphabet_dict:
            raise ValueError(f"Символ '{char}' не найден в алфавите!")

        message_index = alphabet_dict[char]
        key_index = key_sequence[i]

        if decrypt:
            new_index = (message_index - key_index) % alphabet_length
        else:
            new_index = (message_index + key_index) % alphabet_length

        result.append(reverse_dict[new_index])

    return ''.join(result)


def main():
    # Исходный алфавит
    alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ_"[::-1]

    print("Выберите действие:")
    print("1 - Зашифровать сообщение")
    print("2 - Расшифровать сообщение")
    choice = input("Введите номер действия: ")

    if choice == "1":
        message = input("Введите сообщение для зашифровки (только символы из алфавита): ").upper()
        key = input("Введите ключ для зашифровки (только символы из алфавита): ").upper()
        try:
            encrypted_message = gamma_cipher(message, key, alphabet)
            print(f"Зашифрованное сообщение: {encrypted_message}")
        except ValueError as e:
            print(f"Ошибка: {e}")
    elif choice == "2":
        message = input("Введите сообщение для расшифровки (только символы из алфавита): ").upper()
        key = input("Введите ключ для расшифровки (только символы из алфавита): ").upper()
        try:
            decrypted_message = gamma_cipher(message, key, alphabet, decrypt=True)
            print(f"Расшифрованное сообщение: {decrypted_message}")
        except ValueError as e:
            print(f"Ошибка: {e}")
    else:
        print("Некорректный выбор. Перезапустите программу и попробуйте снова.")


if __name__ == "__main__":
    main()
