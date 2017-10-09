import os
import argparse
import random
import time
import logging

from category import *
from developer import *
from datetime import datetime

def _parse_args():
    parser = argparse.ArgumentParser(description="Output all related package names, given a developer or category")
    parser = argparse.ArgumentParser(description="Scrape the Google Play Store for package names; searches all categories by default")
    parser.add_argument('--dev', '-d', help="Scrape a specific Google Play Store developer ID")
    parser.add_argument('--category', '-c', help="Scrape a specific Google Play Store category ID")
    parser.add_argument('--verbose', '-v', action='store_true', help='Show all logging messages')

    return parser.parse_args()

def _show_output(apk_list):
    for apk in apk_list:
        print(apk)

def _full_scrape(min_cooldown_secs=3, max_cooldown_secs=10):
    assert min(min_cooldown_secs, max_cooldown_secs) >= 0 and min_cooldown_secs <= max_cooldown_secs

    # Get apps from all the category top charts, cooling down between them
    categories = ['ANDROID_WEAR', \
                  'ART_AND_DESIGN', \
                  'AUTO_AND_VEHICLES', \
                  'BEAUTY', \
                  'BOOKS_AND_REFERENCE', \
                  'BUSINESS', \
                  'COMICS', \
                  'COMMUNICATION', \
                  'DATING', \
                  'EDUCATION', \
                  'ENTERTAINMENT', \
                  'EVENTS', \
                  'FINANCE', \
                  'FOOD_AND_DRINK', \
                  'HEALTH_AND_FITNESS', \
                  'HOUSE_AND_HOME', \
                  'LIBRARIES_AND_DEMO', \
                  'LIFESTYLE', \
                  'MAPS_AND_NAVIGATION', \
                  'MEDICAL', \
                  'MUSIC_AND_AUDIO', \
                  'NEWS_AND_MAGAZINES', \
                  'PARENTING', \
                  'PERSONALIZATION', \
                  'PHOTOGRAPHY', \
                  'PRODUCTIVITY', \
                  'SHOPPING', \
                  'SOCIAL', \
                  'SPORTS', \
                  'TOOLS', \
                  'TRAVEL_AND_LOCAL', \
                  'VIDEO_PLAYERS', \
                  'WEATHER', \
                  'GAME', \
                  'GAME_ACTION', \
                  'GAME_ADVENTURE', \
                  'GAME_ARCADE', \
                  'GAME_BOARD', \
                  'GAME_CARD', \
                  'GAME_CASINO', \
                  'GAME_CASUAL', \
                  'GAME_EDUCATIONAL', \
                  'GAME_MUSIC', \
                  'GAME_PUZZLE', \
                  'GAME_RACING', \
                  'GAME_ROLE_PLAYING', \
                  'GAME_SIMULATION', \
                  'GAME_SPORTS', \
                  'GAME_STRATEGY', \
                  'GAME_TRIVIA', \
                  'GAME_WORD', \
                  'FAMILY', \
                  'FAMILY?age=AGE_RANGE1', \
                  'FAMILY?age=AGE_RANGE2', \
                  'FAMILY?age=AGE_RANGE3', \
                  'FAMILY_ACTION', \
                  'FAMILY_BRAINGAMES', \
                  'FAMILY_CREATE', \
                  'FAMILY_EDUCATION', \
                  'FAMILY_MUSICVIDEO', \
                  'FAMILY_PRETEND']

    packages = set()
    for cat in categories:
        logging.info('Scraping category %s...' % cat)
        cat_packages = get_category_related(cat)
        packages.update(cat_packages)

        cooldown_secs = random.randint(min_cooldown_secs, max_cooldown_secs)
        logging.info('Cooling down for %d seconds...' % cooldown_secs)
        time.sleep(cooldown_secs)

    return packages

if __name__ == "__main__":
    args = _parse_args()

    # Set logging level
    if(args.verbose):
        logging.basicConfig(level=logging.INFO)

    # Default behavior: scrape all categories
    packages = None
    if(args.dev is None and args.category is None):
        packages = _full_scrape()

    # Otherwise, take in the specified developer or category
    elif(args.dev is not None):
        packages = get_developer_related(args.dev)
    elif(args.category is not None):
        packages = get_category_related(args.category)

    if(packages is not None):
        packages = set(packages)
        _show_output(packages)
    else:
        logging.warning('No packages found')

