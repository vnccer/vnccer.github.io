---
title: "基于vmware的kali_linux下的docker部署(坑多)"
data: 2026-03-18
draft: false
weight: 1
---

# 一、让docker走clash代理（可选）
安装`https://clashclash.org/download.html`

设置好终端走clash，输入proxyoff关闭代理，proxyon开启代理
```BASH
nano ~/.zshrc

# 文件最底部增加如下内容：

# 1. 本地流量白名单（永久保留，防止误伤 Docker）
export no_proxy="localhost,127.0.0.1,0.0.0.0,172.16.0.0/12,192.168.0.0/16,10.0.0.0/8"
# 2. 代理一键开关（默认关闭，需要时才手动输入 proxyon）
alias proxyon='export http_proxy="http://127.0.0.1:7890"; export https_proxy="http://127.0.0.1:7890"; echo "Proxy ON"'
alias proxyoff='unset http_proxy; unset https_proxy; echo "Proxy OFF"'

# 执行命令使其生效
source ~/.zshrc
```

设置docker走代理（docker是后台服务，不读取`.bashrc`环境变量）
```bash
sudo mkdir -p /etc/systemd/system/docker.service.d

sudo nano /etc/systemd/system/docker.service.d/http-proxy.conf

# 写入如下内容
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:7890"
Environment="HTTPS_PROXY=http://127.0.0.1:7890"

sudo systemctl daemon-reload && sudo systemctl restart docker
```

# 二、阿里云镜像加速（可选）
```BASH
sudo vim /etc/docker/daemon.json

"registry-mirrors": ["https://cn1q7mu1.mirror.aliyuncs.com"]

sudo systemctl daemon-reload
sudo systemctl restart docker
```

registry-mirrors":["https://c05xby84.mirror.aliyuncs.com"]

# 二、docker与漏洞部署
```BASH
# 更新软件源列表
sudo apt update

# 安装 Docker
sudo apt install -y docker.io docker-compose

#安装docker-cli
sudo apt install docker-cli

#克隆vulhub
git clone https://github.com/vulhub/vulhub.git

cd vulhub/log4j/CVE-2021-44228/

# 启动 Docker 服务
sudo systemctl start docker

# (可选) 设置开机自启，省得以后每次都要手动启动
sudo systemctl enable docker

# 启动漏洞环境
sudo docker-compose up -d
```

# 三、问题解决
但是由于内存不够（`free -m`）检查，总共只有2g内容，solr是java编写的，jvm分配不到足够的内存，因此需要分配4g内存

同时安装haveged，解决随机数熵值低的问题，`sudo apt update && sudo apt install haveged -y && sudo systemctl start haveged`

同时去掉启动时候的`-d`，发现镜像内的java版本与当前内核不兼容，也会导致底层崩溃，因此修改`docer-compose.yml`中的`image: vulhub/solr:8.11.0`为`image: solr:8.11.0`
