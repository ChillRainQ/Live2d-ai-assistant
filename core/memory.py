class Memory:
    """
    人物对话记忆
    # todo 设计记忆系统，长期记忆以及短期记忆
    """
    def __init__(self):
        self.memory_file_name = None
        self.memory = []
        self.long_term_memory = []
        self.load_memory()

    def load_memory(self):
        pass

    def save_memory(self):
        pass