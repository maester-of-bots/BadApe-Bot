import logging

import pytz
import time
from datetime import date

#Configure log file
logging.basicConfig(
     filename='badape.log',
     level=logging.DEBUG,
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )


# import datetime
# IST = pytz.timezone('America/New_York')
# target_time = datetime.time(hour=9, minute=30).replace(tzinfo=IST)
# job_queue.run_daily(morning_report, target_time, days=['0'], context=None, name=None)
# job_queue.run_repeating(nsfwit, 1)
# updater.start_polling()
# updater.idle()

# Lets HealthChecker know that we're online
def healthChecker():
    import requests
    url='https://hc-ping.com/d0b2fa0b-7c61-44eb-9c3f-ae731532e8ce'
    requests.get(url)

def nsfwit(context):
    submissions = subreddit.new(limit=15)
        for submission in submissions:
            if submission.title == "the mod censoring here is worse than at soupystock!":
            submission.mod.remove(spam=True)
            requests.get(sendURL_THCLab+"SPAMMED a Boat post - " + submission.permalink)
            user = submission.author
            if user == "VoodooMaster101":
                if submission.over_18 == False:
                    submission.mod.nsfw()
                    requests.get(telegram_THCHousehold+"NSFW'd a Voodmaster post - " + str(submission.permalink))
