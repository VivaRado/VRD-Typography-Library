Kerning Adjust (alpha)
===================

Kerning Adjustment interface for variable EFO.
The interface is served through NodeJS, alongside a Flask server.
The Flask server is communicating over Socket.io with the NodeJS interface.
Flask is multi-threaded so you can work on multiple fonts at the same time.

Font rendering is done though fragments and canvas for faster results.
At this point no kerning values are being transfered to the EFOs as it is alpha.

Once the Node server is running, you can visit: ```http://localhost:8008/```

NodeJS is also starting the Flask server, which logs all the threads visit: ```http://localhost:5000/```

### Python Requirements

```flask_socketio, flask_session, flask_cors```

### NodeJS Requirements

```body-parser, express, express-handlebars, handlebars, python-shell, socket.io, cors```

### Usage

```
cd "/kerning_adjust"

npm install

node app --source (source EFO)
```

[By VivaRado](https://www.vivarado.com)
