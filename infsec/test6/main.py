arr = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ_'


def pos(char):
    print(char, arr.find(char) + 1)
    return arr.find(char) + 1


plaintext = input("Введите текст").upper()
key = input("Введите ключ").upper()

key = (key * (len(plaintext) // len(key) + 1))[:len(plaintext)]

if input("1 - расшифровать\n2 - зашифровать") == "2":
    ciphertext = ''
    for i in range(len(plaintext)):
        new_index = (pos(plaintext[i]) + pos(key[i]) - 1) % len(arr)
        ciphertext += arr[new_index]

    print(f'Зашифрованное сообщение: {ciphertext}')
else:
    decoded_text = ''
    for i in range(len(plaintext)):
        new_index = (pos(plaintext[i]) - pos(key[i]) - 1 + len(arr)) % len(arr)
        decoded_text += arr[new_index]

    print(f'Расшифрованное сообщение: {decoded_text}')
