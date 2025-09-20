
# PromptPilot Backend

This is the Flask backend for PromptPilot, an AI-powered prompt improvement assistant. It provides context-aware prompt enhancement, authentication, and data storage.

---

## Features

- AI-powered prompt improvement (never code or answers, only better prompts)
- Context-aware responses based on previous user intent
- JWT authentication
- MongoDB Atlas integration
- CORS support for frontend-backend communication
- Environment variables for secrets

---

## Getting Started

### 1. Install dependencies
```sh
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables
Copy `.env.example` to `.env` and fill in your secrets:
```
MONGO_URI=your_mongo_uri
JWT_SECRET_KEY=your_jwt_secret
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
MONGO_DBNAME=promptpilot
GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
```

### 3. Run the server
```sh
python run.py
```

---

## Deployment

- Deploy to [Render](https://render.com/) (free tier)
- Set environment variables in the Render dashboard
- Use MongoDB Atlas for cloud database

---

## Project Structure

```
backend/
├── app/
│   ├── routes/
│   ├── services/
│   ├── models/
│   └── __init__.py
├── .env.example
├── requirements.txt
└── run.py
```

---

## Example Use Cases

- Prompt engineering for AI models
- Image generation prompt improvement
- Coding prompt refinement (improved prompts, not code)

---

## License

MIT
