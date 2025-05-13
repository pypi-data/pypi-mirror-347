import os
import json
import yaml
import inspect

__all__ = ["configure", "translate", "get_config", "_extra"]

_localizer_instance = None


class Localizer:
    def __init__(self, default_lang='en', translations_path='translations', strict_mode=False):
        self.default_lang = default_lang
        self.translations_path = translations_path
        self.strict_mode = strict_mode
        self.translations = {}
        self.config = {
            "default_lang": default_lang,
            "path": translations_path,
            "mode": strict_mode
        }

    def load(self):
        if not os.path.isabs(self.translations_path):
            caller_frame = inspect.currentframe().f_back.f_back
            caller_file = caller_frame.f_globals.get('__file__')
            if caller_file:
                caller_dir = os.path.dirname(os.path.abspath(caller_file))
                self.translations_path = os.path.join(caller_dir, self.translations_path)
        
        if not os.path.isdir(self.translations_path):
            raise FileNotFoundError(f"Translation path not found: {self.translations_path}")
        
        for filename in os.listdir(self.translations_path):
            if filename.endswith('.json') or filename.endswith('.yml') or filename.endswith('.yaml'):
                lang_code = os.path.splitext(filename)[0]
                filepath = os.path.join(self.translations_path, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f) if filename.endswith('.json') else yaml.safe_load(f)
                    flat_data = self._flatten_dict(data)
                    self._merge_translations(flat_data, lang_code)

    def _flatten_dict(self, d, parent_key='', sep='.'):
        items = {}
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(self._flatten_dict(v, new_key, sep=sep))
            else:
                items[new_key] = v
        return items

    def _merge_translations(self, flat_data, lang_code):
        for key, text in flat_data.items():
            if key not in self.translations:
                self.translations[key] = {}
            self.translations[key][lang_code] = text

    def translate(self, key: str, lang: str = None, **kwargs) -> str:
        lang = lang or self.default_lang
        translations = None

        if self.strict_mode:
            try:
                translations = self.translations[key][lang]
            except KeyError:
                translations = self.translations[key].get(self.default_lang, key)
        else:
            translations = (
                self.translations.get(key, {}).get(lang)
                or self.translations.get(key, {}).get(self.default_lang)
                or key
            )
        if kwargs:
            try:
                return translations.format(**kwargs)
            except (KeyError, AttributeError):
                return translations
        return translations

    def get_config(self, key: str = None) -> str | bool | dict:
        return self.config.get(key, self.config)

def configure(default_lang='en', translations_path='translations', strict_mode=False) -> dict:
    """
    Initializes and configures the localization manager.

    This function must be called before using `translate()` or other public API functions.
    It loads translation files from the specified directory and sets up the default language and behavior.

    Args:
        default_lang (str): Language code to use by default (e.g., 'en', 'ru'). Defaults to 'en'.
        translations_path (str): Path to the directory containing translation files (JSON/YAML).
                                 Can be absolute or relative to the caller. Defaults to 'translations'.
        strict_mode (bool): If True, only keys explicitly translated in the selected language will be used.
                            If False, the default language will be used as fallback, and then the key itself if missing.
                            Defaults to False.

    Returns:
        dict: A configuration dictionary containing:
            - 'default_lang' (str): The default language.
            - 'path' (str): The resolved path to the translations directory.
            - 'mode' (bool): Whether strict mode is enabled.

    Raises:
        FileNotFoundError: If the specified translations directory cannot be found.
    """
    global _localizer_instance
    normalized_path = os.path.normpath(translations_path)
    _localizer_instance = Localizer(default_lang=default_lang, translations_path=normalized_path, strict_mode=strict_mode)
    _localizer_instance.load()
    return _localizer_instance.config

def translate(key: str, lang: str = None, **kwargs) -> str:
    """
    Translates the given key into the specified language.

    If no language is provided, the default language from `configure()` will be used.
    You can also provide keyword arguments to substitute placeholders in the translation string.

    Args:
        key (str): The translation key (e.g. "ui.start_button" or "error.not_found").
        lang (str, optional): Language code (e.g. "en", "ua"). Defaults to the configured default language.
        **kwargs: Optional named arguments for string formatting. For example, `{username}` in a translation.

    Returns:
        str: Translated string, formatted if placeholders are provided.

    Raises:
        RuntimeError: If `configure()` has not been called before using this function.
    """
    if _localizer_instance is None:
        raise RuntimeError("Localizer not configured. Call configure() first.")
    return _localizer_instance.translate(key=key, lang=lang, **kwargs)

def get_config(key: str = None) -> str | bool | dict:
    """
    Returns the current localizer configuration value.

    This function allows you to retrieve the internal settings of the localizer,
    such as the default language, translation path, or strict mode status.

    Args:
        key (str): Configuration key to retrieve. Available keys:
            - "default_lang": Returns the default language code (str)
            - "path": Returns the path to the translations directory (str)
            - "mode": Returns whether strict mode is enabled (bool)
            If omitted, returns the entire config dictionary.

    Returns:
        (str | bool | dict): The value of the requested configuration key, or all config if key is None.
    """
    return _localizer_instance.get_config(key=key)

def _extra() -> Localizer:
    """
    Returns the current instance of the localizer used by the module.
    This can be useful for accessing advanced features or internal state.

    Returns:
        Localizer: The active localizer instance.
    """
    return _localizer_instance