from bottle import route, run, static_file, get, post, request
from database.network import local_ip, server_port
import json
from database.database_manager import *

db = DatabaseManager()


@get('/')
def index():
    return static_file('index.html', root='html')


@post('/')
def post_request():
    print(request.json)
    result = {}
    if request.json['action'] == 'get-all':
        all_cards = db.get_all_cards()
        


    return json.dumps({1: 1})


@route('/<img:re:favicon.ico>')
@route('/img/<img:path>')
def img_serve(img):
    return static_file(img, root='html/img')


# for css and js files
@route('/static/<file:path>')
def static_serve(file):
    return static_file(file, root='html/static')


def run_server():
    run(host=local_ip, port=server_port)
