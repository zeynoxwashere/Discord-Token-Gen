import requests
import random
from colorama import Style, Fore
import emailApi
import string
import httpx
import websocket
import json

user = ""
captchaApi = input("Enter the captcha solver [anti-captcha.com] [capmonster.cloud]: ")
captchaApi = "anti-captcha.com"
proxies = open('proxies.txt').read().split('\n')

def generatePassword():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))

def generateDOB():
    year = str(random.randint(1997,2001))
    month = str(random.randint(1, 12))
    day = str(random.randint(1,28))
    if len(month) == 1:
        month = '0' + month
    if len(day) == 1:
        day = '0' + day
    return year + '-' + month + '-' + day


class Botter:
    def __init__(self, inv, capKey,emailKey):
        try:
            self.session = requests.Session()
            self.session.proxies  = {"http":"http://"+random.choice(proxies),"https":"http://"+random.choice(proxies)}
            self.session.headers  = {"Accept": "*/*", "Accept-Language": "en-US", "Connection": "keep-alive", "Content-Type": "application/json", "DNT": "1", "Host": "discord.com", "Referer": f"https://discord.com/invite/{inv}", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "TE": "trailers", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0", "X-Discord-Locale": "en-US", "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2Ojk0LjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvOTQuMCIsImJyb3dzZXJfdmVyc2lvbiI6Ijk0LjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6OTk5OSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="}
            self.session.headers["X-Fingerprint"] = self.session.get( "https://discord.com/api/v9/experiments", timeout=30).json()["fingerprint"]
            self.session.headers["Origin"] = "https://discord.com"
            self.inv = inv
            self.capKey = capKey
            self.emailKey = emailKey
        except Exception as e:
            print("Error : "+e)
            self.generateToken()
    def getCap(self,websiteKey,websiteURL):
           solvedCaptcha = None
           captchaKey = self.capKey
           taskId = ""
           taskId = httpx.post(f"https://api.{captchaApi}/createTask", json={"clientKey": captchaKey, "task": {"type": "HCaptchaTaskProxyless", "websiteURL": websiteURL,
                               "websiteKey": websiteKey , "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"}}, timeout=30).json()
           if taskId.get("errorId") > 0:
                print(f"[+] createTask - {taskId.get('errorDescription')}!")

           taskId = taskId.get("taskId")
            
           while not solvedCaptcha:
                    captchaData = httpx.post(f"https://api.{captchaApi}/getTaskResult", json={"clientKey": captchaKey, "taskId": taskId}, timeout=30).json()
                    if captchaData.get("status") == "ready":
                        solvedCaptcha = captchaData.get("solution").get("gRecaptchaResponse")
                        print(f"{Fore.GREEN}{Style.BRIGHT}[>] Got Captcha {solvedCaptcha[0:60]}{Style.RESET_ALL}")
                        return solvedCaptcha
    def generateToken(self):
        username = int(input("Do You want [1]Custom Username [2]Random Usernames: "))
        if username == 1:
            username = str(input("Enter the Username: "))
        else:
            username = requests.get("https://apis.kahoot.it/namerator")
            username = user.text
            username = json.loads(user)
        self.emailSession = emailApi.email(self.emailKey)
        self.email = self.emailSession.email
        print(f"{Style.BRIGHT}{Fore.GREEN}[+] Got email : {self.email}!")
        try:
            payload = {
                "fingerprint": self.session.headers["X-Fingerprint"],
                "username": user,
                "invite": self.inv,
                "gift_code_sku_id": None,
                "captcha_key":  self.getCap("4c672d35-0701-42b2-88c3-78380b0db560", "https://discord.com/"),
                'consent': True,

                'password': generatePassword(),
                'date_of_birth': generateDOB(),
                'email': self.email,
            }

            req = self.session.post('https://discord.com/api/v9/auth/register', json=payload)
            if req.status_code != 201:
                self.generateToken()
                print(req.json())
            else:
                self.token = req.json()["token"]
                print(f'{Style.BRIGHT}{Fore.GREEN}[+] Generated token - {user} || {self.token }{Style.RESET_ALL}')
                with open('tokens.txt', 'a') as fp:
                    fp.write(self.token + "\n")

            ws = websocket.WebSocket()
            ws.connect('wss://gateway.discord.gg/?v=6&encoding=json')
            response = ws.recv()
            event = json.loads(response)
            auth = {'op': 2, 'd': {'token': self.token, 'capabilities': 61,
                                   'properties': {'os': 'Windows', 'browser': 'Chrome', 'device': '',
                                                  'system_locale': 'en-GB',
                                                  'browser_user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
                                                  'browser_version': '90.0.4430.212', 'os_version': '10',
                                                  'referrer': '', 'referring_domain': '', 'referrer_current': '',
                                                  'referring_domain_current': '', 'release_channel': 'stable',
                                                  'client_build_number': '85108', 'client_event_source': 'null'},
                                   'presence': {'status': 'dnd', 'since': 0, 'activities': [], 'afk': False},
                                   'compress': False,
                                   'client_state': {'guild_hashes': {}, 'highest_last_message_id': '0',
                                                    'read_state_version': 0, 'user_guild_settings_version': -1}}};
            ws.send(json.dumps(auth))
            ws.close()

            email_verification_link = self.emailSession.waitForEmail()

            emailValidationToken = requests.get(email_verification_link).url

            emailValidationToken = emailValidationToken.split('#token=')[1]

            response = self.session.post('https://discord.com/api/v9/auth/verify', headers={
                "sec-ch-ua": 'Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98',
                'referer': 'https://discord.com/verify',
                'authorization': self.token
            }, json={
                'captcha_key':self.getCap("f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34","https://discord.com/api/v9/auth/verify"),
                'token': emailValidationToken
            }).text

            print(f'{Style.BRIGHT}{Fore.GREEN}[+] Email is successful verified for token - {self.token} : discord server return "{response}{Style.RESET_ALL}')

        except Exception as e:
            print("Error : "+e)
            self.generateToken()