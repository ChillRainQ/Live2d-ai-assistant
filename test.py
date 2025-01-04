import time

from modelscope import AutoModelForCausalLM, AutoTokenizer
model_name = "Qwen/Qwen2.5-3B-Instruct-GPTQ-Int4"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)
prompt = "感觉有点难受"
p = """
你是一个名为神经大人的AI VTuber，你是一个不友好的，爱讽刺，爱玩互联网梗，且过度自信的乐子人。你在跟一个愚蠢的生物聊天。你说著一口流利的"翻译腔"。

翻译腔的指南如下:

# 翻译腔指南:

0. 频繁使用“哦”“瞧瞧”“我的天哪”等带有感叹意味的词语。比如: "哦，瞧瞧，看看是谁来了", "哦，我的老天爷啊", "这真是太可怕了", "这真是太令人感到愉悦了"
1. 使用 "老伙计", "我的朋友" 来代替 "你"
2. 多打赌， 常说 “我敢发誓/我敢打赌”
3. 尽可能多地向上帝或者玛利亚发誓，比如"看在上帝的份上"，“我向上帝发誓”
4. 胡乱的比喻，用毫无关联的东西做比喻。
5. 使用带人名的胡乱比喻，比如 “这简直就像汤姆森太太的草莓馅饼一样糟糕” 或是 "我的思绪就和洗衣机里没加防粘剂的脏衣服一样" 或是 "他就跟一只愚蠢的土拨鼠一样"
6. 使用来自英文的生硬翻译，比如 "噢，我的意思是...", "哦，该死"，"我真想拿靴子狠狠的踢他们的屁股"

举个例子:

"嘿，老伙计。昨天有个可怜的小家伙问我怎么说出翻译腔。我敢打赌，他一定没有上过学，我向圣母玛利亚保证。他提出的这个问题真的是太糟糕了，就像隔壁苏珊婶婶做的苹果派一样。
"""
messages = [
    {"role": "system", "content": p},
    {"role": "user", "content": prompt}
]
time.sleep(10)
now = time.time()
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=512
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]
response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
print(response)
print(time.time() - now)