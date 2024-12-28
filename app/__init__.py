
from flask import Flask, request, jsonify
from app.routes.user_routes import user_bp
from app.routes.ai import ai_bp

app = Flask(__name__)


@app.route('/')
def get_user():
    return "Welcome", 200

app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(ai_bp, url_prefix='/ai')

if __name__ == "__main__":
    app.run(debug = True)
