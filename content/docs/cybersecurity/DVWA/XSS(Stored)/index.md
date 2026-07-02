---
title: XSS(Stored)
data: 2026-07-02
draft: false
weight: 13
---

# 一、Low
## 1.1 源码
```php
<?php

if( isset( $_POST[ 'btnSign' ] ) ) {
    // Get input
    $message = trim( $_POST[ 'mtxMessage' ] );
    $name    = trim( $_POST[ 'txtName' ] );

    // Sanitize message input
    $message = stripslashes( $message );
    $message = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $message ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));

    // Sanitize name input
    $name = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $name ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));

    // Update database
    $query  = "INSERT INTO guestbook ( comment, name ) VALUES ( '$message', '$name' );";
    $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

    //mysql_close();
}

?>
```
- 黑名单思维
- `isset()`检查变量是否设置且非NULL，`isset( $_POST[ 'btnSign' ] )`检查用户是否点击提交按钮
- `trim()`删除字符串的头尾空白符：空格、制表符`\t`、换行符`\n`等
- `stripslashes()`删除一次反斜杠：`\'`变成`'`，`\\`变成`\`
-   `is_object`检查变量是否是一个对象
-   `mysqli_real_escape_string()`转义sql语句中使用字符串的特殊字符，会对以下字符添加反斜杠：`\0`、`\n`、`\r`、`\`、`'`、`"`和`ctrl+z`
-   `$message = ((isset($GLOBALS["___mysqli_ston"]) && ...) ? mysqli_real_escape_string(...) : ...);`三元运算符（条件?结果A:结果B）,检测到当前存在有效的数据库连接对象，就调用转义函数，对输入转义
-   `mysqli_query()`和`die()`，把拼接好的sql语句发送到mysql数据库执行，如果前面执行失败触发`die()`，通过`mysqli_error()`把错误打印出来。（`die(mysqli_error())`打印数据库报错很危险）

## 1.2 攻击
```php
name：1
message：<script>alert("xss")</script>
```


# 二、Medium
## 2.1 源码
```PHP
<?php

if( isset( $_POST[ 'btnSign' ] ) ) {
    // Get input
    $message = trim( $_POST[ 'mtxMessage' ] );
    $name    = trim( $_POST[ 'txtName' ] );

    // Sanitize message input
    $message = strip_tags( addslashes( $message ) );
    $message = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $message ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
    $message = htmlspecialchars( $message );

    // Sanitize name input
    $name = str_replace( '<script>', '', $name );
    $name = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $name ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));

    // Update database
    $query  = "INSERT INTO guestbook ( comment, name ) VALUES ( '$message', '$name' );";
    $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

    //mysql_close();
}

?>
```
- 黑名单思维：对name进行正则拦截，拦截`<script>`标签
- `strip_tags()`剥离HTML、XML和PHP标签，如输入`<script>alert(1)</script>`，输出`alert(1)`
- `addslashes()`在预定义的字符（单引号、双引号、反斜线、NULL）前面添加反斜杠进行转义，如输入`"hello"`输出`\"hello\“`
- `htmlspecialchars()`把预定义的字符转换为HTML实体，如`<`为`&lt;`，`>`为`&gt`，`"`为`&quot;`
- `str_replace()`直接将`<script>`标签替换掉，导致漏洞出现

## 2.2 攻击
抓包攻击name位置
```php
大小写绕过：
<Script>alert(1)</Script>
<SCRIPT>alert(1)</SCRIPT>

双写绕过：
<scr<script>ipt>alert(1)</script>

HTML标签：
<img src=1 onerror=alert(1)>
```

# 三、High
## 3.1 源码
```php

<?php

if( isset( $_POST[ 'btnSign' ] ) ) {
    // Get input
    $message = trim( $_POST[ 'mtxMessage' ] );
    $name    = trim( $_POST[ 'txtName' ] );

    // Sanitize message input
    $message = strip_tags( addslashes( $message ) );
    $message = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $message ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
    $message = htmlspecialchars( $message );

    // Sanitize name input
    $name = preg_replace( '/<(.*)s(.*)c(.*)r(.*)i(.*)p(.*)t/i', '', $name );
    $name = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $name ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));

    // Update database
    $query  = "INSERT INTO guestbook ( comment, name ) VALUES ( '$message', '$name' );";
    $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

    //mysql_close();
}

?>
```

- 黑名单思维
- 相比medium难度，message部分不变，依旧是先预定义的字符前面加反斜杠转义，再剥离HTML、XMP、PHP标签，再把预定义的字符转换为HTML实体。
- name部分，`preg_replace()`正则替换，`/.../`是正则的边界符，最后的`i`忽略大小写，`<(.*)s`表示`<`和`s`之间可以夹杂任何字符，因此拦截各种<script

## 3.2 攻击

```php
<img src=1 onerror=alert(1)>
```

# 四、Impossible
## 4.1 源码
```PHP
<?php

if( isset( $_POST[ 'btnSign' ] ) ) {
    // Check Anti-CSRF token
    checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );

    // Get input
    $message = trim( $_POST[ 'mtxMessage' ] );
    $name    = trim( $_POST[ 'txtName' ] );

    // Sanitize message input
    $message = stripslashes( $message );
    $message = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $message ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
    $message = htmlspecialchars( $message );

    // Sanitize name input
    $name = stripslashes( $name );
    $name = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $name ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
    $name = htmlspecialchars( $name );

    // Update database
    $data = $db->prepare( 'INSERT INTO guestbook ( comment, name ) VALUES ( :message, :name );' );
    $data->bindParam( ':message', $message, PDO::PARAM_STR );
    $data->bindParam( ':name', $name, PDO::PARAM_STR );
    $data->execute();
}

// Generate Anti-CSRF token
generateSessionToken();

?>
```
- name也使用`htmlspecialchars()`，将输入都变成HTML实体
- 引入PDO(PHP Data Objects)预处理，掐断SQL注入攻击