from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
DetectorFactory.seed = 0

def TransLate(text: str, scr: str, dest: str) -> str:
    try:
        translated_text = GoogleTranslator(source=scr, target=dest).translate(text)
        return translated_text
    except Exception as e:
        return f"Помилка: {e}"

def LangDetect(text: str, set: str = "all") -> tuple:
    try:
        lang = detect(text)
        confidence = 1.0
        if set == "lang":
            return lang
        elif set == "confidence":
            return confidence
        elif set == "all":
            return lang, confidence
        else:
            return "Помилка: неправильне значення для параметра 'set'. Використовуйте 'lang', 'confidence' або 'all'."
    except LangDetectException as e:
        return f"Помилка визначення мови: {str(e)}"

def CodeLang(lang: str) -> str:
    languages = GoogleTranslator().get_supported_languages(as_dict=True)

    lang = lang.lower()

    if lang in languages:
        return languages[lang]

    for code, name in languages.items():
        if name.lower() == lang:
            return code

    return "Помилка: введений код або назва мови не знайдено"

from deep_translator import GoogleTranslator


def LanguageList(out: str = "screen", text: str = None) -> str:
    try:
        languages = GoogleTranslator().get_supported_languages(as_dict=True)

        # Якщо текст для перекладу не вказаний, просто вивести список мов
        translate_column = text is not None

        # Формування таблиці для виводу
        table = []
        for lang, code in languages.items():
            if translate_column:
                # Переклад тексту на відповідну мову
                translated_text = GoogleTranslator(source='auto', target=code).translate(text)
                table.append([lang, code, translated_text])
            else:
                table.append([lang, code])

        # Форматування таблиці
        if translate_column:
            headers = ["Мова", "Код", "Переклад"]
            col_widths = [max(len(row[0]) for row in table),
                          max(len(row[1]) for row in table),
                          max(len(row[2]) for row in table)]
        else:
            headers = ["Мова", "Код"]
            col_widths = [max(len(row[0]) for row in table),
                          max(len(row[1]) for row in table)]

        # Формaтування таблиці для виводу
        formatted_table = []
        formatted_table.append(f"{headers[0].ljust(col_widths[0])} | {headers[1].ljust(col_widths[1])}" +
                               (f" | {headers[2].ljust(col_widths[2])}" if translate_column else ""))
        formatted_table.append("-" * (sum(col_widths) + (3 if translate_column else 1)))

        for row in table:
            formatted_table.append(f"{row[0].ljust(col_widths[0])} | {row[1].ljust(col_widths[1])}" +
                                   (f" | {row[2].ljust(col_widths[2])}" if translate_column else ""))

        output = "\n".join(formatted_table)

        # Виведення на екран або у файл
        if out == "screen":
            print(output)
        elif out == "file":
            with open("language_list.txt", "w", encoding="utf-8") as file:
                file.write(output)

        return "Ok"
    except Exception as e:
        return f"Помилка: {e}"