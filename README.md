# chinese-llama2.c
支持中文的 llama2.c


## 简介

[llama2.c](https://github.com/karpathy/llama2.c) 项目提供了大语言模型从训练到部署的完整的技术栈，使得个人可以体验大语言模型的训练和推理。

作为一个学习项目，本项目把场景拓展到中文，训练中文版的 tinyllamas。

训练数据是将英文版的 [TinyStories](https://huggingface.co/datasets/roneneldan/TinyStories) (500万样本) 翻译成中文 [TinyStoriesChinese](https://huggingface.co/datasets/adam89/TinyStoriesChinese) (翻译了约400万)，获得约 1G 字符的训练数据。在此基础上训练得到能够流畅生成中文小故事的语言模型，欢迎大家试玩！


## 试玩
```bash
wget https://huggingface.co/adam89/tinyllamas-chinese/resolve/main/stories15M.bin
make run
./run stories15M.bin -z tok5000.bin
```

```text
从前，有一个小女孩叫莉莉。她喜欢在外面玩，探索她家后面的树林。有一天，她在地上发现了一个闪闪发光的钉子。她捡起来给妈妈看。
"看，妈妈！我找到一个钉子！" 莉莉兴奋地喊道。
"那是一个漂亮的钉子，莉莉。小心别掉下来。" 妈妈说。
莉莉看了看它，然后说："我想把它放在我的小盒子里。我想把它保管好，让我的朋友们知道它很重要。"
"那是一个很好的主意，莉莉。谢谢你这么好的帮手。" 妈妈说。
莉莉笑了笑，然后继续拿着钉子和盒子玩，准备好好地睡一晚。
```

也可增加 prompt，让模型做故事续写：

```
./run stories15M.bin -z tok5000.bin -i '从前，有一只会飞的狗叫波波'
```

```text
从前，有一只会飞的狗叫波波。波波喜欢观察天空中的星星。他在星星下仰望星空，看到它们闪烁并发出响亮的噪音。

有一天，波波看到了一个名叫苏的小女孩。苏正在画一棵大树。波波也想画这棵树。苏笑了笑，说：“波波，我可以和你一起画吗？”波波摇了摇尾巴，飞到了苏的手上。

苏和波波一起画树。他们用彩色的颜料给树涂上了色彩。他们对自己的画非常满意。苏看着画说：“哇，波波！你真棒！”波波为他的朋友感到骄傲，他们一起欣赏了这棵树。
```

如果想获得更好的效果，可以尝试更大的 110M 模型：
```
./run stories110M.bin -z tok5000.bin -t 0 -i '从前，有一只会飞的狗叫波波'
```

```
从前，有一只会飞的狗叫波波。波波喜欢在天空中飞翔。有一天，他看到了一只名叫奇普的小鸟。奇普很伤心，因为她不能像波波一样飞得高。

波波说：“奇普，我可以帮助你飞得高高的。我们可以一起飞！”奇普很高兴地说：“好的，请帮帮我，波波！” 他们开始一起飞行，奇普非常努力地尝试着飞得更高。

但是奇普不够强壮，她无法像波波一样飞得高。奇普摔倒了，受伤了。波波为他的新朋友感到难过。他们都明白，有时候，即使你尽力去做，事情也不总是如你所愿。
``` 
还是蛮有哲理的😂

## 模型
仿照 [llama2.c](https://github.com/karpathy/llama2.c) 原项目，这里也训练了三个规模的中文模型，托管在huggingface hub [tinyllamas-chinese](https://huggingface.co/adam89/tinyllamas-chinese)。
| model | dim | n_layers | n_heads | n_kv_heads | max context length | parameters | val loss | download
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15M | 288 | 6 | 6 | 6 | 256 | 15M | 1.0868 | [stories15M.bin](https://huggingface.co/adam89/tinyllamas-chinese/resolve/main/stories15M.bin) |
| 42M| 512 | 8 | 8 | 8 | 1024 | 42M | 0.8907 | [stories42M.bin](https://huggingface.co/adam89/tinyllamas-chinese/resolve/main/stories42M.bin) |
| 110M| 768 | 12 | 12 | 12 | 1024 | 110M | 0.8205 | [stories110M.bin](https://huggingface.co/adam89/tinyllamas-chinese/resolve/main/stories110M.bin) |

## 自己从头训练

### 训练 tokenizer

使用tinystories数据集：
```bash
python3 tinystories.py download
python3 tinystories.py train_vocab --vocab_size=5000
python3 tinystories.py pretokenize --vocab_size=5000
```

自定义的数据集：
```bash
python3 tinystories.py pretokenize --vocab_size=5000 --data_dir folder_for_jsonl_files
```

将 tokenizer 导出为`.bin`格式：
```bash
python3 tokenizer.py --tokenizer-model=data/tok5000.model
```



### 训练模型

```bash
# 15M模型
torchrun --standalone --nproc_per_node=4 train.py --vocab_source=custom --vocab_size=5000 --batch_size=128 --n_layers=6 --n_heads=6 --n_kv_heads=6 --max_seq_len=256 --gradient_accumulation_steps=4 --max_iters=100000

# 42M模型
torchrun --standalone --nproc_per_node=4 train.py --vocab_source=custom --vocab_size=5000 --batch_size=128 --dim=512 --n_layers=8 --n_heads=8 --n_kv_heads=8 --max_seq_len=1024 --gradient_accumulation_steps=4 --max_iters=20000

# 110M模型
torchrun --standalone --nproc_per_node=4 train.py --vocab_source=custom --vocab_size=5000 --batch_size=128 --dim=768 --n_layers=12 --n_heads=12 --n_kv_heads=12 --max_seq_len=1024 --gradient_accumulation_steps=4 --max_iters=20000
```

训练详情
| 模型 | 显存占用|  epochs | tokens_per_iter | max_iters | num_tokens | 训练时长 |
| - | - | - | - | - | - | - |
| 15M | 6.5G | 13 | 131,072 | 100,000 | 1G | ~1h |
| 42M | 30.5G |  10.5 | 524,288 | 20,000 | 1G | ~1.5h |
| 110M | 53.5G | 10.5 | 524,288 | 20,000 | 1G | ~3.4h |

### 把训练的模型导出到HuggingFace

```bash
python3 export.py ./hf_export/my_model --version -1 --dtype fp16 --checkpoint ./out/ckpt.pt
python3 export_tokenizer.py ./hf_export/my_model -m ./data/tok5000.model
```

注意：使用TinyStories.py生成的数据集训练出来的模型可能会在写完一个故事之后输出乱码。这是因为训练数据中只有bos token没有eos token的缘故。