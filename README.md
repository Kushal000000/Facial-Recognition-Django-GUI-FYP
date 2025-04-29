# Facial Recognition Attendance System – Django GUI (Final Year Project)

This is the **Django-based GUI** component of a **Facial Recognition Attendance System** designed as a Final Year Project (FYP). The complete system enables contactless attendance logging using facial recognition, integrated with a live webcam (ESP32-CAM), real-time LCD messages, and a centralized MySQL (MariaDB) database hosted on a Raspberry Pi.

## 🔧 Technologies Used

- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap
- **Backend:** Python, Django, Flask (Raspberry Pi side)
- **Database:** SQLite3 (for Django), MySQL/MariaDB (for main data)
- **Hardware:** Raspberry Pi, ESP32-CAM, I2C LCD Display

## 🎯 Key Features

- **User/Admin Login**
- **Live Attendance Logs** from MySQL database
- **Search & Filter** attendance by name, ID, section, or date
- **Student Profile Viewer:** Dynamic image and data fetch via Flask API
- **Attendance Statistics & Charts**
- **Face Enrollment** support through integrated ESP32-CAM
- **Report Export (CSV/PDF)** for logs and statistics
- **Real-time Integration** with Flask server running on Raspberry Pi

## ⚙️ System Architecture

```
[User/Admin]
     ↓
[Django GUI (Laptop)]
     ↓ (REST API)
[Flask Server on Raspberry Pi]
     ↓
[MySQL (MariaDB) Attendance DB]
     ↓
[ESP32-CAM] ←→ [Face Recognition Scripts]
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Django 4.x
- SQLite3 (for Django)
- MySQL/MariaDB (on Raspberry Pi)
- Flask Server running on Raspberry Pi
- ESP32-CAM stream configured

### Clone Repository

```bash
git clone https://github.com/Kushal000000/Facial-Recognition-Django-GUI-FYP.git
cd Facial-Recognition-Django-GUI-FYP
```

### Setup Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Database Migration

```bash
python manage.py migrate
```

### Create Superuser (for admin access)

```bash
python manage.py createsuperuser
```

### Run the Server

```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

---

## 🔌 Raspberry Pi Integration (Flask API)

Ensure the Raspberry Pi is running the Flask server (`flask_face_enroll.py`) with:
- Face recognition attendance logging
- Student face enrollment
- MySQL database (`attendance_logs` table)
- REST endpoints accessible from the Django GUI

Update Django GUI's API URLs in views/settings accordingly.

---

## 📊 Django GUI Dashboard Features

- ✅ View today's attendance summary
- 🔍 Search by section, ID, or name
- 🧑 View student profiles & facial data
- 📅 Filter logs by date
- 📤 Export attendance logs
- 📈 Visualize attendance statistics with charts

---

## 🗃️ Folder Structure (Partial)

```
Facial-Recognition-Django-GUI-FYP/
│
├── attendance_gui/        # Main Django app
│   ├── templates/         # HTML files
│   ├── static/            # CSS, JS, images
│   ├── views.py           # Core logic
│   └── urls.py            # Routing
│
├── manage.py
├── db.sqlite3             # Local dev DB
└── requirements.txt       # Python packages
```

---

## 📸 Screenshots

*Add screenshots of:*
- Login Page
- Dashboard
- Attendance Log Table
- Student Profile View
- Chart/Statistics View

---

## 📝 Final Year Project Highlights

- Developed using Agile DSDM Methodology
- Includes pre/post surveys, test cases, Gantt charts
- Real-time deployment on local Raspberry Pi network
- Integrates multiple hardware and software components
- Academic-compliant documentation and analysis

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is for educational purposes. You may adapt or extend it with proper attribution.

---

## 🙋‍♂️ Author

**Kushal [@Kushal000000](https://github.com/Kushal000000)**  
Final Year BSc CS Student  
For queries or collaborations, feel free to open an issue or contact via GitHub.