letter_dict = {}
f = True
first = ''
second = ''
while f:
    input_letter = input('Enter letter [A-Z]: ')
    if input_letter != 'STOP':
        if first == '':
            first = input_letter
        elif second == '':
            second = input_letter


        if letter_dict.get(input_letter) is None:
            print(f'New letter: {input_letter}!')
            letter_dict[input_letter] = 1
        elif letter_dict.get(input_letter) >= 2 and first == second and second == input_letter:
            letter_dict.pop(input_letter)
            print(f'Removing letter: {input_letter}!')
        else:
            letter_dict[input_letter] = letter_dict[input_letter] + 1

        if first !='' and  second !='':
            first = second
            second = input_letter
    else:
        f = False
print()
print('Final Summary:')
for key,value in letter_dict.items():
    print(f'{key}: {value}')