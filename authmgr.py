from fake_useragent import FakeUserAgent
from ddddocr import DdddOcr
import httpx
import time
import cairosvg
import hashlib
import getpass
# import pickle
import base64

ocr = DdddOcr(show_ad=False)

def getFakeUserAgent():
    return FakeUserAgent().random

def _login(username : str, password : str):
    max_retries = 10
    retry_count = 0
    
    with httpx.Client(headers = {"user-agent" : getFakeUserAgent()},
                    follow_redirects = True,) as client:
        # 保存登录页面的cookie
        client.get("https://www.becoder.com.cn/login")
        
        while retry_count < max_retries:
            rep = client.get(f"https://www.becoder.com.cn/captcha?_={time.time()}")
            img = cairosvg.svg2png(rep.content, background_color="white")
            captcha = ocr.classification(img)
            
            rep = client.post("https://www.becoder.com.cn/api/login", 
                            json = {
                                    "username" : username,
                                    "password" : hashlib.md5((password+'syzoj2_xxx').encode("utf-8")).hexdigest(),
                                    "captcha"  : captcha,
                                    "remember_me": False
                            })
            code = rep.json()['error_code']
            
            # 如果不是验证码错误，直接返回结果
            if code != 3000:
                break
                
            retry_count += 1
            if retry_count < max_retries:
                time.sleep(1)  # 等待1秒后重试

        """
        switch (error_code) {
                    case 1001:
                        show_error("用户不存在");
                        break;
                    case 1002:
                        show_error("密码错误");
                        break;
                    case 1003:
                        show_error("您尚未设置密码，请通过下方「找回密码」来设置您的密码。");
                        break;
                    case 3000:
                        show_error("验证码错误");
                        break;
                    case 114514:
                        show_error("用户已被封禁");
                        break;
                    case 1:
                        // 如果用户选择了记住我，保存用户名和密码到localStorage
                        if (rememberMe) {
                            localStorage.setItem('remembered_username', document.getElementById("login-username").value);
                            localStorage.setItem('remembered_password', document.getElementById("login-password").value);
                            localStorage.setItem('remember_me_checked', 'true');
                        } else {
                            // 如果用户没有选择记住我，清除之前保存的信息
                            localStorage.removeItem('remembered_username');
                            localStorage.removeItem('remembered_password');
                            localStorage.removeItem('remember_me_checked');
                        }
                        window.location.href = "/index";
                        return;
                    default:
                        show_error("未知错误");
                        break;
        """

        if code == 1: # 登录成功
            # 将cookies转换为字典格式
            cookies_dict = dict(client.cookies)
            return {
                "status": "success",
                "cookie": base64.b64encode(str(cookies_dict).encode()).decode()
            }
        elif code == 1001:
            return {
                "status": "error",
                "message": "User does not exist",
                "type": "user_not_found"
            }
        elif code == 1002:
            return {
                "status": "error",
                "message": "Incorrect password",
                "type": "incorrect_password"
            }
        elif code == 1003:
            return {
                "status": "error",
                "message": "You have not set a password yet. Please use the 'Forgot Password' option below to set your password.",
                "type": "password_not_set"
            }
        elif code == 3000:
            return {
                "status": "error",
                "message": "Incorrect captcha",
                "type": "incorrect_captcha"
            }
        elif code == 114514:
            return {
                "status": "error",
                "message": "User has been banned",
                "type": "user_banned"
            }
        else:
            return {
                "status": "error",
                "message": "Unknown error",
                "type": "unknown_error"
            }