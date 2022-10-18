from flask import render_template, request, redirect
from app import app

import praw
from operator import itemgetter
from datetime import datetime


reddit = praw.Reddit(
    client_id="",
    client_secret="",
    password="",
    user_agent="Bad Ape 1.0",
    username="BadApe-Bot",
)

def getScores(subreddit,timerange,limit):
    submissions = subreddit.top(timerange,limit=limit)      # Pull all submissions from the top posts of the sub
    info = []                                               # Initialize Info array
    for submission in submissions:                          # Big loop to find users and posts and scores
        user=submission.author                                  # Figure out the user who submitted the post
        if str(submission.author)=="None":                                   # Skip posts with No users.
            pass
        else:
            now = datetime.now().strftime('%m')                 # Date Fuckery
            month = datetime.utcfromtimestamp(int(submission.created)).strftime('%m')
            if timerange=="all":                                # I don't even remember what this does
                now=month
            if now==month:
                if info == []:                                  # If no posts have been added yet, append the first user
                    info.append([user,submission.score])
                else:
                    found=False
                    for i in range(0,len(info)):
                        if user==info[i][0]:                    # Search through the info array to see if the username exists.
                            found=True
                            info[i][1] = info[i][1] + submission.score     # Add the score to that user's score
                    if found==False:
                        info.append([user,submission.score])               # Add that user and their base score to the info array
        for top_level_comment in submission.comments:               # Now run through the comments...this is ugly...
            try:
                if str(top_level_comment.author)=="None":
                    pass
                else:
                    score=submission.score                          # Grab the score
                    now = datetime.now().strftime('%m')             # More date fuckery
                    month = datetime.utcfromtimestamp(int(submission.created)).strftime('%m')
                    if timerange=="all":
                        now=month
                    if now==month:
                        if info == []:
                            info.append([top_level_comment.author,score])               # If no posts have been added yet, append the first user
                        else:
                            found=False
                            for i in range(0,len(info)):
                                if top_level_comment.author==info[i][0]:                # Search through the info array to see if the username exists.   or
                                    found=True
                                    info[i][1] = info[i][1] + score     # Add the score to that user's score,
                            if found==False:
                                info.append([top_level_comment.author,score])           # Add that user and their base score to the info array
            except:
                pass                                                # If something breaks...fuck it lol
    info = sorted(info, key=itemgetter(1),reverse=True)             # Sort all the info, inverse it.
    return info                                                     # Return shit


def makeTable(info):
    table = []
    for i in range(0,len(info)):                        # Do this for every item in the array
        user="u/"+str(info[i][0])                       # Format the username
        score=str(info[i][1])                           # Format the score
        number="#"+str(i+1)                             # Format their number
        row=number+".) "+user+" - "+score+"\n"          # Create the row
        table.append(row)                               # Add the row to the table.  I should make a DB.
    timed = datetime.now().strftime("%H:%M:%S")         # TIME FUCKERY
    status = "\n\n"+"Last updated: Today at "+timed     # Status at the bottom
    table = table+status                               # Oh, wait, can I get rid of this?
    return table

def generateLeaderboard():
    try:
        f = open("leaderboard.txt", "r")
        leaderboard = f.read()
    except:
        alltime = makeTable(getScores(reddit.subreddit("gme_meltdown"), "month", 10000))
        f = open("leaderboard.txt", "a")
        f.write(alltime)
        f.close()
        leaderboard = alltime
    print(leaderboard)


def meltdownCalc(username):
    f = open("log.txt", "a")
    f.write(username)
    f.close()
    meltdownScore = 0  # Start post count at 0
    meltComments = 0
    meltPosts = 0
    for submission in reddit.redditor(username).submissions.top(limit=None):  # This caps at 1,000
        if str(submission.subreddit).lower() == "gme_meltdown":
            meltdownScore += submission.score  # Then it is a good post
            meltPosts += submission.score
    for comment in reddit.redditor(username).comments.top(limit=None):
        if "/r/gme_meltdown/" in comment.permalink.lower():
            if comment.score > 0:
                meltdownScore += comment.score
                meltComments += comment.score
    meltdownScore = "r/gme_meltdown activity for " + str(username) + "\n\nShillScore(tm):  " + str(meltdownScore)
    meltPosts = "Post Karma:  " + str(meltPosts)
    meltComments = "Comment Karma:  " + str(meltComments)
    return meltdownScore, meltPosts, meltComments

# generateLeaderboard()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form.to_dict()
        meltdownScore, meltPosts, meltComments = meltdownCalc(data['Name'])
    else:
        meltdownScore=""
        meltPosts=""
        meltComments=""

    return render_template('index.html', title='ShillScore', response=meltdownScore, meltPosts=meltPosts,meltComments=meltComments)

@app.route('/about.html')
def about():
    return render_template('about.html')
