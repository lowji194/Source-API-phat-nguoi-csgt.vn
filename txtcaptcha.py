from requests import session
import requests

solver_false = 'solver_false'

# Hàm giải CAPTCHA
def autocaptcha(apicaptcha, image_base64, proxy=None):
    TIME_OUT = 20
    api_url = "https://autocaptcha.pro/apiv3/process"
    headers = {'Content-Type': 'application/json'}
    
    payload = {
        "key": apicaptcha,  # Sử dụng apicaptcha thay cho captcha_api_key
        "type": "imagetotext",
        "img": image_base64
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers, proxies=proxy, timeout=TIME_OUT)
        result = response.json()
        if result.get("success"):
            return result.get("captcha")  # Trả về kết quả CAPTCHA đã giải
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


# Hàm chính giải mã CAPTCHA
def bypass_text_captcha(apicaptcha, image_base64, proxy=None):
    if not apicaptcha.endswith("957"):  # Kiểm tra nếu key không kết thúc bằng "957"
        return autocaptcha(apicaptcha, image_base64, proxy)
    
    ss = session()
    TIME_OUT = 20
    
    # Sử dụng OCR API để xử lý base64 image
    api_url = 'https://api8.ocr.space/parse/image'
    header = {
        'apikey': apicaptcha,  # Sử dụng apicaptcha thay cho captcha_api_key
    }
    data = {
        'base64Image': f'data:image/jpeg;base64,{image_base64}',
        'language': 'eng',
        'isOverlayRequired': True,
        'FileType': '.Auto',
        'IsCreateSearchablePDF': False,
        'isSearchablePdfHideTextLayer': True,
        'detectOrientation': False,
        'isTable': False,
        'scale': True,
        'OCREngine': 1,
        'detectCheckbox': False,
        'checkboxTemplate': 0
    }
    
    try:
        # Gửi yêu cầu OCR và lấy kết quả
        captcha_response = ss.post(url=api_url, headers=header, data=data, timeout=TIME_OUT, verify=False).json()
        captcha_text = captcha_response['ParsedResults'][0]['ParsedText'].strip()
        return captcha_text
    except Exception as f:
        print(f"Error: {f}")
        return solver_false


# Ví dụ sử dụng
if __name__ == "__main__":
    
    results = bypass_text_captcha(api_key, base64_image)
    print(results)
