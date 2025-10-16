import os
from flask import jsonify
from config import Config
import google.generativeai as genai
from groq import Groq

PROMPT_INSTRUCTIONS = """
if conversation is hi bye type inputs reply accordingly, don't make improved prompt.

You are an expert creative assistant for prompt engineering. Your task is to take a user's simple concept and expand it into a detailed, rich, effective, and intent-aware prompt by identifying the user's intent (coding, image generation, video generation, music, poems, Q/A's, explanation, etc.).

For coding prompts, DO NOT provide code or answers. Instead, generate an improved prompt that helps the user get better results from an AI coding assistant. Focus on clarifying requirements, specifying languages, edge cases, and expected outputs.

The enhanced prompt must be a length according to the user's intent; don't make it too long if not needed, and must include intent-based features.

Do not ask questions. Generate only the final, enhanced prompt based on the user's input.

User's simple prompt: "{user_prompt}"
Enhanced prompt:
"""

class LLMService:
    def improve_prompt(self, prompt, model_choice, previous_intent=None):
        # Check if prompt is already well structured
        if self._is_well_structured(prompt):
            return jsonify({"improved_prompt": "Your prompt is well structured, no need for improvement."})

        greetings = ["hi", "hello", "hey", "bye", "see you", "goodbye"]
        short_responses = ["ok", "thanks", "thank you", "cool", "great", "got it", "nice", "awesome"]
        prompt_lower = prompt.strip().lower()

        # Only treat as greeting if the prompt is short and matches a greeting exactly
        if prompt_lower in greetings:
            if prompt_lower in ["hi", "hello", "hey"]:
                return jsonify({"improved_prompt": "Hi! Want to make your prompt better? Send me your prompt and I'll provide an improved version."})
            elif prompt_lower in ["bye", "see you", "goodbye"]:
                return jsonify({"improved_prompt": "See you! If you need prompt improvements, just send me your prompt anytime."})

        # Context-aware short response
        if prompt_lower in short_responses:
            if previous_intent == "image_generation":
                return jsonify({"improved_prompt": "You're welcome! If you want to generate images of other things, like bikes, just type your prompt and I'll help you out."})
            elif previous_intent == "coding":
                return jsonify({"improved_prompt": "You're welcome! If you want to create improved prompts for coding tasks, just describe what you want to build and I'll help you craft a better prompt!"})
            # Add more intent-based responses as needed
            else:
                return jsonify({"improved_prompt": "You're welcome! If you need more help, just send another prompt."})

        if model_choice == 'gemini':
            return self._improve_with_gemini(prompt)
        elif model_choice == 'llama3':
            return self._improve_with_llama3(prompt)
        else:
            return jsonify({"message": "Invalid model choice"}), 400

    def _is_well_structured(self, prompt):
        # Simple heuristic: prompt length, punctuation, and keywords
        prompt = prompt.strip()
        if len(prompt) > 40 and ('.' in prompt or ':' in prompt or '-' in prompt):
            return True
        # Add more checks as needed for your use case
        return False

    def _improve_with_gemini(self, simple_prompt: str):
        api_key = Config.GOOGLE_API_KEY
        if not api_key:
            return jsonify({"message": "Google API key is not configured"}), 500
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            full_instruction = PROMPT_INSTRUCTIONS.format(user_prompt=simple_prompt)
            response = model.generate_content(full_instruction)
            return jsonify({"improved_prompt": response.text.strip()})
        except Exception as e:
            return jsonify({"message": f"An error occurred with Gemini: {e}"}), 500

    def _improve_with_llama3(self, simple_prompt: str):
        api_key = Config.GROQ_API_KEY
        if not api_key:
            return jsonify({"message": "Groq API key is not configured"}), 500
        try:
            client = Groq(api_key=api_key)
            full_instruction = PROMPT_INSTRUCTIONS.format(user_prompt=simple_prompt)
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": full_instruction}],
                model="llama-3.1-8b-instant",
            )
            return jsonify({"improved_prompt": chat_completion.choices[0].message.content.strip()})
        except Exception as e:
            return jsonify({"message": f"An error occurred with Llama 3: {e}"}), 500
