from Translator.Gtrans import *

LanguageList("screen", "hello")

print("Введіть текст для перекладу:")
inputText = input()
print("Введіть мову для перекладу (назва або код):")
target_lang = input()

detected_lang, confidence = LangDetect(inputText)
print(f"Визначена мова тексту: {CodeLang(detected_lang)} (Точність: {confidence})")

translation = TransLate(inputText, "auto" , target_lang)
print(f"Перекладений текст: {translation}")