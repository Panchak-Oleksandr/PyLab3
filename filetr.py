import os
from Translator.Gtrans import *

def read_config(config_file: str) -> dict:
    # Зчитування конфігураційного файлу та повернення словника з налаштуваннями.
    config = {}
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            for line in file:
                key, value = line.strip().split('=')
                config[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"Конфігураційний файл {config_file} не знайдено.")
        return None
    return config

def analyze_text(file_path: str, max_chars: int, max_words: int, max_sentences: int):
    # Читання тексту з файлу та аналіз, доки не досягнуто однієї з умов:
    # кількість символів, слів або речень перевищує задані межі.
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не знайдено.")
        return None, "Файл не знайдено."

    char_count = word_count = sentence_count = 0
    text_content = ""

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                text_content += line
                char_count += len(line)
                word_count += len(line.split())
                sentence_count += line.count('.') + line.count('!') + line.count('?')

                if char_count > max_chars or word_count > max_words or sentence_count > max_sentences:
                    break

        return {
            'chars': char_count,
            'words': word_count,
            'sentences': sentence_count,
            'text': text_content
        }, None
    except Exception as e:
        return None, str(e)

def write_to_file(filename: str, content: str):
    # Запис переданий текст до файлу.
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        return "Ok", None
    except Exception as e:
        return None, f"Помилка запису у файл: {str(e)}"

def main():
    # Зчитування конфігураційного файлу
    config = read_config('config')
    if not config:
        return

    file_path = config.get('file_path')
    max_chars = int(config.get('max_chars', 1000))
    max_words = int(config.get('max_words', 200))
    max_sentences = int(config.get('max_sentences', 10))
    output_type = config.get('output', 'screen')
    target_language = config.get('target_language', 'en')

    # Аналізуємо текст із файлу
    text_data, error = analyze_text(file_path, max_chars, max_words, max_sentences)
    if error:
        print(f"Помилка: {error}")
        return

    print(f"Назва файлу: {file_path}")
    print(f"Розмір файлу: {os.path.getsize(file_path)} байт")
    print(f"Кількість символів: {text_data['chars']}")
    print(f"Кількість слів: {text_data['words']}")
    print(f"Кількість речень: {text_data['sentences']}")

    # Визначення мови тексту
    lang_code = LangDetect(text_data['text'])
    if error:
        print(f"Помилка визначення мови: {error}")
        return
    print(f"Мова тексту: {lang_code}")

    # Переклад текстн на цільову мову
    translated_text = TransLate(text_data['text'], "auto", target_language)
    if error:
        print(f"Помилка перекладу: {error}")
        return

    # Виведення на екран або у файл
    if output_type == 'screen':
        print(f"Переклад на {target_language}:")
        print(translated_text)
    elif output_type == 'file':
        output_file = f"{os.path.splitext(file_path)[0]}_{target_language}.txt"
        result, error = write_to_file(output_file, translated_text)
        if error:
            print(f"Помилка запису у файл: {error}")
        else:
            print(result)
    else:
        print("Невірно вказаний тип виведення у конфігурації.")

if __name__ == "__main__":
    main()
