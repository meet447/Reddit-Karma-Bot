import praw
from time import sleep
from fake_useragent import UserAgent
from praw.exceptions import RedditAPIException
from llm.main import create_response    
from config import Config, Botconfig
import random
from modules.sleep.main import goto_sleep
from modules.logging.main import write_log

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
        return submission.title

    def extract_text_content(self, submission: praw.models.Submission) -> str:
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
        
        prompt = f'''
        [SYSTEM] You are an avid Reddit user skilled at crafting concise and engaging comments that resonate with the community and garner significant upvotes. Your task is to generate a comment that seamlessly integrates with the existing discussion, mirroring the tone and sentiment of the most popular comments. Your comment should be succinct yet intriguing, capturing the attention of readers without appearing overly verbose or excessively friendly. Avoid being aggressive or offensive at all costs.

        [CONTENT] The post titled "{title}" contains the following text: "{post_text}". Among the most upvoted comments are: "{comments}". Your objective is to create a comment that aligns with the prevailing mood and opinions expressed in the thread. Keep your response natural and in line with the community's language and attitudes.

        Format your response as a single, short phrase. Example comments may provide helpful guidance in crafting your response. Aim for a balance between simplicity and sophistication to engage readers effectively. 

        [CONTENT]
        '''
                
        new_prompt = str(prompt)
        
        if Botconfig.type == "ai":
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
                    goto_sleep(Botconfig.cooldown)
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
        
        goto_sleep(Botconfig.cooldown)
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
        
        if Botconfig.type == "post":
            while True:
                for sub in Botconfig.subreddits:
                    for post in Botconfig.posts:
                        try:
                            title = post["title"]
                            body = post["body"]
                            self.reddit.subreddit(sub).submit(title=title, selftext=body)
                            print("[SUCCESS] - Submission made")
                            write_log("[SUCCESS] - Submission made")
                            goto_sleep(Botconfig.cooldown)
                            
                        except RedditAPIException as e:
                            if e.error_type == "RATELIMIT":
                                print("[RATE LIMIT] - rate limited sleeping")
                                write_log("[RATE LIMIT] - rate limited sleeping")
                                goto_sleep(Botconfig.cooldown)
                                print("[SLEEP] - sleep completed posting new comments")
                                write_log("[SLEEP] - sleep completed posting new comments")
                                
                            elif e.error_type == "THREAD_LOCKED":
                                print("Thread locked. Skipping.")
                                write_log("thread locked skipping")
                            else:
                                print(e.error_type)
                                write_log(e.error_type)
        
        else:
            if Botconfig.all_subreddits == True:
                trending_topics = self.get_trending_topics()
                print("[SUCCESS] - fetched a trending topic!")
                write_log("SUCCESS] - fetched a trending topic")
                for submission in trending_topics:
                    post_title = self.extract_text_title(submission)
                    print("SUCCESS] - recived title")
                    write_log("SUCCESS] - recived title")
                    text_content = self.extract_text_content(submission)
                    print("SUCCESS] - recived content")
                    write_log("SUCCESS] - received content")
                    comment_content_and_upvotes = self.extract_comment_content_and_upvotes(
                        submission
                    )
                    self.generate_comment(
                        submission, post_title, text_content, comment_content_and_upvotes
                    )
            else:
                while True:
                    subreddit = random.choice(Botconfig.subreddits)
                    posts = []
                    commented_posts = self.load_commented_posts()
                    for submission in self.reddit.subreddit(subreddit).hot(limit=100):
                        if submission.id not in commented_posts:
                            posts.append(submission)
                                            
                    post = random.choice(posts)
                    
                    post_title = self.extract_text_title(submission)
                    print("SUCCESS] - recived title")
                    write_log("SUCCESS] - recived title")
                    text_content = self.extract_text_content(submission)
                    print("SUCCESS] - recived content")
                    write_log("SUCCESS] - received content")
                    comment_content_and_upvotes = self.extract_comment_content_and_upvotes(
                            submission
                    )
                    self.generate_comment(
                            submission, post_title, text_content, comment_content_and_upvotes
                    )

if __name__ == "__main__":
    reddit_bot = RedditBot(Config.client_id, Config.client_secret, Config.username, Config.password)
    reddit_bot.run()