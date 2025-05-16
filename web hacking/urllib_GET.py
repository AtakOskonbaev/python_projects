import urllib.request
url = 'https://dcb.kg/'

headers = {'User-Agent':'GoogleBot'}
request = urllib.request.Request(url, headers=headers)

response = urllib.request.urlopen(url)
print(response.read())
response.close()