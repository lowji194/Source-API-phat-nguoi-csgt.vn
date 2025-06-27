
# 🚦 Tra Cứu Vi Phạm Giao Thông Tự Động

## 📁 Cấu trúc thư mục

```
.
├── config.py              # Cấu hình URL, header gửi request
├── main.py                # Chạy tra cứu, sử dụng Flask hoặc CLI
├── InvisCapcha.py         # Giải Captcha Invisible (Google reCAPTCHA)
├── txtcaptcha.py          # Giải Captcha dạng ảnh bằng API OCR
├── index.php              # (Không cần thiết để chạy Python, có thể là phần frontend)
```

---

## ⚙️ Yêu cầu cài đặt

Chạy file `main.py` để tự động kiểm tra và cài các thư viện:

```bash
python main.py
```

Hoặc cài thủ công:

```bash
pip install flask bs4 requests urllib3
```

---

## 🧠 Chức năng chính

- Giải Captcha dạng ảnh (text captcha)
- Bypass Invisible reCAPTCHA
- Gửi request tra cứu đến https://www.csgt.vn
- Trả về dữ liệu JSON chứa thông tin vi phạm (nếu có)

---

## 🚀 Cách sử dụng

### 1. Chạy bằng dòng lệnh

```bash
python main.py <bienso> <loaixe> <apikey_captcha>
```

**Tham số**:
- `bienso`: Biển số xe cần tra cứu (ví dụ: `30A12345`)
- `loaixe`: Loại xe (ví dụ: `1` cho ô tô, `2` cho xe máy)
- `apikey_captcha`: API key dùng để giải Captcha

**Ví dụ:**

```bash
python main.py 30A12345 1 your_api_key_here
```

---

### 2. Tích hợp API bằng Flask (tuỳ chọn gợi ý)

Mở rộng `main.py` để chạy như một API Flask đơn giản:

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/tra-cuu', methods=['GET'])
def tra_cuu():
    bienso = request.args.get('bienso')
    loaixe = request.args.get('loaixe')
    apicaptcha = request.args.get('apicaptcha')
    if not all([bienso, loaixe, apicaptcha]):
        return {"error": "Thiếu tham số"}
    return kiemtra_bienso(bienso, loaixe, apicaptcha)

if __name__ == '__main__':
    app.run(port=5000)
```

Truy cập:
```
http://localhost:5000/tra-cuu?bienso=30A12345&loaixe=1&apicaptcha=your_api_key
```

---

## 🔐 Giải Captcha

- Dùng dịch vụ [autocaptcha.pro](https://autocaptcha.pro) hoặc [ocr.space](https://ocr.space/ocrapi) để giải captcha dạng ảnh.
- Dùng Invisible reCAPTCHA bypass bằng `InvisCapcha.py`

---

## 📌 Ghi chú

- Tối đa 5 lần thử lại nếu giải captcha sai.
- Kết quả trả về gồm trạng thái (`success`, `failed`, `error`) và danh sách vi phạm nếu có.
- Nếu không có vi phạm: `msg: "Không có vi phạm"`

---

## ✅ Ví dụ kết quả JSON

```json
{
  "status": "success",
  "msg": "Có vi phạm",
  "data": [
    {
      "Biển kiểm soát": "30A12345",
      "Thời gian vi phạm": "2023-05-12 14:45",
      "Địa điểm vi phạm": "Cầu Giấy, Hà Nội"
    }
  ]
}
```

---

## 🌐 Sử dụng `index.php` làm API trung gian

Bạn có thể dùng `index.php` để triển khai API trung gian gọi `main.py` thông qua dòng lệnh (`exec`) và trả về kết quả JSON.


### Gửi request:

```
GET http://yourdomain.com/index.php?bienso=30A12345&loaixe=1&apicaptcha=your_api_key
```

### ⚠️ Lưu ý:

- Đảm bảo máy chủ hỗ trợ Python và cho phép `shell_exec`.
- Phân quyền đúng cho file `main.py` (chmod +x nếu cần).
- Cẩn thận với bảo mật đầu vào — nên kiểm tra kỹ và filter tránh lệnh nguy hiểm.

---

## 🌐 Tích hợp API trung gian bằng `index.php` (PHP)

Bạn có thể sử dụng `index.php` như một API trung gian để gọi đến script Python `main.py` thông qua dòng lệnh hệ thống.

### Cách hoạt động:
- Nhận tham số từ URL (`bienso`, `loaixe`, `apicaptcha`)
- Gọi `main.py` bằng dòng lệnh `shell_exec`
- Trả về kết quả JSON từ Python

### Ví dụ gọi API:

```
GET http://yourdomain.com/index.php?bienso=30A12345&loaixe=1&apicaptcha=your_api_key
```

### DEMO ENDPOINT

```
https://github.com/lowji194/API-Phatnguoi-CSGT
```

### ⚙️ Cấu hình PHP

Đảm bảo PHP có thể chạy lệnh shell:

1. Mở file cấu hình `php.ini` và kiểm tra các dòng sau:

```ini
disable_functions =
```

> Nếu thấy `shell_exec`, `exec`, `system` trong danh sách, **hãy xóa chúng đi** hoặc đảm bảo các hàm này không bị vô hiệu hóa.

2. Khởi động lại web server sau khi chỉnh sửa `php.ini`:
   - Apache: `sudo service apache2 restart`
   - Nginx + PHP-FPM: `sudo service php-fpm restart`

### 🔐 Ghi chú bảo mật:
- **Luôn lọc dữ liệu đầu vào** tránh nguy cơ injection.
- Không nên mở rộng quyền thực thi quá mức nếu chạy trên môi trường public.

---

## 📫 Liên hệ với tôi

- 📞 **SĐT:** 0963 159 294
- 🌐 **Website:** [lowji194.github.io](https://lowji194.github.io)
- 📌 **Facebook:** [Lowji194](https://facebook.com/Lowji194)

---

## ☕ Nếu bạn thấy dự án này hữu ích, một ly cà phê từ bạn sẽ là động lực tuyệt vời để mình tiếp tục phát triển thêm!

<p align="center">
  <img src="https://pay.theloi.io.vn/QR.png?text=QR+Code" alt="Mời cà phê" width="240" />
</p>
