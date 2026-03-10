from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from config.db import get_db
from utils.emails import send_otp_email, send_welcome_email, send_password_reset_email
from datetime import datetime, timedelta
import random

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

# ===== REGISTER =====
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400

        required = ['fullName', 'email', 'phone', 'password', 'accountType']
        for field in required:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        conn = get_db()
        cur = conn.cursor()

        # Check email exists
        cur.execute('SELECT id FROM users WHERE email = %s', (data['email'].lower(),))
        if cur.fetchone():
            cur.close(); conn.close()
            return jsonify({'error': 'Email already registered. Please login.'}), 400

        # Check phone exists
        cur.execute('SELECT id FROM users WHERE phone = %s', (data['phone'],))
        if cur.fetchone():
            cur.close(); conn.close()
            return jsonify({'error': 'Phone number already registered.'}), 400

        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        otp = str(random.randint(100000, 999999))
        otp_expires = datetime.utcnow() + timedelta(minutes=10)

        cur.execute('''
            INSERT INTO users (full_name, email, phone, password, account_type, verified, otp, otp_expires)
            VALUES (%s, %s, %s, %s, %s, FALSE, %s, %s)
            RETURNING id
        ''', (
            data['fullName'],
            data['email'].lower(),
            data['phone'],
            hashed_password,
            data['accountType'],
            otp,
            otp_expires
        ))

        user_id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        conn.close()

        try:
            mail = Mail(current_app)
            send_otp_email(mail, data['fullName'], data['email'], otp)
        except Exception as mail_error:
            print(f'Mail error: {mail_error}')

        return jsonify({
            'message': 'Registration successful! OTP sent to your email.',
            'user_id': user_id,
            'email': data['email'].lower(),
            'otp_for_testing': otp
        }), 201

    except Exception as e:
        print(f'Register error: {e}')
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500


# ===== VERIFY OTP =====
@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    try:
        data = request.get_json()
        email = data.get('email', '').lower()
        otp = data.get('otp', '')

        if not email or not otp:
            return jsonify({'error': 'Email and OTP are required'}), 400

        conn = get_db()
        cur = conn.cursor()

        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cur.fetchone()

        if not user:
            cur.close(); conn.close()
            return jsonify({'error': 'User not found'}), 404

        if user['verified']:
            cur.close(); conn.close()
            return jsonify({'error': 'Account already verified. Please login.'}), 400

        if user['otp'] != otp:
            cur.close(); conn.close()
            return jsonify({'error': 'Incorrect OTP. Please try again.'}), 400

        if datetime.utcnow() > user['otp_expires']:
            cur.close(); conn.close()
            return jsonify({'error': 'OTP has expired. Please request a new one.'}), 400

        cur.execute('''
            UPDATE users SET verified = TRUE, otp = NULL, otp_expires = NULL
            WHERE email = %s
        ''', (email,))
        conn.commit()
        cur.close()
        conn.close()

        try:
            mail = Mail(current_app)
            send_welcome_email(mail, user['full_name'], user['email'], user['account_type'])
        except Exception as mail_error:
            print(f'Welcome mail error: {mail_error}')

        access_token = create_access_token(
            identity=str(user['id']),
            expires_delta=timedelta(days=7)
        )

        return jsonify({
            'message': 'Account verified successfully!',
            'token': access_token,
            'user': {
                'id': str(user['id']),
                'fullName': user['full_name'],
                'email': user['email'],
                'phone': user['phone'],
                'accountType': user['account_type']
            }
        }), 200

    except Exception as e:
        print(f'Verify OTP error: {e}')
        return jsonify({'error': f'Verification failed: {str(e)}'}), 500


# ===== RESEND OTP =====
@auth_bp.route('/resend-otp', methods=['POST'])
def resend_otp():
    try:
        data = request.get_json()
        email = data.get('email', '').lower()

        if not email:
            return jsonify({'error': 'Email is required'}), 400

        conn = get_db()
        cur = conn.cursor()

        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cur.fetchone()

        if not user:
            cur.close(); conn.close()
            return jsonify({'error': 'User not found'}), 404

        if user['verified']:
            cur.close(); conn.close()
            return jsonify({'error': 'Account already verified'}), 400

        otp = str(random.randint(100000, 999999))
        otp_expires = datetime.utcnow() + timedelta(minutes=10)

        cur.execute('''
            UPDATE users SET otp = %s, otp_expires = %s WHERE email = %s
        ''', (otp, otp_expires, email))
        conn.commit()
        cur.close()
        conn.close()

        try:
            mail = Mail(current_app)
            send_otp_email(mail, user['full_name'], user['email'], otp)
        except Exception as mail_error:
            print(f'Resend mail error: {mail_error}')

        return jsonify({
            'message': 'New OTP sent! Check your email.',
            'otp_for_testing': otp
        }), 200

    except Exception as e:
        print(f'Resend OTP error: {e}')
        return jsonify({'error': 'Failed to resend OTP.'}), 500


