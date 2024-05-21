import tweepy
from chat import make_chat

authToken = "token here";
accountHandles = [];

#tweet listener behavior must be defined in subclass
class TweetHandler(tweepy.StreamingClient):

    def on_tweet(self, tweet):
        tweetText = tweet.text
        print(f"{tweet.id} {tweet.created_at} ({tweet.author_id}): {tweetText}")
        if tweet.in_reply_to_user_id != None:
            queryString = "Summarize the following tweet from "+api.get_user(tweet.id).screen_name+"in response to "+api.get_user(tweet.in_reply_to_user_id).screen_name+": \n"
        else:
            queryString = "Summarize the following tweet from "+api.get_user(tweet.id).screen_name+": \n"
        queryString += tweetText
        #call gpt query
        make_chat(queryString)


if __name__ == "__main__":

    try:
        auth = tweepy.OAuth2BearerHandler(authToken)
        api = tweepy.API(auth)
    except Exception as e:
        print("Error: " + str(e))

    ruleString = "from: "
    keep_running = True
    tweetContent = ""

    #open twitter_account.txt file and scan names of people to follow
    with open ("./twitter_account.txt","r") as followAccounts:
        for iterated in followAccounts:
            accountHandles += iterated,

    followAccounts.close()


    #create a stream and listen for followed accounts
    tweetToGPT = TweetHandler(authToken)
    lastAcc = accountHandles.pop()
    for name in accountHandles:
        ruleString += name
        ruleString += " OR "
    accountHandles += lastAcc

    tweetToGPT.add_rules(tweepy.StreamRule(ruleString))
    tweetToGPT.filter()
    #loop to keep script running
    print('Type "quit" to exit: \n')
    while(keep_running):
        toExit = input()
        if toExit == "quit":
            keep_running = False


