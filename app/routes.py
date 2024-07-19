from flask import Blueprint, render_template, session, redirect, url_for
from flask_socketio import emit, join_room, leave_room
from . import socketio

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/create_room', methods=['POST'])
def create_room():
    return redirect(url_for('main.room', room_id='room_id'))

@main.route('/join_room', methods=['POST'])
def join_room():
    return redirect(url_for('main.room', room_id='room_id'))

@main.route('/room/<room_id>')
def room(room_id):
    return render_template('room.html', room_id=room_id)
