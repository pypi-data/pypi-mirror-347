# README.md
# ---------
# # Gemini Translator
# A simple Python wrapper for Google Gemini LLM translations.
#
# ## Installation
# ```bash
# pip install gemini-translator
# ```
#
# ## Usage
# ```python
# from gemini_translator.translator import GeminiTranslator
# tr = GeminiTranslator(api_key="YOUR_API_KEY")
# res = tr.translate(["Hello"], "auto", "ru")
# print(res)


# Gemini Translator

Gemini Translator — лёгкая Python-библиотека для пакетных переводов с помощью Google Gemini LLM.

## Установка

```bash
pip install gemini-translator
```

## Быстрый старт

```python
from gemini_translator.translator import GeminiTranslator

# Передача ключа напрямую
translator = GeminiTranslator(api_key="YOUR_GEMINI_API_KEY")

# Или через переменную окружения (рекомендуется)
# export GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
# translator = GeminiTranslator()

# 1) Перевод одного текста
result = translator.translate(
    ["Hello, world!"],
    source_lang="auto",   # автоопределение языка
    target_lang="ru"      # двухбуквенный код языка
)
print(result["Hello, world!"])

# 2) Пакетный перевод списка строк
texts = ["Good morning", "How are you?"]
translations = translator.translate(
    texts,
    source_lang="en",    # явный код исходного языка
    target_lang="fr"     # код целевого языка
)
for original, translated in translations.items():
    print(f"{original} -> {translated}")
```

## Ключ API Gemini

Для работы с Gemini API необходим API-ключ. Его можно получить в Google Cloud Console:

1. Перейдите в раздел **APIs & Services** → **Credentials**.
2. Создайте или выберите существующий API-ключ.
3. Сохраните значение ключа и передайте в библиотеку одним из способов:

   * Через параметр `api_key` при инициализации `GeminiTranslator`.
   * Через переменную окружения `GOOGLE_API_KEY`.

## Параметры

* `api_key: str` — ваш Gemini API-ключ. Если не указан, будет использована переменная окружения `GOOGLE_API_KEY`.
* `model: str` — имя модели Gemini (по умолчанию `gemini-2.0-flash`).
* `timeout: int` — таймаут HTTP-запроса в секундах (по умолчанию 30).

## Примечания

* Коды языков указываются по стандарту ISO 639-1 (двухбуквенные, например, `en`, `ru`, `fr`).
* Если у вас возникает `ValueError: API key must be provided`, проверьте корректность передачи ключа.

