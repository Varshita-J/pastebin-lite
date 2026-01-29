# Pastebin-Lite

A minimal Pastebin-like application built with **Django**.  
Users can create text pastes and share a link to view them.  
Designed to be simple, fast, and testable.

---

## 🚀 Features

- Create a text paste  
- Retrieve a paste via unique ID  
- Optional expiration via view count  
- Health check endpoint  
- PostgreSQL persistence (Neon)  
- Deployed on Vercel  

---

## 🛠 Tech Stack

- **Backend:** Django, Django REST Framework  
- **Database:** PostgreSQL (Neon)  
- **Deployment:** Vercel  
- **Language:** Python 3.11+  

---
## API Endpoints
### **Health Check**
- **GET** `/api/healthz`  
Check if the server is running.

**Response:**
```json
{
  "ok": true
}
```

---

### **Create Paste**
- **POST** `/api/pastes`  
Create a new paste.

**Request Body:**
```json
{
  "content": "Hello world",
  "max_views": 5
}
```

**Response:**
```json
{
  "id": "mdGGVsNF",
  "content": "Hello world",
  "max_views": 5,
  "view_count": 0
}
```

---

### **Retrieve Paste**
- **GET** `/api/pastes/{id}`  
Retrieve a paste by its ID.

**Behavior:**
- Increments `view_count` on each request  
- Automatically deletes the paste when `max_views` is exceeded  

---

## ⚙️ Environment Variables

The following variables are required:
```env
DATABASE_URL=postgresql://<your-db-url>
TEST_MODE=1
```

---

## 🧑‍💻 Local Development

1. **Clone the repository**
```bash
git clone https://github.com/<your-username>/pastebin-lite.git
cd pastebin-lite
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Start the development server**
```bash
python manage.py runserver
```

Server will be running at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🌐 Deployment

- Connected to **Vercel**  
- PostgreSQL hosted on **Neon**  
- Environment variables configured in Vercel dashboard  
- Automatic redeploys on push to `main`

---

## 📄 Notes

- Uses Django ORM & REST framework  
- No authentication (by design)  
- Optimized for automated testing  
- Development server only (not production WSGI)

---

## 👤 Author

**Varshita**
