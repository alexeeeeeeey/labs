alp = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ_'

def vigenere_encrypt(text, key, alphabet=alp):
    """Зашифровывает сообщение с использованием шифра Виженера."""
    encrypted_text = []
    key_length = len(key)
    key_index = 0

    for char in text:
        if char in alphabet:
            shift = alphabet.index(key[key_index])
            encrypted_char = alphabet[(alphabet.index(char) + shift) % len(alphabet)]
            encrypted_text.append(encrypted_char)
            key_index = (key_index + 1) % key_length
        else:
            raise ValueError(f"Символ '{char}' не найден в алфавите.")

    return ''.join(encrypted_text)


def vigenere_decrypt(text, key, alphabet=alp):
    """Расшифровывает сообщение с использованием шифра Виженера."""
    decrypted_text = []
    key_length = len(key)
    key_index = 0

    for char in text:
        if char in alphabet:
            shift = alphabet.index(key[key_index])
            decrypted_char = alphabet[(alphabet.index(char) - shift) % len(alphabet)]
            decrypted_text.append(decrypted_char)
            key_index = (key_index + 1) % key_length
        else:
            raise ValueError(f"Символ '{char}' не найден в алфавите.")

    return ''.join(decrypted_text)


# Алфавит и сопоставление символов с числами
alphabet = "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ_"
char_to_num = {char: idx for idx, char in enumerate(alphabet)}
num_to_char = {idx: char for idx, char in enumerate(alphabet)}

def vernam_encrypt_decrypt(text, key):
    # Приведение ключа к длине текста
    key = (key * (len(text) // len(key) + 1))[:len(text)]
    
    result = []
    for t_char, k_char in zip(text, key):
        t_num = char_to_num[t_char]
        k_num = char_to_num[k_char]
        
        # Операция XOR
        result_num = (t_num ^ k_num)  # добавлено взятие по модулю
        result.append(num_to_char[result_num])
    return "".join(result)


# Функция для выбора сценария
def choose_scenario():
    print("Выберите сценарий:")
    print("1. Зашифровка с использованием шифра Виженера")
    print("2. Расшифровка с использованием шифра Виженера")
    print("3. Зашифровка с использованием шифра Вернама")
    print("4. Расшифровка с использованием шифра Вернама")

    choice = int(input("Введите номер сценария (1-4): "))
    
    # Ввод текста и ключа
    # text = input("Введите текст: ").upper()
    key = input("Введите ключ шифрования: ").upper()

    if choice == 1:
        text = input("Введите текст: ").upper()
        encrypted_message = vigenere_encrypt(text, key)
        print(f"Зашифрованное сообщение (Шифр Виженера): {encrypted_message}")
    
    elif choice == 2:
        encrypted_message = input("Введите зашифрованное сообщение: ").upper()
        decrypted_message = vigenere_decrypt(encrypted_message, key)
        print(f"Расшифрованное сообщение (Шифр Виженера): {decrypted_message}")
    
    elif choice == 3:
        text = input("Введите текст: ").upper()
        encrypted_message1 = vernam_encrypt_decrypt(text, key)
        print(f"Зашифрованное сообщение (Шифр Вернама): {encrypted_message1}")
    
    elif choice == 4:
        encrypted_message1 = input("Введите зашифрованное сообщение: ").upper()
        decrypted_message1 = vernam_encrypt_decrypt(encrypted_message1, key)
        print(f"Расшифрованное сообщение (Шифр Вернама): {decrypted_message1}")
    
    else:
        print("Неверный выбор!")

# Главная функция
if __name__ == "__main__":
    choose_scenario()
