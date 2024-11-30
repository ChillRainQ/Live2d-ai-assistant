# from cosyvoice.cli.cosyvoice import CosyVoice
# import torchaudio
#
# cosyvoice = CosyVoice('tts_clients/data/model/CosyVoice-300M',load_jit=True, load_onnx=False, fp16=True)
# # sft usage
# print(cosyvoice.list_avaliable_spks())
# # change stream=True for chunk stream inference
# for i, j in enumerate(cosyvoice.inference_sft('你好，我是通义生成式语音大模型，请问有什么可以帮您的吗？', '中文女', stream=False)):
#     torchaudio.save('sft_{}.wav'.format(i), j['tts_speech'], 22050)
import torchaudio
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from cosyvoice.cli.cosyvoice import CosyVoice
from cosyvoice.utils.file_utils import load_wav

app = FastAPI()
print("正在加载CosyVoice模型，请稍后...")
model = CosyVoice('tts_clients/data/model/CosyVoice-300M')
prompt_speech = load_wav('tts_clients/data/example.wav', 16000)
# with open('example参考音频文本.txt', 'r', encoding='utf-8') as file:
#     lines = file.readlines()
prompt_text = '看来还是受了点伤，咱也不问啦，走吧，送你回去，我就知道，不是我干的，一定是反物质军团的错。'
output_path = 'tts_clients/data/cache/cache.wav'


@app.get("/cosyvoice/")
def run_cosyvoice(text: str):
    results = model.inference_zero_shot(text, prompt_text, prompt_speech)
    tts_speech = results['tts_speech']
    torchaudio.save(output_path, tts_speech, 22050)
    return FileResponse(output_path)


print("本地CosyVoice语音合成大模型API服务器启动成功!")
uvicorn.run(app, host="0.0.0.0", port=9881)
