with open("./123.txt", encoding="UTF-8") as f:
    data = f.read()

raw_list = [i for i in data.split("\n") if i != "" and i != " "]

total_digits = {}
last_char = ""
for i in raw_list:
    i = i.strip()
    if not i.isdigit() or i == "_":
        total_digits[i] = []
        last_char = i
    else:
        total_digits[last_char].append(int(i))


string = input("Введите строку: ")
encoded = ""

chars_been = {}
for i in string:
    if i not in chars_been:
        chars_been[i] = 0

    try:
        encoded += str(total_digits[i][chars_been[i]])
    except IndexError:
        chars_been[i] = 0
        encoded += str(total_digits[i][chars_been[i]])
    chars_been[i] += 1

print(encoded)
