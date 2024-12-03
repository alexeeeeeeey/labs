with open("./123.txt", encoding="UTF-8") as f:
    data = f.read()

raw_list = [i for i in data.split("\n") if i != "" and i != " "]

reverse_map = {}
current_char = ""
for i in raw_list:
    i = i.strip()
    if not i.isdigit() or i == "_":
        current_char = i
    else:
        reverse_map[int(i)] = current_char

string = input("Введите строку: ")
decoded = ""

for i in [string[j:j + 3] for j in range(0, len(string), 3)]:
    decoded += reverse_map[int(i)]

print(decoded)
