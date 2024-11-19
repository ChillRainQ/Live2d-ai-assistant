import atexit
import json
import os
import time
from typing import Iterator

from transformers import AutoModelForCausalLM, AutoTokenizer

from config.application_config import ApplicationConfig
from core.abstract_chat_client import AbstractChatClient


class QwenClient(AbstractChatClient):
    def __init__(self, config: ApplicationConfig):
        self.config = config
        self.model_path = "qwen2.5_1.5B"
        self.memory_file_name = self.model_path + ".json"
        self.model = AutoModelForCausalLM.from_pretrained(os.path.join('chat_clients', self.model_path),torch_dtype="auto",device_map="auto")
        self.tokenizer = AutoTokenizer.from_pretrained(os.path.join('chat_clients', self.model_path))
        self.system_prompt = self.config.llm_prompt.value
        self.memory = self.load_memory(self.memory_file_name)
        atexit.register(self.hook)

    def chat(self, message):
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
        return self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    def chat_iter(self, message: str) -> Iterator[str]:
        full_response = ""
        for char in self.chat(message):
            yield char
            full_response += char


if __name__ == '__main__':
    config = ApplicationConfig()
    chat = QwenClient(config)
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
