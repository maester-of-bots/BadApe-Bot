from datetime import *
import praw
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
    submissions = subreddit.top("week",limit=11111110)          # Gets the top 250 posts
    info = []           # Creates an empty array
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
    info = sorted(info, key=itemgetter(1),reverse=True)                 # Process the array of scores
    debug_info = ""
    for i in range (0,len(info)):
        linkcount = info[i][2].count("https://reddit.com/r/")
        debug_info = debug_info + "\n\nUser:  " + str(info[i][0]) + "\nKarma:  " + str(info[i][1]) + "\nLinks: " + str(linkcount) + "\n" + str(info[i][2])
    reddit.redditor("BadApe-Bot").message("Debug Info", debug_info)
    return info, debug_info

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
    scores, debug_info = getScores()
    parsed = "**Here's some folks with the most karma from posts yesterday - if there were any.**  \n\n" + parse_scores(scores)
    body = traffic + "&#x200B;" + parsed + "&#x200B;" + modUpdates
    post = subreddit.submit(title=title, selftext=body, flair_id=flair_id)
    return post



postMorningNews()