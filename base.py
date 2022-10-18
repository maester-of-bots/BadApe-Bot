import praw
from datetime import *
from sql import *

reddit = praw.Reddit(
    client_id="",
    client_secret="",
    password="",
    user_agent="Bad Ape 1.0",
    username="BadApe-Bot",
)


# If a meltdown poster has posted more in ape subs than meltdown, have the bot find the price of GME when they make their first post in an ape sub.

bot_username = 'BadApe-Bot'
subreddit = reddit.subreddit('gme_meltdown')    #Making the code look prettier.

response = "UNDRS_BOT 1.00: UTC->{}\n\n✅ {} SHARES REMOVED!\n\nu/{} has successfully removed {} shares total from ComputerShare through {} transactions!\n\nKenny thanks you for all the hard work and toil, fellow Shill!  Your BTC is in the mail."

with open('log.txt','r') as file:
    data = file.read().split("\n")

for comment in subreddit.stream.comments():
    all_comments = getComments()
    if comment.id in all_comments:
        print("Already seen this post.")
        pass
    else:
        if comment.body[:12] == "!DRS-REMOVE:":
            count = comment.body[12:]
            if count.isnumeric():
                if int(count) > 10000:
                    writeComment(comment.id)
                    comment.reply(body="Please register your copy of the Pulte plan before removing more than 5,000 shares from DRS.")
                else:
                    # Get the date timestamp
                    datevar = datetime.utcnow()

                    # Write new removals to DB
                    writeCharges(comment.author.name, count)

                    # Get total removals
                    total, times = getCharges(comment.author.name)
    
                    # Make response
                    print(datevar)
                    print(count)
                    print(comment.author.name)
                    print(total)
                    newResponse = response.format(datevar,count, comment.author.name, total, times)
                    comment.reply(body=newResponse)

                    # Log comment
                    writeComment(comment.id)