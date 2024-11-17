import queue
import threading

from utils import queues
from application import Application
from config.application_config import ApplicationConfig
from llm.llm_factory import LLMFactory

config = ApplicationConfig()
def llm_setup():
    llm = LLMFactory.create(config.llm_type.value)
    while True:
        message = queues.send_queue.get()
        response = llm.send_message_to_llm(message)
        queues.getMsg_queue.put(response)
        print(response)


if __name__ == '__main__':
    print("llm init....")
    threading.Thread(target=llm_setup, daemon=True).start()
    print("application init....")
    app = Application(config)
    print("load config....")
    app.load_config()
    print("setup app....")
    app.setup()
    print("run app....")
    app.start()