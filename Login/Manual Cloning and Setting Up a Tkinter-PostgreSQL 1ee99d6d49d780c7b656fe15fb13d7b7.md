# Manual: Cloning and Setting Up a Tkinter-PostgreSQL Login System

This guide explains how to **clone, install, and run** a Python-based **GUI login system** using **Tkinter** and **PostgreSQL**. Follow these steps to get the project running on a new machine.

---

## **Prerequisites**

Before starting, ensure you have:

1. **Python 3.8+** ([Download Python](https://www.python.org/downloads/))
2. **PostgreSQL** ([Download PostgreSQL](https://www.postgresql.org/download/))
3. **Git** (for cloning the repository)
4. **pip** (usually comes with Python)

---

## **Step 1: Clone the Repository**

1. Open **Terminal (Linux/macOS)** or **Command Prompt/PowerShell (Windows)**.
2. Run:

```bash
git clone https://github.com/peter-njuku/Python_Projects
cd Python_Projects
```

---

## **Step 2: Set Up PostgreSQL Database**

1. **Start PostgreSQL**:
    - **Linux**

```bash
sudo systemctl start postgresql
```

• **Windows**: Open **pgAdmin** or run PostgreSQL from Services.

1. **Create a Database & User** (if not already set up):
- Open **psql** (PostgreSQL CLI) or use **pgAdmin**.
- Run:

```sql
CREATE DATABASE login;
CREATE USER python_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE login TO python_user;
```

• If the database already exists, change and verify credentials in **`connection.py`**.

---

## **Step 3: Install Dependencies**

1. Install packages from **`requirements.txt`**:

```bash
pip install -r requirements.txt
```

---

## **Step 4: Run the Application**

1. Execute the GUI:

```bash
python login_gui.py
```

1. **Expected Output**:
- A Tkinter window with **Username** and **Password** fields.
- Buttons for **Login** and **Register**.
- Test registration and login functionality.

---

## **Step 5: Troubleshooting**

### **1. PostgreSQL Connection Errors**

- **Error**: **`psycopg2.OperationalError: connection failed`**
    
    **Solution**:
    
    - Ensure PostgreSQL is running (**`sudo systemctl start postgresql`**).
    - Verify credentials in **`connection.py`** match your PostgreSQL setup.

### **3. Missing Dependencies**

- **Error**: **`ModuleNotFoundError: No module named 'psycopg2'`**
    
    **Solution**:
    

```bash
pip install -r requirements.txt
```