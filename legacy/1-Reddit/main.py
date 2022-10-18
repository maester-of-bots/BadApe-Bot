import praw
import logging

# Configure logging...
logging.basicConfig(
    filename=("BadApe.log"),
    level=logging.INFO,
    format='[%(asctime)s] (%(pathname)s:%(lineno)d) %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

target_sub = "superstonk"  # Where the bot looks for the posts
subreddit = reddit.subreddit(target_sub)  # Making the code look prettier.
troll_subs = ["https://www.reddit.com/r/gme_meltdown", "https://www.reddit.com/r/amc_meltdown"] # Not in use

# Check through a user's post history to see how much they have posted on gme_meltdown
def checkPosts(username):
    links = []  # Empty array for links
    goodPostCount=0 # Start post count at 0
    for submission in reddit.redditor(username).submissions.new(limit=None):  # This caps at 1,000
        if str(submission.subreddit).lower() == "gme_meltdown": 
            if submission.score > 1:  # If post is upvoted
                goodPostCount+=1      # Then it is a good post
                if goodPostCount < 5: # Limit number of links to post to 5
                    links.append(submission.permalink)
    return goodPostCount, links

# Check through a user's comment history to see how much they have commented in gme_meltdown
# Really should put these functions together, but I'm lazy
def checkComments(username):
    links = []
    goodCommentCount=0
    for comment in reddit.redditor(username).comments.new(limit=None):
        if "/r/gme_meltdown/" in comment.permalink.lower():
            if comment.score > 0:
                goodCommentCount+=1
                if goodCommentCount < 5:
                    links.append(comment.permalink)
    return goodCommentCount,links

# Function to scan profile and post if necessery
def scanInit(username):
    print("We are investigating " + username)   # Console output
    goodPostCount, postLinks = checkPosts(username) # Pull post history
    goodCommentCount, commentLinks = checkComments(username)  # Pull comment history
    score = goodPostCount + goodCommentCount  # Calculate shill score
    if score > 5:                             # Self-post data, if they have any comments in GME_Meltdown
        selfSub = reddit.subreddit('u_BadApe-Bot')  # Set to self-post
        title = username + " - ShillScore " + str((goodPostCount + goodCommentCount)) # Generate post title
        allLinks = postLinks + commentLinks # Combine arrays
        post = "Here's a preview of this u/" + username + "'s activity in gme_meltdown:\n\n"  # First line of post
        for link in allLinks:
            post = post + "https://reddit.com" + str(link) + "\n\n"   # Add all the links
        selfSub.submit(title, post)   # Post the post
        print("--BadApe-Bot Flings Poo--")

# This is what runs the bot.  It runs until you stop it, or it crashes.  One for posts, one for comments.
posts = reddit.subreddit("superstonk").stream.submissions(pause_after=-1, skip_existing=True)
cmts = reddit.subreddit("superstonk").stream.comments(pause_after=-1, skip_existing=True)

# Run bot forever
while True:
    for post in posts:  # Read through posts
        if post is None:  # If there are no new posts, break out
            break
        scanInit(post.author.name)  # Scan a user who posted in superstonk
    for cmt in cmts:
        if cmt is None:
            break
        scanInit(cmt.author.name)   # Scan a user who commented in superstonk
