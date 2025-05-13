# Mini language Manager

**Mini localization manager for Python using JSON/YAML files**

Mini language Manager is a lightweight and developer-friendly localization tool for Python. It allows you to organize translations in plain JSON or YAML files and access them with nested keys. Supports fallback and placeholders.

---

## 📦 Installation

```bash
pip install m-lang-m
```

---

## 🧰 Features

- Supports both `.json` and `.yaml`/`.yml` translation files
- Automatic directory resolution relative to the caller
- Nested key support (e.g., `menu.settings.language`)
- String formatting with `{placeholders}`
- Returns the current config if needed

---

## 📁 Translation File Example

**locale/en.json**
```json
{
    "title": "Main",
    "menu": {
        "settings": {
            "language": "Language",
            "placeholders": "Many {one}, {two} and {thee}"
        },
        "back" : "Go back"
    }
}
```

**locale/ua.yml**
```yml
title: "Головна"
menu:
  settings:
    language: "Мова"
    placeholders: "Багато {one}, {two} і {thee}"
  back: "Повернутися"
```

---

## 🚀 Usage

### Configure the localizer

```python
from mlangm import configure, translate, get_config

config_info = configure(default_lang='en', translations_path='locale')
# config_info = {
#     'default_lang': 'en',
#     'path': 'locale',
#     'mode': False
# }

print(translate('menu.settings.language'))  # Output: "Language"
print(translate('menu.back')) # Output: "Go back"
print(translate('menu.settings.language', 'ua'))  # Output: "Мова"
print(translate('title', 'ua')) # Output: "Головна"

print(translate('menu.settings.placeholders', one='first', two='second', thee='third'))
# Output: "Many first, second and third"
```

---

## 🔧 API

### `configure(default_lang = 'en', translations_path = 'translations', strict_mode = False) -> dict`

Initializes the localizer and loads translations.

- `default_lang`(str): The default language code.
- `translations_path`(str): Directory with `.json` / `.yaml` files.
- `strict_mode`(bool): If True, disables fallbacks.

Returns the configuration dictionary.

Example:
```python
config_info = configure(default_lang = 'en', translations_path = 'locale', strict_mode = False)
```
```python
configure()
```
---

### `translate(key: str, lang: str = None, **kwargs) -> str`

Retrieves a translated string.  
Supports fallback and placeholders.

Example:
```python
translate('hello', 'en', name='Alex') # Output: "Hello, Alex!" | if 'hello' key -> "Hello, {name}!"
```
```python
translate()
```
---

### `get_config(key: str = None) -> str | bool | dict`

Returns the current configuration or a single setting.

- `default_lang`(str): Returns the default language code
- `path`(str): Returns the path to the translations directory
- `mode`(bool): Returns whether strict mode is enabled


Example:
```python
get_config("path") # Output: "locale"
```
```python
get_config()
```
---

### `_extra() -> Localizer`

Technical action, under normal conditions, **not to be used**.

Access the internal `Localizer` instance directly.

Example:
```python
from mlangm import configure, _extra

configure(default_lang='en', translations_path='locale')

print(_extra().config) # Output: {'default_lang': 'en', 'path': 'locale', 'mode': False}
print(_extra().default_lang) # Output: 'en'
print(_extra().translations) # Output: Dictionary with translations from the 'locale' folder
```
```python
_extra()
```
---

## 📄 License

MIT License