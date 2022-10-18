from datetime import *
import praw
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
import pytz
import time
from datetime import date
from operator import itemgetter

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
flair_id = '70c8af34-22f5-11ec-b8c2-6a9752c5302d'
commentInfo = []  # Creates an empty array`1

def morning_report(context: CallbackContext):
    date = str(datetime.now().month) + "/" + str(datetime.now().day) + "/" + str(datetime.now().year)
    title = 'The Daily Synapse for ' + date
    modUpdates = modChecker()
    traffic = stonky_yesterday()
    scores, comments = getScores()
    parsed = "**Post Karma Leaderboard**  \n\n" + parse_scores(scores)
    parsed2 = "**Comment Karma Leaderboard**  \n\n" + parse_comments(comments)
    body = traffic + "&#x200B;" + parsed + "&#x200B;" + parsed2 + modUpdates
    post = subreddit.submit(title=title, selftext=body, flair_id=flair_id)
    # context.bot.send_message(job.context, text=response)
    requests.get(sendURL_THCLab+"Made a post - " + post.id)


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
    timestamp = [datetime.now(), datetime.now() - timedelta(days=1)]
    # Big loop to find users and posts and scores
    for comment in commentList:  # Looks through all submissions in the subreddit, but only back 250 because limitations
        try:
            user = comment.author  # User is the post creator
            if str(user) == "None":
                pass  # If the post has no author, don't count it.
            created = datetime.fromtimestamp(comment.created)
            if created.month == timestamp[1].month and created.day == timestamp[1].day:
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



def stonky_yesterday():
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    traffic_data = subreddit.traffic()
    for day in traffic_data['day']:
        date = datetime.fromtimestamp(day[0]) + timedelta(days=1)
        if date.month == yesterday.month:
            if date.day == yesterday.day:
                visits = day[1]
                views = day[2]
                joined = day[3]
                statement = "\n\nUnique Sub Visits: " + str(visits) + "\n\nPage Views: " + str(views) + "\n\nNew Users Joined: " + str(joined) + "\n\n"
                response = "**Here's the sub's traffic report for yesterday to get you started.**\n\n \n\n" + statement
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
    info = []           # Creates an empty array
    commentInfo = []
    timestamp = [datetime.now(), datetime.now() - timedelta(days=1)]
    # Big loop to find users and posts and scores
    for submission in submissions:          # Looks through all submissions in the subreddit, but only back 250 because limitations
        user=submission.author              # User is the post creator
        if str(user)=="None":
            pass        # If the post has no author, don't count it.
        created = datetime.fromtimestamp(submission.created)
        if created.month == timestamp[1].month and created.day == timestamp[1].day:
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
    # debug_info = ""
    # for i in range (0,len(info)):
        # linkcount = info[i][2].count("https://reddit.com/r/")
        # debug_info = debug_info + "\n\nUser:  " + str(info[i][0]) + "\nKarma:  " + str(info[i][1]) + "\nLinks: " + str(linkcount) + "\n" + str(info[i][2])
    # reddit.redditor("BadApe-Bot").message("Debug Info", debug_info)
    return info, commentInfo# , debug_info

def parse_comments(comments):
    commentInfo = sorted(comments, key=itemgetter(1), reverse=True)  # Process the array of scores
    response = ""
    for user in commentInfo:
        response = response + "u/" + str(user[0]) + " - " + str(user[1]) + " comment karma\n\n"
    return response

def parse_scores(data):
    response = ""
    for entry in data:
        response = response + "u/" + str(entry[0]) + " - " + str(entry[1]) + " post karma\n\n"
    return response

def postMorningNews():
    date = str(datetime.now().month) + "/" + str(datetime.now().day) + "/" + str(datetime.now().year)
    title = 'The Daily Synapse for ' + date
    modUpdates = modChecker()
    traffic = stonky_yesterday()
    scores, comments = getScores()
    parsed = "**Post Karma Leaderboard**  \n\n" + parse_scores(scores)
    parsed2 = "**Comment Karma Leaderboard**  \n\n" + parse_comments(comments)
    body = traffic + "&#x200B;" + parsed + "&#x200B;" + parsed2 + modUpdates
    post = subreddit.submit(title=title, selftext=body, flair_id=flair_id)
    return post

def nsfwit(context):
    submissions = subreddit.new(limit=15)
    for submission in submissions:
        #if submission.title == "the mod censoring here is worse than at soupystock!":
            #submission.mod.remove(spam=True)
            #requests.get(sendURL_THCLab+"SPAMMED a Boat post - " + submission.permalink)
        user = submission.author
        if user == "VoodooMaster101":
            if submission.over_18 == False:
                submission.mod.nsfw()
                requests.get(sendURL_THCLab+"NSFW'd a Voodmaster post - " + submission.permalink)
        
def main():
    dp.add_handler(CommandHandler("help", help))
    print("Stonky Ape is online.")
    import datetime
    IST = pytz.timezone('America/New_York')
    t = datetime.time(9, 30)
    target_time = datetime.time(hour=9, minute=30).replace(tzinfo=IST)
    # job_queue.run_daily(morning_report, target_time, days=(0, 1, 2, 3, 4, 5, 6), context=None, name=None)
    # job_queue.run_repeating(nsfwit, 1)
    updater.start_polling()
    updater.idle()

main()