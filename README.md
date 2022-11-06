# fake_server

Lightweight server for fake backend data.

# What's this for

When spinning up a front end app connecting to a REST server, it's often good to have fake REST data available during early testing. Fake static data can take the place of dynamic content and help finalize the contract that will help provide the specification for the dynamic data. One thing that is required for this to work is the ability to set the mime type on the data.

This tool spins up a server that points to a directory of fake server data and serves that based on structure of the fake data. This allows a directory structure that mimics the REST logical directory structure to be synthesized. Additionally, the mime type of the element can be set by extending the file name with signatures that indicate the mime type that should be used for the response.

# Running the server

The server takes the following arguments:

```
$ python server.py --help
fake_server

A basic server for mocking REST interfaces.

Usage:
    fake_server [<DIRECTORY>] [--port=<PORT>]

Options:
    <DIRECTORY>     Base directory of local filesystem to serve [default: .].
    --port=<PORT>   Override port number [default: 3000].
```

* `<DIRECTORY>`: Overriding of the root directory to be served is possible by specifying a path for this option. Default is the current directory.

* `--port=<PORT>`: Overriding the port is possible with the `--port` option. Default is 3000.

# Format of the fake data

From the root server directory (as specified by the `<DIRECTORY>` argument), the file system will be served with the REST path mimicking the file system path. However, there are a few things to mention about how these files are served to mock a REST server.

## Serving mime encoded data

To mock data of a full REST path, you can create a file at the desired location. For example, populating a file at path `/videos/myfile`, will serve the contents of that file to a GET of the `http://localhost:3000/videos/myfile` REST path:

```
ROOT/
└── videos
    └── myfile
```

By default the mime type of the returned data will be `text/plain`.

If you want the contents of the file to be served with another mime type, say `json`, you can add the tail extension `_json` to the filename:

```
ROOT/
└── videos
    └── myfile_json
```

This is a way of specifying an override for the default mime type. This will serve a GET request of path `http://localhost:3000/videos/myfile` as with mime type `applications/json`.

It's worth noting that a file with a normal filename extension won't use it to infer mime type. For example the file `myfile.json` will be served as the default REST mime type `text/plain`. In order to have this REST path populated as `json` data, the filename needs to be set to: `myfile.json_json`.

For example, a GET query of `http://localhost:3000/videos/myfile.json` will return the contents of `myfile.json` with the default mime type `text/plain`

```
ROOT/
└── videos
    └── myfile.json
```

However, a GET query of `http://localhost:3000/videos/myfile.json` with the following file structure, will return the contents of `myfile.json` with the default mime type `application/json`

```
ROOT/
└── videos
    └── myfile.json_json
```

To be clear, we're trying to mock REST, not provide a static file server.

## Supported mime types

The following tail extension mime type specifiers are supported:

`_txt` => `text/plain`

`_htm` or `_html`  => `text/html`

`_json` => `application/json`

`_jsonapi` => `application/vnd.api+json`

## Serving directories

Directory listings are not returned by default and will return a 404.

This means that a file system like this (where `ROOT` is the value of the `<DIRECTORY>` argument) a GET query of path `http://localhost:3000/videos` will return a `404` response:

```
ROOT/
└── videos
    ├── 1_json
    ├── 2_json
    └── 3_json
```

This is because for a REST server, returning a directory listing doesn't necessarily make sense.

However, if you want a directory path to return `json` data, you can populate a response to the path by adding a file with the name `videos_json` which will take a higher precedence and will return the contained data (in this case) as `json`:

```
ROOT/
├── videos
│   ├── 1_json
│   ├── 2_json
│   └── 3_json
└── videos_json
```
