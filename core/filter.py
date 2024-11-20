class Filter:
    """
    违禁词过滤器
    """
    filter_table: list
    __switch: bool

    def __init__(self, filter_lsit_path):
        self.filter_table = list()
        self.__switch = True
        with open(filter_lsit_path, 'r', encoding='utf-8') as f:
            for line in f:
                self.filter_table.append(line.strip())

    def add(self, text) -> str:
        self.filter_table.append(text)
        return f'add {text}'

    def remove(self, text) -> str:
        self.filter_table.remove(text)
        return f'remove {text}'

    def filter(self, word) -> str:
        if self.__switch and any(char in word for char in self.filter_table):
            return 'Filter.'
        else:
            return word

    def switch_on(self) -> str:
        self.__switch = True
        return f'过滤器开关状态已更改为：{self.__switch}'

    def switch_off(self) -> str:
        self.__switch = False
        return f'过滤器开关状态已更改为：{self.__switch}'
