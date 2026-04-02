# MediBot — Hospital Chatbot Widget

A Python-based keyword matching chatbot embedded as a widget on a mock hospital website. Built as a college mini project for B.Tech Computer Engineering.

---

## What It Does

MediBot is a chatbot that sits on a hospital website and helps patients with:

- **Appointment Booking** — step-by-step flow to pick a doctor, day, and time slot
- **Doctor Search** — find doctors by specialization
- **Vaccine Information** — flu, typhoid, hepatitis, tetanus schedules
- **Daily Health Tips** — rotating wellness advice
- **Patient Support** — billing, insurance, lab reports, cancellation queries
- **Emergency Info** — ambulance contacts and emergency hours

---

## Project Structure

```
hospital-chatbot/
│
├── index.html       → Mock hospital website with the chat widget
├── chatbot.py       → Python keyword matching engine (all bot logic lives here)
└── server.py        → Flask API that connects the website to the Python bot
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Bot Engine | Python 3 (keyword matching) |
| Web Framework | Flask |
| Communication | fetch() / JSON |

---

## How to Run

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/hospital-chatbot.git
cd hospital-chatbot
```

**2. Install dependencies**
```bash
pip install flask flask-cors
```

**3. Start the Flask server**
```bash
python server.py
```
You should see:
```
MediBot server running at http://localhost:5000
```

**4. Open the website**

Open `index.html` directly in your browser. The chat widget is in the bottom-right corner.

---

## How It Works

```
User types in widget
        ↓
JS sends POST request to localhost:5000/chat
        ↓
Flask receives the message
        ↓
chatbot.py runs keyword matching and returns a response
        ↓
Flask sends reply back as JSON
        ↓
Widget displays the message
```

### Keyword Matching

The bot does not use any AI or machine learning. It works by scanning the user's message for known keywords:

```python
msg = user_message.lower().strip()

if any(w in msg for w in ["appointment", "book", "schedule"]):
    return "Let us book your appointment..."
```

The message is lowercased first so "APPOINTMENT" and "appointment" both match. The bot checks intents from top to bottom and returns the first match.

### Appointment Booking Flow

The booking feature uses a session state dictionary to remember where the user is across multiple messages:

```
"book appointment" -> choose specialization -> choose doctor -> choose day -> choose time -> Confirmed
```

---

## Future Scope

- Connect to a real database (SQLite / MySQL)
- Add NLP using NLTK for smarter matching
- User login and appointment history
- Email / SMS confirmation after booking
- Multilingual support (Hindi, Marathi)
- AI-powered symptom checker

---

## Requirements

```
Python 3.x
flask
flask-cors
```

---

## Author
Varun Kolambekar
Made as a Mini Project — B.Tech Computer Engineering
