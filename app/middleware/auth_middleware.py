from flask import g, jsonify, request

def auth_middlewre():
    g.user={
        "user_id": "1",
        "user_name": "Arjun",
        "user_about":"2 year experieced pro developer",
        "user_specialization":"2 year experienced backend engineer",
        "user_job_role":"BE Engineer"
    }


