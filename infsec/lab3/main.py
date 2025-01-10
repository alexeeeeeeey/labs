import time
import math
import matplotlib.pyplot as plt

N = 24


class LinearCongruentialGenerator:
    def __init__(self, n):
        self.m = 2**n
        self.gen_params()
        self.last = self.c0

    def next(self, last_num=None, save_last: bool=False):
        if save_last:
            last_num = self.last

        num = (self.a * last_num + self.b) % self.m

        if save_last:
            self.last = num

        return num

    def gen_params(self):
        "Генерация параметров a, b, c0"
        t = int(time.time_ns() // 1e3 % 1e9)

        self.a = ((((t << t % 3) * 5 + 2) & ~3) | 1) % self.m

        b = ((t << t % 4) * 7 + 5 | 1) % self.m
        while math.gcd(b, self.m) != 1:
            b = (b * 7 + 3) % self.m
        self.b = b

        self.c0 = ~(t ^ self.a ^ self.b) % self.m
        self.last = self.c0

    def get_params(self):
        return (self.a, self.b, self.c0)


def check_uniformity(
    generator: LinearCongruentialGenerator, length, filename, m=2**24
):
    "построение гистограммы и проверка равномерности"
    counts = [0] * 100
    step = m // 100

    with open(filename, "w") as f:
        num = generator.c0
        for _ in range(length):
            num = generator.next(num)
            f.write(f"{num}\n")
            counts[num // step % 100] += 1

    print(f"Последовательность сохранена в {filename}")

    frequencies = [count / length for count in counts]

    print(f"Средняя частота: {sum(frequencies) / 100:.4f}")
    print(f"Минимальная частота: {min(frequencies):.4f}")
    print(f"Максимальная частота: {max(frequencies):.4f}")

    plt.bar(range(100), frequencies, color="blue", width=1.0)
    plt.title("Гистограмма распределения частот")
    plt.xlabel("Интервалы")
    plt.ylabel("Частота")
    plt.show()


def main():
    print("Генерация параметров ГПСЧ...")
    generator = LinearCongruentialGenerator(N)
    a, b, c0 = generator.get_params()
    print(f"Параметры: a={a}, b={b}, c0={c0}")

    while True:
        print("\nВыберите действие:")
        print("1. Сгенерировать и вывести следующее число")
        print("2. Сгенерировать последовательность и записать в файл")
        print("3. Сгенерировать новые параметры")

        choice = input("Ваш выбор: ").strip()
        if choice == "1":
            print(f"Сгенерированное число: {generator.next(save_last=True)}")
        elif choice == "2":
            length = int(input("Введите длину последовательности: "))
            filename = input("Введите имя файла для сохранения: ")

            check_uniformity(generator, length, filename)
        elif choice == "3":
            generator.gen_params()
            a, b, c0 = generator.get_params()
            print(f"Новые параметры: a={a}, b={b}, c0={c0}")
        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
