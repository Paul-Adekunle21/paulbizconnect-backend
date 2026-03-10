import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_socketio import SocketIO
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CORS(app)

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return response

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'paulbizconnect_secret_2024')
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

jwt = JWTManager(app)
mail = Mail(app)
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='threading')

# Initialize database tables
from config.db import init_db
init_db()

from routes.auth import auth_bp
from routes.messages import messages_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(messages_bp, url_prefix='/api/messages')

online_users = {}

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join_room')
def handle_join_room(data):
    from flask_socketio import join_room
    room = data.get('room')
    if room:
        join_room(room)

@socketio.on('send_message')
def handle_send_message(data):
    from flask_socketio import emit
    room = data.get('room')
    if room:
        emit('receive_message', data, room=room)

@socketio.on('typing')
def handle_typing(data):
    from flask_socketio import emit
    room = data.get('room')
    if room:
        emit('user_typing', data, room=room, include_self=False)

@socketio.on('stop_typing')
def handle_stop_typing(data):
    from flask_socketio import emit
    room = data.get('room')
    if room:
        emit('user_stop_typing', data, room=room, include_self=False)

@app.route('/')
def index():
    return {'message': 'PaulBizConnect API is running! 🚀'}

@app.route('/api/health')
def health():
    try:
        from config.db import get_db
        conn = get_db()
        conn.close()
        return {'status': 'healthy', 'database': 'connected'}
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
