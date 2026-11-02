with open('scratch/generate_57_manual.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('"MOD ', '"MODULE ')

with open('scratch/generate_57_manual.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated MOD to MODULE in generate_57_manual.py')

