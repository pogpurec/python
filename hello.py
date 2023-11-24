# Ask user for their name
name = input('Whats your name? ').strip().title()

# Split users name
first, last = name.split(' ')

# Say hello to user
print(f'Hello, {name}')
print('Your first name is', first)
print('And second name is', last)