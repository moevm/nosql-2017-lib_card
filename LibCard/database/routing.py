from bottle import route, run, static_file
from database.network import local_ip, server_port


@route('/')
def index():
    return static_file('index.html', root='html')


@route('/<img:re:favicon.ico>')
@route('/img/<img:path>')
def img_serve(img):
    return static_file(img, root='html/img')


# for css files
@route('/static/<file:path>')
def static_serve(file):
    return static_file(file, root='html/static')


def run_server():
    run(host=local_ip, port=server_port)
