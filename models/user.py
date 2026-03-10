from datetime import datetime

def create_user(fullName, email, phone, password, accountType, otp, otp_expires):
    return {
        'fullName': fullName,
        'email': email.lower(),
        'phone': phone,
        'password': password,
        'accountType': accountType,
        'verified': False,
        'otp': otp,
        'otp_expires': otp_expires,
        'profilePic': None,
        'bio': '',
        'createdAt': datetime.utcnow(),
        'updatedAt': datetime.utcnow()
    }

def user_to_dict(user):
    return {
        'id': str(user['_id']),
        'fullName': user['fullName'],
        'email': user['email'],
        'phone': user['phone'],
        'accountType': user['accountType'],
        'verified': user.get('verified', False),
        'profilePic': user.get('profilePic', None),
        'bio': user.get('bio', ''),
        'createdAt': str(user.get('createdAt', ''))
    }