---
title: "anaconda环境配置"
data: 2026-03-07
draft: false
weight: 1
---

# 一、环境配置
## 1.1 创建新项目
先把\anaconda3、\anaconda3\Library\bin、\anaconda3\Scripts添加到PATH中
```powershell
conda create -n project_name python=3.11
conda env list #检查虚拟环境
conda init #将conda的功能注入终端中
conda activate project_name
```

## 1.2 常用库记录
- 安装举例：
pip/conda install 库名
pip install -U scikit-learn -i https://pypi.tuna.tsinghua.edu.cn/simple #从清华镜像源，下载并安装最新版本的 scikit-learn，如果我已经有旧版本了，请帮我升级，-U 全称--upgrade，-i 全称--index-url（实际这里安装不需要-i或-U）
- 卸载举例：
pip/conda uninstall 库名

1. scikit-learn机器学习库
2. prettytable能在终端中打印出整齐的文本表格


## 1.3 删除环境
```
conda env list
conda uninstall -n 环境名 --all
```