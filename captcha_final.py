import requests
import base64
import re
import subprocess
import time

def captcha_me_if_you_can():
    session = requests.Session()
    url = 'http://challenge01.root-me.org/programmation/ch8/'
    
    for attempt in range(1, 21):
        print(f"Attempt {attempt}")
        try:
            page = session.get(url).text
            if img := re.search(r'data:image/png;base64,(.*)" />', page):
                img_file = f'captcha_{attempt}.png'
                open(img_file, 'wb').write(base64.b64decode(img.group(1)))
                
                ocr = subprocess.run(['gocr', '-i', img_file], capture_output=True, text=True)
                captcha = re.sub(r'[^a-zA-Z0-9]', '', ocr.stdout.strip())
                print(f"Captcha: {captcha} (Length: {len(captcha)})")
                
                if len(captcha) != 12:
                    continue
                
                result = session.post(url, data={'cametu': captcha}).text
                if "Congrat" in result:
                    if flag := re.search(r'flag\{[^}]+\}', result):
                        print(f"Flag: {flag.group()}")
                    else:
                        clean = re.sub(r'\s+', ' ', re.sub('<[^<]+?>', '', result)).strip()
                        print(f"Success: {clean}")
                    return True
        except:
            pass
        time.sleep(0.5)
    
    print("Failed after 20 attempts")
    return False

if __name__ == "__main__":
    captcha_me_if_you_can()