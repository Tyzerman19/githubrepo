import praw
import random
import time

# reddit account credentials
username = "effjayjay"
password = "bandit19"

reddit = praw.Reddit(
    client_id="yfGEKRS5QVRro-n28jPuWQ",
    client_secret="WGsNN5bGU6MtWqcB4Ri2EeiBM1hNVA",
    user_agent="<effjayjay 2.0>",
    username = username,
    password = password
)

# enter desired size and scale parameters
#example subs ~ ["mma", "ufc","mmamemes", "mmabetting", "thefighterandthekid", "joerogan", "sports", "martialarts", "mmagifs"]
subreddits_of_interest = ["mma",
                          "ufc"
                          ]
scanned_posts_per_subreddit = 100
number_of_comments = 10
total_submissions = scanned_posts_per_subreddit * len(subreddits_of_interest)
replies = ["lol Jon Jones is such a clown",
           "jon jones isn't what I would consider a good guy",
           "jon jones beats women",
           "I wouldn't trust Jon Jones to be around my family",
           "we may disagree on whether he is a good or bad guy but we can agree that Jon Jones is not the goat",
           "Jon Jones ain't my cup of tea, definitely NOT goat material",
           "jon jones is the goat, of doping",
           "it's almost hard to hate on Jon since he never fights organized matches, only exhibitions with his wife",
           "Jon Jones needs a timeout",
           "more like Gone Jones",
           "Jon Jokes is more like it",
           "eff Jon Jones, all my homies hate him",
           "I don't really like jon jones that much",
           "jon jones will never make a comeback",
           "jon jones couldn't beat his way out of a rhythm",
           "jon jones needs to lighten up",
           "jon jones is like a bad pimple at this point",
           "Jon Jones ugh",
           "get outta here with this jon jones nonsense",
           "get that jon talk outta here",
           "we don't take kindly to those that talk about jon jones",
           "We don't talk about Jon Jones here",
           "Send jon jones straight into the sun!",
           "I want to see jon jones fight on the moon",
           "Jon Jones the type of guy that would beat up your puppy",
           "Jon Jones was pretty good at fighting but he is not in goat contention. Just putting that out there.",
           "Jon Jones for president. Why not at this point"
           ]

# function scans existing comments and posts in submissions that this user has not posted in yet
def comment_poster():
    submissions_scanned = 0
    submissions_skipped = 0
    comments_scanned = 0
    comments_written = 0
    ignored_submissions = []
    print("Preparing to scan " + str(total_submissions) + " submissions and post up to " +
          str(number_of_comments) + " comments.")
    for i in range(len(subreddits_of_interest)):
        subreddit = reddit.subreddit(subreddits_of_interest[i])
        print("Reading comments from r/" + str(subreddits_of_interest[i]))
        print("*****")
        for submission in subreddit.hot(limit=scanned_posts_per_subreddit):
            author_list = []
            if comments_written < number_of_comments:
                submissions_scanned += 1
                if submissions_scanned % 50 == 0:
                    print("Number of submissions scanned: " + str(submissions_scanned))
                    print("Number of comments scanned: " + str(comments_scanned))
                    print("Number of replies written: " + str(comments_written))
                    print("--<3--")
                for comment in submission.comments:
                    comments_scanned += 1
                    if hasattr(comment, "author"):
                        author_list.append(str(comment.author))
                        for reply in comment.replies:
                            comments_scanned += 1
                            if hasattr(reply, "author"):
                                    author_list.append(str(reply.author))
                if username in author_list:
                    ignored_submissions.append(submission.title)
                    submissions_skipped += 1
                    print("PREVIOUSLY COMMENTED IN: " + str(submission.title))
                    print("...")
                if submission.title not in ignored_submissions:
                    for comment in submission.comments:
                        if hasattr(comment, "body"):
                            comment_lower = comment.body.lower()
                            if "jon jones" in comment_lower:
                                random_index = random.randint(0, len(replies) - 1)
                                reply_comment = replies[random_index]
                                comment.reply(str(reply_comment))
                                comments_written += 1
                                print("Submission title: " + str(submission.title))
                                print("Comment body: " + str(comment.body))
                                print("Replied with: " + str(reply_comment))
                                print("-----")
                                print("Sleeping for 5 seconds..")
                                ignored_submissions.append(submission.title)
                                time.sleep(5)
                                print("Finished sleeping.")
                                break
    print("Task summmary")
    print("Number of submissions skipped: " + str(submissions_skipped))
    print("Number of submissions scanned: " + str(submissions_scanned))
    print("Number of comments scanned: " + str(comments_scanned))
    print("Total replies written: " + str(comments_written))
    print("Task completed: Fuck Jon Jones")

comment_poster()