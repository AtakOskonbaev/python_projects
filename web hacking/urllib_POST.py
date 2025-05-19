import urllib.parse
import urllib.request

url = 'https://dcb.kg/'
info = {'i':'am', 'the':'best'}
data = urllib.parse.urlencode(info).encode()
req = urllib.request.Request(url, data)
with urllib.request.urlopen(url) as response:
    content = response.read()
print(content)