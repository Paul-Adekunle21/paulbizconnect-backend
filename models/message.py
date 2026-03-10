from datetime import datetime

def create_message(conversation_id, sender_id, receiver_id, text, msg_type='text'):
    return {
        'conversation_id': conversation_id,
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'text': text,
        'msgType': msg_type,
        'read': False,
        'createdAt': datetime.utcnow()
    }

def create_conversation(participant1_id, participant2_id):
    return {
        'participants': [participant1_id, participant2_id],
        'createdAt': datetime.utcnow(),
        'updatedAt': datetime.utcnow()
    }

def message_to_dict(msg, current_user_id):
    return {
        'id': str(msg['_id']),
        'conversation_id': msg['conversation_id'],
        'sender_id': msg['sender_id'],
        'receiver_id': msg['receiver_id'],
        'text': msg.get('text', ''),
        'msgType': msg.get('msgType', 'text'),
        'type': 'sent' if msg['sender_id'] == current_user_id else 'received',
        'read': msg.get('read', False),
        'time': msg['createdAt'].strftime('%I:%M %p')
    }