# import threading
# import time
# import numpy as np
# import sounddevice as sd
# import torch
# import torchaudio
# from core.tts_factory import TTSClientFactory
#
# # 设置音频的采样率和位深等参数
# sample_rate = 22050  # 你的音频采样率
# dtype = np.float32  # 假设是 16 位 PCM 数据
# all_audio_data = []
# audio_data = np.array([], dtype=dtype)  # 全局音频数据存储
# lock = threading.Lock()  # 线程锁，用于保护 `audio_data`
# stop_event = threading.Event()  # 用于控制播放线程的停止
#
#
# def play_audio():
#     global audio_data
#     while not stop_event.is_set():
#         with lock:
#             if audio_data.size > 0:
#                 lens = audio_data.size
#                 sd.play(audio_data, samplerate=sample_rate)
#                 sd.wait()  # 等待播放完成
#                 # 播放后移除已播放的数据
#                 audio_data = audio_data[lens * audio_data.itemsize:]
#             else:
#                 time.sleep(0.01)  # 等待数据生成，避免占用过多 CPU
#
#
# def generate_audio(cosyvoice, text):
#     global audio_data
#     # 开始生成音频数据
#     for i in cosyvoice.model.inference_cross_lingual(text, cosyvoice.prompt_speech, stream=True):
#         chunk = i['tts_speech'].numpy()
#         all_audio_data.append(i['tts_speech'])
#         with lock:
#             audio_data = np.append(audio_data, chunk)  # 拼接新生成的音频数据
#
#
# def main():
#     cosyvoice = TTSClientFactory.create("cosyvoice")
#
#     # 模型预热
#     print("开始模型预热")
#     for i in cosyvoice.model.inference_cross_lingual(cosyvoice.prompt_text, cosyvoice.prompt_speech, stream=True):
#         pass
#     print("预热完成")
#     while True:
#         text = input(">>")
#         if text.strip() == "":
#             continue
#         now = time.time()
#
#         # 启动播放线程
#         player_thread = threading.Thread(target=play_audio, daemon=True)
#         player_thread.start()
#
#         print("start generate")
#
#         # 启动生成线程
#         generate_audio(cosyvoice, text)
#
#         # 等待生成完成
#         print(f'generate time: {time.time() - now}')
#
#         # 停止播放线程
#         stop_event.set()
#         player_thread.join()
#         torchaudio.save('audio.wav', torch.concat(all_audio_data, dim=1), 22050, format='wav')
#         # 重置停止事件，以便下次播放
#         stop_event.clear()
#
#
# if __name__ == '__main__':
#     main()

# import threading
# import time
# import numpy as np
# import sounddevice as sd
# from core.tts_factory import TTSClientFactory
#
# sample_rate = 22050  # 你的音频采样率
# dtype = np.float32  # 假设是 32 位 PCM 数据
# audio_buffer = []  # 缓冲区用于存储音频数据块
# audio_buffer_lock = threading.Lock()  # 线程锁，用于保护 `audio_buffer`
# stop_event = threading.Event()  # 用于控制生成线程的停止
#
#
# def audio_callback(outdata, frames, time, status):
#     if status:
#         print(status)
#     with audio_buffer_lock:
#         if len(audio_buffer) >= frames:
#             outdata[:] = np.array(audio_buffer[:frames], dtype=dtype).reshape(-1, outdata.shape[1])
#             del audio_buffer[:frames]
#         elif len(audio_buffer) > 0:
#             # 如果缓冲区不足以填满 `frames`，则填充剩余部分为零
#             outdata[:len(audio_buffer)] = np.array(audio_buffer, dtype=dtype).reshape(-1, outdata.shape[1])
#             outdata[len(audio_buffer):] = np.zeros((frames - len(audio_buffer), outdata.shape[1]), dtype=dtype)
#             del audio_buffer[:]
#         else:
#             outdata[:] = np.zeros((frames, outdata.shape[1]), dtype=dtype)
#             if stop_event.is_set():  # 如果停止事件触发且缓冲区为空，则停止播放
#                 raise sd.CallbackStop
#
#
# def generate_audio(cosyvoice, text):
#     global audio_buffer
#     for i in cosyvoice.model.inference_cross_lingual(text, cosyvoice.prompt_speech, stream=True):
#         chunk = i['tts_speech'].numpy().flatten().tolist()  # 确保数据是 1D 列表
#         with audio_buffer_lock:
#             audio_buffer.extend(chunk)  # 将生成的音频数据块添加到缓冲区
#     stop_event.set()  # 生成完成，触发停止事件
#
#
# def main():
#     cosyvoice = TTSClientFactory.create("cosyvoice")
#
#     # 模型预热
#     print("开始模型预热")
#     for i in cosyvoice.model.inference_cross_lingual(cosyvoice.prompt_text, cosyvoice.prompt_speech, stream=True):
#         pass
#     print("预热完成")
#     while True:
#         text = input(">>")
#         if text.strip() == "":
#             continue
#         # 清空缓冲区并重置停止事件
#         with audio_buffer_lock:
#             audio_buffer.clear()
#         stop_event.clear()
#
#         print("start generate")
#
#         # 启动生成线程
#         generate_thread = threading.Thread(target=generate_audio, args=(cosyvoice, text), daemon=True)
#         generate_thread.start()
#
#         # 启动播放流
#         try:
#             with sd.OutputStream(samplerate=sample_rate, channels=1, callback=audio_callback, dtype=dtype):
#                 while True:
#                     with audio_buffer_lock:
#                         if stop_event.is_set() and len(audio_buffer) == 0:
#                             break  # 缓冲区为空且生成完成，退出循环
#                     time.sleep(0.05)  # 避免忙等待
#         except sd.CallbackStop:
#             print("音频播放完成")
#
#         print(f'生成和播放完成')
#
#
# if __name__ == '__main__':
#     main()


