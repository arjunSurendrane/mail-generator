from crypt import methods

from flask import Blueprint, jsonify, request
from chromadb_client.portfolio import portfolio

user_bp = Blueprint('user_bp', __name__)

portfolio_client = portfolio()


@user_bp.route('/')
def get_users():
    user_id = "1"
    respones = portfolio_client.get_all_project(user_id)
    return jsonify({"message": "List of users", "respones": respones})

@user_bp.route('/login', methods=["post"])
def login():
    body = request.get_json()
    return "Stroed user details into db"

@user_bp.route('/onboarding', methods=['put'])
def user_onboarding():
    body = request.get_json()
    # TODO: Store user details into db
    return "Stored user onboarded details into db"


@user_bp.route('/project', methods=['put'])
def update_project():
    body = request.get_json()
    user_id= "1"
    project_link = body["link"]
    project_stack = body["stack"]

    if not project_link and not project_stack:
        return jsonify({"message": "project link and project skills are required"}), 400

    try:
        response = portfolio_client.add_project(user_id, project_link, project_stack)
        return jsonify({
            "message":"success",
            "response": response
        })

    except Exception as error:
        print(error)
        return jsonify({"error": str(error)}), 500
