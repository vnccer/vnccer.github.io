<?php
function encrypt($plaintext, $key) {
    return bin2hex(openssl_encrypt($plaintext, 'aes-128-ecb', $key, OPENSSL_RAW_DATA));
}

$key = "ik ben een aardbei"; // 这是密钥
$new_payload = json_encode([
    "user" => "sweep",
    "ex" => 1823620672,
    "level" => "admin",
    "bio" => "hacked"
]);

$encrypted_token = encrypt($new_payload, $key);
echo "New Token: " . $encrypted_token . "\n";
?>