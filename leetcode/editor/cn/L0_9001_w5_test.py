garden = [
    ['🌲', '🌱', '🌹', '🦋'],
    ['🐛', '🌹', '🌲', '🐛'],
    ['🌲', '🌱', '🌱', '🌲'],
    ['🌱', '🐛', '🦋', '🌲']
]

# TODO: define bird_emojis
# ...

bird_emojis = {
    '🐛': '💀',
    '🦋': '💀',
    '🌱': '🌹',
    '🌲': '🌲',
    '🌹': '🌹',
    '🪵': '🪵',
    '🥀': '🥀',
    '💀': '💀'
}

scarlet_emojis = {
    '🦋': '🐛',
    '🌲': '🪵',
    '🌹': '🥀',
    '🐛': '💀',
    '🌱': '💀',
    '🪵': '💀',
    '🥀': '💀',
    '💀': '💀'
}

# TODO: define gandalf_emojis
# ...
gandalf_emojis = {
    '💀': '🌱',
    '🐛': '🦋',
    '🌱': '🌲',
    '🪵': '🌲',
    '🥀': '🌹',
    '🦋': '🦋',
    '🌲': '🌲',
    '🌹': '🌹'
}

print('Event 1 - Bird Landing 🦜')
bird_landing = input('Enter bird landing coordinates: ').split()
x = int(bird_landing[0])
y = int(bird_landing[1])
target = garden[x][y]
outcome = bird_emojis[target]
if target == '🦋' or target == '🐛':
    garden[x][y] = '💀'
    print(f'{target} at ({x}, {y}) eaten by 🦜')
elif target == '🌱':
    garden[x][y] = outcome
    print(f'{target} at ({x}, {y}) has turned into a {outcome}')
else:
    print('Nothing happens.')
for i in range(len(garden)):
    print(garden[i])
print()


print('Event 2 - Scarlet Witch 🔮')
coordinates = input('Enter chaos magic coordinates: ').split()
x = int(coordinates[0])
y = int(coordinates[1])
target = garden[x][y]
outcome = scarlet_emojis[target]

if target == '🦋' or target == '🌲' or target == '🌹':
    garden[x][y] = outcome
    print(f'{target} at ({x}, {y}) has turned into a {outcome}')
elif target == '💀':
    print('Nothing happens.')
else:
    garden[x][y] = outcome
    print(f'{target} at ({x}, {y}) eradicated by 🔮')

for i in range(len(garden)):
    print(garden[i])
print()



# print('Event 3 - Gandalf ✨')
# TODO: complete Event 3
# ...
print('Event 3 - Gandalf ✨')
gandalf_landing = input('Enter spell coordinates: ').split()
x = int(gandalf_landing[0])
y = int(gandalf_landing[1])
target = garden[x][y]
outcome = gandalf_emojis[target]
if target != outcome:
    garden[x][y] = outcome
    print(f'{target} at ({x}, {y}) has turned into a {outcome}')
else:
    print('Nothing happens.')
for i in range(len(garden)):
    print(garden[i])