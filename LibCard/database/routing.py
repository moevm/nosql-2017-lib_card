from bottle import route, run, static_file, get, post, request, response
from database.network import local_ip, server_port
import json
import base64
from database.database_manager import *


@get('/')
def index():
    return static_file('index.html', root='html')


@post('/')
def post_request():

    response.content_type = 'application/json'

    print('POST', request.json)
    result = dict()

    if request.json['action'] == 'get-all':
        all_cards = []
        for key, card in map(lambda x: (x, db.get_card(x)), db.get_all_keys()):
            curr_card = dict()
            curr_card['id'] = key
            curr_card['title'] = card.title
            curr_card['author'] = card.author
            curr_card['year'] = card.year
            curr_card['image'] = card.image
            all_cards += [curr_card]
        result['cards'] = all_cards
        result['db'] = db.print_curr_database()

    elif request.json['action'] == 'add':
        try:
            key = db.add_card(request.json['title'],
                              request.json['author'],
                              request.json['year'],
                              request.json['image'])
            result['success'] = True
            result['id'] = key
            result['title'] = request.json['title']
            result['author'] = request.json['author']
            result['year'] = request.json['year']
            result['image'] = request.json['image']

        except:
            result['success'] = False

    elif request.json['action'] == 'switch-db':
        try:
            db.switch_to_database(request.json['db'])
            result['success'] = True

        except:
            result['success'] = False

    return json.dumps(result)


@route('/<img:re:favicon.ico>')
@route('/img/<img:path>')
def img_serve(img):
    return static_file(img, root='html/img')


# for css and js files
@route('/static/<file:path>')
def static_serve(file):
    return static_file(file, root='html/static')


def run_server():
    global db
    db = DatabaseManager()
    db.set_test_enviroment()
    run(host=local_ip, port=server_port)
