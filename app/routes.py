from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_socketio import emit, join_room, leave_room
from . import socketio
import random

main = Blueprint('main', __name__)

rooms = {}  # Dictionary to store room information

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/create_room', methods=['POST'])
def create_room():
    username = request.form.get('username')
    room_id = generate_room_id()
    rooms[room_id] = {
        'creator': username,
        'players': {username: None},  # None means role not assigned yet
        'roles': []  # Roles will be added later
    }
    session['username'] = username
    session['room'] = room_id
    return redirect(url_for('main.room', room_id=room_id))

@main.route('/join_room', methods=['POST'])
def join_room():
    username = request.form.get('username')
    room_id = request.form.get('room_id')
    if room_id in rooms:
        session['username'] = username
        session['room'] = room_id
        rooms[room_id]['players'][username] = None
        return redirect(url_for('main.room', room_id=room_id))
    return redirect(url_for('main.index'))

@main.route('/room/<room_id>')
def room(room_id):
    if 'username' in session and 'room' in session:
        return render_template('room.html', room_id=room_id, rooms=rooms)
    return redirect(url_for('main.index'))

def generate_room_id():
    return str(random.randint(1000, 9999))

@socketio.on('connect')
def handle_connect():
    if 'username' in session and 'room' in session:
        username = session['username']
        room = session['room']
        join_room(room)
        emit('player_joined', {'username': username}, room=room)

@socketio.on('disconnect')
def handle_disconnect():
    if 'username' in session and 'room' in session:
        username = session['username']
        room = session['room']
        leave_room(room)
        rooms[room]['players'].pop(username, None)
        emit('player_left', {'username': username}, room=room)

@socketio.on('assign_roles')
def handle_assign_roles(data):
    room = data['room']
    roles = data['roles']
    players = list(rooms[room]['players'].keys())
    random.shuffle(players)
    
    for i, player in enumerate(players):
        rooms[room]['players'][player] = roles[i % len(roles)]
    
    emit('roles_assigned', rooms[room]['players'], room=room)
