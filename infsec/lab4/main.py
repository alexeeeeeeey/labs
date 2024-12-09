import time
import os
import math
import json


class LinearCongruentialGenerator:
    def __init__(self, n=24):
        self.m = 2**n

    def next(self):
        self.last = (self.a * self.last + self.b) % self.m

        return self.last

    def set_params(self, a, b, c0):
        self.a = a
        self.b = b
        self.c0 = c0
        self.last = self.c0

    def gen_params(self):
        "Генерация параметров a, b, c0"
        t = int(time.time() * 10000)

        self.a = ((((t << t % 3) * 5 + 2) & ~3) | 1) % self.m

        b = ((t << t % 4) * 7 + 5 | 1) % self.m
        while math.gcd(b, self.m) != 1:
            b = (b * 7 + 3) % self.m
        self.b = b

        self.c0 = (t ^ self.a ^ self.b) % self.m
        self.last = self.c0

    def get_params(self):
        return (self.a, self.b, self.c0)


def gen_key(generator: LinearCongruentialGenerator, key_len: int):
    key = ""
    while len(key) < key_len:
        key += bin(generator.next())[2:]

    return int(key[:key_len], base=2)


def decode_file(file_path: str, key_file_path: str):
    generator = LinearCongruentialGenerator()
    with open(file_path, "rb") as f:
        file_data = int.from_bytes(f.read())

    with open(key_file_path, encoding="UTF-8") as f_key:
        key_file_data: dict = json.loads(f_key.read())

    key_length = key_file_data.pop("key_length")
    generator.set_params(**key_file_data)

    key = gen_key(generator, key_length)

    decoded_data = file_data ^ key

    with open("./decoded_file.txt", "wb") as f:
        length = key_length // 8
        f.write(decoded_data.to_bytes(length, byteorder="big"))


def encode_file(file_path: str, key_file_path: str | None = None):
    with open(file_path, "rb") as f:
        file_data = int.from_bytes(f.read())
    key_length = ((len(bin(file_data)[2:]) + 7) // 8) * 8

    generator = LinearCongruentialGenerator()

    if key_file_path is None:
        generator.gen_params()
    else:
        with open(key_file_path, encoding="UTF-8") as f_key:
            generator.set_params(**json.loads(f_key.read()))

    key = gen_key(generator, key_length)

    encoded_data = file_data ^ key

    with open("./encoded_file", "wb") as f:
        f.write(encoded_data.to_bytes(key_length // 8, byteorder="big"))

    with open("./key_file.json", "w") as f:
        a, b, c0 = generator.get_params()
        f.write(
            json.dumps(
                {"a": a, "b": b, "c0": c0, "key_length": key_length},
                ensure_ascii=False,
            )
        )


def main():
    while True:
        print("1 - зашифровать файл\n" "2 - расшифровать файл")
        op = input("Введите номер операции: ")
        if op == "1":
            file_path = os.path.abspath(input("Введите путь к файлу: "))
            key_path = input(
                "Введите путь к файлу ключа или нажмите ENTER, "
                "чтобы сгенерировать новый: "
            )

            if key_path == "":
                key_path = None
            else:
                key_path = os.path.abspath(key_path)

            encode_file(file_path, key_path)

        elif op == "2":
            file_path = os.path.abspath(input("Введите путь к файлу: "))
            key_path = os.path.abspath(input("Введите путь к файлу ключа: "))

            decode_file(file_path, key_path)
        else:
            print("Неверная операция")


if __name__ == "__main__":
    main()
