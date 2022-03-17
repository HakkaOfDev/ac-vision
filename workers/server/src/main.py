import socketio
import eventlet
import requests

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)

@sio.on('ONU_INFO')
def onu_balancer(sid, data):
    requests.post('http://api:8000/api/v1.0/ressources/notification/new', data=data, headers={'Accept':'application/json'})
    sio.emit('ONU', data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 6969)), app)