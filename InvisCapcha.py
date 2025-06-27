from requests import session

def bypass_captcha(get_invisible_captcha,post_invisible_captcha,proxy=None):
    try:
        ss = session()
        recaptcha_token = ss.get(url=get_invisible_captcha,proxies= proxy , timeout = 20,verify=False).text.split('<input type="hidden" id="recaptcha-token" value="')[1].split('">')[0]
        string_v = get_invisible_captcha.split('&v=')[1].split('&')[0]
        string_k = get_invisible_captcha.split('&k=')[1].split('&')[0]
        string_co = get_invisible_captcha.split('&co=')[1].split('&')[0]
        post_data = f'v={string_v}&reason=q&c={recaptcha_token}&k={string_k}&co={string_co}&hl=en&size=invisible&chr=1&vh=1&bg=5'
        header = {
            'accept': '*/*',
            'accept-language': 'en,vi;q=0.9,vi-VN;q=0.8,fr-FR;q=0.7,fr;q=0.6,en-US;q=0.5',
            'content-length': '9811',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.google.com',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
            }
        capcha_solver = ss.post(url=post_invisible_captcha,headers=header,data=post_data , proxies= proxy , timeout = 20,verify=False).text.split('["rresp","')[1].split('",')[0]
        return capcha_solver
    except Exception as f:
        print(f)
        return 'null'
    