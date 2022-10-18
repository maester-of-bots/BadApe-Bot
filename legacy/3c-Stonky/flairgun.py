tags = ["meta", "gme", "meltie", "deadmemes", "toilet", "buckfoat", "popcorn"]
commands = ["!flairmod","!grantflair","meta", "gme", "meltie", "deadmemes", "toilet", "buckfoat", "popcorn"]

from sql import *
from reddit import *

def anal(comment):
    for tag in tags:                                # Read through each of the tags above
        postlist = []                               # Create a list for the posts
        posts = Neurotic_Read(tag)                  # Read in posts that match the tag from the DB
        comment_var = str(comment.body).lower()     # Give the comment text a variable to clean up the code
        for post in posts:                          # Data is stupid, gotta extract it, this is probably the least-efficient way
            postlist.append(post[0])                # Add the post to the post list.  Again, not an efficient way to do it.
        if comment_var == ("!" + tag) and comment not in postlist:          # If it's a tag, and the comment hasn't been responded to
            if comment_var == "!buckfoat":                                  # Seriously tho
                comment.reply("If you shave a boat, is it still a boat?")   # Can probably make a pool to choose from
                Neurotic_Write(str(comment), tag)                       # Record that we responded
                print("Boat comment was not in DB, submission is " + str(comment.submission))       # Feedback to console for debug
            else:   # If it isn't buckfoat...
                if comment not in postlist:
                    comment.reply("Apparently this is a " + tag + " post, and it's been logged.  Reply with '!BuckFoat' to try and reverse this decision")      # Generic response
                    Neurotic_Write(str(comment), tag)       # Record that we responded
                    print("Found a " + tag + " post")           # Feedback to console for debug


def flairGun_check(comment):
    modList, commentList = sqlite_load_all()
    commentList2 = []
    modList2 = []
    comment_body = (comment.body).lower()
    comment_parent = str(comment.parent())
    comment_author = str(comment.author)
    for x in modList:
        modList2.append(x[0])
    for x in commentList:
        commentList2.append(x[0])
    if str(comment) not in commentList2:
        if (comment_body[0:9]) == "!flairmod" and comment.parent().author not in modList2 and comment_author in modList2:
            if len(modList2) <= 8:
                flairmod_write(str(comment.parent().author), comment_author, str(comment))
                comment.reply("Admin access to flairs granted.")
                print("Admin access to flairs granted.")
            else:
                print("Sorry, it looks like our Flair Mod slots are all full.")
                comment.reply("Sorry, it looks like our Flair Mod slots are all full.")
                flaircomment_write(str(comment.author), datetime.now(), str(comment))
        elif (comment_body[0:9]) == "!flairmod" and comment.parent().author not in modList2 and comment_author not in modList2:
            comment.reply("Ah ah ah, you didn't say the magic word.")
            flaircomment_write(str(comment.author), datetime.now(), str(comment))
        elif (comment_body[0:9]) == "!flairmod" and comment.parent().author in modList2 and comment_author in modList2:
            comment.reply("That user is already a mod, dingus.")
            print("Already a mod")
            flaircomment_write(str(comment.author), datetime.now(), str(comment))
        if (comment_body[0:11]) == "!grantflair" and str(comment) not in commentList2:
            if "faggot" in comment_body or "nigger" in comment_body or "meaniefacefacist" in comment_body:
                comment.reply("Do you kiss your mother with that mouth, you Oedipal degenerate?")
                comment.delete()
                flaircomment_write(str(comment.author), datetime.now(), str(comment))
            else:
                if comment.author in modList2:
                    text = ((comment.body).split("!grantflair "))[1]
                    flaircomment_write(str(comment.author), datetime.now(), str(comment))
                    subreddit.flair.set(str(comment.parent().author), text)
                    comment.reply("Flair changed.  Probably.")
                    response = str(comment.author) + " changed " + str(comment.parent().author) + "'s flair to " + text
                    # discord_init(response)
                    print(response)
                else:
                    comment.reply("Ah ah ah, you didn't say the magic word.")
                    flaircomment_write(str(comment.author), datetime.now(), str(comment))
    else:
        pass