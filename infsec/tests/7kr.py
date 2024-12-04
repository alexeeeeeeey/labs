from itertools import permutations

def assemble(block, key):
    """
    Собирает блок сообщения на основе ключа.
    
    :param block: Блок для сборки.
    :param key: Ключ, определяющий порядок символов в блоке.
    :return: Собранный блок.
    """
    key = filter(lambda x: x < len(block), key)
    res = ""
    for k in key:
        res += block[k]
    return res

def disassemble(block, key):
    """
    Разбирает блок сообщения на основе ключа.
    
    :param block: Блок для разборки.
    :param key: Ключ, определяющий порядок символов для разборки.
    :return: Разобранный блок.
    """
    key = filter(lambda x: x < len(block), key)
    res = ["" for _ in range(len(block))]
    for i, k in enumerate(key):
        res[k] = block[i]
    return "".join(res)

def encrypt_message():
    """
    Шифрует сообщение, используя введённый ключ.
    """
    message_to_encrypt = input("Введите сообщение для шифровки: ")
    key_encrypt = input("Введите ключ для шифровки (например, '543162'): ")
    key_encrypt = list(int(i) - 1 for i in key_encrypt)
    d = int(input("Введите длину блока: "))
    blocks_encrypt = [message_to_encrypt[i: min(i + d, len(message_to_encrypt))] for i in range(0, len(message_to_encrypt), d)]
    
    encrypted_message = ""
    for block in blocks_encrypt:
        encrypted_message += assemble(block, key_encrypt)
    
    print(f"Зашифрованное сообщение: {encrypted_message}")

def decrypt_message():
    """
    Расшифровывает сообщение, используя введённый ключ.
    """
    encrypted_message_to_decrypt = input("Введите зашифрованное сообщение: ")
    key_decrypt = input("Введите ключ для расшифровки (например, '534126'): ")
    key_decrypt = list(int(i) - 1 for i in key_decrypt)
    d = int(input("Введите длину блока: "))
    blocks_decrypt = [encrypted_message_to_decrypt[i: min(i + d, len(encrypted_message_to_decrypt))] for i in range(0, len(encrypted_message_to_decrypt), d)]
    
    decrypted_message = ""
    for block in blocks_decrypt:
        decrypted_message += disassemble(block, key_decrypt)
    
    print(f"Расшифрованное сообщение: {decrypted_message}")

def find_key():
    """
    Ищет ключ шифрования по открытому сообщению и зашифрованному.
    """
    open_message = input("Введите открытое сообщение: ")
    encrypted_message_with_key = input("Введите зашифрованное сообщение с ключом: ")
    d = int(input("Введите длину блока: "))
    
    blocks_open = [open_message[i: min(i + d, len(open_message))] for i in range(0, len(open_message), d)]
    blocks_encrypted = [encrypted_message_with_key[i: min(i + d, len(encrypted_message_with_key))] for i in range(0, len(encrypted_message_with_key), d)]

    key_found = None
    for perm in permutations(range(d)):
        is_key = True
        for block_open, block_encrypted in zip(blocks_open, blocks_encrypted):
            if assemble(block_open, perm) != block_encrypted:
                is_key = False
                break
        if is_key:
            key_found = perm
            break

    if key_found:
        key_found = [k + 1 for k in key_found]
        print("Найденный ключ:", "".join(map(str, key_found)))
    else:
        print("Ключ не найден.")

# Основной сценарий работы
if __name__ == "__main__":
    print("Выберите действие: 1 - Зашифровать, 2 - Расшифровать, 3 - Найти ключ")
    choice = input("Введите номер действия: ")

    if choice == "1":
        encrypt_message()
    elif choice == "2":
        decrypt_message()
    elif choice == "3":
        find_key()
    else:
        print("Некорректный выбор действия. Перезапустите программу.")
