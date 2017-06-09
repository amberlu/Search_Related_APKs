import requests
import logging
from bs4 import BeautifulSoup
import sys


def get_category_related(category_name):
    """Given a category name, the function returns all apks from the category
       :output: a set of package names in unicode
    """
    

    apk_lst = set()
    logging.info('start')
    # Process category_name into the correct format
    if ' ' in category_name:
        category_name = '_'.join(category_name.split(' '))
    category_name = category_name.upper()
    
    # Visit the main page of the category
    base_url = 'https://play.google.com/store/apps/category/'
    url = base_url + category_name + '?hl=en'
    r = requests.get(url)
    if check_error(r, url):
        return
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')

    # Collect urls of all the sub-categories 
    link_lst = set()
    for item in soup.find_all('a', class_='title-link id-track-click'):
        link_url = item.get('href').encode('utf-8').strip()
        url = 'https://play.google.com' + link_url
        link_lst.add(url)
    
    # Visit the webpage of each sub-category and collect all package names
    for link_url in link_lst:
        count = 0
        for _ in range(50):
            data = {'start':str(count), 'num':60}
            r = requests.post(link_url, data=data)
            if check_error(r, url):
                break
            
            data = r.text
            soup = BeautifulSoup(data, 'html.parser')

            tmp = list()
            for item in soup.find_all('span', class_='preview-overlay-container'):
                tmp.append(item.get('data-docid'))
            old_size = len(apk_lst)
            apk_lst = apk_lst.union(tmp)
            if old_size == len(apk_lst):
                logging.info('sub-category %s done; current size: %d' % (link_url, len(apk_lst)))
                
                break 
            count += 60
    logging.info('category %s done; total size: %d' % (category_name, len(apk_lst)))
    return apk_lst

########################################################################################
###################### Helper Functions
########################################################################################

def check_error(r, url):
    if r.status_code != 200:
        logging.error('Exception in HTTP request: %s' % url)
        print('http_error')
        return True
    return False 

# TODO: uncomment this part if using this file independently
#if __name__ == '__main__':
#    if len(sys.argv) != 2:
#        print('please provide exactly one category name \ne.x python category.py "Auto And Vehicles"')
#        exit()
#    #c = sys.argv[1]
#    c = 'Auto And Vehicles'
#    apk_lst = get_category_related(c)


