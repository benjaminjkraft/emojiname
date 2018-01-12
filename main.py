import json
import os
import random
import sys

sys.path.insert(0, 'lib')

import flask


app = flask.Flask(__name__)
app.config.update(
    DEBUG=os.environ.get('SERVER_SOFTWARE', '').startswith('Development'))


_EMOJI = None


def _emoji():
    global _EMOJI
    if _EMOJI is None:
        with open('emoji-data/emoji.json') as f:
            _EMOJI = json.load(f)
    return _EMOJI


def character(emoji_datum):
    return ''.join(unichr(int(c, 16))
                   for c in emoji_datum['unified'].split('-'))


def shortcode(emoji_datum):
    return ':%s:' % random.choice(emoji_datum['short_names'])


def name(emoji_datum):
    return (emoji_datum.get('name') or shortcode(emoji_datum)).upper()


def team_name_data():
    emoji = random.sample(_emoji(), 3)
    return {
        'characters': ''.join(character(e) for e in emoji),
        'shortcodes': ' '.join(shortcode(e) for e in emoji),
        'names': ' '.join(name(e) for e in emoji),
    }


@app.route('/slash', methods=['POST'])
def slash():
    return flask.jsonify({
        'response_type': 'in_channel',
        'text': (u'Our team name is %(characters)s '
                 'which you can type like so: `%(shortcodes)s` '
                 'or pronounce like so: %(names)s.'
                 % team_name_data()),
    })
