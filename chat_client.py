from core.queues import send_queue, getMsg_queue


class ChatClient:
    def send(self, text, callback: callable):
        send_queue.put(text)
        response = getMsg_queue.get()
        callback()