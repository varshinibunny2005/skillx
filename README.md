# SkillX — Skill Swap Platform

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py makemigrations accounts skills matching community learning
python manage.py migrate
```

### 3. Seed Initial Data (Skills + Tests)
```bash
python manage.py seed_data
```

### 4. Create Admin User
```bash
python manage.py createsuperuser
```

### 5. Run Server
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

---

## 📁 Project Structure

```
skillx/
├── accounts/       # User auth, profiles, streaks, leaderboard
├── skills/         # Skills, tests, verification
├── matching/       # Matching algorithm, requests, chat, video
├── community/      # Communities, groups, posts
├── learning/       # (Extensible learning module)
├── templates/      # All HTML templates
├── static/
│   ├── css/style.css   # Full custom dark UI
│   └── js/main.js      # Interactivity
└── manage.py
```

---

## ✨ Features

### 👤 User System
- Signup with name, bio, email, DOB, gender, language preference
- Email-based authentication
- Profile with avatar, bio, location

### 🎯 Skills
- 35+ pre-seeded skills across 14 categories
- "Skills I Have" + "Skills I Want to Learn" setup
- **Skill Test System** — Beginner / Intermediate / Expert tests
- XP awarded on test completion
- Verified badge shown on profile

### 🔍 Smart Matching
- Algorithm matches users based on complementary skills + language
- **Filters**: Age range, Gender, Language
- Match score shown visually

### 💬 Connections & Communication
- Send/Accept/Decline connection requests with custom messages
- **Real-time Chat** (text messaging)
- **Video Sessions** — in-browser WebRTC camera/mic controls, screen sharing
- Session history

### 🔥 Gamification
- **Daily Streak** tracker with fire animation
- **XP System** — earn points for completing tests, sessions
- **Leaderboard** — XP ranking + Streak ranking (Top 50)

### 🌐 Community
- Create/join **public or private Communities** around skills
- **Groups** within communities (max 20 members)
- Post feed with likes and comments
- Member directory

---

## 🔧 Admin Panel

Visit `/admin/` to:
- Add/manage skills and categories
- Create skill tests and questions
- View all connections, sessions, communities

---

## 🛠️ Tech Stack

- **Backend**: Django 4.2, Python
- **Frontend**: Bootstrap 5.3, Font Awesome 6, Google Fonts (Syne + DM Sans)
- **Database**: SQLite (dev) — swap with PostgreSQL for production
- **Video**: WebRTC (browser-native)
- **Styling**: Custom dark theme CSS with CSS variables

---

## 🔮 Extending

- **Real-time chat**: Replace polling with Django Channels + WebSocket
- **WebRTC signaling**: Add a signaling server for real peer-to-peer video
- **Email verification**: Configure SMTP in settings.py EMAIL_BACKEND
- **Push notifications**: Integrate Firebase FCM
