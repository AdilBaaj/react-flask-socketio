from flask_socketio import SocketIO, emit, disconnect, join_room, send
from flask import Flask, request
from random import random

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
secret_to_user = {
    'secret1': 'user1',
    'secret2': 'user2'
}

@app.route('/user1', methods=['GET'])
def emit_to_user1():
    data = {'data': round(random()*10, 3)}
    socketio.emit('responseMessage', data, to='user1')
    return data

@app.route('/user2', methods=['GET'])
def emit_to_user2():
    data = {'data': round(random()*10, 3)}
    socketio.emit('responseMessage', data, to='user2')
    return data

# Handle the webapp connecting to the websocket
@socketio.on('connect')
def connect():
    secret = request.args['token']
    print(secret)
    if secret != "secret1" and secret !='secret2':
        print("Unable to authenticate user")
        disconnect()
        print("Disconnected")
    print(f'{secret_to_user[secret]} connected to websocket')
    join_room(secret_to_user[secret])
    emit('responseMessage', {'data': 'Connected! ayy'})

# Handle the webapp sending a message to the websocket
@socketio.on('message')
def handle_message(message):
    # print('someone sent to the websocket', message)
    print('Data', message["data"])
    print('Status', message["status"])


# Handle the webapp sending a message to the websocket, including namespace for testing
@socketio.on('message', namespace='/devices')
def handle_message_with_namespace():
    print('someone sent to the websocket!')


@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    print('An error occured:')
    print(e)


if __name__ == '__main__':
    # socketio.run(app, debug=False, host='0.0.0.0')
    http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
