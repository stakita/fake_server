#!/usr/bin/env python3
'''fake_server

A basic server for mocking REST interfaces.

Usage:
    fake_server [<DIRECTORY>] [--port=<PORT>]

Options:
    <DIRECTORY>     Base directory of local filesystem to serve [default: .].
    --port=<PORT>   Override port number [default: 3000].
'''

import sys
from flask import Flask, Response
from flask_cors import CORS
import os.path
import glob
import time
try:
    from docopt import docopt
except ImportError as e:
    sys.stderr.write('Error: %s\nTry:\n    pip install --user docopt\n' % e)
    sys.exit(1)

app = Flask(__name__)
allowed_origins = '*'
CORS(app, resources={r'/api/*': {'origins': allowed_origins}})

current_dir = os.path.abspath(os.path.curdir)
root_dir = None

# Favorite type not here? Add entry based on: https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
extension_map = {
    'txt': 'text/plain',
    'htm': 'text/html',
    'html': 'text/html',
    'json': 'application/json',
    'jsonapi': 'application/vnd.api+json'
}

@app.route('/<path:filepath>')
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
            raise Exception('calculated path does not equal mapped_path: "%s" != "%s"' % (path_section, mapped_path))
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
                content_type = extension_map['txt'] # default to txt
                result = Response(fd.read(), mimetype=content_type)
        else:
            result = Response("Not found", status=404)

    return result

def main(args):
    global root_dir
    print(args)
    port = int(args['--port'] or 3000)
    directory = (args['<DIRECTORY>'] or '.') .strip('/')
    root_dir = current_dir + '/' + directory
    app.run(port=port)


if __name__ == '__main__':
    args = docopt(__doc__)
    sys.exit(main(args))

