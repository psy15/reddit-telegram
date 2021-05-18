import telegram
import praw
import os
import sys
import logging
import pandas as pd

PORT = int(os.environ.get('PORT', 5000))

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.propagate = False

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s- %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


if ('TOKEN' or 'SUBREDDIT' or 'CHANNEL' or 'SECRET') not in os.environ:
    raise RuntimeError("env/config vars missing!")

ID = os.environ['ID']
SECRET = os.environ['SECRET']
TOKEN = os.environ['TOKEN']
SUBREDDIT = os.environ['SUBREDDIT']
CHANNEL = os.environ['CHANNEL']

reddit = praw.Reddit(client_id=ID,
                     client_secret=SECRET, user_agent='webapp by /u/psydv')
hot_posts = reddit.subreddit('news').hot(limit=10)

posts = []
for post in hot_posts:
    posts.append([post.title, post.score, post.id, post.subreddit,
                  post.url, post.num_comments, post.selftext, post.created])
posts = pd.DataFrame(posts, columns=[
    'title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
