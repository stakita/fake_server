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

...






