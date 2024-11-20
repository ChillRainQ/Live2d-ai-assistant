import atexit
import os
import time
from typing import Iterator

from transformers import AutoModelForCausalLM, AutoTokenizer

import prompts.prompts_loader
from config.application_config import ApplicationConfig
from core.abstract_chat_client import AbstractChatClient

"""
Qwen2.5 1.5B 客户端，建议使用的方式。 模型占用大概3G左右显存
如果安装不成功,不会操作或者硬件资源不足，亦可以使用http的方式。
使用http_client,并在config/chat_client_config.yaml中添加配置。
"""


class QwenClient(AbstractChatClient):
    def __init__(self, **kwargs):
        self.chat_client_dir = os.path.dirname(os.path.abspath(__file__))
        self.config = kwargs.get("config")
        self.model_name = self.config.get("model_name")
        self.memory_file_name = self.model_name + ".json"
        self.model = AutoModelForCausalLM.from_pretrained(os.path.join(self.chat_client_dir, self.model_name),
                                                          torch_dtype="auto", device_map="auto")
        self.tokenizer = AutoTokenizer.from_pretrained(os.path.join(self.chat_client_dir, self.model_name))
        self.system_prompt = prompts.prompts_loader.load_personality(
            self.config.get('personality')
        )
        self.memory = self.load_memory(self.memory_file_name)
        atexit.register(self.hook)

    def chat(self, message) -> str:
        self.memory.append({
            "role": "user",
            "content": message
        })
        messages = [
                       {"role": "system", "content": self.system_prompt},
                       {"role": "user", "content": message}
                   ] + self.memory
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        generated_ids = self.model.generate(**model_inputs, max_new_tokens=512)
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        self.memory.append({
            "role": "assistant",
            "content": response
        })
        self.save_memory(self.memory_file_name)
        return response

    def chat_iter(self, message: str) -> Iterator[str]:
        full_response = ""
        for char in self.chat(message):
            yield char
            full_response += char


if __name__ == '__main__':
    config = ApplicationConfig()
    chat = QwenClient()
    while True:
        message = input(">> ")
        now = time.time()  # 记录当前时间
        char_iter: Iterator[str] = chat.chat_iter(message)
        full_response = ""
        for char in char_iter:
            full_response += char
            print(char, end='')
        elapsed_time = time.time() - now  # 计算耗时
        print(f"\ncost time: {elapsed_time:.2f}s")  # 输出耗时
