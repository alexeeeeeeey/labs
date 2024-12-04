def atbash_cipher(word, alphabet):
    """
    Функция для шифрования и расшифровки методом Атбаш.
    Заменяет буквы слова на "зеркальные" по алфавиту.
    """
    # Создаем словарь соответствий для алфавита
    atbash_mapping = {alphabet[i]: alphabet[-(i + 1)] for i in range(len(alphabet))}
    # Зашифровываем или расшифровываем слово
    transformed_word = ''.join(atbash_mapping[char] for char in word)
    return transformed_word

def main():
    # Исходный алфавит
    alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

    print("Выберите действие:")
    print("1. Зашифровать слово методом Атбаш")
    print("2. Расшифровать слово методом Атбаш")
    choice = input("Введите номер действия (1 или 2): ")

    if choice not in {"1", "2"}:
        print("Ошибка: неверный выбор действия!")
        return

    # Ввод слова
    word = input("Введите слово: ").upper()

    # Проверяем, что все символы есть в алфавите
    # if any(char not in alphabet for char in word):
    #     print("Ошибка: слово содержит символы, отсутствующие в алфавите!")
    #     return

    if choice == "1":
        # Шифрование
        result = atbash_cipher(word, alphabet)
        print(f"Зашифрованное слово: {result}")
    elif choice == "2":
        # Расшифровка (та же функция, так как метод Атбаш симметричен)
        result = atbash_cipher(word, alphabet)
        print(f"Расшифрованное слово: {result}")

if __name__ == "__main__":
    main()
