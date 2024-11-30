class MultiplyError(Exception):
    pass


def matrix_sum(str_length: int) -> list[int]:
    """Создаёт матрицу контрольной суммы для заданной длины строки"""
    matrix = []

    bit_position = 1
    while bit_position <= str_length:
        # Изначально строка заполняется нулями
        row = [0] * str_length

        # Проставляем 1 в позиции, где бит участвует
        for i in range(bit_position - 1, str_length, 2 * bit_position):
            row[i : i + bit_position] = [1] * min(bit_position, str_length - i)

        matrix.append(row)
        bit_position *= 2

    return matrix


def gen_code(seq: list) -> list[int]:
    """Генерирует код с контрольными битами"""
    m = len(seq)  # Количество информационных битов
    r = 0  # Число проверочных битов

    while 2**r < m + r + 1:
        r += 1

    total_bits = m + r
    encoded = [None] * total_bits

    # Заполняем проверочные биты значениями None
    for i in range(total_bits):
        if (i + 1) & i == 0:  # Позиции 1, 2, 4, 8...
            encoded[i] = 0
        else:
            encoded[i] = seq.pop(0)

    # Рассчитываем проверочные биты
    for i in range(r):
        parity_index = 2**i - 1
        parity = 0
        for j in range(parity_index, total_bits, 2 ** (i + 1)):
            parity ^= sum(encoded[j : j + 2**i])
        encoded[parity_index] = parity % 2

    return encoded


def check_code(seq: list):
    """функция проверки на наличие ошибок"""
    n = len(seq)
    r = 0

    while 2**r < n:
        r += 1

    error_pos = 0
    for i in range(r):
        parity_index = 2**i - 1
        parity = 0
        for j in range(parity_index, n, 2 ** (i + 1)):
            parity ^= sum(seq[j : j + 2**i])
        if parity % 2 != 0:
            error_pos += 2**i

    return error_pos


def main():
    # константы режимов
    GEN_CODE = 1
    CHECK_CODE = 2

    while True:
        # ввод действия.
        while True:
            optype = input(
                "Выберите действие:\n"
                f"{GEN_CODE} - сгенерировать последовательность\n"
                f"{CHECK_CODE} - проверить последовательность\n"
            )
            if optype in (str(GEN_CODE), str(CHECK_CODE)):
                optype = int(optype)
                break
            else:
                print("Неправильный ввод, попробуйте ещё")

        # ввод кода
        while True:
            rawseq = input("Введите код: ")
            try:
                seq = [int(i) for i in rawseq]
            except ValueError:
                print("Неправильный ввод, попробуйте ещё")
                continue

            if set(seq) != {1, 0}:
                print("В коде присутствуют символы помимо 0 и 1.")
                continue
            break

        # генерация нового кода.
        if optype == GEN_CODE:

            matrix = matrix_sum(len(seq))

            print("==== MATRIX ====")
            for line in matrix:
                print(line)
            print("== END MATRIX ==")

            code = gen_code(seq)

            print(
                f"Сгенерированный код имеет длину {len(code)}:\n"
                f"{''.join(map(str, code))}"
            )

        # проверка существующего кода.
        elif optype == CHECK_CODE:
            try:
                error_pose = check_code(seq)

                if error_pose == 0:
                    print("Ошибок не найдено.")
                else:
                    print(" " * (12 + error_pose) + "^")
                    print(f"Ошибка в позиции {error_pose} ")
            except MultiplyError:
                print("В коде больше 2 ошибок")


if __name__ == "__main__":
    main()
