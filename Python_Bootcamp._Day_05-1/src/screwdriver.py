import requests
import sys
from bs4 import BeautifulSoup

if sys.argv[1] == 'list':
    response = requests.get("http://127.0.0.1:8888")
    soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
    for el in soup.find_all('h'):
        print(el.string.replace('\n', ''))
else:
    print(sys.argv[2])
    files = {'file': open(sys.argv[2], 'rb')}
    requests.post("http://127.0.0.1:8888", files=files)