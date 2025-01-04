import io
from typing import Union

from ..contant import i18n, splits


class CliRequest:
    text: str  # 输入文本
    text_language: str  # 输入语言
    how_to_cut: str  # 文本切割方式
    top_k: int
    top_p: float
    temperature: float
    ref_wav: str  # 参考音频
    ref_text: str  # 参考音频文本内容
    ref_language: str  # 参考音频语言
    ref_tree: bool
    if_freeze: bool
    inp_refs: None
    def __init__(self, text, text_language,
                 how_to_cut=i18n("不切"), top_k=20, top_p=0.6, temperature=0.6, speed=1,
                 ref_wav=None, ref_text=None, ref_language=None,
                 ref_free=False, if_freeze=False, inp_refs=None):
        self.text = text
        self.text_language = i18n(text_language)
        self.how_to_cut = how_to_cut
        self.top_k = top_k
        self.top_p = top_p
        self.temperature = temperature
        self.speed = speed
        self.ref_wav = ref_wav
        self.ref_text = ref_text
        self.ref_language = i18n(ref_language)
        self.ref_free = ref_free
        self.if_freeze = if_freeze
        self.inp_refs = inp_refs

    def params_check_and_init(self):
        if self.ref_wav is None:
            raise ValueError(i18n('请上传参考音频'))
        if self.text is None or len(self.text) == 0:
            raise ValueError(i18n('请填入推理文本'))
        if self.ref_text is None or len(self.ref_text) == 0:
            self.ref_free = True
        if not self.ref_free:
            self.ref_text = self.ref_text.strip("\n")
            if (self.ref_text[-1] not in splits): self.ref_text += "。" if self.ref_language != "en" else "."
            print(i18n("实际输入的参考文本:"), self.ref_text)
        self.text = self.text.strip("\n")
        print(i18n("实际输入的目标文本:"), self.text)
