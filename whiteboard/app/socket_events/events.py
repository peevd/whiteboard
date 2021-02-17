from flask_socketio import emit, join_room, leave_room  # , send
from .. import socketio


@socketio.on('joined', namespace='/data')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = message["room"]
    join_room(room)
    emit('status', message["data"], room=room)


@socketio.on('text', namespace='/data')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = message["room"]
    emit('message', message["data"], room=room)


@socketio.on("b_data", namespace="/data")
def board_data(data):
    """Sent by a client when the user drow something on board.
    The board data is send to all peaople in the room."""
    room = data["room"]
    emit("data_transfer", data["data"], room=room)


@socketio.on("task_id", namespace="/data")
def task_ID(data):
    """Sent by a client when the course owner move to next task.
    The task ID is send to all peaople in the room."""
    room = data["room"]
    emit("task_transfer", data["data"], room=room)


@socketio.on('left', namespace='/data')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = message["room"]
    # send(message["data"], room=room)
    leave_room(room)
    emit('status', message["data"], room=room)


@socketio.on('b_edit', namespace='/data')
def b_edit(payload):
    room = payload['room']
    emit('b_edit', payload['data'], room=room)


@socketio.on('ppt', namespace='/data')
def ppt(data):
    room = data["room"]
    if(data["action"] == "join"):
        join_room(room)
    else:
        emit('ppt', data, room=room)
