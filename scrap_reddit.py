import configparser
import praw
import requests

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from timeit import default_timer as timer

config = configparser.ConfigParser()
config.read('config.ini')
credentials = config['REDDIT_CRED']


reddit = praw.Reddit(
    client_id=credentials['client_id'],
    client_secret=credentials['client_secret'],
    user_agent=credentials['user_agent'],
)

options = Options()
options.headless = True
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

# reddit = praw.Reddit(
#     client_id="SzUISScjtzaVzKhFfHtSjg",
#     client_secret="S8gobzzkLNZiHtDXs223UxWqolG3Zw",
#     user_agent="nearReddit python"
# )

#NOTE: Skipped for now as utility not that important

def get_club_and_score(raw_text: str) -> list:
    """
    Function that returns club name, club score and if they scored 
    the goal in question

    Parameters
    ----------
    raw_text: str, club name with score, eg: Real Salt Lake 3

    Returns
    -------

    list:
        - club_name: str
        - goals: int
        - scored: bool, if they scored the current goal or not (using the [])
    """
    scored = False
    start = raw_text.find('[')
    if  start != -1:
        scored = True
        end = raw_text.find(']')
        goals = raw_text[start+1:end]
        if start < 2:
            club_name = raw_text.split(' [goals]')[0]
        else:
            club_name = raw_text.split('[goal] ')[1]
    else:
        pass
    return [" ", 0, False]


def get_video_link(url:str) -> str:
    """
    Function that gets video link from url

    Parameters
    ----------
    ulr: str, url to the streaming service

    Returns
    -------
    video_link: str, link to the video
    """
    start = timer()
    website = url.split('//')[1]
    website = website.split('.')[0]

    # source_tag = ['streamin', 'streamja']
    video_tag = ['dubz', 'streamff']
    if website in video_tag:
        return get_video_link_selenium(url)
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    tag = soup.find('source')
    end = timer()
    print(end - start)
    return tag.attrs['src']

def get_video_link_selenium(url: str) -> str:
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    tag = soup.find('video')
    return tag.attrs['src']


def get_submissions(limit: int = 5) -> list:
    """
    Function that get submissions from r/soccer subreddit
    And checks if it's a goal link or not

    Parameters
    ----------
    limit: int, Number of posts retreived

    Returns
    -------
    submissions: List of submissions that are goals

    """

    # Will use two things: media flair and if '[]' is present in the title
    # This is temporary
    start = timer()
    submissions = list(reddit.subreddit('soccer').new(limit=limit))

    result = []
    for sub in submissions:

        if sub.link_flair_text == "Media" and sub.title.find('[') != -1:
            result.append(sub)

    end = timer()
    print(end - start)
    return result






