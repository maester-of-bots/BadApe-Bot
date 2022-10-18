import requests


flair_id = '70c8af34-22f5-11ec-b8c2-6a9752c5302d'
commentInfo = []  # Creates an empty array`1



# Pull the data for the morning report, and post it to Reddit
def morning_report():
    date = str(datetime.now().month) + "/" + str(datetime.now().day) + "/" + str(datetime.now().year)   # Get the date for the title
    title = 'The Weekly Synapse for ' + date                                                             # Make the title
    modUpdates = modChecker()                                                                           # Check and see if there are any mod updates
    traffic = stonky_traffic()                                                                        # Get the traffic
    scores, comments = getScores()                                                                      # Get post karma and comment karma
    parsed = "**Post Karma Leaderboard**  \n\n" + parse_scores(scores)                                  # Format the post karma
    parsed2 = "**Comment Karma Leaderboard**  \n\n" + parse_comments(comments)                          # Format the comment karma
    body = traffic + "&#x200B;" + parsed + "&#x200B;" + parsed2 + modUpdates                            # Create the post's body
    post = subreddit.submit(title=title, selftext=body, flair_id=flair_id)                              # Post to Reddit.
    requests.get(sendURL_THCLab+"Made a post - " + post.id)                                             # Double announce the post because why not


def main():
    date = str(datetime.now().month) + "/" + str(datetime.now().day) + "/" + str(datetime.now().year)
    title = 'The Weekly Synapse for ' + date
    modUpdates = modChecker()
    traffic = stonky_traffic()
    scores, comments = getScores()
    parsed = "**Post Karma Leaderboard**  \n\n" + parse_scores(scores)
    parsed2 = "**Comment Karma Leaderboard**  \n\n ^[Note, ^you ^must ^have ^10 ^or ^more ^total ^comment ^karma ^for ^the ^last ^week ^to ^be ^listed]\n\n" + parse_comments(
        comments)
    body = traffic + "&#x200B;" + parsed + "&#x200B;" + parsed2 + modUpdates
    post = subreddit.submit(title=title, selftext=body, flair_id=flair_id)
    return post


main()