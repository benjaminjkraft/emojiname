import json
import logging
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


def _weight(emoji_datum):
    if emoji_datum['short_name'].startswith('flag'):
        return 0.1
    if emoji_datum['short_name'].startswith('keycap'):
        return 0.1
    if emoji_datum['short_name'].startswith('skin-tone'):
        return 0
    return 1


def _random_emoji(n):
    exclude = set()
    # TODO: something clever with emojitracker data
    emoji = [(e, _weight(e)) for e in _emoji()]
    for _ in xrange(n):
        total = sum(w for e, w in emoji if e['unified'] not in exclude)
        r = random.random() * total
        for e, w in emoji:
            if e['unified'] in exclude:
                continue
            elif r < w:
                yield e
                exclude.add(e['unified'])
                break
            else:
                r -= w
        else:
            logging.error('Got to end of emoji list! r = %s' % r)
            yield emoji[-1]


def random_emoji(n=3):
    return list(_random_emoji(n))


def character(emoji_datum):
    return ''.join(unichr(int(c, 16))
                   for c in emoji_datum['unified'].split('-'))


def shortcode(emoji_datum):
    return ':%s:' % random.choice(emoji_datum['short_names'])


def name(emoji_datum):
    return (emoji_datum.get('name') or
            emoji_datum.get('short_name').replace('_', ' ').replace('-', ' ')
            ).upper()


def team_name_data():
    emoji = random_emoji()
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
