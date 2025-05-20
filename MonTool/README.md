# 📝 MonTool

A simple Monitoring tool integrated with Telegram

---

## 🚀 Features

- Create, update, delete servers
- Create, update, profile
- See dynamic stats of each server
- Receive alerts in Telegram in case of server failure
- List all servers in Telegram
- Contact Support team via Telegram

---


## 🛠️ Setup Instructions

### 1. Clone the repository

git clone https://github.com/hermit12195/montool.git

### 2. Run docker-compose
#### cd MonTool 
#### Setup .env with following required constants:
- DJANGO_SECRET_KEY=
- DJANGO_DEBUG="True or False"
- ENCRYPTION_KEY="for server password encryption
- POSTGRES_PASSWORD=
- POSTGRES_DB= 
- POSTGRES_USER= 
- POSTGRES_HOST=
- TOKEN="Telegram token"

#### docker compose up --build
