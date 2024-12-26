from core.emotion_net import EmotionNet


class Memory:
    memory_file_name: str
    short_term_memory: []
    long_term_memory: []
    all_memory: []
    emotion_net: EmotionNet | None
    """
    人物对话记忆
    # todo 设计记忆系统，长期记忆以及短期记忆
    对于长期记忆，可能需要使用到一种机制来确定当前对话是否重要，比如关键字，或者使用神经网络做情感分析来确定。
    """
    def __init__(self, max_short_term_memory_size=30, memory_file_name="memory.json"):
        self.memory_file_name = memory_file_name
        self.short_term_memory = []
        self.long_term_memory = []
        self.all_memory = []
        self.emotion_net = None

    def load_memory(self):
        pass

    def save_memory(self):
        pass

    def add_short_memory(self, message):
        pass

    def add_long_memory(self, message):
        pass
