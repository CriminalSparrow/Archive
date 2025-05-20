import re
import sys

def build_exceptions(text):
    exceptions = [0] * len(text)
    
    # правило 1: первая буква текста
    for i, c in enumerate(text):
        if c.isalpha():
            if c.isupper():
                exceptions[i] = 0  # по правилу
            break

    # правило 2: после [.?!] и пробела/переноса строки
    for match in re.finditer(r'[\.\!\?][\s\n]+([A-Za-z])', text):
        idx = match.start(1)
        if text[idx].isupper():
            exceptions[idx] = 0  # по правилу

    # правило 3: одиночная 'I'
    for match in re.finditer(r'[^A-Za-z]I[^A-Za-z]', text):
        idx = match.start() + 1
        if text[idx] == 'I':
            exceptions[idx] = 0  # по правилу

    # все остальные заглавные — исключения
    for i, c in enumerate(text):
        if c.isupper() and exceptions[i] == 0:
            # если это не по правилу, ставим 1
            is_exception = True
            # (уже учтено? если да — пропускаем)
            if (
                i == 0 or
                (i > 1 and text[i-2:i] in {'. ', '! ', '? ', '.\n', '!\n', '?\n'}) or
                (i > 0 and text[i-1] == ' ' and i+1 < len(text) and text[i+1] == ' ')
            ):
                is_exception = False
            if is_exception:
                exceptions[i] = 1

    return exceptions

def decapitalize(text):
    return ''.join(c.lower() if c.isupper() else c for c in text)

def main():
    filename = 'text.txt'
    with open(filename, 'r', encoding='ASCII') as f:
        text = f.read()

    exceptions = build_exceptions(text)
    lower_text = decapitalize(text)

    # Сохраняем результат
    with open('decapitalized.txt', 'w', encoding='ASCII') as f:
        f.write(lower_text)

    with open('exceptions.txt', 'w', encoding='ASCII') as f:
        f.write(''.join((str(j) for j in exceptions)))


if __name__ == '__main__':
    main()
