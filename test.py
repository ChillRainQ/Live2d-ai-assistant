import io
import time

import torch
import torchaudio

from core.tts_factory import TTSClientFactory
from utils import audio_player

if __name__ == '__main__':
    cosyvoice = TTSClientFactory.create("cosyvoice")
    text = '测试文本生成'
    speech = []
    now = time.time()
    for i in cosyvoice.model.inference_zero_shot(text, cosyvoice.prompt_text, cosyvoice.prompt_speech):
        speech.append(i['tts_speech'])
    print(f"Time: {time.time() - now}")
    audio_data = torch.concat(speech, dim=1)
    audio_bytes = io.BytesIO()
    torchaudio.save(audio_bytes, audio_data, 22050, format='wav')
    audio_bytes.seek(0)
    player = audio_player.AudioPlayer()
    player.play_audio(audio_bytes)