import requests

url = 'http://rochellebastian.pythonanywhere.com/level/'
payload = {'level': 8}
headers = {'content-type': 'application/json'}

r = requests.post(url, params=payload, headers=headers)

print(r.url)


#send data from sensor to web server