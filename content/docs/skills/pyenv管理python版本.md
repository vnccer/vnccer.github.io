---
title: "pyenv管理python版本"
data: 2026-04-28
draft: false
weight: 1
---

# 一、安装pyenv
https://github.com/pyenv/pyenv
## 1.1 环境配置
```ZSH
sudo apt update
curl -fsSL https://pyenv.run | bash
```
```ZSH
# 安装底层依赖库
sudo apt install -y libbz2-dev libreadline-dev libsqlite3-dev tk-dev

# 修改zsh
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init - zsh)"' >> ~/.zshrc

source ~/.zshrc

exec "$SHELL"
```

## 1.2 安装python3.10
```zsh
# clashon（开着代理）
pyenv install 3.10.14
cd ~/sec/attacker/MHDDoS
pyenv local 3.10.14
python -V
```

## 1.3 创建新venv
```ZSH
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 1.4 删除python
```ZSH
pyenv uninstall -f 3.10.14
```