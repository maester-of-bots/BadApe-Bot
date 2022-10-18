import praw
from operator import itemgetter
from datetime import datetime

# Authenticate to Reddit
reddit = praw.Reddit(
    client_id="",
    client_secret="",
    password="",
    user_agent="Bad Ape 1.0",
    username="BadApe-Bot",
    check_for_async=False
)

target_sub = "stonkymemes"  # Where the bot looks for the words
subreddit = reddit.subreddit(target_sub)  # Making the code look prettier.


###########################################
############      Meltdown     ############
###########################################


# Calculate a user's score based on Meltdown history
def meltdownCalc(username):
    f = open("log.txt", "a")
    f.write(username + "\n")
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
    if username=="narry":
        meltdownScore = 360694200
        meltPosts = 360690000
        meltComments = 4200
    meltdownScore = "r/gme_meltdown activity for " + str(username) + "\n\nShillScore(tm):  " + str(meltdownScore)
    meltPosts = "Post Karma:  " + str(meltPosts)
    meltComments = "Comment Karma:  " + str(meltComments)
    response = meltdownScore + "\n" + meltPosts + "\n" + meltComments
    return response



# Get Meltdown Scores
def getScores(subreddit,timerange,limit):
    submissions = subreddit.top(timerange,limit=limit)      # Pull all submissions from the top posts of the sub
    info = []                                               # Initialize Info array
    for submission in submissions:                          # Big loop to find users and posts and scores
        user=submission.author                                  # Figure out the user who submitted the post
        link = "https://reddit.com" + submission.permalink

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

def meltDatabase(subreddit, timerange, limit):
        submissions = subreddit.top(timerange, limit=limit)  # Pull all submissions from the top posts of the sub
        info = []  # Initialize Info array
        for submission in submissions:  # Big loop to find users and posts and scores
            user = submission.author  # Figure out the user who submitted the post
            if user == "None":  # Skip posts with No users.
                pass
            else:
                now = datetime.now().strftime('%m')  # Date Fuckery
                month = datetime.utcfromtimestamp(int(submission.created)).strftime('%m')
                if timerange == "all":  # I don't even remember what this does
                    now = month
                if now == month:
                    if info == []:  # If no posts have been added yet, append the first user
                        info.append([user, submission.score])
                    else:
                        found = False
                        for i in range(0, len(info)):
                            if user == info[i][0]:  # Search through the info array to see if the username exists.
                                found = True
                                info[i][1] = info[i][1] + submission.score  # Add the score to that user's score
                        if found == False:
                            info.append(
                                [user, submission.score])  # Add that user and their base score to the info array
            for top_level_comment in submission.comments:  # Now run through the comments...this is ugly...
                try:
                    if str(top_level_comment.author) == "None":
                        pass
                    else:
                        score = submission.score  # Grab the score
                        now = datetime.now().strftime('%m')  # More date fuckery
                        month = datetime.utcfromtimestamp(int(submission.created)).strftime('%m')
                        if timerange == "all":
                            now = month
                        if now == month:
                            if info == []:
                                info.append([top_level_comment.author,
                                             score])  # If no posts have been added yet, append the first user
                            else:
                                found = False
                                for i in range(0, len(info)):
                                    if top_level_comment.author == info[i][
                                        0]:  # Search through the info array to see if the username exists.   or
                                        found = True
                                        info[i][1] = info[i][1] + score  # Add the score to that user's score,
                                if found == False:
                                    info.append([top_level_comment.author,
                                                 score])  # Add that user and their base score to the info array
                except:
                    pass  # If something breaks...fuck it lol
        info = sorted(info, key=itemgetter(1), reverse=True)  # Sort all the info, inverse it.
        return info


def makeTable(info):
    table = []
    for i in range(0,len(info)):
        user="u/"+str(info[i][0])
        score=str(info[i][1])
        number="#"+str(i+1)
        row=number+".) "+user+" - "+score+"\n"
        table.append(row)
    timed = datetime.now().strftime("%H:%M:%S")
    status = "\n\n"+"Last updated: Today at "+timed
    Header = 'Yzri is annoying.\n\n'
    if len(table)>100:
        x=101
    else:
        x=len(table)
    for i in range(0,x):
        Header = Header + table[i]
    table = Header+status
    return table


def getSubComments(comment, allComments, verbose=True):
  allComments.append(comment)
  if not hasattr(comment, "replies"):
    replies = comment.comments()
    if verbose: print("fetching (" + str(len(allComments)) + " comments fetched total)")
  else:
    replies = comment.replies
  for child in replies:
    getSubComments(child, allComments, verbose=verbose)


def getAll(r, submissionId, verbose=True):
  submission = r.submission(submissionId)
  comments = submission.comments
  commentsList = []
  for comment in comments:
    getSubComments(comment, commentsList, verbose=verbose)
  return commentsList


