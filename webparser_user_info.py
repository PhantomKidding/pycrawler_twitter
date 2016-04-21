import re
import sys

import requests
from bs4 import BeautifulSoup


def get_user_info(user_id):

    url = 'https://twitter.com/' + str(user_id)
    html = requests.request('GET', url).text.encode('ascii', 'ignore')
    soup = BeautifulSoup(html, 'html.parser')
    out = dict()

    profile_navigation_soup = soup.find('div', class_='ProfileNav')
    try:
        out['tweets'] = profile_navigation_soup.find('li', class_='ProfileNav-item ProfileNav-item--tweets is-active').a.attrs['title']
    except AttributeError:
        out['tweets'] = str(0)
    try:
        out['following'] = profile_navigation_soup.find('li', class_='ProfileNav-item ProfileNav-item--following').a.attrs['title']
    except AttributeError:
        out['following'] = str(0)
    try:
        out['followers'] = profile_navigation_soup.find('li', class_='ProfileNav-item ProfileNav-item--followers').a.attrs['title']
    except AttributeError:
        out['followers'] = str(0)
    try:
        out['likes'] = profile_navigation_soup.find('li', class_='ProfileNav-item ProfileNav-item--favorites').a.attrs['title']
    except AttributeError:
        out['likes'] = str(0)

    out['tweets'] = re.sub(' Tweets| Tweet|,', '', out['tweets'])
    out['following'] = re.sub(' Following|,', '', out['following'])
    out['followers'] = re.sub(' Followers| Follower|,', '', out['followers'])
    out['likes'] = re.sub(' Likes| Like|,', '', out['likes'])


    profile_header_soup = soup.find('div', class_='ProfileHeaderCard')
    try:
        out['bio'] = profile_header_soup.find('p', class_='ProfileHeaderCard-bio u-dir').text.strip()
        out['bio'] = re.sub('"|\n', '', out['bio'])
    except AttributeError:
        out['bio'] = ''
    try:
        out['location'] = profile_header_soup.find('div', class_='ProfileHeaderCard-location').text.strip()
    except AttributeError:
        out['location'] = ''
    try:
        out['join_date'] = profile_header_soup.find('div', class_='ProfileHeaderCard-joinDate').text.strip()
    except AttributeError:
        out['join_date'] = ''
    try:
        out['is_verified'] = profile_header_soup.h1.span.text.strip()
        out['is_verified'] = 'yes'
    except AttributeError:
        out['is_verified'] = 'no'

    return out

if __name__ == '__main__':
    argvs = sys.argv[1:]
    input = argvs[0]
    output = input + '.csv'

    f = open(input, 'r')
    o = open(output, 'a')
    i = 0
    for line in f:
        i += 1
        if i / 10000:
            print i,
        user = line.strip()
        info = get_user_info(user)
        try:
            o.write(','.join([user, info['is_verified'],
                          '"' + info['bio'] + '"', '"' + info['location'] + '"', '"' + info['join_date'] + '"',
                          info['tweets'], info['following'], info['followers'], info['likes']]).encode('ascii', 'ignored'))
            o.write('\n')
        except KeyboardInterrupt:
            r = open('record', 'a')
            r.write(input + '\t' + str(i) + '\n')
            r.close()
    f.close()
    o.close()