import threading
import time
import numpy as np
import sounddevice as sd
from core.tts_factory import TTSClientFactory

sample_rate = 22050  # 音频采样率
dtype = np.float32  # 假设是 32 位 PCM 数据
audio_data = np.array([], dtype=dtype)  # 全局缓冲区，用于存储音频数据
lock = threading.Lock()  # 线程锁，保护对缓冲区的访问
stop_event = threading.Event()  # 用于控制播放线程的停止
stream = None  # 存储流对象


def play_audio():
    global audio_data, stream
    while not stop_event.is_set() or audio_data.size > 0:
        with lock:
            if audio_data.size > 0:
                if stream is None or not stream.active:
                    # 如果流未初始化或已停止，重新启动流
                    stream = sd.OutputStream(
                        samplerate=sample_rate,
                        channels=1,
                        dtype=dtype
                    )
                    stream.start()

                # 播放缓冲区中的音频
                data_to_play = audio_data.copy()  # 复制数据以避免数据竞争
                audio_data = np.array([], dtype=dtype)  # 清空缓冲区
                stream.write(data_to_play)  # 异步写入数据
            else:
                time.sleep(0.01)  # 等待新数据生成，避免忙等待


def generate_audio(cosyvoice, text):
    global audio_data
    for i in cosyvoice.model.inference_cross_lingual(text, cosyvoice.prompt_speech, stream=True):
        chunk = i['tts_speech'].numpy().astype(dtype).flatten()
        with lock:
            if audio_data.size == 0:
                audio_data = chunk  # 如果缓冲区为空，直接赋值
            else:
                audio_data = np.concatenate((audio_data, chunk))  # 否则追加数据
    stop_event.set()  # 生成完成，触发停止事件


def main():
    cosyvoice = TTSClientFactory.create("cosyvoice")

    # 模型预热
    print("开始模型预热")
    for i in cosyvoice.model.inference_cross_lingual(cosyvoice.prompt_text, cosyvoice.prompt_speech, stream=True):
        pass
    print("预热完成")

    while True:
        text = input(">>")
        if text.strip() == "":
            continue

        # 清空缓冲区并重置停止事件
        with lock:
            audio_data = np.array([], dtype=dtype)
        stop_event.clear()

        print("start generate")

        # 启动生成线程
        generate_thread = threading.Thread(target=generate_audio, args=(cosyvoice, text), daemon=True)
        generate_thread.start()

        # 启动播放线程
        play_thread = threading.Thread(target=play_audio, daemon=True)
        play_thread.start()

        # 等待生成线程完成
        generate_thread.join()

        # 等待播放线程结束
        play_thread.join()

        print(f'生成和播放完成')


if __name__ == '__main__':
    main()
