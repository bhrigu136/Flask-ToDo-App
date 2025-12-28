```
# 📝 Flask To-Do App with Google Calendar Sync

A complete To-Do task manager web application built using Flask.  
It includes secure authentication, task priority management, deadline selection, task search, filters, and status tracking for each user.

---

## 🚀 Key Features

### 👤 User Authentication
- User registration and login system
- Password hashing (safe storage, no plain text)
- Logout functionality
- Each user sees only **their own tasks**

### ✔ Task Management
- Add new tasks
- Delete individual tasks
- Clear all tasks for a user
- Change task status (Pending → Working → Completed)
- Automatic created date storage

### 🏷 Task Attributes
- Priority (Low / Medium / High)
- Optional deadline (date)
- Visual badge colors for task status & priority

### 🔍 Search & Filter
- Search tasks by name
- Filter by status
- Filter by priority
- Combine both filters together

---

## 🗂 Project Structure

```

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

````

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/bhrigu136/Flask-ToDo-App.git
cd Flask-ToDo-App
````

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

⚠️ **Never commit Google credentials to GitHub.**

---

### 5️⃣ Run the App

```
python run.py
```

Open:

```
http://127.0.0.1:5000
```

---
## 🧩 Future Enhancements

- Edit Task modal
- PostgreSQL DB
- Email reminders
- CSV export
- Dark mode UI

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
B.Tech – Poornima College of Engineering (2026)

- 💻 GitHub: https://github.com/bhrigu136  
- 🔗 LinkedIn: https://linkedin.com/in/tamanna-bhrigunath-578b43190  
- 📧 Email: bhrigunathtamanna@gmail.com  

---

## ⭐ Show Support

If you like this project, please:

- ⭐ Star the repository  
- 🍴 Fork it  
- 🐛 Create an issue if something breaks  
