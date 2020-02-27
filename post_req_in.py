import requests

url = 'http://rochellebastian.pythonanywhere.com/inbound'
data = {'level': 10}
headers = {'Content-Type': 'application/json'}

r = requests.post(url, json=data, headers=headers)

print(r.status_code)
print(r.content)


#send data to web server from sensor