
```md
# Flask To-Do App with Google Calendar Sync

A full-stack To-Do web application built with **Flask**, featuring **user authentication**, **task prioritization**, **deadlines with time slots**, **inline editing**, and **two-way Google Calendar integration**.

This is not a beginner CRUD demo — it handles real user state, OAuth, and external API sync.

---

## Key Features

### User Authentication
- Secure registration & login (Flask-Login)
- Password hashing (Werkzeug)
- Session-based access control
- Each user sees **only their own tasks**

### Task Management
- Create, edit (inline), and delete tasks
- Toggle task status: **Pending → Working → Completed**
- Clear all tasks (user-specific)
- Automatic task creation timestamps

### Deadlines & Priority
- Optional deadline **date + time**
- Priority levels: Low / Medium / High
- Visual badges for status & priority

### Search & Filters
- Search tasks by title
- Filter by status
- Filter by priority
- Combine search + filters together

### Google Calendar Integration
- OAuth 2.0 login with Google
- Auto-create calendar events when tasks have deadlines
- Auto-update events when tasks are edited
- Auto-delete calendar events when tasks are removed
- Token refresh handled securely (no hard crashes)

---

## Why This Project Matters

Most To-Do apps stop at CRUD.

This one demonstrates:
- Real authentication flow
- OAuth with third-party APIs
- Background failure-safe integrations
- Clean Flask blueprint architecture
- Production deployment readiness (Gunicorn + Render)

This is **resume-worthy**, not tutorial-level.

---

## 🗂 Project Structure


Flask-ToDo-App/
├── run.py
├── requirements.txt
├── Procfile
├── .env
├── app/
│   ├── **init**.py
│   ├── extensions.py
│   ├── models.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── tasks.py
│   │   └── google.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── tasks.html
│   └── static/
│       ├── css/style.css
│       └── js/script.js
└── instance/
└── todo.db

```

````

---

## ⚙️ Installation & Setup

### 1️ Clone Repository
```bash
git clone https://github.com/bhrigu136/Flask-ToDo-App.git
cd Flask-ToDo-App
````

### 2️ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
```

### 3️ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️ Configure Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

⚠️ **Never commit Google credentials to GitHub.**

---

### 5️ Run the App

```bash
python run.py
```

Open:

```
http://127.0.0.1:5000
```

---

## 🌍 Deployment

* Deployed using **Gunicorn**
* Render-ready (`Procfile` included)
* SQLite for simplicity (can be swapped with PostgreSQL)

---

## 🧪 Tech Stack

* **Backend:** Flask, SQLAlchemy
* **Auth:** Flask-Login
* **Frontend:** HTML, CSS, Vanilla JS
* **Database:** SQLite
* **API:** Google Calendar API
* **Deployment:** Render + Gunicorn

---

## 👩‍💻 Author

**Tamanna Bhrigunath**
B.Tech – Poornima College of Engineering (Batch 2026)

* GitHub: [https://github.com/bhrigu136](https://github.com/bhrigu136)
* LinkedIn: [https://linkedin.com/in/tamanna-bhrigunath-578b43190](https://linkedin.com/in/tamanna-bhrigunath-578b43190)

