# 💸 Expense Tracker API

A simple backend API for an **Expense Tracker Application** built with **Django**, **Django REST Framework**, and **JWT Authentication**. It allows users to register, log in, and manage their daily expenses with analytics support.

---

## 📌 Features

- 🔐 User Registration & Login using JWT (access/refresh tokens)
- 💰 Create & View Expenses
- 📆 Filter expenses by date range
- 📊 Expense Analytics:
  - Total Expenses
  - Category-wise Breakdown
  - Daily / Weekly / Monthly Trends

---

## 🛠️ Tech Stack

- **Backend:** Django, Django REST Framework
- **Authentication:** JWT (`djangorestframework-simplejwt`)
- **Database:** SQLite (can be switched to PostgreSQL or MySQL)

---

## 📂 Project Structure

expense_tracker/
├── expense_tracker_app/
│ ├── models.py # Custom User & Expense Models
│ ├── serializers.py # DRF Serializers
│ ├── views.py # API Views (Register, Login, Expense, Analytics)
│ ├── urls.py # App-level Routing
├── expense_tracker_pro/
│ ├── settings.py # Project Settings
│ ├── urls.py # Main Routing

## 🔐 API Endpoints

### 🔸 Auth

- `POST /api/register/` — Register new user  
  **Body:**
  ```json
  {
    "email": "user@example.com",
    "name": "John Doe",
    "phone": "1234567890",
    "password": "YourPassword",
    "password2": "YourPassword"
  }
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/c005f43f-3975-4fa1-8432-e74f2889f9f1" />
