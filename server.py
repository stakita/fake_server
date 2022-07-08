#!/usr/bin/env python3
'''server

A basic server for mocking REST interfaces.

Usage:
    server [--directory=PATH] [<PORT>]

Options:
    <PORT>                      Port number [default: 3000].
'''

import sys
from flask import Flask, Response
from flask_cors import CORS
import os.path
import glob
try:
    from docopt import docopt
except ImportError as e:
    sys.stderr.write('Error: %s\nTry:\n    pip install --user docopt\n' % e)
    sys.exit(1)

app = Flask(__name__)
# allowed_origins = 'http://localhost:8080'
allowed_origins = '*'
CORS(app, resources={r'/api/*': {'origins': allowed_origins}})

current_dir = os.path.abspath(os.path.curdir)
print('current_dir:', current_dir)

root_dir = current_dir

# Favorite type not here? Add entry based on: https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
extension_map = {
    'txt': 'text/plain',
    'htm': 'text/html',
    'html': 'text/html',
    'json': 'application/json',
    'jsonapi': 'application/vnd.api+json'
}

@app.route('/api/<path:filepath>')
def server_fake(filepath):
    print('filepath:', filepath)
    print('root_dir:', root_dir)
    result = None
    mapped_path = root_dir + '/' + filepath
    content_type = 'text/plain'
    print('mapped_path:', mapped_path)

    matches = glob.glob(mapped_path + '_*')
    print(matches)

    if len(matches) == 1:
        print('matched content encoded file')
        match = matches[0]
        path_section, extension = match.rsplit('_', 1)
        if path_section != mapped_path:
            raise Exception('Ambiguous underscore sequence in path')
        if extension in extension_map.keys():
            content_type = extension_map[extension]
        with open(match, 'rb') as fd:
            result = Response(fd.read(), mimetype=content_type)

    elif len(matches) > 1:
        raise Exception('Multiple matches - fix your test files')

    elif len(matches) == 0:
        if os.path.exists(mapped_path):
            print('exists')
            # exact match
            with open(mapped_path, 'rb') as fd:
                content_type = 'application/json'
                result = Response(fd.read(), mimetype=content_type)
        else:
            result = Response("Not found", status=404)

    return result

def main(args):
    print(args)
    port = int(args['<PORT>'] or 3000)
    app.run(port=port)


if __name__ == '__main__':
    args = docopt(__doc__)
    sys.exit(main(args))