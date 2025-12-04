# 📝 Flask To-Do App (User Auth + Priority + Deadlines + Search & Filter)

A full-stack task management application built using **Flask**, featuring user authentication, task organization, priority management, deadlines, filters, and time slot scheduling.  
The application is fully deployed and live on the internet.

---

## 🚀 Live Demo

🔗 https://flask-todo-app-9fms.onrender.com

> Register a new user and start managing your tasks instantly.

---

## ✨ Features

✔ User register & login system  
✔ Add tasks with:
- Title  
- Priority (High / Medium / Low)  
- Deadline (date)  
- Time Slot (HH:MM AM/PM)  
- Status (Pending → Working → Completed)

✔ Filter tasks by:
- Status  
- Priority  
- Search text

✔ Change task status using **Next** button  
✔ Delete individual tasks  
✔ Clear all tasks  
✔ Flash message notifications  
✔ Responsive UI with custom CSS styling  
✔ SQLite database with SQLAlchemy ORM  
✔ Deployed using Gunicorn on Render

---

## 🛠️ Tech Stack

### Backend
- Python 3
- Flask
- SQLAlchemy
- Flask-Login

### Frontend
- HTML5
- CSS3
- Jinja2 Template Engine

### Deployment
- Render.com
- Gunicorn
- Requirements.txt
- Procfile

---

## 📁 Project Structure

```
project/
│   run.py
│
└───app/
    │   __init__.py
    │   models.py
    │
    └───routes/
    │    │   auth.py
    │    │   tasks.py
    │
    └───templates/
    │    │   base.html
    │    │   login.html
    │    │   register.html
    │    │   tasks.html
    │
    └───static/
         └───css/style.css
         └───js/script.js
```

---

## 🚀 Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/bhrigu136/Flask-ToDo-App.git
cd Flask-ToDo-App
```

### 2️⃣ Create a virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### 3️⃣ Install dependencies

```bash
pip install flask flask_sqlalchemy flask_login werkzeug
```

### 4️⃣ Remove old database (if it exists)

```bash
del todo.db
```

### 5️⃣ Run the application

```bash
python run.py
```

### 6️⃣ Open in browser

```
http://127.0.0.1:5000/
```

---
## 🧩 Future Enhancements

- Edit Task modal
- PostgreSQL DB
- Email reminders
- CSV export
- Dark mode UI

---

## ✍️ Author

**Tamanna Bhrigunath**  
B.Tech – Poornima College of Engineering (2026)
Python & Data Science Enthusiast

- 💻 GitHub: https://github.com/bhrigu136  
- 🔗 LinkedIn: https://linkedin.com/in/tamanna-bhrigunath-578b43190  
- 📧 Email: bhrigunathtamanna@gmail.com  

---

## ⭐ Show Support

If you like this project, please:

- ⭐ Star the repository  
- 🍴 Fork it  
- 🐛 Create an issue if something breaks  
