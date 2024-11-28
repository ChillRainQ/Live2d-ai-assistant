import asyncio
import io
import multiprocessing
import os
import subprocess
import time
import wave

import numpy as np
import sounddevice
from pydub import AudioSegment

from utils import audio_player

import multiprocess
import psutil
import requests
from core.abstract_tts_client import AbstractTTSClient

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
class CosyVoiceClient(AbstractTTSClient):
    def __init__(self, voice, cache_dir=None):
        self.type = 'cosyvoice'
        # multiprocessing.Process(target=self.run_bat).start()

    def run_bat(self):
        bat_path = os.path.join(CURRENT_DIR, os.path.join('CosyVoice-300M', 'run.bat'))
        # api = subprocess.Popen(
        #     [bat_path],  # 运行 .bat 文件
        #     shell=True,  # 使用 shell 执行命令
        #     cwd=os.path.dirname(bat_path),  # 设置工作目录为 .bat 文件所在目录
        #     stdout=subprocess.PIPE,  # 捕获标准输出
        #     stderr=subprocess.PIPE,  # 捕获标准错误
        #     creationflags=subprocess.CREATE_NEW_CONSOLE
        # )
        process = subprocess.run(
            [bat_path],
            shell=True,
            cwd=os.path.dirname(bat_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        print('cosyvoice api now running....')
    async def generate_audio(self, text: str):
        url = f'http://127.0.0.1:9881/cosyvoice/?text={text}'
        return io.BytesIO(requests.get(url).content)

    def close(self):
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr.port == 9881:
                try:
                    # 获取对应的进程
                    process = psutil.Process(conn.pid)
                    print(f"正在终止进程: PID={conn.pid}, 名称={process.name()}")
                    process.terminate()  # 发送终止信号
                    process.wait(timeout=3)  # 等待进程终止
                    print(f"进程 {conn.pid} 已成功终止")
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired) as e:
                    print(f"无法终止进程 {conn.pid}: {e}")
                return
        print(f"未找到监听端口 {9881} 的进程")



if __name__ == '__main__':
    tts = CosyVoiceClient("","")
    # time.sleep(10)
    response = asyncio.run(tts.generate_audio('现在测试一下声音生成'))
    audio_file = io.BytesIO(response.content)

    player = audio_player.AudioPlayer()
    player.play_audio(player.prepare_audio(audio_file))
    tts.close()

# import requests
# import io
# import numpy as np
# import sounddevice as sd
# from pydub import AudioSegment
#
# # 请求并获取 WAV 数据
# url = 'http://127.0.0.1:9881/cosyvoice/?text=测试'
# response = requests.get(url)
#
# # 检查响应是否成功
# if response.status_code == 200:
#     # 将响应数据转换为 BytesIO 对象
#     audio_data = io.BytesIO(response.content)
#
#     # 使用 pydub 加载 BytesIO 数据
#     audio_segment = AudioSegment.from_file(audio_data, format="wav")
#
#     # 将音频数据转换为 NumPy 数组
#     audio_array = np.array(audio_segment.get_array_of_samples())
#     sample_rate = audio_segment.frame_rate
#
#     # 使用 sounddevice 播放音频
#     sd.play(audio_array, sample_rate)
#     sd.wait()  # 等待播放完成
# else:
#     print("音频请求失败，状态码:", response.status_code)

