# Text-Based Browser

import sys
import os
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore

init()

nytimes_com = '''
This New Liquid Is Magnetic, and Mesmerizing

Scientists have created “soft” magnets that can flow 
and change shape, and that could be a boon to medicine 
and robotics. (Source: New York Times)


Most Wikipedia Profiles Are of Men. This Scientist Is Changing That.

Jessica Wade has added nearly 700 Wikipedia biographies for
 important female and minority scientists in less than two 
 years.

'''

bloomberg_com = '''
The Space Race: From Apollo 11 to Elon Musk

It's 50 years since the world was gripped by historic images
 of Apollo 11, and Neil Armstrong -- the first man to walk 
 on the moon. It was the height of the Cold War, and the charts
 were filled with David Bowie's Space Oddity, and Creedence's 
 Bad Moon Rising. The world is a very different place than 
 it was 5 decades ago. But how has the space race changed since
 the summer of '69? (Source: Bloomberg)


Twitter CEO Jack Dorsey Gives Talk at Apple Headquarters

Twitter and Square Chief Executive Officer Jack Dorsey 
 addressed Apple Inc. employees at the iPhone maker’s headquarters
 Tuesday, a signal of the strong ties between the Silicon Valley giants.
'''

# write your code here

history = []
history_changed = False


def filename_from_url(url):
    return f'{url[:url.rfind(".")]}'


def add_history(url):
    history.append(url)
    global history_changed
    history_changed = True


def visit_back(mem_dir):
    if history_changed:
        history.pop()
    page = history.pop()
    if page in os.listdir(mem_dir):
        with open(os.path.join(mem_dir, page)) as f:
            print(f.read())
    else:
        fixed_url = fix_url(page)
        r = requests.get(fixed_url)
        text = parse_request(r)
        print(text)


def fix_url(url):
    if url.startswith('https://'):
        return url
    else:
        return f'https://{url}'


def parse_request(r):
    soup = BeautifulSoup(r.content, 'html.parser')
    text = ''
    par = soup.find_all(['p', 'a', 'ul', 'ol', 'li'])
    for p in par:
        if p.name == 'a':
            text += f'{Fore.BLUE + p.text}\n'
        else:
            text += f'{p.text} + \n'
    return text


def get_input(mem_dir):
    url = input()
    if url == 'exit':
        exit()
    elif url == 'back':
        visit_back(mem_dir)
    elif url in os.listdir(mem_dir):
        with open(os.path.join(mem_dir, url)) as f:
            print(f.read())
        add_history(url)
    else:
        fixed_url = fix_url(url)
        try:
            r = requests.get(fixed_url)
        except requests.exceptions.ConnectionError:
            print('Incorrect URL')
            return
        text = parse_request(r)
        print(text)
        with open(os.path.join(mem_dir, filename_from_url(url)), 'w') as f:
            f.write(text)
        add_history(url)


def set_dir():
    target_dir = sys.argv[1]
    if not os.access(target_dir, os.F_OK):
        os.mkdir(target_dir)
    return target_dir
    # os.chdir(target_dir)


def main():
    mem_dir = set_dir()
    while True:
        get_input(mem_dir)


main()
