from torch import nn


class EmotionNet(nn.Module):
    """
    记忆分析网络，负责管理对话记忆
    """
    short_term_memory: list
    long_term_memory: list
    all_memory: None

    def add_long_term_memory(self, long_term_memory):
        """
        添加长记忆
        :param long_term_memory: 长记忆
        :return:
        """
        pass