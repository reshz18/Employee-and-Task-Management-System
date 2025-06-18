# 👩‍💼 Employee and Task Management System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Django](https://img.shields.io/badge/Django-Framework-success)

A powerful, web-based **Employee and Task Management System** built with Django and MySQL. This system simplifies HR operations like employee record keeping, task tracking, attendance monitoring, leave approvals, and real-time team communication—all in one place.

---

## 📚 Table of Contents

- [Description](#description)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## 📝 Description

The **Employee and Task Management System** streamlines HR and administrative workflows by combining CRUD operations, real-time communication, and data analytics into a single intuitive interface. Built for managers and employees to interact seamlessly.

---

## ✨ Features

### 👤 Admin/Manager:
- Add / Edit / Delete Employees  
- Assign & Track Tasks  
- Attendance Management (with Graphs)  
- Salary Management  
- Approve Leave Requests  
- Performance Analytics  
- Real-Time Chat (WebSocket)  
- Google Meet-style Video Meetings  
- Export Reports (Excel/PDF)

### 🙋 Employee:
- View & Submit Tasks  
- Mark Attendance  
- Apply for Leave  
- View Salary Info  
- Track Own Performance  
- Join Chat & Video Meetings

---

## ⚙️ Tech Stack

| Layer        | Tech Used                    |
|--------------|------------------------------|
| Backend      | Python, Django               |
| Database     | MySQL (configurable)         |
| Real-Time    | Django Channels (WebSockets) |
| Frontend     | HTML, CSS, Bootstrap         |
| Exporting    | OpenPyXL, ReportLab          |
| Auth & Admin | Django Auth + Superuser      |
| Others       | CORS Headers, Virtual Env    |

---

## 🚀 Installation

### 🔧 Prerequisites

- Python 3.8+
- pip
- Django
- MySQL (or SQLite for dev)
- Git

### 📦 Setup Steps

```bash
# Clone the repository
git clone https://github.com/reshz18/Employee-and-Task-Management-System.git

# Navigate to the project
cd office_emp_proj

# Create & activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Set up MySQL in settings.py
# (update NAME, USER, PASSWORD in DATABASES config)

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run development server
python manage.py runserver
````

---

## 🔐 Usage

* Visit `http://127.0.0.1:8000/` in your browser
* Login with your admin credentials
* Use the dashboard to manage employees and tasks

---

## 📸 Screenshots

> Add screenshots or screen recordings of dashboard, task view, attendance graph, etc. here for better understanding.

```
📷 screenshots/dashboard.png  
📷 screenshots/employee_list.png  
📷 screenshots/chat_module.png  
```

---

## 🤝 Contributing

Pull requests are welcome!

```bash
# Fork the repository
# Create your feature branch
git checkout -b my-feature

# Commit your changes
git commit -m "Add awesome feature"

# Push to GitHub
git push origin my-feature

# Open a Pull Request ✨
```

---


## 👨‍💻 Author

Made with 💙 by **Kopparapu Sai Reshwant**
GitHub: [@reshz18](https://github.com/reshz18)

---




