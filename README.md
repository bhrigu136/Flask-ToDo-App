# 📝 Flask To-Do App (User Auth + Priority + Deadlines + Search & Filter)

A complete To-Do task manager web application built using Flask.  
It includes secure authentication, task priority management, deadline selection, task search, filters, and status tracking for each user.

---

## ✨ Features

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

## ✍️ Author

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
