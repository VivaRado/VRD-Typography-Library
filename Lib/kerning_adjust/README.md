Kerning Adjust (beta)
===================

![Screenshot](https://github.com/VivaRado/VRD-Typography-Library/blob/master/Lib/kerning_adjust/assets/img/kerning_adjust_preview.gif)

Kerning Adjustment interface for variable EFO.
The interface is served through NodeJS, alongside a Flask server.
The Flask server is communicating over Socket.io with the NodeJS interface.

### Features

 - Colaborative, Flask is multi-threaded so you can work on multiple EFOs at the same time.
 - Interface Font rendering is done though fragments for faster result.
 - Each Master can have it's own set of kerning adjustments.
 - Your kerning gets stored in LocalStorage.
 - Class Kerning, so you can kern all letters of a class.
 - Snap Kerning, take screens of your kerning so you can verify it passing after saving and compiling.

On save, the data is transfered to ```efo/kerning/adjustments.json```
And on ```kerning_compress_flat.py``` on that EFO, you get new PLIST and FEA files.
Runing ```efo_to_var.py``` - to compile with fontmake, clearing the browser cache data and reload - the interface mirrors the changes.
Working on integrating those last steps and making it easier.

### Python Requirements

```flask, flask_socketio, flask_session, flask_cors, ufoLib, lxml```

### NodeJS Requirements

```body-parser, express, express-handlebars, handlebars, minimist, python-shell, socket.io, cors```

### JS Requirements

```jquery, domtoimage, socket.io```

### Usage

```
cd "/kerning_adjust"

npm install

node app --source (source EFO)
```

Once the Node server is running, you can visit: ```http://localhost:8008/```

NodeJS is also starting the Flask server, which logs all the threads visit: ```http://localhost:5000/```


[By VivaRado](https://www.vivarado.com)
