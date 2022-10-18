from reddit import *
from sql import *

# This authenticates to Reddit using BadApe's credentials
reddit = praw.Reddit(
    client_id="",
    client_secret="",
    password="",
    user_agent="Bad Ape 1.0",
    username="BadApe-Bot",
    check_for_async=False
)

# Variables to keep things organized
subreddit = reddit.subreddit("stonkymemes")  # Making the code look prettier.
tags = ["meta", "gme", "meltie", "deadmemes", "toilet", "buckfoat", "popcorn"]

print("Smart Ape is online.")
for comment in subreddit.stream.comments():         # Read through comments as they are made
    for tag in tags:                                # Read through each of the tags above
        postlist = []                               # Create a list for the posts
        posts = Neurotic_Read(tag)                  # Read in posts that match the tag from the DB
        comment_var = str(comment.body).lower()     # Give the comment text a variable to clean up the code
        for post in posts:                          # Data is stupid, gotta extract it, this is probably the least-efficient way
            postlist.append(post[0])                # Add the post to the post list.  Again, not an efficient way to do it.
        if comment_var == ("!" + tag) and comment not in postlist:          # If it's a tag, and the comment hasn't been responded to
            if comment_var == "!buckfoat":                                  # Seriously tho
                comment.reply("If you shave a boat, is it still a boat?")   # Can probably make a pool to choose from
                Neurotic_Write(str(comment_var), tag)                       # Record that we responded
                print("Boat comment was not in DB, submission is " + str(comment.submission))       # Feedback to console for debug
            else:   # If it isn't buckfoat...
                comment.reply("Apparently this is a " + tag + " post, and it's been logged.  Reply with '!BuckFoat' to try and reverse this decision")      # Generic response
                Neurotic_Write(str(comment_var), tag)       # Record that we responded
                print("Found a " + tag + " post")           # Feedback to console for debug


