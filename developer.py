import requests
import logging
from bs4 import BeautifulSoup
import re
import sys
from category import check_error

def get_developer_related(developer_name, type=0):
    """ Given a developer name, the function returns a set of its package names 
        :params:
                developer_name: a string of the  developer name 
                type: 0 --> number encoded; 1 --> character encoded
        :output: a set of package names in unicode version
    """

    apk_lst = set()
    
    # If developer_name is number encoded
    if type == 0:
        # Visit the main webpage of the developer    
        apk_base_url = 'https://play.google.com/store/apps/dev?id='
        apk_url = apk_base_url + developer_name + '&hl=en'
        r = requests.get(apk_url)
        if check_error(r, apk_url):
           return 

        data = r.text
        soup = BeautifulSoup(data, 'html.parser')
        apk_lst = search_apk(soup, apk_lst)
        item = soup.find('div', class_= 'cards expandable id-card-list')
        
        # Retrieve data to forge future requests 
        sp = item.get('data-load-more-suggest-params')
        pg_token = item.get('data-load-more-first-continuation-token')

        search_url = 'https://play.google.com/store/xhr/searchcontent?authuser=0'
        headers = {'referer': apk_url, 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        count = 1
        
        # Request the server to load more apps 
        for _ in range(50):
            data = {'pageNum': str(count), 'xhr': '1', 'sp': sp, 'pagTok': pg_token}
            r = requests.post(search_url, data=data, headers=headers)
            if check_error(r, search_url):
                break
            response = r.text
            
            tmp = set()
            tmp_lst = re.findall(r'preview-overlay-container\\" data-docid\\u003d\\((.\w+)*)', response)
            for i in tmp_lst:
                apk = i[0][1:]
                tmp.add(apk)
            old_size = len(apk_lst)
            apk_lst = apk_lst.union(tmp)
            if old_size == len(apk_lst):
                logging.info('developer %s done!' % developer_name)
                break
            pg_token = get_next_page_token(response)
            count += 1
    
    # If developer_name is character encoded
    elif type == 1:
        # Convert developer_name into the correct format
        developer_name = _parse_developer_name(developer_name)
        base_url = 'https://play.google.com/store/apps/developer?id='
        url = base_url + developer_name + '&hl=en'

        count = 0
        for _ in range(50):
            data = {'start':str(count), 'num':60}
            r = requests.post(url, data=data)
            if check_error(r, url):
                break

            data = r.text
            soup = BeautifulSoup(data, 'html.parser')
            tmp = set()
            tmp = search_apk(soup, tmp)
            old_size = len(apk_lst)
            apk_lst = apk_lst.union(tmp)
            if old_size == len(apk_lst):
                logging.info('developer %s done!' % developer_name)
                break 
            count += 60

    logging.info('total count %d' % len(apk_lst))
    return apk_lst


###########################################################################
############### Helper Functions
###########################################################################

def _parse_developer_name(developer_name):
    if ' ' in developer_name:
        developer_name = '+'.join(developer_name.split(' '))        
    return developer_name.upper()

def get_next_page_token(data):
    token = re.findall(r'([a-zA-Z0-9:]+)', data)[-1]
    return token

def search_apk(soup, apk_lst):
    for app in soup.find_all('span', class_='preview-overlay-container'):
        apk_lst.add(app.get('data-docid'))
    return apk_lst

# TODO: uncomment this part if using this file independently
#if __name__ == '__main__':
#    if len(sys.argv) != 3:
#        print('please provide exactly one developer name and its type (0 if number encoded; 1 if character encoded)')
#        print('e.x: python developer.py "zc game" 1\ne.x: python developer.py 8050969478732289508 0')
#        exit()
#
#    get_developer_related(sys.argv[1], int(sys.argv[2]))
   
