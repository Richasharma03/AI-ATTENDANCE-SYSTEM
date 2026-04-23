# 🚀 AI Attendance System

A full-stack AI-powered attendance system built using **FastAPI (Backend)**, **React (Frontend)**, and **MongoDB**.
It includes features like attendance tracking, AI-based queries, and authentication.

---

## 📌 Features

* ✅ Student Attendance Management
* 🤖 AI Query System (Ask attendance-related questions)
* 🔐 Authentication with JWT
* 📊 MongoDB Database Integration
* 🌐 Full-stack Deployment (Render + Vercel)

---

## 🛠️ Tech Stack

### Backend:

* FastAPI
* Uvicorn
* MongoDB (PyMongo)
* Python-dotenv

### Frontend:

* React (Vite)
* Axios

---

## 📁 Project Structure

```
AI-ATTENDANCE-SYSTEM/
│
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   ├── .env
│   └── package.json
│
└── README.md
```

---

## ⚙️ Backend Setup

### 1. Go to backend folder

```bash
cd backend
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

```
MONGO_URI=your_mongodb_connection_string
OPENROUTER_API_KEY=your_openrouter_api_key
```

### 5. Run server

```bash
uvicorn app.main:app --reload
```

👉 Backend runs at:

```
http://127.0.0.1:8000
```

---

## ⚛️ Frontend Setup

### 1. Go to frontend folder

```bash
cd frontend
```

### 2. Install dependencies

```bash
npm install
```

### 3. Create `.env` file

```
VITE_API_URL=http://127.0.0.1:8000
```

### 4. Run frontend

```bash
npm run dev
```

👉 Frontend runs at:

```
http://localhost:5173
```

---

## 🔗 API Integration

All frontend API calls use:

```js
const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});
```

---

## 🌍 Deployment

### Backend (Render)

* Platform: Render
* URL:

```
https://ai-attendance-system-ij3s.onrender.com
```

---

### Frontend (Vercel)

#### Environment Variable:

```
VITE_API_URL=https://ai-attendance-system-ij3s.onrender.com
```

---

## 📡 Important Endpoints

| Method | Endpoint      | Description  |
| ------ | ------------- | ------------ |
| GET    | `/`           | Check server |
| GET    | `/docs`       | Swagger API  |
| POST   | `/ai/query`   | AI Query     |
| POST   | `/auth/login` | Login        |

---

## ⚠️ Notes

* Make sure `.env` files are not pushed to GitHub
* Use environment variables for API URLs
* Backend may take time to wake up (Render free tier)

---

## 📷 Demo

Backend Live:

```
https://ai-attendance-system-ij3s.onrender.com
```

---

## 👩‍💻 Author

Richa Sharma

---

