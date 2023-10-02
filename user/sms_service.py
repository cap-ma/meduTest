import os 
import requests 


from dotenv import load_dotenv

FAILED=400   
SUCCESS = 200
PROCESSING = 102


ESKIZ_EMAIL="uone2323@gmail.com"
ESKIZ_PASSWORD="uGKnO0ptNkleDlJh9CxvjOVr7nTWg7hry9xMgyCq"

class SendSms:
    def __init__(self,message,phone,email=ESKIZ_EMAIL,password=ESKIZ_PASSWORD):
        self.message=message
        self.phone=phone
        self.spend=None
        self.email=email
        self.password=password

    def send(self):
        rsult=self.send_messege(self.message)
        return rsult
    

    def authorization(self):
        data={
            'email':self.email,
            'password':self.password


        }
        AUTHORIZATION_URL="http://notify.eskiz.uz/api/auth/login"
        r=requests.request('POST',AUTHORIZATION_URL,data=data)
        print(r.json())
        if r.json()['data']['token']:
            return r.json()['data']['token']
        return FAILED
    
    def send_messege(self,message):
        token=self.authorization()
        print("this is tokennnnnnnnnnnnnnn" ,token)
        if token==FAILED:
            return FAILED
        
        SEND_SMS_URL="http://notify.eskiz.uz/api/message/sms/send"

        PAYLOAD={
            "mobile_phone":'998'+str(self.phone),
            "message":message,
            'from':'4546',
            
            
        }

        FILES=[

        ]
        HEADERS={
            'Authorization':f'Bearer {token}'
        }

        r=requests.request("POST",SEND_SMS_URL, headers=HEADERS,data=PAYLOAD,files=FILES)
        print(f"ESKIZ : {r.json()}")
        print("zksjfhksjdzfknsJKBZDFjasebhfj")
        return r.status_code

# message="Pulatov kurinmisan"
# phone=995887756
# e_api=SendSms(message=message,phone=phone)
# r=e_api.send()
# print(r)