import requests
from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth

params = {'firstname': 'Ryan', 'lastname': 'Mitchell'}
r = requests.post("http://pythonscraping.com/pages/processing.php", data=params)
print(r.text)

files = {'uploadFile': open('./logo.jpg', 'rb')}
r = requests.post('http://pythonscraping.com/pages/processing2.php', files=files)
print(r.text)

# login cookies
session = requests.Session()
params = {'firstname': 'Ryan', 'lastname': 'Mitchell'}
s = session.post('http://pythonscraping.com/pages/cookies/welcome.php', params)
print('cookie is set to ')
print(s.cookies.get_dict())
print('Going to profile page...')
s = session.get('http://pythonscraping.com/pages/cookies/profile.php')
print(s.text)
# http auth
auth = HTTPBasicAuth('ryan', 'password')
r = requests.post(url='http://pythonscraping.com/pages/auth/login.php', auth=auth)
print(r.text)


