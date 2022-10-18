import os
from time import sleep
from sql import *
from stonks import *
from traffic import *
keyword = "!check "



# Telegram
token = ""
chatid = ""

# Reddit
target_sub = "stnok"  # Where the bot looks for the words
bot_username = ["BadApe-Bot", "B0tRank"]  # Bot's username, because I'm too lazy to pull it from reddit.
rating_report = ["Time: ", "Comment ID", "Comment Body", "Comment Link", "Parent ID", "Parent Body", "Parent Link"]

# Responses
bot_feedback = [
    ['good bot', 'Yes, thank you!'],
    ['bad bot', '[Sorry about that.  I\'ve logged your review.  Please DM u/TheGreatSkeeve_ if you have any further feedback to provide]']
]
bot_response = [
        ">",
        "",
        "\n\n[The Greater Good.](https://www.reddit.com/r/hotfuzz)",
        "\n\n^(I'm) ^(a) ^(bot)^(,) ",
        "^(please) ^(message) [^(u/thegreatskeeve_)](https://www.reddit.com/user/thegreatskeeve_) ^(for) ^(comments) ^(or) ^(complaints)"
]

# Admin
data_file = ["comment_list.txt", "bot_ratings.txt"]  # Persistant storage
consoleoutput = ["\nTime to post tickers!!\n", "Ignoring comments from the bot rater...", "Thanking a voter!",
                 "Apoligizing and deleting...whoops.",]

# Sign into Reddit
reddit = praw.Reddit(
    client_id="",
    client_secret="",
    password="",
    user_agent="Bad Ape 1.0",
    username="BadApe-Bot",
    check_for_async=False
)
# Set the target sub (r/all)
subreddit = reddit.subreddit(target_sub)  # Making the code look prettier.



# Function to send a message to THC-Development group in Telegram
def sendMessage(message):
    import requests
    msg1 = "https://api.telegram.org/bot"
    msg2 = "/sendMessage?chat_id="
    msg3 = "&text="
    URL = msg1+token+msg2+chatid+msg3+message
    r = requests.get(url=URL)

# Function to respond if we're rate-limited
# This doesn't happen much, will probably delete
def rateLimit(error,comment):
    timeleft = ((error.split("try again in "))[1].split(" minute"))[0]
    part_1 = "We're being rate-limited...stupid Reddit."
    part_2 = error
    part_3 = "Sleeping for " + timeleft + " minutes until I can comment again..."
    link = "(" + str(comment.permalink) + ")"
    outOfJail = "Okay, ratelimit should be over"
    message = part_1 + "\n" + link + "\n" + part_2 + "\n" + part_3
    sendMessage(message)
    sendMessage(link)
    sleep((int(timeleft) * 60) + 1)
    sendMessage(outOfJail)

# Function to delete the comment if we get a "Bad Bot" rating
def badBot(comment):
    global badbot_count
    comment_parent = comment.parent()
    parent_author = str(comment_parent.author)
    if parent_author == "SimonSkinnerBot":
        badbot_count += 1
        sendMessage("Bad Bot Alert - Bad Bot Alert")
        sendMessage(comment.permalink)
        sendMessage("Bad Bot Alert - Bad Bot Alert")
        if comment_parent.score < 10:
            comment_parent.delete()
    sqlite_write(comments_me_count, comments_processed_count, goodbot_count, badbot_count, deleted_count)

def findSubString(comment,text):
    numstart = comment.index(text)
    numend = numstart + 16
    replytext = comment[numstart:numend]
    return replytext

def healthCheckerPing():
    import requests
    url = "https://hc-ping.com/86d42e5c-5ec3-4e48-89f0-9e9a7c2834b6"
    requests.get(url)

# Let Telegram know we're running
sendMessage("Simon Skinner is powering up")
# Let the console know we're running
print(consoleoutput[0])
# Count the comments

badape_load()

# Runs for the last 100 comments / any new comments
for comment in subreddit.stream.comments():
    healthCheckerPing()
    # Add it to the count of comments we've read
    comments_processed_count += 1
    # Make the comment all lower case
    comment_body = comment.body.lower()
    # Catch if it's a "bad bot" rating
    if "bad bot" in comment_body:
        badBot(comment)
    # Don't get caught in a Greater Good loop.
    if comment.author == bot_username[0]:
        comment_body="Fuck off"
    # Someone said "The Greater Good", time to chime in.
    if ("!check " in comment_body[0:7]):
        ticker = comment_body.replace("!check ", "")
        response = checkStonks(ticker)
        try:
            comment.reply(response)     # Try and make the comment
            comments_me_count += 1
        except Exception as e:
            print("Probably rate-limited again.\n"+e)
        try:
            sqlite_write(comments_me_count, comments_processed_count, goodbot_count, badbot_count, deleted_count)       # Try and update SQL
        except Exception as e:
            sendMessage("Caught an exception writing to SQL.\n"+str(e))
    if ("!info " in comment_body[0:6]):
        ticker = comment_body.replace("!info ", "")
        response = getInfo(ticker)
        try:
            comment.reply(response)     # Try and make the comment
            comments_me_count += 1
        except Exception as e:
            print("Probably rate-limited again.\n"+e)
        try:
            sqlite_write(comments_me_count, comments_processed_count, goodbot_count, badbot_count, deleted_count)       # Try and update SQL
        except Exception as e:
            sendMessage("Caught an exception writing to SQL.\n"+str(e))


