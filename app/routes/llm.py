from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.llm_service import LLMService

llm_bp = Blueprint("llm", __name__)
llm_service = LLMService()

@llm_bp.route("/improve", methods=["POST"])
@jwt_required()
def improve_prompt():
    data = request.get_json()
    prompt = data.get("prompt")
    model_choice = data.get("model", "gemini")  # Default to gemini if not provided
    previous_intent = data.get("previous_intent")
    if not prompt:
        return jsonify({"message": "Prompt is required"}), 400
    return llm_service.improve_prompt(prompt, model_choice, previous_intent)
