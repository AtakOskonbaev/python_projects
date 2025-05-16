import urllib.request
url = 'https://dcb.kg/'
response = urllib.request.urlopen(url)
print(response.read())
response.close()