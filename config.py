#CONFIGURE YOUR REDDIT ACC DETAILS HERE

class Config:
    client_id = ""
    client_secret = ""
    username = ""
    password = ""


#SELECT PURPOSE OF BOT KARMA FARMER OR ADVERTISEMENT (karma/ad)

class Botconfig:
    
    #SET TO TRUE IF YOU NEED TO SETUP WEBHOOK FOR LOGS
    webhook = ""
    
    discord_webhook = False
    
    type = "karma"
    
    ads = [
        '''
        Advertisement 1: Type what u want to advertise here the exact same message will be commented on random posts!
        ''',
        '''
        Advertisement 2: Another ad message here!
        ''',
        '''
        Advertisement 3: Yet another ad message here!
        ''',
    ]

   

