import requests
# from thelegram import *
from reddit import *
from dotenv import load_dotenv
import os
from flairgun import *


flair_id = '70c8af34-22f5-11ec-b8c2-6a9752c5302d'
commentInfo = []  # Creates an empty array`1



def main():
    print("Stonky Ape is online.")
    for comment in reddit.subreddit("stonkymemes").stream.comments():
        anal(comment)
        flairGun_check(comment)
main()