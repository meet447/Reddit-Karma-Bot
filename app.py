import praw
from time import sleep
from fake_useragent import UserAgent
from praw.exceptions import RedditAPIException
from llm.main import create_response    
from config import Config, Botconfig
import random, requests

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
        
#REDDIT BOT CODE
class RedditBot:
    def __init__(
        self,
        client_id: str = None,
        client_secret: str = None,
        username: str = None,
        password: str = None,
        user_agent: str = None,
        log_file: str = None,
    ) -> None:
        
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent=user_agent or UserAgent().random,
        )
        self.log_file = log_file or "commented_posts.txt"

    def login(self) -> None:
      
        if self.reddit.user.me() is None:
            print("[LOGIN] - Failed to log in")
            write_log("[LOGIN] - Failed to log in")
        else:
            print("[LOGIN] - Logged in as {}".format(self.reddit.user.me()))
            write_log("[LOGIN] - Logged in as {}".format(self.reddit.user.me()))

    def get_trending_topics(self) -> list[praw.models.Submission]:
      
        trending_topics = []
        commented_posts = self.load_commented_posts()
        for submission in self.reddit.subreddit("all").hot(limit=500):
            if submission.id not in commented_posts:
                trending_topics.append(submission)
        return trending_topics

    def extract_text_title(self, submission: praw.models.Submission) -> str:
        
        write_log(submission.title)
        return submission.title

    def extract_text_content(self, submission: praw.models.Submission) -> str:
       
        write_log(submission.selftext)
        return submission.selftext

    def extract_comment_content_and_upvotes(
        self, submission: praw.models.Submission
    ) -> list[tuple[str, int]]:
        
        submission.comments.replace_more(limit=0)
        comments = submission.comments.list()
        comment_content_and_upvotes = []
        for comment in comments:
            comment_content_and_upvotes.append((comment.body, comment.score))
        return comment_content_and_upvotes

    def generate_comment(
        self,
        submission: praw.models.Submission,
        title: str,
        post_text: str,
        comments: list[tuple[str, int]],
    ) -> None:
      
        
        comments = sorted(comments, key=lambda comment: comment[1], reverse=True)
        if len(comments) >= 4:
            comments = comments[:4]
        else:
            comments = comments[: len(comments)]
        comments = [comment[0] for comment in comments]
        comments = ", ".join(comments)
        
        prompt =[
            {
                "role": "system",
                "content": "You are an avid reddit user that knows how to provide simple and short interesting comments that will get upvotes. Now I'll provide you the contents of the post and the most important comments and you will have to generate a comment that will get tons of upvotes, it is important that you integrate with the group, mimic their tone and align your opinions to theirs to be upvoted, your way to respond should be similar to the other comments.",
            },
            {
                "role": "user",
                "content": f"The post of title {title}, its text content is: {post_text}. The most voted comments are: {comments}. Now generate a comment that will fit in and earn upvotes, remember to speak in a similar tone to the other comments, short phrases and simple words are the best don't be too verbose, only one short phrase with natural language mimicking the others and their mood, don't be too simple or too happy and friendly as it looks bad, make yourself look a bit interesting and NEVER EVER BE AGGRESIVE OR OFFENSIVE. Only reply with the comment, the format of your response is quite important so don't reply anything else.",
            },
        ],
        
        new_prompt = str(prompt)
        
        if Botconfig.type == "karma":
            comment = create_response(post=new_prompt)
        else:
            comment = random.choice(Botconfig.ads)
        exit = False
        while not exit:
            try:
                submission.reply(comment)
                print("[SUCCESS] - replied to the post!")
                write_log("[SUCCESS] - replied to the post")
                exit = True
            except RedditAPIException as e:
                if e.error_type == "RATELIMIT":
                    print("[RATE LIMIT] - rate limited sleeping 10 mins")
                    write_log("[RATE LIMIT] - rate limited sleeping for 10 mins")
                    sleep(60)
                    write_log("[SLEEP] - 9 more minutes left")
                    sleep(60)
                    write_log("[SLEEP] - 8 more minutes left")
                    sleep(60)
                    write_log("[SLEEP] - 7 more minutes left")
                    sleep(60)
                    write_log("[SLEEP] - 6 more minutes left")
                    sleep(60)
                    write_log("[SLEEP] - 5 more minutes left")
                    sleep(60)
                    write_log("[SLEEP] - 4 more minutes left")
                    sleep(60)
                    write_log("[SLEEP] - 3 more minutes left")
                    sleep(60)
                    write_log("[SLEEP] - 2 more minutes left")
                    sleep(60)
                    write_log("[SLEEP] - 1 more minutes left")
                    sleep(60)
                    print("[SLEEP] - sleep completed posting new comments")
                    write_log("[SLEEP] - sleep completed posting new comments")
                    
                elif e.error_type == "THREAD_LOCKED":
                    print("Thread locked. Skipping.")
                    write_log("thread locked skipping")
                    exit = True
                else:
                    print(e.error_type)
                    write_log(e.error_type)
                    exit = True

        print(f"Replied to '{submission.title}' with '{comment}'")
        write_log(f"Replied to '{submission.title}' with '{comment}'")
        
        self.log_commented_post(submission.id)
        
        print("[SLEEP] - going to sleep for 10 mins")
        write_log("[SLEEP] - going to sleep 10 mins")
        sleep(60)
        write_log("[SLEEP] - 9 more minutes left")
        sleep(60)
        write_log("[SLEEP] - 8 more minutes left")
        sleep(60)
        write_log("[SLEEP] - 7 more minutes left")
        sleep(60)
        write_log("[SLEEP] - 6 more minutes left")
        sleep(60)
        write_log("[SLEEP] - 5 more minutes left")
        sleep(60)
        write_log("[SLEEP] - 4 more minutes left")
        sleep(60)
        write_log("[SLEEP] - 3 more minutes left")
        sleep(60)
        write_log("[SLEEP] - 2 more minutes left")
        sleep(60)
        write_log("[SLEEP] - 1 more minutes left")
        sleep(60)
        print("[SLEEP] - sleep completed posting new comments")
        write_log("[SLEEP] - sleep completed posting new comments")

    def load_commented_posts(self) -> list[str]:
       
        try:
            with open(self.log_file, "r") as f:
                commented_posts = f.read().splitlines()
        except FileNotFoundError:
            commented_posts = []
        return commented_posts

    def log_commented_post(self, post_id: str) -> None:
        
        with open(self.log_file, "a") as f:
            f.write(post_id + "\n")

    def run(self) -> None:
        
        self.login()
        trending_topics = self.get_trending_topics()
        print("fetched a trending topic!")
        write_log("fetched a trending topic")
        for submission in trending_topics:
            post_title = self.extract_text_title(submission)
            print("recived title")
            write_log("recived title")
            text_content = self.extract_text_content(submission)
            print("recived content")
            write_log("received content")
            comment_content_and_upvotes = self.extract_comment_content_and_upvotes(
                submission
            )
            
            self.generate_comment(
                submission, post_title, text_content, comment_content_and_upvotes
            )

if __name__ == "__main__":
    reddit_bot = RedditBot(Config.client_id, Config.client_secret, Config.username, Config.password)
    reddit_bot.run()