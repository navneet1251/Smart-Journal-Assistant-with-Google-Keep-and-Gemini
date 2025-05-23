# 🧠 Smart Journal Assistant (LLM + Google Workspace)

The **Smart Journal Assistant** is a Python-based CLI tool that reads your journal entries from **Google Docs**, extracts structured information using **Gemini AI**, and automatically creates **Google Calendar events** and **Google Tasks**.

It helps automate the transition from unstructured daily notes to actionable items.

---

## ✨ Features

- 📄 **Read journal entries** directly from Google Docs
- 🤖 **Extract insights using Gemini AI**:
  - Tasks (with optional due dates)
  - Calendar Events (with time and date)
  - Hashtags / Tags (e.g. `#meeting`, `#idea`)
- 🗓 **Create Calendar Events** using Google Calendar API
- ✅ **Create Tasks** using Google Tasks API
- 📦 Save structured output as a log in JSON format

---

## 📦 Example Input & Output

**Journal Input in Google Docs:**

```text
Team call Friday at 10am. Need to book flight by Wednesday. Think about project X. #meeting #todo
```

---

**Output JSON:**
```json
{
  "tasks": [
    {
      "description": "Book flight",
      "due_date": "Wednesday"
    }
  ],
  "events": [
    {
      "description": "Team call",
      "datetime": "Friday at 10am"
    }
  ],
  "tags": ["#meeting", "#todo"]
}
```

---

##🚀 Getting Started

1. Clone the Repository
   
2. Install Dependencies
```bash
pip install -r requirements.txt
```

3. Enable Google Cloud APIs
Go to Google Cloud Console:
- Enable these APIs:
  - Google Docs API
  - Google Calendar API
  - Google Tasks API
- Create OAuth 2.0 Client ID credentials for a Desktop App
- Download the credentials as credentials.json and place it in the root directory

4. Create a .env File
Create a .env file in the root directory:
```ini
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_DOC_ID=your_google_doc_id
```
---

##▶️ Usage
Run the main script:
```bash
python main.py
```

You’ll see output like:
```yaml
📖 Note:
Team call Friday at 10am. Need to book flight by Wednesday...

🔍 Gemini Response:
{ "tasks": [...], "events": [...], "tags": [...] }

🗓 Event Created: ...
✅ Task Created: ...
📦 Actions saved to logs/summary.json
```

---

##🗂 Project Structure
```bash
smart-journal-assistant/
│
├── main.py                      # Main CLI runner
├── .env                         # API keys and Google Doc ID
├── credentials.json             # Google OAuth credentials
├── token.json                   # Saved access/refresh token (auto-generated)
│
├── docs_listener.py             # Reads content from Google Docs
├── gemini_nlp_extractor.py      # Uses Gemini to extract structured info
├── calendar_task_sync.py        # Google Calendar and Tasks integration
│
├── logs/
│   └── summary.json             # Saved results from last run
│
├── requirements.txt
└── README.md
```

---

##⚙️ Tech Stack
- Python
- Google Workspace APIs
- Google Docs
- Google Calendar
- Google Tasks
- Gemini 1.5 Flash via google.generativeai
- OAuth2 using google-auth-oauthlib and google-auth

---

##📋 Requirements
- Python 3.8+
- Google Cloud Project with enabled APIs
- Gemini API key (via AI Studio)

---

##🔐 Authentication & Tokens
- On first run, the app will open a browser for Google authentication.
- A token.json file will be created to store refresh tokens.
- Keep credentials.json and .env secure.

---
