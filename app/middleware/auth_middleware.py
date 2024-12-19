from flask import g, jsonify, request
import firebase_admin
from firebase_admin import credentials

# cred = credentials.Certificate("/home/arjun/PycharmProjects/email-generator/firebase-cred/firebase-config.json")
# firebase_admin.initialize_app(cred)


def auth_middlewre():
    g.user={
        "user_id": "1",
        "user_name": "Arjun",
        "user_about":"2 year experieced pro developer",
        "user_specialization":"2 year experienced backend engineer",
        "user_job_role":"BE Engineer"
    }
    # auth_header = request.headers.get('Authorization')
    # if not auth_header:
    #     return jsonify({'error': 'Missing Authorization Header'}), 401
    #
    # token = auth_header.split("Bearer ")[-1]
    #
    # try:
    #     # Verify the token
    #     decoded_token = auth.verify_id_token(token)
    #     uid = decoded_token['uid']  # User ID from the token
    #     g.user = decoded_token
    # except firebase_admin.auth.InvalidIdTokenError:
    #     return jsonify({'error': 'Invalid ID token'}), 401
    # except firebase_admin.auth.ExpiredIdTokenError:
    #     return jsonify({'error': 'Token expired'}), 401
    # except firebase_admin.auth.RevokedIdTokenError:
    #     return jsonify({'error': 'Token has been revoked'}), 401
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500



