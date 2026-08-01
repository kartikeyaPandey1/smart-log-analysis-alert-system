# 🚀 Smart Log Analysis & Alert System

An AI-powered log analysis platform built using **Python, FastAPI, Streamlit, PostgreSQL, and Plotly** that automates the parsing, monitoring, and visualization of Spring Boot application logs.

The system enables developers to upload log files, analyze application behavior, detect anomalies, visualize trends, receive automated alerts, and gain actionable insights through an interactive dashboard.

---

## 📌 Overview

Application logs are one of the most valuable resources for monitoring software systems. However, manually analyzing thousands of log entries is time-consuming and error-prone.

The **Smart Log Analysis & Alert System** automates this process by extracting structured information from raw Spring Boot log files, performing intelligent analysis, generating interactive visualizations, and highlighting important system events.

---

# ✨ Features

- 📂 Upload Spring Boot log files
- ⚡ Fast log parsing using Regular Expressions (Regex)
- 📊 Interactive dashboard built with Streamlit
- 📈 Error trend visualization
- 📉 Severity distribution charts
- 🔥 Top recurring error analysis
- 📋 Recent logs with advanced filtering
- 🤖 AI-generated insights
- 🚨 Automated email alerts
- 📥 Export filtered logs as CSV
- 🗄 PostgreSQL database integration

---

# 🏗 System Architecture

```
                +----------------------+
                |   Spring Boot Logs   |
                +----------+-----------+
                           |
                           |
                    Upload Log File
                           |
                           ▼
                +----------------------+
                |   Streamlit Dashboard |
                +----------+-----------+
                           |
                           |
                           ▼
                +----------------------+
                |     FastAPI Backend   |
                +----------+-----------+
                           |
          +----------------+----------------+
          |                                 |
          ▼                                 ▼
    Log Parser                      PostgreSQL Database
          |                                 |
          +---------------+-----------------+
                          |
                          ▼
             Analytics & AI Insights Engine
                          |
                          ▼
                Interactive Dashboard
```

---

# 📊 Dashboard Modules

### 📌 Dashboard Summary

Provides an overview of:

- Total Logs
- Error Logs
- Warning Logs
- Info Logs
- Debug Logs

---

### 📈 Analytics

Visualizes

- Error Trend
- Severity Distribution
- Top Error Messages

using interactive Plotly charts.

---

### 📋 Recent Logs

Supports

- Service filtering
- Log level filtering
- Date range filtering
- Search by message
- Pagination
- CSV export

---

### 🤖 AI Insights

Automatically generates insights including

- Error percentage
- Most active service
- Most frequent error
- System health analysis
- Debug log statistics

---

### 🚨 Alert System

Automatically detects

- High error rates
- Critical failures
- Frequent exceptions

and sends email notifications.

---

# 🛠 Tech Stack

## Backend

- Python
- FastAPI
- SQLAlchemy

## Frontend

- Streamlit

## Database

- PostgreSQL

## Data Analysis

- Pandas

## Visualization

- Plotly

## Parsing

- Regular Expressions (Regex)

## Email Service

- SMTP

---

# 📂 Project Structure

```
SmartLogSystem
│
├── app
│   ├── database
│   ├── models
│   ├── routes
│   ├── schemas
│   └── services
│
├── dashboard
│   ├── modules
│   └── dashboard.py
│
├── main.py
├── requirements.txt
└── .gitignore
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/kartikeyaPandey1/smart-log-analysis-alert-system.git
```

```bash
cd smart-log-analysis-alert-system
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file and configure:

```env
DATABASE_URL=YOUR_DATABASE_URL

EMAIL_USER=YOUR_EMAIL

EMAIL_PASSWORD=YOUR_APP_PASSWORD

ALERT_RECEIVER=YOUR_EMAIL
```

---

## Start FastAPI

```bash
uvicorn main:app --reload
```

Open

```
http://127.0.0.1:8000/docs
```

---

## Start Streamlit

```bash
streamlit run dashboard/dashboard.py
```

---

# 📈 Future Improvements

- Docker Support
- Kubernetes Deployment
- Authentication & User Management
- Multi-file Log Upload
- Cloud Storage Integration
- AI-based Root Cause Analysis
- Predictive Failure Detection
- Real-time Log Streaming

---


---

# 👨‍💻 Author

**Kartikeya Pandey**

- GitHub: https://github.com/kartikeyaPandey1
- Portfolio: https://my-portfolio-psi-ashy-58.vercel.app/
- LinkedIn: www.linkedin.com/in/kartikeya-pandey-451b97289

---

# ⭐ Support

If you found this project helpful, consider giving it a ⭐ on GitHub.

---

## 📄 License

This project is developed for educational and internship purposes.
