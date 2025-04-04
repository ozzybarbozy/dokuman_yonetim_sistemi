from flask import Blueprint

# Create blueprint for preview
preview_bp = Blueprint('preview', __name__)

@preview_bp.route('/')
def index():
    return "Hello from preview"