def getCommentsMain(submission_id):
    global commentInfo
    commentList = getAll(reddit, submission_id)
    # Big loop to find users and posts and scores
    for comment in commentList:  # Looks through all submissions in the subreddit, but only back 250 because limitations
        try:
            user = comment.author  # User is the post creator
            if str(user) == "None":
                pass  # If the post has no author, don't count it.
            score = comment.score  # Get the score of the post
            if commentInfo == []:  # If no posts have been added yet, append the first user
                commentInfo.append([user, score])
            else:
                found = False
                # Search through the info array to see if the username exists.
                for i in range(0, len(commentInfo)):
                    if user == commentInfo[i][0]:
                        found = True
                        commentInfo[i][1] = commentInfo[i][1] + score
                        commentInfo[i][2] = commentInfo[i][2]  # add that user and their base score to the info array
                if found == False:
                    commentInfo.append([user, score])  # Add the score to that user's score, or
        except:
            pass

def stonky_traffic():
    traffic_data = subreddit.traffic()          # Get traffic data
    traffic_array = [0,0,0]
    for day in traffic_data['day'][0:7]:             # Go through traffic data...
        print(day)
        traffic_array[0] = traffic_array[0] + day[1]
        traffic_array[1] = traffic_array[1] + day[2]
        traffic_array[2] = traffic_array[2] + day[3]
    statement = "\n\nUnique Sub Visits: " + str(traffic_array[0]) + "\n\nPage Views: " + str(traffic_array[1]) + "\n\nNew Users Joined: " + str(traffic_array[2]) + "\n\n"
    response = "**Here's the sub's traffic report for this past week to get you started.**\n\n\n\n" + statement
    return response

def modWriter():
    f = open("mods.txt", "w")
    for moderator in subreddit.moderator():
        f.write(str(moderator) + "\n")
    f.close()

def modReader():
    # Pull recorded mod data
    f = open("mods.txt", "r")
    list_saved = (f.read()).split("\n")
    while '' in list_saved:
        list_saved.remove('')
    f.close()
    return list_saved

def modGetter():
    list_current = []
    for moderator in subreddit.moderator():
        list_current.append(str(moderator))
    return list_current

def modChecker():
    list_saved = modReader()
    list_current = modGetter()
    # Check to see if there were any mod changes
    mods_removed = [x for x in list_saved if x not in list_current]
    mods_added = [x for x in list_current if x not in list_saved]
    mod_response = ""
    if mods_removed != []:
        removed_text = "**MODERATOR DEPARTURES**\n\n\n"
        for mod in mods_removed:
            removed_text = removed_text + mod + "\n\n"
        mod_response = removed_text
    if mods_added != []:
        added_text = "**MODERATOR ADDITIONS**\n\n\n"
        for mod in mods_added:
            added_text = added_text + mod + "\n\n"
        mod_response = mod_response + added_text
    modWriter()
    return mod_response

def getScores():
    global commentInfo
    submissions = subreddit.top("week",limit=11111110)          # Gets the top 250 posts
    info = []                                                   # Creates an empty array
    commentInfo = []
    # Big loop to find users and posts and scores
    for submission in submissions:          # Looks through all submissions in the subreddit, but only back 250 because limitations
        user=submission.author              # User is the post creator
        if str(user)=="None":
            pass        # If the post has no author, don't count it.
        postlink = "https://reddit.com" + str(submission.permalink)
        score=submission.score          # Get the score of the post
        if info == []:              # If no posts have been added yet, append the first user
            info.append([user,score, postlink])
        else:
            found=False
            # Search through the info array to see if the username exists.
            for i in range(0,len(info)):
                if user==info[i][0]:
                    found=True
                    info[i][1] = info[i][1] + score
                    info[i][2] = info[i][2] + "\n" + postlink       # add that user and their base score to the info array
            if found==False:
                info.append([user,score, postlink])                 # Add the score to that user's score, or
        getCommentsMain(submission.id)
    info = sorted(info, key=itemgetter(1),reverse=True)                 # Process the array of scores
    commentInfo = sorted(commentInfo, key=itemgetter(1),reverse=True)                 # Process the array of scores
    debug_info = ""
    for i in range (0,len(info)):
        linkcount = info[i][2].count("https://reddit.com/r/")
        debug_info = debug_info + "\n\nUser:  " + str(info[i][0]) + "\nKarma:  " + str(info[i][1]) + "\nLinks: " + str(linkcount) + "\n" + str(info[i][2])
    # reddit.redditor("BadApe-Bot").message("Debug Info", debug_info)
    return info, commentInfo# , debug_info

def parse_comments(comments):
    commentInfo = sorted(comments, key=itemgetter(1), reverse=True)  # Process the array of scores
    response = ""
    for user in commentInfo:
        if user[1] >= 10:
            response = response + "u/" + str(user[0]) + " - " + str(user[1]) + " comment karma\n\n"
    return response

def parse_scores(data):
    response = ""
    for entry in data:
        response = response + "u/" + str(entry[0]) + " - " + str(entry[1]) + " post karma\n\n"
    return response