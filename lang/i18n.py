import os.path


CURRENT_DIR = os.path.dirname(__file__)
class I18N:
    """
    多语言支持
    """
    def __init__(self):
        self.config = None
        self.str_map = dict()
        self.flash()
        self.language = 'en_us'

    def set_language(self, language):
        self.language = language


    def get_str(self, key):
        """
        从 i18n 读取文本
        """

        string = self.str_map.get(f"{self.language}-{key}", f"en-us-{key}")
        if string is None:
            raise KeyError("i18n error: " + key)
        # if string is None:
        #     string = self.str_map.get("en_us-" + key)
        #     if string is None:
        #         raise KeyError("i18n error: " + key)
        return string

    def get_lang_dir(self):
        return CURRENT_DIR

    def flash(self):
        """
        刷新 i18n
        """
        self.str_map = dict()
        for filename in os.listdir(CURRENT_DIR):
            if filename.endswith('.lang'):
                self.lang_file_read(filename)
    def lang_file_read(self, name):
        """
        读取 lang 文件
        """
        file_path = os.path.join(CURRENT_DIR, name)
        name = name.replace('.lang', '')
        with open(file_path, 'r', encoding='utf-8') as lang:
            for line in lang:
                if line and not line.startswith('#'):
                    key, value = line.strip().split('=')
                    key = name + '-' + key
                    self.str_map[key] = value