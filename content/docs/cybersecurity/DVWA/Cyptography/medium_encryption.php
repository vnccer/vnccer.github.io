<?php
// 密文（示例：hex 编码的 token）
$hex_token = "5fec0b1c993f46c8bad8a5c8d9bb9698174d4b2659239bbc50646e14a70becef83f2d277d9e5fb9a951e74bee57c77a3c9acb1f268c06c5e760a9d728e081fab65e83b9f97e65cb7c7c4b8427bd44abc16daa00fd8cd0105c97449185be77ef5";

// 解密密钥
$key = "ik ben een aardbei";

// 将 HEX 编码的 token 转换为二进制
$encrypted_token = hex2bin($hex_token);

// 解密
$decrypted_json = openssl_decrypt($encrypted_token, 'aes-128-ecb', $key, OPENSSL_PKCS1_PADDING);

// 输出解密后的 JSON 字符串
echo "解密后的内容: \n" . $decrypted_json . "\n";

// 解析 JSON
$decoded_object = json_decode($decrypted_json, true);
print_r($decoded_object);
?>