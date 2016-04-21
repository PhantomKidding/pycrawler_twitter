import re

import requests
from bs4 import BeautifulSoup


def parse_tweet(uid, tid):
    tweet_info = dict()
    user_info = dict()

    url = 'https://twitter.com/' + uid + '/status/' + tid
    html = requests.request('GET', url).text.encode('ascii', 'ignore')
    soup = BeautifulSoup(html, 'html.parser')

    # PermalinkOverlay
    tweet_inner_soup = soup.find('div', attrs={"data-tweet-id": tid})
    tweet_info['tweet'] = re.sub('\n', '', tweet_inner_soup.find('div', class_="js-tweet-text-container").text)
    tweet_info['retweets'] = re.sub('[^0-9]', '', tweet_inner_soup.find('a', class_="request-retweeted-popup").text)
    retweet_users = tweet_inner_soup.find('ul', class_='stats').find_all(has_data_user_id)
    retweet_users_str = ''
    for retweet_user in retweet_users:
        retweet_users_str += retweet_user.attrs['data-user-id'] + "/"
    tweet_info['retweet_users'] = re.sub('\/$', '', retweet_users_str)
    tweet_info['timedate'] = re.sub('[^a-zA-Z0-9: ]', '', tweet_inner_soup.find('div', class_='client-and-actions').text)
    tweet_info['likes'] = tweet_inner_soup\
        .find('div', class_='ProfileTweet-action ProfileTweet-action--favorite js-toggleState')\
        .find('span', class_='ProfileTweet-actionCount').span.text
    tweet_info['likes'] = u'0' if tweet_info['likes'] == '' else tweet_info['likes']


    # ProfileHeaderCard
    #user_info['bio'] = soup.find('p', class_='ProfileHeaderCard-bio u-dir').text

    return tweet_info


def has_data_user_id(tag):
    return tag.has_attr('data-user-id')
