def alter(words, i):
    result = []
    for char in words:
        if 'a' <= char <= 'z':
            new_char = chr(ord('a') + (ord(char) - ord('a') + i) % 26)
            result.append(new_char)
        elif 'A' <= char <= 'Z':
            new_char = chr(ord('A') + (ord(char) - ord('A') + i) % 26)
            result.append(new_char)
        else:
            result.append(char)
    return ''.join(result)


def main():
    try:
        key_input = input('Enter key: ')
        i = int(key_input)
    except ValueError:
        print('Invalid key!')
        return

    if not (0 <= i <= 26):
        print('Invalid key!')
        return

    line = input('Enter line: ')
    encrypted_line = alter(line, i)
    print()

    print(encrypted_line)


if __name__ == '__main__':
    main()




