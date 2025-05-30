import queue
import requests
import threading
import sys

EXTENSIONS = ['.php', '.bak', '.orig', '.inc']
TARGET = 'http://testphp.vulnweb.com'
THREADS = 50
WORDLIST = '/home/archuser/tools/SecLists/Discovery/Web-Content/common.txt'

def get_words(resume=None):
    
    def extend_words(word):
        if '.' in word:
            words.put(f'/{word}')
        else:
            words.put(f'/{word}/')
        for extension in EXTENSIONS:
            words.put(f'/{word}{extension}')
    
    with open(WORDLIST) as f:
        raw_words = f.read()
        
    found_resume = False
    words = queue.Queue()
    for word in raw_words.split():
        if resume is not None:
            if found_resume:
                extend_words(word)
            elif word == resume:
                found_resume = True
                print(f'resuming from {resume}')
        else:
            print(word)
            extend_words(word)
    return words

def dir_bruter(words):
    while not words.empty():
        url = f'{TARGET}{words.get()}'
        try:
            r = requests.get(url)
        except requests.exceptions.ConnectionError:
            sys.stderr.write('x');sys.stderr.flush()
            continue
        if r.status_code == 200:
            print(f'success {r.status_code}: {url}')
        elif r.status_code == 404:
            sys.stderr.write('.');sys.stderr.flush()
        else:
            print(f'{r.status_code} => {url}')
            
if __name__ == '__main__':
    words = get_words()
    print('press return to continue')
    sys.stdin.readline()
    for _ in range(THREADS):
        t = threading.Thread(target=dir_bruter, args=(words, ))
        t.start()