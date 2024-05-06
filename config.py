#CONFIGURE YOUR REDDIT ACC DETAILS HERE

class Config:
    client_id = ""
    client_secret = ""
    username = ""
    password = ""


class Botconfig:
    
    #interval between posts or comments in minutes 
    cooldown = 10 
    
    #SET TO TRUE IF YOU NEED TO SETUP WEBHOOK FOR LOGS
    webhook = ""
    
    discord_webhook = False
     
    #SELECT PURPOSE OF BOT KARMA FARMER OR ADVERTISEMENT (ai/ad/post)
    type = "ai"
    
    all_subreddits = False
    
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
    
    #if set to False will only post in the specific subreddits
        
    subreddits = [
        "test",
        "gachagaming",
        "TowerofGod",
    ]

    posts = [
        {"title":"hey there upvote for a upvote!", "body":"UPVOTE PLEASE"},
        {"title":"hey there upvote for a upvote 2!", "body":"UPVOTE PLEASE"}
    ]
