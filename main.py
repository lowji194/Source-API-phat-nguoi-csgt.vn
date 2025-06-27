import sys
import subprocess

def install_library(library_name):
    try:
        __import__(library_name)
        print(f"{library_name} đã được cài đặt.")
    except ImportError:
        print(f"{library_name} chưa được cài đặt. Đang cài đặt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", library_name])
        print(f"{library_name} đã được cài đặt thành công.")

# Kiểm tra và cài đặt các thư viện
install_library("flask")
install_library("bs4")
install_library("requests")  # Thêm nếu cần
install_library("urllib3")   # Thêm nếu cần

""" File liên quan """
from txtcaptcha import bypass_text_captcha
from InvisCapcha import bypass_captcha
from config import *

""" Thư viện """
from urllib3 import disable_warnings
from requests import session
import json
from flask import Flask, jsonify
from bs4 import BeautifulSoup
import base64

disable_warnings()

def extract_violations_from_html(html_content,url_csgt):
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        violations = []

        # Kiểm tra xem có phần tử chứa thông tin vi phạm không
        body_print = soup.find("div", id="bodyPrint123")
        if not body_print:
            return {"status": "failed", "data": None}

        # Tách các vi phạm dựa trên thẻ <hr>
        sections = body_print.find_all(recursive=False)

        current_violation = None
        for element in sections:
            if "form-group" in element.get("class", []):
                if current_violation is None:
                    current_violation = {
                        "Biển kiểm soát": "",
                        "Màu biển": "",
                        "Loại phương tiện": "",
                        "Thời gian vi phạm": "",
                        "Địa điểm vi phạm": "",
                        "Hành vi vi phạm": "",
                        "Trạng thái": "",
                        "Đơn vị phát hiện vi phạm": "",
                        "Nơi giải quyết vụ việc": []  # Đảm bảo đây là một danh sách
                    }

                # Xử lý thông tin chính (label-value)
                label = element.find("label", class_="control-label")
                value = element.find("div", class_="col-md-9")
                if label and value:
                    key = label.get_text(strip=True).replace(":", "")
                    val = value.get_text(strip=True)
                    if key in current_violation:
                        # Đảm bảo không ghi đè "Nơi giải quyết vụ việc" bằng giá trị khác
                        if key != "Nơi giải quyết vụ việc":
                            current_violation[key] = val

                # Xử lý thông tin "Nơi giải quyết vụ việc"
                if "Nơi giải quyết vụ việc" in element.get_text():
                    continue  # Bỏ qua dòng label "Nơi giải quyết vụ việc"

                # Lấy thông tin bổ sung (Đội, Địa chỉ, Số điện thoại)
                text = element.get_text(strip=True)
                if text and ("Đội" in text or "Địa chỉ" in text or "Số điện thoại" in text):
                    # Đảm bảo "Nơi giải quyết vụ việc" là một danh sách trước khi append
                    if isinstance(current_violation["Nơi giải quyết vụ việc"], list):
                        current_violation["Nơi giải quyết vụ việc"].append(text)
                    else:
                        # Nếu không phải là list, khởi tạo lại thành list
                        current_violation["Nơi giải quyết vụ việc"] = [text]

            elif element.name == "hr":
                # Kết thúc vi phạm hiện tại và bắt đầu vi phạm mới
                if current_violation:
                    violations.append(current_violation)
                    current_violation = None

        # Thêm vi phạm cuối cùng nếu có
        if current_violation:
            violations.append(current_violation)
            
        if not violations:
            return {"status": "success", "url": url_csgt, "msg": "Không có vi phạm", "data": None}
            
        # Trả về kết quả thành công
        return {"status": "success","url" :url_csgt, "msg": "Có vi phạm","data": violations}

    except Exception as e:
        # Xử lý lỗi nếu có
        return {"status": "success","url" :url_csgt,"msg": "Không có vi phạm", "data": None}
    
    
def image_to_base64(ss,url):
    response = ss.get(url)
    if response.status_code == 200:
        # Chuyển dữ liệu ảnh thành base64
        image_base64 = base64.b64encode(response.content).decode('utf-8')
        return image_base64
    else:
        return None  # Hoặc bạn có thể xử lý lỗi ở đây


