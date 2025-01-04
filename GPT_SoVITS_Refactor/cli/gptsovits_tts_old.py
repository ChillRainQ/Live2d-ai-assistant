# import json
# import os
# import re
# import time
# import traceback
#
# import LangSegment
# import librosa
# import numpy as np
# import torch
# import soundfile as sf
# from transformers import AutoModelForMaskedLM, AutoTokenizer
# import resources.pretrained_models.resources as resources
# import tools.str_util as str_util
# import cli_util
# from AR.models.t2s_lightning_module import Text2SemanticLightningModule
# from cli.dict_to_AttrRecursive import DictToAttrRecursive
# from contant import i18n, version, splits
# from feature_extractor import cnhubert
# from module.mel_processing import spectrogram_torch
# from module.models import SynthesizerTrn
# from request import CliRequest
# from text import chinese
# from tools.my_utils import load_audio
#
#
# class GPTSovits:
#     """
#     gpt sovits客户端
#     """
#     config: dict
#
#     def __init__(self, config):
#         if config is None:
#             config = {}
#         self.config = config
#         self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#         self.is_half = True and torch.cuda.is_available()
#         self.tokenizer = AutoTokenizer.from_pretrained(resources.BERT_PATH)
#         self.bert_model = AutoModelForMaskedLM.from_pretrained(resources.BERT_PATH)
#         self.ssl_model = cnhubert.CNHubert(resources.CNHUBERT_PATH)
#         self.vq_model, self.hps = self.change_sovits_weights(resources.SOVITS_LIST[1])  # 报错
#         self.t2s_model, self.max_sec = self.change_gpt_weights(resources.GPT_LIST[1])
#         self.cache = {}
#         self.dtype = torch.float16 if self.is_half else torch.float32
#         self.hz = 50
#         self.init()
#
#     def init(self):
#         """
#         初始化
#         """
#         if self.is_half:
#             self.bert_model = self.bert_model.half().to(self.device)
#             self.ssl_model = self.ssl_model.half().to(self.device)
#             self.vq_model = self.vq_model.half().to(self.device)
#             self.t2s_model = self.t2s_model.half().to(self.device)
#         else:
#             self.bert_model = self.bert_model.to(self.device)
#             self.ssl_model = self.ssl_model.to(self.device)
#             self.vq_model = self.vq_model.to(self.device)
#             self.t2s_model = self.t2s_model.to(self.device)
#         self.vq_model.eval()
#         self.ssl_model.eval()
#         self.vq_model.eval()
#         self.t2s_model.eval()
#
#     def generate_audio(self, request: CliRequest):
#         request.params_check_and_init()
#         t = []
#         zero_wav = np.zeros(
#             int(self.hps.data.sampling_rate * 0.3),
#             dtype=np.float16 if self.is_half else np.float32,
#         )
#         t0 = time.time()
#         if not request.ref_free:
#             with torch.no_grad():
#                 wav16k, sr = librosa.load(request.ref_wav, sr=16000)
#                 if wav16k.shape[0] > 160000 or wav16k.shape[0] < 48000:
#                     raise OSError(i18n("参考音频在3~10秒范围外，请更换！"))
#                 wav16k = torch.from_numpy(wav16k)
#                 zero_wav_torch = torch.from_numpy(zero_wav)
#                 if self.is_half:
#                     wav16k = wav16k.half().to(self.device)
#                     zero_wav_torch = zero_wav_torch.half().to(self.device)
#                 else:
#                     wav16k = wav16k.to(self.device)
#                     zero_wav_torch = zero_wav_torch.to(self.device)
#                 wav16k = torch.cat([wav16k, zero_wav_torch])
#                 ssl_content = self.ssl_model.model(wav16k.unsqueeze(0))[
#                     "last_hidden_state"
#                 ].transpose(
#                     1, 2
#                 )  # .float()
#                 codes = self.vq_model.extract_latent(ssl_content)
#                 prompt_semantic = codes[0, 0]
#                 prompt = prompt_semantic.unsqueeze(0).to(self.device)
#         t1 = time.time()
#         t.append(t1 - t0)
#         text = str_util.cut(request.text, request.how_to_cut)
#         print(i18n("实际输入的目标文本(切句后):"), text)
#         texts = text.split("\n")
#         texts = str_util.process_text(texts)
#         texts = str_util.merge_short_text_in_array(texts, 5)
#         audio_opt = []
#         if not request.ref_free:
#             phones1, bert1, norm_text1 = self.get_phones_and_bert(request.ref_text, request.ref_language, version, self.device, self.is_half)
#
#         for i_text, text in enumerate(texts):
#             # 解决输入目标文本的空行导致报错的问题
#             if len(text.strip()) == 0:
#                 continue
#             if text[-1] not in splits: text += "。" if request.text_language != "en" else "."
#             print(i18n("实际输入的目标文本(每句):"), text)
#             phones2, bert2, norm_text2 = self.get_phones_and_bert(text, request.text_language, version, self.device, self.is_half)
#             print(i18n("前端处理后的文本(每句):"), norm_text2)
#             if not request.ref_free:
#                 bert = torch.cat([bert1, bert2], 1)
#                 all_phoneme_ids = torch.LongTensor(phones1 + phones2).to(self.device).unsqueeze(0)
#             else:
#                 bert = bert2
#                 all_phoneme_ids = torch.LongTensor(phones2).to(self.device).unsqueeze(0)
#
#             bert = bert.to(self.device).unsqueeze(0)
#             all_phoneme_len = torch.tensor([all_phoneme_ids.shape[-1]]).to(self.device)
#
#             t2 = time.time()
#             # cache_key="%s-%s-%s-%s-%s-%s-%s-%s"%(ref_wav_path,prompt_text,prompt_language,text,text_language,top_k,top_p,temperature)
#             # print(cache.keys(),if_freeze)
#             if i_text in self.cache and request.if_freeze:
#                 pred_semantic = self.cache[i_text]
#             else:
#                 with torch.no_grad():
#                     pred_semantic, idx = self.t2s_model.model.infer_panel(
#                         all_phoneme_ids,
#                         all_phoneme_len,
#                         None if request.ref_free else prompt,
#                         bert,
#                         # prompt_phone_len=ph_offset,
#                         top_k=request.top_k,
#                         top_p=request.top_p,
#                         temperature=request.temperature,
#                         early_stop_num=self.hz * self.max_sec,
#                     )
#                     pred_semantic = pred_semantic[:, -idx:].unsqueeze(0)
#                     self.cache[i_text] = pred_semantic
#             t3 = time.time()
#             refers = []
#             if request.inp_refs:
#                 for path in request.inp_refs:
#                     try:
#                         refer = self.get_spepc(self.hps, path.name).to(self.dtype).to(self.device)
#                         refers.append(refer)
#                     except:
#                         traceback.print_exc()
#             if (len(refers) == 0): refers = [self.get_spepc(self.hps, request.ref_wav).to(self.dtype).to(self.device)]
#             audio = (self.vq_model.decode(pred_semantic, torch.LongTensor(phones2).to(self.device).unsqueeze(0), refers,
#                                           speed=request.speed).detach().cpu().numpy()[0, 0])
#             max_audio = np.abs(audio).max()  # 简单防止16bit爆音
#             if max_audio > 1: audio /= max_audio
#             audio_opt.append(audio)
#             audio_opt.append(zero_wav)
#             t4 = time.time()
#             t.extend([t2 - t1, t3 - t2, t4 - t3])
#             t1 = time.time()
#         print("%.3f\t%.3f\t%.3f\t%.3f" %
#               (t[0], sum(t[1::3]), sum(t[2::3]), sum(t[3::3]))
#               )
#         return self.hps.data.sampling_rate, (np.concatenate(audio_opt, 0) * 32768).astype(
#             np.int16
#         )
#
#     def get_spepc(self, hps, filename):
#         audio = load_audio(filename, int(hps.data.sampling_rate))
#         audio = torch.FloatTensor(audio)
#         maxx = audio.abs().max()
#         if maxx > 1: audio /= min(2, maxx)
#         audio_norm = audio
#         audio_norm = audio_norm.unsqueeze(0)
#         spec = spectrogram_torch(
#             audio_norm,
#             hps.data.filter_length,
#             hps.data.sampling_rate,
#             hps.data.hop_length,
#             hps.data.win_length,
#             center=False,
#         )
#         return spec
#
#     def generate_audio_stream(self):
#         pass
#
#     def language_check(self):
#         pass
#
#     def get_bert_feature(self, text, word2ph):
#         with torch.no_grad():
#             inputs = self.tokenizer(text, return_tensors="pt")
#             for i in inputs:
#                 inputs[i] = inputs[i].to(self.device)
#             res = self.bert_model(**inputs, output_hidden_states=True)
#             res = torch.cat(res["hidden_states"][-3:-2], -1)[0].cpu()[1:-1]
#         assert len(word2ph) == len(text)
#         phone_level_feature = []
#         for i in range(len(word2ph)):
#             repeat_feature = res[i].repeat(word2ph[i], 1)
#             phone_level_feature.append(repeat_feature)
#         phone_level_feature = torch.cat(phone_level_feature, dim=0)
#         return phone_level_feature.T
#
#     def change_sovits_weights(self, sovits_path):
#         dict_s2 = torch.load(sovits_path, map_location="cpu")
#         hps = dict_s2["config"]
#         hps = DictToAttrRecursive(hps)
#         hps.model.semantic_frame_rate = "25hz"
#         if dict_s2['weight']['enc_p.text_embedding.weight'].shape[0] == 322:
#             hps.model.version = "v1"
#         else:
#             hps.model.version = "v2"
#         vq_model = SynthesizerTrn(
#             hps.data.filter_length // 2 + 1,
#             hps.train.segment_size // hps.data.hop_length,
#             n_speakers=hps.data.n_speakers,
#             **hps.model
#         )
#         if "pretrained" not in sovits_path:
#             del vq_model.enc_q
#         return vq_model, hps
#
#     def change_gpt_weights(self, gpt_path):
#         dict_s1 = torch.load(gpt_path, map_location="cpu")
#         config = dict_s1["config"]
#         max_sec = config["data"]["max_sec"]
#         t2s_model = Text2SemanticLightningModule(config, "****", is_train=False)
#         t2s_model.load_state_dict(dict_s1["weight"])
#         total = sum([param.nelement() for param in t2s_model.parameters()])
#         print("Number of parameter: %.2fM" % (total / 1e6))
#         # with open("./weight.json") as f:
#         #     data = f.read()
#         #     data = json.loads(data)
#         #     data["GPT"][version] = gpt_path
#         # with open("./weight.json", "w") as f: f.write(json.dumps(data))
#         return t2s_model, max_sec
#
#     def get_phones_and_bert(self, text, language, version, device, is_half, final=False):#
#         # 可能存在问题
#
#         if language in {"en", "all_zh", "all_ja", "all_ko", "all_yue"}:
#             language = language.replace("all_", "")
#             if language == "en":
#                 LangSegment.setfilters(["en"])
#                 formattext = " ".join(tmp["text"] for tmp in LangSegment.getTexts(text))
#             else:
#                 # 因无法区别中日韩文汉字,以用户输入为准
#                 formattext = text
#             while "  " in formattext:
#                 formattext = formattext.replace("  ", " ")
#             if language == "zh":
#                 if re.search(r'[A-Za-z]', formattext):
#                     formattext = re.sub(r'[a-z]', lambda x: x.group(0).upper(), formattext)
#                     formattext = chinese.mix_text_normalize(formattext)
#                     return self.get_phones_and_bert(formattext, "zh", version)
#                 else:
#                     phones, word2ph, norm_text = cli_util.clean_text_inf(formattext, language, version)
#                     bert = self.get_bert_feature(norm_text, word2ph).to(device)
#             elif language == "yue" and re.search(r'[A-Za-z]', formattext):
#                 formattext = re.sub(r'[a-z]', lambda x: x.group(0).upper(), formattext)
#                 formattext = chinese.mix_text_normalize(formattext)
#                 return self.get_phones_and_bert(formattext, "yue", version)
#             else:
#                 phones, word2ph, norm_text = cli_util.clean_text_inf(formattext, language, version)
#                 bert = torch.zeros(
#                     (1024, len(phones)),
#                     dtype=torch.float16 if is_half == True else torch.float32,
#                 ).to(device)
#         elif language in {"zh", "ja", "ko", "yue", "auto", "auto_yue"}:
#             textlist = []
#             langlist = []
#             LangSegment.setfilters(["zh", "ja", "en", "ko"])
#             if language == "auto":
#                 for tmp in LangSegment.getTexts(text):
#                     langlist.append(tmp["lang"])
#                     textlist.append(tmp["text"])
#             elif language == "auto_yue":
#                 for tmp in LangSegment.getTexts(text):
#                     if tmp["lang"] == "zh":
#                         tmp["lang"] = "yue"
#                     langlist.append(tmp["lang"])
#                     textlist.append(tmp["text"])
#             else:
#                 for tmp in LangSegment.getTexts(text):
#                     if tmp["lang"] == "en":
#                         langlist.append(tmp["lang"])
#                     else:
#                         # 因无法区别中日韩文汉字,以用户输入为准
#                         langlist.append(language)
#                     textlist.append(tmp["text"])
#             print(textlist)
#             print(langlist)
#             phones_list = []
#             bert_list = []
#             norm_text_list = []
#             for i in range(len(textlist)):
#                 lang = langlist[i]
#                 phones, word2ph, norm_text = cli_util.clean_text_inf(textlist[i], lang, version)
#                 bert = self.get_bert_inf(phones, word2ph, norm_text, lang, self.is_half, self.device)
#                 phones_list.append(phones)
#                 norm_text_list.append(norm_text)
#                 bert_list.append(bert)
#             bert = torch.cat(bert_list, dim=1)
#             phones = sum(phones_list, [])
#             norm_text = ''.join(norm_text_list)
#         if not final and len(phones) < 6:
#             return self.get_phones_and_bert("." + text, language, version, final=True)
#         return phones, bert.to(self.dtype), norm_text
#
#     def get_bert_inf(self, phones, word2ph, norm_text, language, is_half, device):
#         language = language.replace("all_", "")
#         if language == "zh":
#             bert = self.get_bert_feature(norm_text, word2ph).to(device)  # .to(dtype)
#         else:
#             bert = torch.zeros(
#                 (1024, len(phones)),
#                 dtype=torch.float16 if is_half == True else torch.float32,
#             ).to(device)
#
#         return bert
#
#
# if __name__ == "__main__":
#     gptsovits = GPTSovits(None)
#     req = CliRequest("还有其他更快的么, 这个生成效果感觉最后也有概率会破音, 如何避免啊", "zh", ref_wav="D:\PythonCode\GPT-SoVITS-Refactor\cli\murasame.wav",
#                      ref_text="さいごのさいごで、まだごしゅじんにおおきいな降ったんおかけてしまったな", ref_language="all_ja")
#     audio = gptsovits.generate_audio(req)
#     last_sampling_rate, last_audio_data = audio
#     output_wav_path = os.path.join("", "output.wav")
#     sf.write("output.wav", last_audio_data, last_sampling_rate)
