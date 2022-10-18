from dotenv import load_dotenv
import praw
from operator import itemgetter
from datetime import datetime

load_dotenv()                               # This is for .env loading
# Would you be able to make bad ape display for the top 5 posters their highest post score, their average post score, and their total posts?

commentInfo = []  # Creates an empty array`1
flair_id = '70c8af34-22f5-11ec-b8c2-6a9752c5302d'

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
                commentInfo.append([user, score, 1])
            else:
                found = False
                # Search through the info array to see if the username exists.
                for i in range(0, len(commentInfo)):
                    if user == commentInfo[i][0]:
                        found = True
                        commentInfo[i][1] = commentInfo[i][1] + score
                        commentInfo[i][2] = commentInfo[i][2] + 1 # add that user and their base score to the info array
                if found == False:
                    commentInfo.append([user, score, 1])  # Add the score to that user's score, or
        except:
            pass

def stonky_traffic():
    traffic_data = subreddit.traffic()          # Get traffic data
    traffic_array = [0,0,0]
    for day in traffic_data['day'][0:7]:             # Go through traffic data...
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

def getScores_old():
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
        score=submission.score          # Get the score of the post
        if info == []:              # If no posts have been added yet, append the first user
            info.append([user,score, 1])
        else:
            found=False
            # Search through the info array to see if the username exists.
            for i in range(0,len(info)):
                if user==info[i][0]:
                    found=True
                    info[i][1] = info[i][1] + score
                    info[i][2] = info[i][2] + 1       # add that user and their base score to the info array
            if found==False:
                info.append([user,score, 1])                 # Add the score to that user's score, or
        getCommentsMain(submission.id)
    info = sorted(info, key=itemgetter(1),reverse=True)                 # Process the array of scores
    commentInfo = sorted(commentInfo, key=itemgetter(1),reverse=True)                 # Process the array of scores
    return info, commentInfo

def parse_comments(comments):
    commentInfo = sorted(comments, key=itemgetter(1), reverse=True)  # Process the array of scores
    response = ""
    for user in commentInfo:
        if user[1] >= 10:
            response = response + "u/" + str(user[0]) + " - " + str(user[1]) + " comment karma, " + str(user[2]) + " comments. (" + str(round(user[1]/user[2],2)) + " average karma per comment)\n\n"
    return response

def parse_scores(data):
    response = ""
    for entry in data:
        if entry[1] >= 10:
            response = response + "u/" + str(entry[0]) + " - " + str(entry[1]) + " post karma, " + str(entry[2]) + " posts. (" + str(round(entry[1]/entry[2],2)) + " average karma per post)\n\n"
    return response

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


# Pull the data for the morning report, and post it to Reddit
def main():
    title = 'The Weekly Synapse for ' + str(datetime.now().month) + "/" + str(datetime.now().day) + "/" + str(datetime.now().year)  # Make the title
    print("Checking mods.")
    modUpdates = modChecker()
    print("Checking traffic.")                                                                           # Check and see if there are any mod updates
    traffic = stonky_traffic()
    print("Getting scores.")                                                                           # Get the traffic
    scores, comments = getScores()                                                                          # Get post karma and comment karma
    print("Parsing data.")
    parsed = "**Post Karma Leaderboard**  \n\n" + parse_scores(scores)                                      # Format the post karma
    parsed2 = "**Comment Karma Leaderboard**  \n\n" + parse_comments(comments)                              # Format the comment karma
    body = traffic + "&#x200B;" + parsed + "&#x200B;" + parsed2 + modUpdates                                # Create the post's body
    # subreddit = reddit.subreddit("stonkyBOTS")
    print("Making post.")
    # dailynews = subreddit.submit(title=title, selftext=body, flair_id=flair_id)                             # Post to Reddit.
    dailynews = subreddit.submit(title=title, selftext=body)                             # Post to Reddit.
    dailynews.mod.distinguish(how="yes", sticky=True)

main()