# ===== LOGIN =====
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email', '').lower()
        password = data.get('password', '')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        conn = get_db()
        cur = conn.cursor()

        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401

        if not bcrypt.check_password_hash(user['password'], password):
            return jsonify({'error': 'Invalid email or password'}), 401

        if not user['verified']:
            return jsonify({
                'error': 'Account not verified. Please verify your OTP first.',
                'not_verified': True,
                'email': email
            }), 401

        access_token = create_access_token(
            identity=str(user['id']),
            expires_delta=timedelta(days=7)
        )

        return jsonify({
            'message': 'Login successful!',
            'token': access_token,
            'user': {
                'id': str(user['id']),
                'fullName': user['full_name'],
                'email': user['email'],
                'phone': user['phone'],
                'accountType': user['account_type']
            }
        }), 200

    except Exception as e:
        print(f'Login error: {e}')
        return jsonify({'error': f'Login failed: {str(e)}'}), 500


# ===== FORGOT PASSWORD =====
@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    try:
        data = request.get_json()
        email = data.get('email', '').lower()

        if not email:
            return jsonify({'error': 'Email is required'}), 400

        conn = get_db()
        cur = conn.cursor()

        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cur.fetchone()

        if not user:
            cur.close(); conn.close()
            return jsonify({'message': 'If this email exists, a reset code has been sent.'}), 200

        reset_otp = str(random.randint(100000, 999999))
        reset_expires = datetime.utcnow() + timedelta(minutes=15)

        cur.execute('''
            UPDATE users SET reset_otp = %s, reset_expires = %s WHERE email = %s
        ''', (reset_otp, reset_expires, email))
        conn.commit()
        cur.close()
        conn.close()

        try:
            mail = Mail(current_app)
            send_password_reset_email(mail, user['full_name'], user['email'], reset_otp)
        except Exception as mail_error:
            print(f'Reset mail error: {mail_error}')

        return jsonify({
            'message': 'Password reset code sent to your email.',
            'otp_for_testing': reset_otp
        }), 200

    except Exception as e:
        print(f'Forgot password error: {e}')
        return jsonify({'error': 'Failed to process request.'}), 500


# ===== RESET PASSWORD =====
@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        email = data.get('email', '').lower()
        otp = data.get('otp', '')
        new_password = data.get('new_password', '')

        if not email or not otp or not new_password:
            return jsonify({'error': 'Email, OTP and new password are required'}), 400

        if len(new_password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400

        conn = get_db()
        cur = conn.cursor()

        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cur.fetchone()

        if not user:
            cur.close(); conn.close()
            return jsonify({'error': 'User not found'}), 404

        if user['reset_otp'] != otp:
            cur.close(); conn.close()
            return jsonify({'error': 'Incorrect OTP'}), 400

        if datetime.utcnow() > user['reset_expires']:
            cur.close(); conn.close()
            return jsonify({'error': 'OTP has expired'}), 400

        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

        cur.execute('''
            UPDATE users SET password = %s, reset_otp = NULL, reset_expires = NULL
            WHERE email = %s
        ''', (hashed_password, email))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'message': 'Password reset successful! Please login.'}), 200

    except Exception as e:
        print(f'Reset password error: {e}')
        return jsonify({'error': 'Failed to reset password.'}), 500


# ===== GET CURRENT USER =====
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()
        conn = get_db()
        cur = conn.cursor()

        cur.execute('SELECT * FROM users WHERE id = %s', (int(user_id),))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'user': {
                'id': str(user['id']),
                'fullName': user['full_name'],
                'email': user['email'],
                'phone': user['phone'],
                'accountType': user['account_type']
            }
        }), 200

    except Exception as e:
        print(f'Get user error: {e}')
        return jsonify({'error': 'Failed to get user'}), 500
