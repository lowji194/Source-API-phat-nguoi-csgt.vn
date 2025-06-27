<?php
// Lấy tham số từ URL (GET)
$bienso = isset($_GET['bienso']) ? $_GET['bienso'] : '';
$loaixe = isset($_GET['loaixe']) ? $_GET['loaixe'] : '';
$apicaptcha = isset($_GET['captcha']) ? $_GET['captcha'] : '';

// Kiểm tra tham số
if (empty($bienso) || empty($loaixe) || empty($apicaptcha)) {
    echo "[-] Tham số không hợp lệ!";
    exit;
}

// Gọi tệp Python và truyền tham số
$command = "/usr/bin/python3 main.py " . escapeshellarg($bienso) . " " . escapeshellarg($loaixe) . " " . escapeshellarg($apicaptcha) . " 2>&1";
$output = shell_exec($command);

// Kiểm tra và hiển thị lỗi
if ($output === null) {
    echo "[-] Lỗi khi thực thi tệp Python!";
} else {
    echo "<pre>$output</pre>";
}
?>
