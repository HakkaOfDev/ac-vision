import socketio
import eventlet

sio = socketio.Server()

app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    
    
    
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 6969)), app)