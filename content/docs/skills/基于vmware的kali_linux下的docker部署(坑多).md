---
title: "基于vmware的kali_linux下的docker部署(坑多)"
data: 2026-03-18
draft: false
weight: 1
---

# 一、让docker走clash代理（可选）
见[linux_clash部署](/docs/skills/linux_clash部署/)

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
