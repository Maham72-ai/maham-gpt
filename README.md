# 🤖 Maham GPT - Intelligent AI Chatbot

> Maham GPT is a modern, intelligent conversational AI assistant built to provide human-like, context-aware responses using Google's Gemini AI.

---

## 📖 Overview

**Maham GPT** is a full-stack AI chatbot designed to deliver seamless and intelligent conversations. It leverages **Google Gemini AI** for natural language understanding, **Qdrant** for vector-based knowledge retrieval, and **【entity-MongoDB¦canonical_name=MongoDB】** for secure data storage.

This project is developed as a production-ready chatbot with secure authentication and persistent chat history.

---

## ✨ Key Features

- 💬 **Intelligent Conversations** - Powered by Google Gemini AI for natural responses
- 🔐 **Secure Authentication** - JWT-based user registration & login
- 📜 **Chat History** - All conversations saved in 【entity-MongoDB¦canonical_name=MongoDB】
- ⚡ **Fast & Lightweight** - FastAPI backend with optimized performance
- 🎨 **Modern UI** - Clean, responsive React frontend (Vite)
- 🧠 **Knowledge Base** - Qdrant vector database for contextual intelligence
- 🔒 **User Privacy** - Isolated user data and secure sessions

---

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI (Python)
- **AI Engine:** Google Gemini API
- **Database:** 【entity-MongoDB¦canonical_name=MongoDB】 Atlas
- **Vector Database:** Qdrant Cloud
- **Authentication:** JWT (HS256)
- **Server:** Uvicorn

### Frontend
- **Framework:** React.js + Vite
- **Styling:** Modern CSS / Tailwind CSS
- **HTTP Client:** 【entity-Axios¦canonical_name=Axios】

---

## 📁 Project Structure

Maham-GPT/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── db/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md

---

## 🚀 Quick Start

### 1. Clone the Repository
git clone https://github.com/Maham72-ai/maham-gpt
cd Maham-GPT

### 2. Backend Setup
cd backend
pip install -r requirements.txt

Run Backend:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

### 3. Frontend Setup
cd frontend
npm install
npm run dev

---

## 🔑 Environment Variables

Create a .env file in backend/ folder:

GEMINI_API_KEY=your_gemini_api_key
MONGODB_URI=your_mongodb_connection_string
MONGODB_DB_NAME=ai_chatbot_db
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION=knowledge_base
JWT_SECRET_KEY=your_super_secure_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
FRONTEND_URL=http://localhost:5173

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
| POST | /api/auth/register | Register new user |
| POST | /api/auth/login | Login user |
| POST | /api/chat/ | Send message to Maham GPT |
| GET | /api/chat/history | Get chat history |
| DELETE | /api/chat/clear | Clear chat history |

---

## 💡 How It Works

1. Authentication: User logs in and receives JWT token
2. Message: User sends message via React frontend
3. Retrieval: System queries Qdrant for relevant context
4. Generation: Gemini AI generates intelligent response
5. Storage: Conversation saved in MongoDB
6. Response: Answer displayed in chat UI

---

## 👩‍💻 Developed By

Maham
Project: Maham GPT - AI Chatbot
Built with ❤️ using FastAPI, React & Gemini AI

---

## 📄 License

This project is developed for academic purposes.
### ⭐ Don't forget to star this repository!
