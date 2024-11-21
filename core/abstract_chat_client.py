import json
import os.path
from abc import ABC, abstractmethod
from json import JSONDecodeError
from typing import Iterator

from config.application_config import ApplicationConfig




class AbstractChatClient(ABC):
    prompt: str
    memory: []
    memory_file_name: str
    config: ApplicationConfig
    chat_client_dir: str

    @abstractmethod
    def chat(self, message) -> str:
        raise NotImplementedError

    @abstractmethod
    def chat_iter(self, message: str) -> Iterator[str]:
        raise NotImplementedError

    def save_memory(self, filename: str):
        print("memory serializable....")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, ensure_ascii=False, sort_keys=True, indent=4)

    def load_memory(self, filename: str):
        if not os.path.exists(filename):
            print("Memory file not found")
            return []
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except JSONDecodeError:
            print("Memory file is corrupted")
            return []

    def hook(self):
        self.save_memory(self.memory_file_name)

