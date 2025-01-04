import io
import os

import torch
import soundfile as sf

from GPT_SoVITS_Refactor.TTS_infer_pack.TTS import TTS, TTS_Config
from pydantic import BaseModel
from GPT_SoVITS_Refactor.contant import language
from GPT_SoVITS_Refactor.cli.cli_util import pack_audio
from GPT_SoVITS_Refactor.resources.configs.config import TTS_CONFIG
from core.audio_device import AudioPlayer


class GPTSovitsTTS:
    class TTS_Request(BaseModel):
        text: str = None
        text_lang: str = None
        ref_audio_path: str = None
        aux_ref_audio_paths: list = None
        prompt_lang: str = None
        prompt_text: str = ""
        top_k: int = 5
        top_p: float = 1
        temperature: float = 1
        text_split_method: str = "cut5"
        batch_size: int = 1
        batch_threshold: float = 0.75
        split_bucket: bool = True
        speed_factor: float = 1.0
        fragment_interval: float = 0.3
        seed: int = -1
        media_type: str = "wav"
        streaming_mode: bool = False
        parallel_infer: bool = True
        repetition_penalty: float = 1.35

        def __init__(self, config,  **data):
            super().__init__(**data)
            self.text_lang = config.get("text_lang", "")
            self.ref_audio_path = config.get("ref_audio", "")
            self.prompt_text = config.get("ref_text", "")
            self.prompt_lang = config.get("ref_language", "")

    def __init__(self, config):
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tts = TTS(config)


    def check_params(self, req: dict):
        text: str = req.get("text", "")
        text_lang: str = req.get("text_lang", "")
        ref_audio_path: str = req.get("ref_audio_path", "")
        streaming_mode: bool = req.get("streaming_mode", False)
        media_type: str = req.get("media_type", "wav")
        prompt_lang: str = req.get("prompt_lang", "")
        version: str = req.get("version", "v2")
        text_split_method: str = req.get("text_split_method", "cut5")
        if ref_audio_path in [None, ""]:
            raise "ref_audio_path is required"
        if text in [None, ""]:
            raise "text is required"
        if (text_lang in [None, ""]):
            raise "text_lang is required"
        elif text_lang.lower() not in language.get(version):
            raise "text_lang is not supported"
        if (prompt_lang in [None, ""]):
            raise "prompt_lang is required"
        elif prompt_lang.lower() not in language.get(version):
            raise "prompt_lang is not supported"
        if media_type not in ["wav", "raw", "ogg", "aac"]:
            raise "media_type is not supported"
        elif media_type == "ogg" and not streaming_mode:
            raise "ogg format is not supported in non-streaming mode"
        return None

    def tts_handle(self, req: TTS_Request):
        """
        Text to speech handler.

        Args:
            req (dict):
                {
                    "text": "",                   # str.(required) text to be synthesized
                    "text_lang: "",               # str.(required) language of the text to be synthesized
                    "ref_audio_path": "",         # str.(required) reference audio path
                    "aux_ref_audio_paths": [],    # list.(optional) auxiliary reference audio paths for multi-speaker synthesis
                    "prompt_text": "",            # str.(optional) prompt text for the reference audio
                    "prompt_lang": "",            # str.(required) language of the prompt text for the reference audio
                    "top_k": 5,                   # int. top k sampling
                    "top_p": 1,                   # float. top p sampling
                    "temperature": 1,             # float. temperature for sampling
                    "text_split_method": "cut5",  # str. text split method, see text_segmentation_method.py for details.
                    "batch_size": 1,              # int. batch size for inference
                    "batch_threshold": 0.75,      # float. threshold for batch splitting.
                    "split_bucket: True,          # bool. whether to split the batch into multiple buckets.
                    "speed_factor":1.0,           # float. control the speed of the synthesized audio.
                    "fragment_interval":0.3,      # float. to control the interval of the audio fragment.
                    "seed": -1,                   # int. random seed for reproducibility.
                    "media_type": "wav",          # str. media type of the output audio, support "wav", "raw", "ogg", "aac".
                    "streaming_mode": False,      # bool. whether to return a streaming response.
                    "parallel_infer": True,       # bool.(optional) whether to use parallel inference.
                    "repetition_penalty": 1.35    # float.(optional) repetition penalty for T2S model.
                }
        returns:
            StreamingResponse: audio stream response.
        """
        req = req.__dict__
        streaming_mode = req.get("streaming_mode", False)
        media_type = req.get("media_type", "wav")
        check_res = self.check_params(req)
        if check_res is not None:
            return check_res
        if streaming_mode:
            req["return_fragment"] = True

        tts_generator = self.tts.run(req)

        if streaming_mode:
            pass
        else:
            sr, audio_data = next(tts_generator)
            sf.write("output.wav", audio_data, sr)
            audio_data = pack_audio(io.BytesIO(), audio_data, sr, media_type)
            return audio_data, sr


if __name__ == "__main__":
    tts = GPTSovitsTTS(config=TTS_CONFIG)
    req = GPTSovitsTTS.TTS_Request()
    req.text = "还有其他更快的么, 这个生成效果感觉最后也有概率会破音, 如何避免啊"
    audio, _ = tts.tts_handle(req)
    AudioPlayer().play_audio(audio)



