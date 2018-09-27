from bs4 import BeautifulSoup
from slackclient import SlackClient
import json
import logging
import os
import requests


def handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info("Started Holidaybot!")
    url = json.load(open('config.json', 'r'))['holidayUrl']
    logger.debug("Getting from {}", url)
    doc = requests.get(url).text
    soup = BeautifulSoup(doc, 'html.parser')
    holidays = []
    for entry in soup.find_all('article', 'whatis'):
        link_elem = entry.a
        holidays.append((link_elem.h4.text, link_elem.get['href']))
    slack_token = os.environ['SLACK_TOKEN']
    slack_client = SlackClient(slack_token)
    msg = ""
    for holiday in holidays:
        msg += holiday[0]
        msg += " "
        msg += holiday[1]
        msg += " | "
    slack_client.api_call('chat.postMessage',
                          channel='C0000000',
                          text=msg)
