# GPT-SoVITS-Refactor
原项目：[GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS)
## 概述

GPT-SoVITS-Refactor是[GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS)的TTS功能重构。
解决了原项目的api可用性问题，可以整合入自己的项目或自行编写webAPI。

## 使用
```python
from cli.gptsovits_tts import GPTSovitsTTS
from resources.configs.config import TTS_CONFIG
tts = GPTSovitsTTS(config=TTS_CONFIG)
req = GPTSovitsTTS.TTS_Request()
req.text = "还有其他更快的么, 这个生成效果感觉最后也有概率会破音, 如何避免啊"
audio = tts.tts_handle(req)
```

### 依赖项
同GPT-SOVITS

    
