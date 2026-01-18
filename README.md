# UOttahack 8 — Safe Step

## Project Overview

This project is a UOttahack 8 hackathon submission designed to assist individuals with visual impairments. It uses a real-time camera feed to understand the environment around the user and provides spoken feedback and guidance.

Users interact with the system using voice commands triggered by a chosen keyword (currently **“Jarvis”**). The system can:

- **Request help** —> notify the volunteer application that a person is in need of help, sharing the location of the user.
- **Describe the surroundings** —> identify objects or obstacles in front of the user.
- **Provide safe path guidance** —> suggest the best route to avoid danger or obstacles.

---

## Features

- Real-time object recognition using camera input
- Voice activation with keyword detection
- Voice-based responses and guidance
- Help request feature to alert someone nearby or remotely
- Integrates with ElevenLabs and OpenRouter for speech and AI capabilities

---

## Demo

Temporary Demo (While we make a better one)
https://www.youtube.com/watch?v=YQZsb7ThCmM

---

## Requirements

- Python 3.10+
- `venv` for virtual environment
- `ngrok` for exposing the backend API to the frontend
- A webcam or camera device for real-time vision input

---

## Setup Instructions

### 1. Create a Python Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

### 1. Run the Backend API

```bash
uvicorn backend.api.api:app --host 0.0.0.0 --port 8000 --workers 1
```

### 2. Run ngrok (Or alternative)

```bash
ngrok http 8000
```

Copy the ngrok forwarding URL (e.g., https://somelink.ngrok.io).

### 3. Configure .env

```bash
ELEVENLABS_API_KEY=<your_elevenlabs_api_key>
OPENROUTER_API_KEY=<your_openrouter_api_key>
NGROK_URL=<your_ngrok_url>
```

### 4. Update script.js

Replace the API base URL in script.js with the NGROK_URL you obtained from ngrok.

---

## Running The Voice Code

```bash
python -m backend.speech.listening
```

---

## Running the Frontend

```bash
live-server
```

### Example Commands

“Jarvis, help me”

“Jarvis, what’s in front of me?”

“Jarvis, guide me to a safe path”

In this case Jarvis is the key word, but this can be replaced in backend/speech/listen.py
