from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config.db import get_db
from datetime import datetime

messages_bp = Blueprint('messages', __name__)

# ===== GET ALL CONVERSATIONS =====
@messages_bp.route('/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    try:
        user_id = int(get_jwt_identity())
        conn = get_db()
        cur = conn.cursor()

        cur.execute('''
            SELECT c.id, c.participant1_id, c.participant2_id,
                   u.id as other_id, u.full_name, u.account_type
            FROM conversations c
            JOIN users u ON (
                CASE WHEN c.participant1_id = %s
                THEN c.participant2_id ELSE c.participant1_id END = u.id
            )
            WHERE c.participant1_id = %s OR c.participant2_id = %s
        ''', (user_id, user_id, user_id))

        convs = cur.fetchall()
        result = []

        for conv in convs:
            cur.execute('''
                SELECT text, msg_type, created_at FROM messages
                WHERE conversation_id = %s
                ORDER BY created_at DESC LIMIT 1
            ''', (conv['id'],))
            last_msg = cur.fetchone()

            cur.execute('''
                SELECT COUNT(*) as count FROM messages
                WHERE conversation_id = %s AND sender_id != %s AND is_read = FALSE
            ''', (conv['id'], user_id))
            unread = cur.fetchone()['count']

            result.append({
                'id': str(conv['id']),
                'contact': {
                    'id': str(conv['other_id']),
                    'fullName': conv['full_name'],
                    'accountType': conv['account_type']
                },
                'lastMessage': last_msg['text'] if last_msg else '',
                'lastTime': str(last_msg['created_at']) if last_msg else '',
                'unread': unread
            })

        cur.close()
        conn.close()
        return jsonify({'conversations': result}), 200

    except Exception as e:
        print(f'Get conversations error: {e}')
        return jsonify({'error': 'Failed to get conversations'}), 500


# ===== GET MESSAGES =====
@messages_bp.route('/<int:conversation_id>', methods=['GET'])
@jwt_required()
def get_messages(conversation_id):
    try:
        user_id = int(get_jwt_identity())
        conn = get_db()
        cur = conn.cursor()

        cur.execute('''
            SELECT * FROM messages
            WHERE conversation_id = %s
            ORDER BY created_at ASC
        ''', (conversation_id,))
        messages = cur.fetchall()

        cur.execute('''
            UPDATE messages SET is_read = TRUE
            WHERE conversation_id = %s AND sender_id != %s AND is_read = FALSE
        ''', (conversation_id, user_id))
        conn.commit()

        result = []
        for msg in messages:
            result.append({
                'id': str(msg['id']),
                'text': msg['text'] or '',
                'msgType': msg['msg_type'],
                'sender_id': str(msg['sender_id']),
                'type': 'sent' if msg['sender_id'] == user_id else 'received',
                'time': msg['created_at'].strftime('%I:%M %p'),
                'read': msg['is_read']
            })

        cur.close()
        conn.close()
        return jsonify({'messages': result}), 200

    except Exception as e:
        print(f'Get messages error: {e}')
        return jsonify({'error': 'Failed to get messages'}), 500


# ===== SEND MESSAGE =====
@messages_bp.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        receiver_id = data.get('receiver_id')
        text = data.get('text', '')
        msg_type = data.get('msgType', 'text')

        if not receiver_id:
            return jsonify({'error': 'Receiver ID is required'}), 400

        conn = get_db()
        cur = conn.cursor()

        # Find or create conversation
        cur.execute('''
            SELECT id FROM conversations
            WHERE (participant1_id = %s AND participant2_id = %s)
            OR (participant1_id = %s AND participant2_id = %s)
        ''', (user_id, receiver_id, receiver_id, user_id))
        conv = cur.fetchone()

        if not conv:
            cur.execute('''
                INSERT INTO conversations (participant1_id, participant2_id)
                VALUES (%s, %s) RETURNING id
            ''', (user_id, receiver_id))
            conversation_id = cur.fetchone()['id']
        else:
            conversation_id = conv['id']

        cur.execute('''
            INSERT INTO messages (conversation_id, sender_id, receiver_id, text, msg_type)
            VALUES (%s, %s, %s, %s, %s) RETURNING id
        ''', (conversation_id, user_id, receiver_id, text, msg_type))

        message_id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            'message': 'Message sent!',
            'message_id': str(message_id),
            'conversation_id': str(conversation_id)
        }), 201

    except Exception as e:
        print(f'Send message error: {e}')
        return jsonify({'error': 'Failed to send message'}), 500


# ===== GET ALL USERS =====
@messages_bp.route('/users/all', methods=['GET'])
@jwt_required()
def get_all_users():
    try:
        user_id = int(get_jwt_identity())
        conn = get_db()
        cur = conn.cursor()

        cur.execute('''
            SELECT id, full_name, email, account_type FROM users
            WHERE id != %s AND verified = TRUE
        ''', (user_id,))
        users = cur.fetchall()
        cur.close()
        conn.close()

        result = [{
            'id': str(u['id']),
            'fullName': u['full_name'],
            'email': u['email'],
            'accountType': u['account_type']
        } for u in users]

        return jsonify({'users': result}), 200

    except Exception as e:
        print(f'Get users error: {e}')
        return jsonify({'error': 'Failed to get users'}), 500
