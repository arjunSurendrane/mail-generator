from crypt import methods

from flask import Blueprint, g, jsonify, request
from chromadb_client.portfolio import portfolio
from middleware.auth_middleware import auth_middlewre

from database.mongodb import collection

user_bp = Blueprint('user_bp', __name__)

portfolio_client = portfolio()

@user_bp.before_request
def user_middleware():
    print('inside middleware')
    auth_middlewre()


@user_bp.route('/<user_id>')
def get_users(user_id):
    response = collection.find_one({"user_id": user_id}, {"_id": 0});
    return jsonify({"message": "List of users", "respones": response});

@user_bp.route('/login', methods=["post"])
def login():
    body = request.get_json()
    user = g.user
    response = collection.insert_one(user)
    print(response)
    return "Stroed user details into db"

@user_bp.route('/onboarding', methods=['PUT'])
def user_onboarding():
    body = request.get_json()
    user = g.user
    user_id = user['user_id']

    # Extract values from the request body with default None
    user_about = body.get("user_about", None)
    user_specialization = body.get("user_specialization", None)
    user_job_role = body.get("user_job_role", None)

    # Construct the update object dynamically
    update_object = {}
    if user_about:
        update_object["user_about"] = user_about
    if user_specialization:
        update_object["user_specialization"] = user_specialization
    if user_job_role:
        update_object["user_job_role"] = user_job_role

    # Update the database only if there are fields to update
    if update_object:
        collection.update_one({"user_id": user_id}, {"$set": update_object})

    return "Stored user onboarded details into db", 200



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
