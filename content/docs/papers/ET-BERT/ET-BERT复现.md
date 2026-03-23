---
title: "ET-BERT复现"
weight: 2
bookCollapseSection: true  #控制折叠
---

https://github.com/linwhitehat/ET-BERT
# 一、环境
```powershell
conda create -n BERT python=3.11
conda activate BERT
pip install -r requirements.txt
pip install numpy
pip install tqdm

# 先卸载可能存在的旧版或CPU版 torch
pip uninstall torch torchvision torchaudio -y

# 安装支持 CUDA 12.1 的版本（最适合 40 系显卡）
pip install torch --index-url https://download.pytorch.org/whl/cu121

# 验证显卡是否被激活
python -c "import torch; print(torch.cuda.is_available())"
```
  - 由于`requirements.txt`文件中的`torch>=1.0`太笼统，默认安装不带显卡驱动的通用版
修改`models/`中的`encryptd`为`encrypted`

windows
```
$env:PYTHONPATH = "."; python fine-tuning/run_classifier.py --pretrained_model_path models/pre-trained_model.bin --vocab_path models/encryptd_vocab.txt --train_path datasets/cstnet-tls1.3/packet/train_dataset.tsv --dev_path datasets/cstnet-tls1.3/packet/valid_dataset.tsv --test_path datasets/cstnet-tls1.3/packet/test_dataset.tsv --epochs_num 10 --batch_size 8 --embedding word_pos_seg --encoder transformer --mask fully_visible --seq_length 128 --learning_rate 2e-5
```

linux
```
# 1. 设置环境变量，让程序找到 uer 文件夹
export PYTHONPATH=$PYTHONPATH:.
# 2. 脚本
python3 fine-tuning/run_classifier.py --pretrained_model_path models/pre-trained_model.bin \
                                   --vocab_path models/encryptd_vocab.txt \
                                   --train_path datasets/cstnet-tls1.3/packet/train_dataset.tsv \
                                   --dev_path datasets/cstnet-tls1.3/packet/valid_dataset.tsv \
                                   --test_path datasets/cstnet-tls1.3/packet/test_dataset.tsv \
                                   --epochs_num 10 --batch_size 32 --embedding word_pos_seg \
                                   --encoder transformer --mask fully_visible \
                                   --seq_length 128 --learning_rate 2e-5
```