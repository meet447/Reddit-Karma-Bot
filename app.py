import os
import praw
from requests import Session
from time import sleep
from fake_useragent import UserAgent
from praw.exceptions import RedditAPIException
from llm.main import create_response
from config import Config, Botconfig
import random
from modules.sleep.main import goto_sleep
from modules.logging.main import write_log

class RedditBot:
    def __init__(
        self,
        account,
        proxy=None,
    ) -> None:
        self.username = account['username']
        self.password = account['password']
        self.client_id = account['client_id']
        self.client_secret = account['client_secret']
        self.proxy = proxy
        self.session = Session()
        
        # Configure proxy if provided
        if proxy:
            self.configure_proxy(self.session, proxy)

        self.reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            username=self.username,
            password=self.password,
            user_agent=UserAgent().random,
            requestor_kwargs={"session": self.session}
        )
        self.log_file = Botconfig.log_file or "commented_posts.txt"

    def configure_proxy(self, session, proxy):
        proxy_parts = proxy.split(':')
        if len(proxy_parts) == 4:
            ip, port, proxy_username, proxy_password = proxy_parts
            proxy_url = f"http://{proxy_username}:{proxy_password}@{ip}:{port}"
            session.proxies['http'] = proxy_url
            session.proxies['https'] = proxy_url
            print("[Using proxy:] - ", proxy_url)
        else:
            print("[PROXY] - Proxy format is incorrect. Expected format is 'ip:port:username:password'")

    def login(self) -> bool:
        try:
            print(f"[LOGIN] - Attempting login for {self.username}")
            print(f"[LOGIN] - Logged in as {self.reddit.user.me()}")
            write_log(f"[LOGIN] - Logged in as {self.reddit.user.me()}")
            return True
        except Exception as e:
            print(f"[LOGIN] - Failed to log in: {e}")
            write_log(f"[LOGIN] - Failed to log in: {e}")
            return False

    def get_trending_topics(self) -> list[praw.models.Submission]:
        trending_topics = []
        commented_posts = self.load_commented_posts()
        
        if Botconfig.new_posts == False:
            for submission in self.reddit.subreddit("all").hot(limit=500):
                if submission.id not in commented_posts:
                    trending_topics.append(submission)
        else:
            for submission in self.reddit.subreddit("all").new(limit=500):
                if submission.id not in commented_posts:
                    trending_topics.append(submission)

        return trending_topics

    def extract_text_title(self, submission: praw.models.Submission) -> str:
        return submission.title

    def extract_text_content(self, submission: praw.models.Submission) -> str:
        return submission.selftext

    def extract_comment_content_and_upvotes(
        self, submission: praw.models.Submission
    ) -> list[tuple[str, int]]:
        
        submission.comments.replace_more(limit=0)
        comments = submission.comments.list()
        return [(comment.body, comment.score) for comment in comments]

    def generate_comment(
        self,
        submission: praw.models.Submission,
        title: str,
        post_text: str,
        comments: list[tuple[str, int]],
    ) -> None:
        comments = sorted(comments, key=lambda comment: comment[1], reverse=True)[:4]
        comments = ", ".join([comment[0] for comment in comments])
        
        prompt = f'''
        [SYSTEM] You are an avid Reddit user skilled at crafting concise and engaging comments that resonate with the community. Create a comment that aligns with the post titled "{title}" and its top comments: "{comments}". 
        '''
                
        new_prompt = str(prompt)
        
        if Botconfig.type == "ai":
            comment = create_response(post=new_prompt)
        else:
            comment = random.choice(Botconfig.ads)
        
        while True:
            try:
                submission.reply(comment)
                print("[SUCCESS] - replied to the post!")
                write_log("[SUCCESS] - replied to the post")
                break
            except RedditAPIException as e:
                if e.error_type == "RATELIMIT":
                    print("[RATE LIMIT] - Rate limited. Sleeping.")
                    write_log("[RATE LIMIT] - Rate limited. Sleeping.")
                    goto_sleep(Botconfig.cooldown)
                elif e.error_type == "THREAD_LOCKED":
                    print("Thread locked. Skipping.")
                    write_log("Thread locked. Skipping.")
                    break
                else:
                    print(e.error_type)
                    write_log(e.error_type)
                    break

        print(f"[Replied to] - {submission.title} with {comment}")
        write_log(f"[Replied to] - {submission.title} with {comment}")
        
        self.log_commented_post(submission.id)
        goto_sleep(Botconfig.cooldown)

    def load_commented_posts(self) -> list[str]:
        try:
            with open(self.log_file, "r") as f:
                return f.read().splitlines()
        except FileNotFoundError:
            return []

    def log_commented_post(self, post_id: str) -> None:
        with open(self.log_file, "a") as f:
            f.write(post_id + "\n")

    def run_for_account(self):
        if self.login():
            trending_topics = self.get_trending_topics()
            for submission in trending_topics:
                title = self.extract_text_title(submission)
                content = self.extract_text_content(submission)
                comments = self.extract_comment_content_and_upvotes(submission)
                self.generate_comment(submission, title, content, comments)

def get_working_proxy(account):
    for _ in range(len(Botconfig.proxies)):
        proxy = random.choice(Botconfig.proxies)
        bot = RedditBot(account, proxy=proxy)
        if bot.login():
            return proxy
    return None  # If no proxies work

def main():
    for account in Config.accounts:
        proxy = get_working_proxy(account)
        
        if proxy is None:
            print("[PROXY] - All proxies failed. Trying without proxy.")
            reddit_bot = RedditBot(account)
            if not reddit_bot.login():
                print(f"[LOGIN] - Failed to log in without proxy for account {account['username']}")
                continue
        
        else:
            reddit_bot = RedditBot(account, proxy=proxy)

        reddit_bot.run_for_account()
        goto_sleep(Botconfig.cooldown)

if __name__ == "__main__":
    main()
