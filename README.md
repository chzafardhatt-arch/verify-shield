# VerifyShield AI 🛡️
### Fraud Intelligence Platform · Built by Ahmad

![VerifyShield](https://img.shields.io/badge/Status-Live-brightgreen) ![Python](https://img.shields.io/badge/Python-3.13-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688) ![License](https://img.shields.io/badge/License-MIT-yellow)

> **Detect fraud instantly** — check emails, phone numbers & IP addresses in seconds using AI-powered risk scoring.

🌐 **Live Demo:** [verifyshield.netlify.app](https://verifyshield.netlify.app)

---

## ✨ Features

- 📧 **Email Risk Analysis** — Detect disposable, fake & high-risk email addresses
- 📱 **Phone Number Verification** — Identify VoIP, invalid & suspicious phone numbers
- 🌐 **IP Address Intelligence** — Detect VPNs, proxies, Tor networks & bots
- ⚡ **Real-time Results** — Instant risk scoring with detailed analysis
- 🔑 **API Key System** — Built-in client management with usage tracking
- 🛡️ **Admin Dashboard** — Manage clients, create API keys, monitor usage
- 🆓 **5 Free Checks** — No signup required to try

---

## 🚀 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| Database | SQLite |
| Hosting | Netlify (frontend) + Railway (backend) |
| APIs | Abstract API (Email, Phone, IP) |

---

## 🛠️ Local Setup

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/chzafardhatt-arch/verify-shield.git
cd verify-shield

# Install dependencies
pip install fastapi uvicorn requests

# Start the backend server
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Then open `index.html` in your browser.

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/check?email=` | GET | Email risk analysis |
| `/check-phone?phone=` | GET | Phone number verification |
| `/check-ip?ip=` | GET | IP address intelligence |
| `/admin/clients` | GET | List all clients (admin only) |
| `/admin/create-client` | GET | Create new API client |

### Example Usage

```bash
# Check an email
curl "https://verify-shield-production.up.railway.app/check?email=test@gmail.com&api_key=demo"

# Check a phone number
curl "https://verify-shield-production.up.railway.app/check-phone?phone=+1234567890&api_key=demo"

# Check an IP address
curl "https://verify-shield-production.up.railway.app/check-ip?ip=8.8.8.8&api_key=demo"
```

---

## 📊 Response Example

```json
{
  "email": "test@gmail.com",
  "score": 85,
  "status": "Safe",
  "risk": "low",
  "is_disposable": false,
  "requests_remaining": "demo"
}
```

---

## 🔧 Project Structure

```
verify-shield/
├── index.html          # Main frontend
├── admincommand.html   # Admin dashboard
├── app.py              # FastAPI backend
├── database.py         # Database & API key management
├── logo.png            # Brand logo
├── requirements.txt    # Python dependencies
└── Procfile            # Deployment config
```

---

## 🌟 Screenshots

Visit [verifyshield.netlify.app](https://verifyshield.netlify.app) to see it live!

---

## 📄 License

MIT License — free to use and modify.

---

## 👨‍💻 Author

**Ahmad Shehroz**
- GitHub: [@chzafardhatt-arch](https://github.com/chzafardhatt-arch)

---

⭐ **If you find this useful, please give it a star!**
