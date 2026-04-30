# WhatsApp AI Automation (MVP)

> AI-powered WhatsApp sales automation system with product search, order handling, and unified backend for web + messaging.

---

## Table of Contents

* Overview
* Project Structure
* Setup & Installation
* Environment Variables
* Running the Project
* Webhook Setup (WhatsApp)
* API Endpoints
* License

---

# Overview

This project is a **WhatsApp AI Automation System** that allows businesses to:

* Automatically respond to customer messages
* Help users find products
* Take orders via WhatsApp
* Manage everything from a single backend

It connects:

* WhatsApp (customer interaction)
* Website (product browsing)
* Backend (AI + database + logic)

---

# Tech Stack

* Backend: FastAPI
* AI: LLM (LangChain-ready)
* Database: PostgreSQL
* Messaging: WhatsApp Cloud API
* Dev Tunnel: ngrok
* Frontend: Next.js / React.js

---

# Project Structure

```plaintext
backend/
 ├── app/
 │   ├── api/            # webhook routes
 │   ├── services/       # product, order, AI logic
 │   ├── db/             # database session & models
 │   ├── core/           # config & settings
 │   └── main.py         # FastAPI entry
 ├── requirements.txt
 └── .env
```

---

# Setup & Installation

```bash
# clone repo
 git clone <repo-url>
 cd backend

# create virtual env
 python -m venv .venv
 .venv\Scripts\activate

# install dependencies
 pip install -r requirements.txt
```

---

# Environment Variables (.env)

```env
DATABASE_URL=your db url
GOOGLE_API_KEY=Google api key
WHATSAP_BASE_URL=whatsapp Base Url
PHONE_ID=Whatsapp Phone Id
WHATSAPP_TOKEN=Whatsapp Pemanent Access Tokens
```

---

# Running the Project

```bash
uvicorn app.main:app --reload
```

---

# Webhook Setup (WhatsApp)

1. Run ngrok:

```bash
ngrok http 8000
```

2. Copy URL:

```
https://xxxx.ngrok-free.app/webhook
```

3. Set in Meta Dashboard:

* Callback URL = ngrok URL
* Verify Token = same as .env

4. Subscribe to:

* messages
* message_status

---

# API Endpoints

### Search Products

```
GET /products/search?q=keyword
```

### Webhook

```
GET /webhook   (verification)
POST /webhook  (incoming messages)
```

---

# License

This project is for MVP and educational/business prototype use.

---
