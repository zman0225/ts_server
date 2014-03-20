import os

import praw
import redis

re = redis.Redis()

HERE = os.path.abspath(os.path.dirname(__file__))
print HERE
DB_FILE = os.path.join(HERE, 'SubscriberDB.txt')
# The number of id's we keep to make sure that a result haven't been processed
# before. One is insufficient as if becomes deleted/removed/placed in private
# subreddit, then we will message for every returned result.
IDS_KEPT = 3
MESSAGE = """Hi there, \nThis is a timesavor bot. We recognize that you have been talking about meal planning.
We are a nonprofit organization with the goal of a better, healthier world: http://timesavorapp.com\n Thank you for your support"""

def main():
    r = praw.Reddit('timesavorapp by u/_Daimon_ ver 0.1.1. Source see '
                    'github.com/Damgaard/Reddit-Bots')
    r.login('zman0225', 'a2e7rqej')
    last_found_ids = load_last_found_ids()
    search_word = 'food homecook dinner meal planning'
    bad_words = ['subreddit stats', 'electro', 'dubstep', 'house', 'music']
    newest_ids = get_newest_ids(r, search_word)
    print "searching"
    while True:
        for result in search_results(r, search_word, last_found_ids):
        	print "searching"
            if is_valid_result(result, bad_words):
                message_me(r, result, search_word)
        store_last_found_ids(newest_ids)


def load_last_found_ids():
    try:
        with open(DB_FILE, 'r') as db:
            last_ids = db.readlines()[:IDS_KEPT]
            last_ids = [id.strip() for id in last_ids if id.strip() != '']
            return last_ids + [None] * (IDS_KEPT - len(last_ids))
    except IOError:
        return [None] * IDS_KEPT


def store_last_found_ids(new_ids):
    with open(DB_FILE, 'w') as db:
        for id in new_ids:
            db.write("%s\n" % id)


def search_results(reddit_session, search_word, stop_ids):
    """
    Yield search results coming from the search_word.

    Stop when we hit stop_id

    """
    print reddit_session
    for result in reddit_session.search(search_word, sort='new', limit=None,
                                        place_holder=stop_ids[0]):
        if result.id in stop_ids:
            break
        yield result


def get_newest_ids(reddit_session, search_word):
    result_generator = reddit_session.search(search_word, sort='new',
                                             limit=IDS_KEPT)
    newest_ids = list(result.id for result in result_generator)
    return newest_ids + [None] * (IDS_KEPT - len(newest_ids))


def is_valid_result(result, bad_words):
    """Does the title or subreddit contain a bad word?"""
    good_title = all(word not in result.title.lower() for word in bad_words)
    good_subreddit = all(word not in result.subreddit.display_name.lower()
                         for word in bad_words)
    return good_title and good_subreddit


def message_me(reddit_session, result, search_word):
    title = 'Nonprofit free meal planning app'
    # print result.author, result.title
    body = '[%s](%s)' % ("timesavorapp", "http://timesavorapp.com")
    if result.author not in re.smembers('sent'):
        re.sadd('sent',result.author)
        print 'sent to %s'%(str(result.author))
        reddit_session.send_message(result.author, title, body)

if __name__ == '__main__':
    main()