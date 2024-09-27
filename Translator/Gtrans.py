import googletrans as gtl
translator = gtl.Translator()
languages = gtl.LANGUAGES

def TransLate(text: str, scr: str, dest: str) -> str:
    # Перевірка наявності мов у списку підтримуваних
    if scr != 'auto' and scr not in gtl.LANGUAGES and scr not in gtl.LANGUAGES.values():
        return "Помилка: неправильний код початкової мови"
    if dest not in gtl.LANGUAGES and dest not in gtl.LANGUAGES.values():
        return "Помилка: неправильний код мови призначення"

    try:
        # Виконання перекладу
        translated = translator.translate(text, src=scr, dest=dest)
        return translated.text
    except Exception as e:
        return f"Помилка перекладу: {str(e)}"


# Визначення мови тексту
def LangDetect(text: str, set: str = "all") -> tuple:
    try:
        detection = translator.detect(text)
        lang = detection.lang
        confidence = detection.confidence

        if set == "lang":
            return lang
        elif set == "confidence":
            return confidence
        elif set == "all":
            return lang, confidence
        else:
            return "Помилка: неправильне значення для параметра 'set'. Використовуйте 'lang', 'confidence' або 'all'."

    except Exception as e:
        return f"Помилка визначення мови: {str(e)}"


def CodeLang(lang: str) -> str:
    lang = lang.lower()

    if lang in languages:
        return languages[lang]

    for code, name in languages.items():
        if name.lower() == lang:
            return code

    return "Помилка: введений код або назва мови не знайдено"

def LanguageList(out: str = "screen", text: str = None) -> str:
    table_data = []

    for code, name in languages.items():
        if text:
            try:
                translated = translator.translate(text, dest=code).text
            except Exception as e:
                return f"Помилка перекладу: {str(e)}"
            table_data.append((code, name, translated))
        else:
            table_data.append((code, name))

    # Форматування таблиці
    if text:
        header = f"{'Код мови':<10} {'Назва мови':<20} {'Переклад':<40}"
        row_format = "{:<10} {:<20} {:<40}"
    else:
        header = f"{'Код мови':<10} {'Назва мови':<20}"
        row_format = "{:<10} {:<20}"

    table_output = header + "\n" + "-" * len(header) + "\n"
    for row in table_data:
        table_output += row_format.format(*row) + "\n"

    # Виведення таблиці на екран або у файл
    if out == "screen":
        print(table_output)
    elif out == "file":
        try:
            with open("language_list.txt", "w", encoding="utf-8") as file:
                file.write(table_output)
        except Exception as e:
            return f"Помилка запису у файл: {str(e)}"
    else:
        return "Помилка: неправильне значення для параметра 'out'. Використовуйте 'screen' або 'file'."

    return "Ok"