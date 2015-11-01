#!/usr/bin/env python
# encoding: utf-8
"""
Tweet a random line from a text file.
For example, use it to tweet a random six-word sentence from Project Gutenberg.
https://twitter.com/sixworderbot
"""
from __future__ import print_function, unicode_literals

try:
    import resource
    mem0 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024*1024.0)
except ImportError:
    # resource not on Windows
    pass

import argparse
import random
import sys
import twitter
import webbrowser
import yaml

TWITTER = None

SEPERATORS = [" ", " ", " ", " ", "\n", "\n", "\n\n"]


# cmd.exe cannot do Unicode so encode first
def print_it(text):
    print(text.encode('utf-8'))


def timestamp():
    if args.quiet:
        return
    import datetime
    print(datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"))


def load_yaml(filename):
    """
    File should contain:
    consumer_key: TODO_ENTER_YOURS
    consumer_secret: TODO_ENTER_YOURS
    access_token: TODO_ENTER_YOURS
    access_token_secret: TODO_ENTER_YOURS
    """
    f = open(filename)
    data = yaml.safe_load(f)
    f.close()
    if not data.viewkeys() >= {
            'access_token', 'access_token_secret',
            'consumer_key', 'consumer_secret'}:
        sys.exit("Twitter credentials missing from YAML: " + filename)

    return data


def get_twitter():
    global TWITTER

    if TWITTER is None:
        data = load_yaml(args.yaml)

        # Create and authorise an app with (read and) write access at:
        # https://dev.twitter.com/apps/new
        # Store credentials in YAML file
        TWITTER = twitter.Twitter(auth=twitter.OAuth(
            data['access_token'],
            data['access_token_secret'],
            data['consumer_key'],
            data['consumer_secret']))

    return TWITTER


def get_random_sentence_from_file():
    with open(args.infile) as f:
        lines = f.read().splitlines()

    return random.choice(lines)


def tweet_it(string, in_reply_to_status_id=None):
    global TWITTER

    if len(string) <= 0:
        print("ERROR: trying to tweet an empty tweet!")
        return

    t = get_twitter()

    if not args.quiet:
        print_it("TWEETING THIS: " + string)

    if args.test:
        if not args.quiet:
            print("(Test mode, not actually tweeting)")
    else:
        if not args.quiet:
            print("POST statuses/update")
        result = t.statuses.update(
            status=string,
            in_reply_to_status_id=in_reply_to_status_id)
        url = "http://twitter.com/" + \
            result['user']['screen_name'] + "/status/" + result['id_str']
        if not args.quiet:
            print("Tweeted: " + url)
        if not args.no_web:
            webbrowser.open(url, new=2)  # 2 = open in a new tab, if possible


def get_random_hashtag():
    # CSV string to list
    hashtags = args.hashtags.split(",")
    # Replace "None" with None
    hashtags = [None if x == "None" else x for x in hashtags]
    # Return a random hashtag
    return random.choice(hashtags)


def main():
    random_sentence = get_random_sentence_from_file()
    print(random_sentence)

    hashtag = get_random_hashtag()
    if not hashtag:
        tweet = random_sentence
    else:
        # 50% lowercase hashtag
        if random.randint(0, 1) == 0:
            hashtag = hashtag.lower()
        # Random order of text and hashtag
        things = [hashtag, random_sentence]
        random.shuffle(things)
        if not args.quiet:
            print(">"+" ".join(things)+"<")
        # Random separator between text and hashtag
        tweet = random.choice(SEPERATORS).join(things)

    if not args.quiet:
        print(">"+tweet+"<")
        print("Tweet this:\n", tweet)

    try:
        tweet_it(tweet)

    except twitter.api.TwitterHTTPError as e:
        print("*"*80)
        print(e)
        print("*"*80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Tweet a random line from a text file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-y', '--yaml',
        default='/Users/hugo/Dropbox/bin/data/randomsentencebot.yaml',
        # default='E:/Users/hugovk/Dropbox/bin/data/randomsentencebot.yaml',
        help="YAML file location containing Twitter keys and secrets")
    parser.add_argument(
        '-i', '--infile',
        default='/Users/hugo/Dropbox/bots/six-worders12.txt',
        # default='E:/Users/hugovk/Dropbox/bots/six-worders12.txt',
        help="A random line is chosen from this text file")
    parser.add_argument(
        '--hashtags',
        default="#SixWordStories,#SixWordStory,#6WordStory,#6WordStories,None",
        help="Comma-separated list of random hashtags")
    parser.add_argument(
        '-nw', '--no-web', action='store_true',
        help="Don't open a web browser to show the tweeted tweet")
    parser.add_argument(
        '-x', '--test', action='store_true',
        help="Test mode: go through the motions but don't update anything")
    parser.add_argument(
        '-q', '--quiet', action='store_true',
        help="Only print out tweet (and errors)")
    args = parser.parse_args()

    timestamp()
    main()

# End of file
