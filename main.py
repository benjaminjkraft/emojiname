import os
import sys

sys.path.insert(0, 'lib')

import flask


app = flask.Flask(__name__)
app.config.update(
    DEBUG=os.environ.get('SERVER_SOFTWARE').startswith('Development'))


@app.route('/slash', methods=['POST'])
def slash():
    return flask.jsonify({
        'response_type': 'in_channel',
        'text': u'testing 123',
    })
