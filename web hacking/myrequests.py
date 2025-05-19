import requests

url = 'http://scanme.com'
response = requests.get(url)

data = {'user':'tim', 'name':'hello'}
response = requests.post(url, data=data)
print(response.text)