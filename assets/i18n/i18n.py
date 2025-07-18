import os, sys
import json
from pathlib import Path
from locale import getdefaultlocale

now_dir = os.getcwd()
sys.path.append(now_dir)


class I18nAuto:
    LANGUAGE_PATH = os.path.join(now_dir, "assets", "i18n", "languages")

    def __init__(self, language=None, fallback=False):
        with open(
            os.path.join(now_dir, "assets", "config.json"), "r", encoding="utf8"
        ) as file:
            config = json.load(file)
            override = config["lang"]["override"]
            lang_prefix = config["lang"]["selected_lang"]

        self.language = lang_prefix

        if override == False:
            language = language or getdefaultlocale()[0]
            lang_prefix = language[:2] if language is not None else "en"
            available_languages = self._get_available_languages()
            matching_languages = [
                lang for lang in available_languages if lang.startswith(lang_prefix)
            ]
            self.language = matching_languages[0] if matching_languages else "en_US"

        self.language_map = self._load_language_list(fallback)

    def _load_language_list(self, fallback):
        file_path = Path(self.LANGUAGE_PATH) / (self.language + ".json")

        if not file_path.exists():
            if fallback:
                file_path = Path(self.LANGUAGE_PATH) / "en_US.json"
            else:
                raise FileNotFoundError(
                    f"Failed to load language file for {self.language}. Check if the correct .json file exists."
                )

        with open(file_path, "r", encoding="utf-8") as file:
            lang = json.load(file)

        lang = {k: k if not v else v for k, v in lang.items()}
        lang = {k: v.strip("") for k, v in lang.items()}

        return lang

    def _get_available_languages(self):
        language_files = [path.stem for path in Path(self.LANGUAGE_PATH).glob("*.json")]
        return language_files

    def _language_exists(self, language):
        return (Path(self.LANGUAGE_PATH) / f"{language}.json").exists()

    def __call__(self, key):
        return self.language_map.get(key, key)
