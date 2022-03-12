import tweepy
import os

auth = tweepy.OAuthHandler("WlRLfqVaCAvvmjS0BcMq5FA3z", "Ey7Ox6wAsxK6XVqgU0QblwG6ANPgDCmNolnJlbKNMzwvi53zrM")
auth.set_access_token("1416406932752003074-TFckE4beTrZ3aaGl5ay2filcmjpjqx",
                      "0z2kAQ3JEq16Q17aX78oAPOmRQpts8OBZDLEbnyKD16I8")

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

main_dir = r"D:\Docs\Code\Python\tweepy"


def GetInfo(user):
    print(
        f"\n--------------------------------------------------------------------------------------------------\nUser Details:\n")

    x = f'https://twitter.com/{user.screen_name}'
    print(
        f'URL: {x}\nUsername: {user.screen_name}\nUserID: {user.id}\nName: {user.name}\nLocation: {user.location}\nFollower Count: {user.followers_count}\nFollowing Count: {user.friends_count}\nAccount Created: {user.created_at}\nVerified: {user.verified}\nProfile Image: {user.profile_image_url_https.replace("_normal.","_400x400.")}\nDescription:\n{user.description}\n--------------------------------------------------------------------------------------------------\n')


def GetFirstFollowers(Usernamestr, api, main_dir):
    try:
        user = api.get_user(Usernamestr)
        GetInfo(user)
        tweet_this = f"fetching {user.screen_name}'s followers ids"
        try:
            api.update_status(tweet_this)
        except:
            print("Duplicate Tweet, skipping")

        user_dir = os.path.join(main_dir, user.screen_name)
        try:
            os.makedirs(user_dir)
        except:
            print("folder already exists")
        filename = os.path.join(user_dir, "followers.txt")

        f = open(filename, 'w')
        for x in tweepy.Cursor(api.followers_ids, user.screen_name).pages():
            for i in x:
                f.write(f'{i}\n')

        print("fetching success\n")
        tweet_this = f"follower list of {user.screen_name} acquired successfully!"
        api.update_status(tweet_this)
        f.close()
        return user_dir
    except:
        print("Some Error Occurred :(")



def GetSecFollowers(api, user_dir):
    foll = os.path.join(user_dir, "followers.txt")
    mainfile = open(foll, 'r')
    for id in mainfile.readlines():
        str = id.replace('\n', '') + ".txt"
        filename = os.path.join(user_dir, str)
        try:
            user = api.get_user(id)
            f = open(filename, 'w')
            for x in tweepy.Cursor(api.followers_ids, user.screen_name).pages():
                for i in x:
                    f.write(f'{i}\n')
                f.close()
        except:
            print(f'Some error occurred with user with userid: {id}')
    mainfile.close()
    print("second followers fetched")


def GetThirdFollowerCount(api, user_dir):
    foll = os.path.join(user_dir, "followers.txt")
    mainfile = open(foll, 'r')
    for id in mainfile.readlines():
        existing = id.replace('\n', '') + ".txt"
        newstr = id.replace('\n', '') + "BenfordData.txt"
        filename = os.path.join(user_dir, existing)
        thirdfollower= os.path.join(user_dir, newstr)

        secfile = open(filename, 'r')

        print("in third function!")
        for secid in secfile.readlines():
            secfollid = secid.replace('\n', '')
            thirdfile = open(thirdfollower, 'a')
            try:
                secuser = api.get_user(secfollid)
                follcnt = str(secuser.followers_count)
                #print(follcnt)
                thirdfile.write(f"{follcnt[0]}\n")  #use 'with' to reduce time.
                thirdfile.close()

            except:
                print(f'Some error occurred with user with userid: {secid}')

        secfile.close()


    mainfile.close()


Usernamestr = input("Enter Twitter Username/UserID: ")
User_dir = GetFirstFollowers(Usernamestr, api, main_dir)
GetSecFollowers(api, User_dir)

GetThirdFollowerCount(api, User_dir)
print("Done!")
