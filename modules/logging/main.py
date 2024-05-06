from config import Botconfig
import requests

def write_log(data):
    if Botconfig.discord_webhook == True:
        try:
            url = Botconfig.webhook
            payload = {
            "embeds": [
                {
                    "title": "Reddit log",
                    "description": data,
                    "color": 16711680  
                }
                ]
            }

            response = requests.post(url, json=payload)
            
            print(response)
    
        except:
            print("INVADLID WEBHOOK")
            
    else:
        with open("log.txt","a") as log:
            log.write(data)
            log.write("\n")
            log.write('---------------------------')
            log.write("\n")