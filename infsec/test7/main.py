def permutation_decryption(input_str, key):
    result = ""

    while len(input_str) % 6 != 0:
        input_str += ' '

    k = 0
    while len(result) < len(input_str):
        s = ""
        for i in range(6):
            if k + i < len(input_str):
                s += input_str[k + i]
        k += 6

        for i in range(6):
            for j in range(6):
                if key[j] == str(i + 1):
                    result += s[j]
        s = ""

    result = result.replace(" ", "")

    return result


def permutation_encryption(input_str, key):
    result = ""

    while len(input_str) % 6 != 0:
        input_str += ' '

    k = 0
    while len(result) < len(input_str):
        s = ""
        for i in range(6):
            if k + i < len(input_str):
                s += input_str[k + i]
        k += 6

        for i in range(6):
            for j in range(6):
                if key[i] == str(j + 1):
                    result += s[j]
        s = ""

    result = result.replace(" ", "")

    return result


input_str = ""
key = ""
encrypted = permutation_encryption(input_str, key)
print(encrypted)
