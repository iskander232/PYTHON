import flask
import requests
import argparse
from datetime import *
from base import *

app = flask.Flask("base")
create_tables()


@app.route('/', methods=['GET'])
def show_all():
    return flask.jsonify(in_base())


@app.route('/num', methods=['GET'])
def show_with_num():
    args = flask.request.args
    min_num = args['min_num']
    max_num = args['max_num']
    return flask.jsonify(search_with_num(min_num, max_num))


@app.route('/time', methods=['GET'])
def show_with_date():
    args = flask.request.args
    x_from = args['min_date'].split(' ')
    x_to = args['max_date'].split(' ')
    min_date = datetime(int(x_from[0]), int(x_from[1]), int(x_from[2]))
    max_date = datetime(int(x_to[0]), int(x_to[1]), int(x_to[2]))
    return flask.jsonify(search_with_date(min_date, max_date))


@app.route('/name', methods=['GET'])
def show_with_name():
    return flask.jsonify(search_with_name(flask.request.args['name']))


@app.route('/post', methods=['POST'])
def post():
    args = flask.request.args
    date = datetime.now()
    write_post(args['post'], date, args['name'], db.post_number)
    db.post_number += 1
    return 'OK'


def main():
    app.run()


if __name__ == '__main__':
    main()