def kiemtra_bienso(bienso, loaiXe, apicaptcha, attempts=1):
    ss = session()
    url_check = f'https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html?&LoaiXe={loaiXe}&BienKiemSoat={bienso}'
    
    #print("[+] Đang gửi request kiểm tra...")
    response = ss.get(url=url_check, headers=check_header, verify=False)
    #print(f"[+] Response Status Code: {response.status_code}")
    
    if response.status_code != 200:
        return json.dumps({"status": "error","message": "Lỗi kết nối csgt.vn"}, ensure_ascii=False, indent=4)
    
    url_check_respond_cookie = response.cookies.get_dict()
    
    PHPSESSID = url_check_respond_cookie.get('PHPSESSID', 'MISSING_PHPSESSID')
    #print(f"[+] PHPSESSID: {PHPSESSID}")
    tracuu_cookie = f'_ga=GA1.2.1205164913.1684257681; _gid=GA1.2.1479880717.1684257681; PHPSESSID={PHPSESSID}'
    
    captcha_image = None
    image_base64 = image_to_base64(ss,captcha_url_csgt)
    if image_base64:
        captcha_image = bypass_text_captcha(apicaptcha, image_base64)
    else:
        print("Không tải được captcha")
    

    captcha_image = str(captcha_image).replace(' ','').lower()
    captcha_invisible = bypass_captcha(get_invisible_captcha, post_invisible_captcha)
    
    #print("[+] Captcha text:", capcha_image)
    
    tracuu_data = f'BienKS={bienso}&Xe={loaiXe}&captcha={captcha_image}&token={captcha_invisible}&ipClient=9.9.9.91&cUrl=1'
    #print("[+] Data gửi đi:", tracuu_data)
    
    tracuu_header = {
        'Accept': '*/*',
        'Accept-Language': 'en,vi;q=0.9,vi-VN;q=0.8,fr-FR;q=0.7,fr;q=0.6,en-US;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': tracuu_cookie,
        'Host': 'www.csgt.vn',
        'Origin': 'https://www.csgt.vn',
        'Referer': url_check,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    #print("[+] Đang gửi request tra cứu...")
    response_check = ss.post(url=tracuu_url, headers=tracuu_header, data=tracuu_data)
    #print(f"[+] Response Status Code: {response_check.status_code}")
    
    try:
        json_response = response_check.json()
        #print("[+] JSON Response:", json_response)
        respond_check = json_response.get('href')
        
        if not respond_check:
            #print("[-] Không tìm thấy 'href' trong JSON response!")
            if attempts < 5:
                #print(f"[+] Thử lại lần {attempts + 1}...")
                time.sleep(3)  # Chờ 3 giây trước khi thử lại
                return kiemtra_bienso(bienso, loaiXe, apicaptcha, attempts + 1)  # Gọi lại hàm với số lần thử tăng lên
            else:
                return json.dumps({"status": "error","message": "Giải captcha sai quá 5 lần"}, ensure_ascii=False, indent=4)
        
    except Exception as e:
        #print("[-] Lỗi khi parse JSON:", e)
        #print("[-] Phản hồi từ server:", response_check.text)
        if attempts < 5:
            #print(f"[+] Thử lại lần {attempts + 1}...")
            time.sleep(3)  # Chờ 3 giây trước khi thử lại
            return kiemtra_bienso(bienso, loaiXe, apicaptcha, attempts + 1)  # Gọi lại hàm với số lần thử tăng lên
        else:
            return json.dumps({"status": "error","message": "Giải captcha sai quá 5 lần"}, ensure_ascii=False, indent=4)
    
    #print("[+] Đang gửi request lấy kết quả...")
    respond_tracuu = ss.get(url=respond_check, verify=False)
    violations = extract_violations_from_html(respond_tracuu.text,respond_check)
    violations_json = json.dumps(violations, ensure_ascii=False, indent=4)
    
    return violations_json

if __name__ == '__main__':
    if len(sys.argv) > 3:  # Đảm bảo có đủ tham số biển số xe và loại xe
        bienso = sys.argv[1]  
        loaiXe = sys.argv[2]  
        apicaptcha = sys.argv[3]  
        result = kiemtra_bienso(bienso, loaiXe,apicaptcha)
        print(result)
    else:
        print("Thiếu tham số biển số xe hoặc loại xe!")
