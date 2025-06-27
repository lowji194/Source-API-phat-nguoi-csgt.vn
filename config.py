captcha_url_csgt = 'https://www.csgt.vn/lib/captcha/captcha.class.php'
get_invisible_captcha = 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LdtSj0iAAAAAJ7Wnm9KQVEa86pNd1a8_FLcKfW0&co=aHR0cHM6Ly93d3cuY3NndC52bjo0NDM.&hl=en&v=wqcyhEwminqmAoT8QO_BkXCr&size=invisible&cb=hh6sew8p25xy'
post_invisible_captcha = 'https://www.google.com/recaptcha/api2/reload?k=6LdtSj0iAAAAAJ7Wnm9KQVEa86pNd1a8_FLcKfW0'
url_check = 'https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html'
tracuu_url = 'https://www.csgt.vn/?mod=contact&task=tracuu_post&ajax'
tracuu_header = {
            'Accept': '*/*',
            'Accept-Language': 'en,vi;q=0.9,vi-VN;q=0.8,fr-FR;q=0.7,fr;q=0.6,en-US;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '1788',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'www.csgt.vn',
            'Origin': 'https://www.csgt.vn',
            'Pragma': 'no-cache',
            'Referer': 'https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
            }
check_header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en,vi;q=0.9,vi-VN;q=0.8,fr-FR;q=0.7,fr;q=0.6,en-US;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'www.csgt.vn',
    'Pragma': 'no-cache',
    'Referer': 'https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
    }






if __name__ == '__main__':
    from bypassInvisCapcha import bypass_capcha
    capcha_results = bypass_capcha(api_get_invisible_capcha,api_post_invisible_capcha)
    print(capcha_results)