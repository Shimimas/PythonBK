from wsgiref.simple_server import make_server
import json
import sys

d = {
        'Cyberman': 'John Lumic',
        'Dalek': 'Davros',
        'Judoon': 'Shadow Proclamation Convention 15 Enforcer',
        'Human': 'Leonardo da Vinci',
        'Ood': 'Klineman Halpen',
        'Silence': 'Tasha Lem',
        'Slitheen': 'Coca-Cola salesman',
        'Sontaran': 'General Staal',
        'Time Lord': 'Rassilon',
        'Weeping Angel': 'The Division Representative',
        'Zygon': 'Broton'
    }

def hello_world_app(environ, start_response):
    status = "200 OK"
    print(environ['QUERY_STRING'])
    headers = [("Content-type", "text/plain; charset=utf-8")]
    start_response(status, headers)
    req = environ['QUERY_STRING'].replace('%20', ' ').replace('species=', '')
    if req in d:
        json_data = {'credentials': d[req]}
    else:
        json_data = {'credentials': 'Unknown'}
    return [bytes(str(json.dumps(json_data)), encoding = 'utf-8')]

with make_server("", 8888, hello_world_app) as httpd:
    httpd.serve_forever()
