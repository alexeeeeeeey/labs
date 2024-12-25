def matrix_sum(str_length: int) -> list[int]:
    """Создаёт матрицу контрольной суммы для заданной длины строки"""
    matrix = []

    bit_position = 1
    while bit_position <= str_length:
        row = [0] * str_length

        for i in range(bit_position - 1, str_length, 2 * bit_position):
            row[i : i + bit_position] = [1] * min(bit_position, str_length - i)

        matrix.append(row)
        bit_position *= 2

    return matrix


def gen_control_vector(seq_with_more_bits: list, matrix: list[list[int]]):

    contorl_vector = []

    for i in matrix:
        xored_vector = []
        for (i, j) in zip(i, seq_with_more_bits):
            xored_vector.append(i * j)
        contorl_vector.append(sum(xored_vector) % 2)
    
    return contorl_vector


def insert_control_vector(contol_vector: list, seq: list) -> list:
    new_seq = []
    j = 0
    k = 0
    seq_copy = seq.copy()
    total_bits = len(seq) + len(contol_vector)
    for i in range(total_bits):
        if i + 1 == 2**j:
            new_seq.append(contol_vector[k])
            k += 1
            j += 1
        else:
            new_seq.append(seq_copy.pop(0))

    return new_seq


def gen_code(seq: list, matrix: list[list[int]]) -> list[int]:
    """Генерирует код с контрольными битами"""
    r = len(matrix[0])
    cb = r - len(seq)

    seq_with_zero_sums = insert_control_vector([0] * cb, seq)

    control_vector = gen_control_vector(seq_with_zero_sums, matrix)
    print("Контрольный вектор: ", control_vector)

    encoded = insert_control_vector(control_vector, seq)

    return encoded


def check_code(seq: list, matrix: list[list[int]]) -> int:
    """Функция проверки на наличие ошибок"""


    control_vector = gen_control_vector(seq, matrix)

    error_pos = int("".join(map(str, control_vector[::-1])), 2)

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

        if optype in [GEN_CODE, CHECK_CODE]:
            m = len(seq)  # Количество информационных битов
            r = 0  # Число проверочных битов

            while 2**r < m + r + 1:
                r += 1

            matrix = matrix_sum(m + r)

        # генерация нового кода.
        if optype == GEN_CODE:
            print("==== MATRIX ====")
            for line in matrix:
                print(line)
            print("== END MATRIX ==")

            code = gen_code(seq, matrix)

            print(
                f"Сгенерированный код:\n"
                f"{''.join(map(str, code))}"
            )

        # проверка существующего кода.
        elif optype == CHECK_CODE:
            error_pose = check_code(seq, matrix)

            if error_pose == 0:
                print("Ошибок не найдено.")
            else:
                print(" " * (12 + error_pose) + "^")
                print(f"Ошибка в позиции {error_pose} ")


if __name__ == "__main__":
    main()
