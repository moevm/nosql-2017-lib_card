from bottle import route, run, static_file, get, post, request, response
from database.network import local_ip, server_port
import json
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

    elif request.json['action'] == 'search':

        type_ = request.json['type']

        title = request.json['title']
        author = request.json['author']
        year = request.json['year']
        id_ = request.json['id']

        cards = list(map(lambda x: (x, db.get_card(x)), db.get_all_keys()))

        if type_ == 'all':
            pass

        elif type_ == 'available':
            cards = [card for card in cards if card[1].is_available()]

        elif type_ == 'unavailable':
            cards = [card for card in cards if not card[1].is_available()]

        else:
            cards = []

        cards = [card for card in cards if title in card[1].title and
                 author in card[1].author and year in card[1].year and id_ in card[0]]

        found_cards = []
        for key, card in cards:
            curr_card = dict()
            curr_card['id'] = key
            curr_card['title'] = card.title
            curr_card['author'] = card.author
            curr_card['year'] = card.year
            curr_card['image'] = card.image
            found_cards += [curr_card]
        result['cards'] = found_cards

    elif request.json['action'] == 'update':

        try:

            result['success'] = True
            db.update_card(request.json['id'],
                           request.json['title'],
                           request.json['author'],
                           request.json['year'])

        except:
            result['success'] = False

    elif request.json['action'] == 'get-info':

        card = db.get_card(request.json['id'])
        result['id'] = request.json['id']
        result['title'] = card.title
        result['author'] = card.author
        result['year'] = card.year
        result['image'] = card.image
        result['available'] = card.is_available()

        history = []
        if history is not None:
            for curr in card.history:
                elem = dict()
                elem['reader'] = curr.reader
                elem['from'] = curr.date_from
                elem['to'] = curr.date_to
                history += [elem]

        result['history'] = history

    elif request.json['action'] == 'give-card':

        try:

            if request.json['date'] == '':
                raise ValueError

            result['success'] = True
            id_ = request.json['id']
            reader = request.json['reader']
            date_from = request.json['date']
            db.give_book(id_, reader, date_from)

        except:
            result['success'] = False

    elif request.json['action'] == 'return-card':

        try:

            if request.json['date'] == '':
                raise ValueError

            result['success'] = True
            id_ = request.json['id']
            date_to = request.json['date']
            db.return_book(id_, date_to)

        except:
            result['success'] = False

    elif request.json['action'] == 'delete':

        try:
            result['success'] = True
            id_ = request.json['id']
            db.remove_card(id_)

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
