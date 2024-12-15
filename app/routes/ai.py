from flask import Blueprint, g, jsonify, request
from chromadb_client.portfolio import portfolio
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from utils import clean_text
from middleware.auth_middleware import auth_middlewre

ai_bp = Blueprint('ai_bp', __name__)

@ai_bp.before_request
def user_middleware():
    print('inside middleware')
    auth_middlewre()


@ai_bp.route("/")
def ai_welcome_route():
    user = g.user
    print(user)
    return "Welcome to AI api", 200


# Initialize the portfolio client
portfolio_client = portfolio()

@ai_bp.route('/job-description', methods=['POST'])
def get_users():
    """
    Endpoint to process job descriptions from either a URL or raw text,
    extract job information, and return projects for a specific user.
    """
    llm = Chain()

    # extract it from authentication
    user = g.user

    user_id = user["user_id"]

    # Validate the JSON body
    body = request.get_json()
    if not body:
        return jsonify({"error": "Request body must be JSON"}), 400

    # Retrieve 'url' and 'text' fields from the body
    url = body.get('url')
    text = body.get('text')

    if not url and not text:
        return jsonify({"error": "Either 'url' or 'text' is required"}), 400

    try:
        data = None
        # Process data: Load from URL or use raw text
        if url:
            loader = WebBaseLoader([url])
            data = clean_text(loader.load()[0].page_content)
        elif text:
            data = clean_text(text)

        # Extract job details using LLM chain
        jobs = llm.extract_jobs(data)

        emails = []

        for job in jobs:
            skills = job.get('skills', [])
            print("skills", skills)

            # Retrieve portfolio projects for the user
            vectorResults = portfolio_client.query_user_projects(str(skills), user_id)
            links = vectorResults.get('metadatas', [])
            skills = vectorResults.get('documents', [])
            email = llm.write_mail(job, links, skills, user["user_name"], user["user_specialization"], user["user_job_role"], user["user_about"])
            emails.append(email)
            print("email", email)

        # Return a successful response
        return jsonify({
            "message": "Job description processed successfully",
            "jobs": jobs,
            "email": emails,
        })
    except Exception as e:
        # Handle errors gracefully
        print(e)
        return jsonify({"error": str(e)}), 500
