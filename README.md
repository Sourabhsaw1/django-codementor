# 🤖 CodeMentor AI

> **AI-Powered Code Review & Learning Platform** — Submit code, get instant feedback on bugs, performance, security & best practices. Built with Django.

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-darkgreen?logo=django)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Live-brightgreen)](https://github.com/Sourabhsaw1/django-codementor)

---

## 🚀 Live Demo

> 🔗 **[Live App →](#)** *(deploying soon on Railway)*

---

## 📸 What It Does

A developer submits their Python/JavaScript code → our engine analyzes it → they get:

- 🐛 **Bug report** with line numbers and exact fixes
- ⚡ **Performance tips** (e.g. "use list comprehension — 40% faster")
- 🔒 **Security scan** (detects eval(), hardcoded passwords, SQL injection risks)
- 📚 **Best practices** (PEP 8, docstrings, naming conventions)
- 🏆 **Score 0–100** + points added to leaderboard

---

## 🏗️ Project Structure

```
django-codementor/
├── codementor/          # Django project settings & URLs
├── users/               # Custom user model, auth (register/login/profile)
├── submissions/         # Code submission + analysis engine
│   └── analyzer.py      # Core AI analysis logic (bug detection, scoring)
├── leaderboard/         # Points & ranking system
├── templates/           # All HTML templates (dark UI)
│   ├── home.html
│   ├── dashboard.html
│   ├── submissions/
│   └── users/
├── static/              # CSS & JS assets
├── manage.py
├── requirements.txt
├── Procfile             # Railway/Heroku deployment
└── railway.json         # Railway config
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2 |
| Frontend | Django Templates + Bootstrap 5 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Auth | Django built-in + session auth |
| Deployment | Railway + Gunicorn + WhiteNoise |
| Analysis | Custom Python engine (`analyzer.py`) |

---

## ✨ Features

- ✅ User registration, login, logout, profile
- ✅ Code submission with language selection (Python, JS, Java, C++, Go)
- ✅ Real bug detection with severity levels (critical/high/medium/low)
- ✅ Performance analysis with improvement % estimates
- ✅ Security vulnerability scanner
- ✅ Best practices checker (PEP 8, docstrings, variable naming)
- ✅ Scoring system (0–100) with grade (A+/A/B/C/D)
- ✅ Points & leaderboard (top 50 users with medals 🥇🥈🥉)
- ✅ Submission history
- ✅ Responsive dark-theme UI

---

## 🔧 Run Locally

```bash
# 1. Clone
git clone https://github.com/Sourabhsaw1/django-codementor.git
cd django-codementor

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup database
python manage.py migrate

# 4. Run server
python manage.py runserver
```

Open: **http://localhost:8000**

---

## 🔍 How the Analyzer Works

The core analysis engine (`submissions/analyzer.py`) checks real code patterns:

```python
# Example detections:
except:              → "Bare except catches KeyboardInterrupt" (medium bug)
eval(user_input)     → "Code injection risk — CRITICAL security issue"
password = "abc123"  → "Hardcoded password detected" (high severity)
for i in range(len(x)) → "Use enumerate() instead" (performance tip)
```

Each check produces: **line number + severity + message + exact fix suggestion**

---

## 📊 Scoring Formula

```
Overall Score = (Readability × 0.3) + (Performance × 0.3) + (Security × 0.2) + (Best Practices × 0.2)
```

Points earned per submission → updates leaderboard automatically.

---

## 🚀 Deploy on Railway

```bash
# Already configured — just connect GitHub repo to Railway
# railway.json + Procfile + requirements.txt are ready
```

Environment variables needed:
```
DEBUG=False
SECRET_KEY=your-secret-key-here
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `submissions/analyzer.py` | Core analysis engine — bug detection, scoring |
| `submissions/models.py` | CodeSubmission model with all score fields |
| `users/models.py` | Custom User model with points & stats |
| `leaderboard/models.py` | LeaderboardEntry with rank calculation |
| `templates/submissions/result.html` | Tabbed results page (bugs/perf/security/practices) |
| `templates/home.html` | Landing page with live stats |

---

## 👨‍💻 Developer

**Sourabh Saw**
- GitHub: [@Sourabhsaw1](https://github.com/Sourabhsaw1)
- Email: sourabhsaw20052@gmail.com

---

## 📄 License

Apache License 2.0 — see [LICENSE](LICENSE)

---

*Built to demonstrate Django skills for open source contribution.*
