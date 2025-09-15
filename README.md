# Pub Quiz Buzzer Web App

A real-time buzzer system for pub quizzes 🏆.  
Teams join with a unique name, buzz in when the host opens the buzzers, and scores are tracked across the round.  
Built with **FastAPI** + **WebSockets**, containerized with **Docker**.

---

## 🚀 Features
- Host screen: control the round, open/close buzzers, track scores, see buzz order.
- Player screen: join with team name, buzz in, see fastest buzzers and live leaderboards.
- Score tallying: points awarded for correct answers.
- Question counter: visible to both host and players.
- Final leaderboard: shows after the last question.
- Works on any device via **ngrok remote access**.

---

## 🐳 Run with Docker

1. Make sure [Docker](https://docs.docker.com/get-docker/) is installed.  
   (On Windows with WSL2 you can install Docker Engine inside Ubuntu instead of Docker Desktop.)

2. Clone the repo and open the folder:
   ```bash
   cd /mnt/d/OneDrive/Quiz_App
   ```

3. Build the Docker image:
   ```bash
   docker build -t quiz_app .
   ```

4. Run the container:
   ```bash
   docker run -p 8000:8000 quiz_app
   ```

5. Open in your browser:
   - Host: [http://localhost:8000/host/QUIZ123](http://localhost:8000/host/QUIZ123)
   - Player: [http://localhost:8000/player/QUIZ123](http://localhost:8000/player/QUIZ123)

---

## 🌍 Remote Access with ngrok

1. [Download ngrok](https://ngrok.com/download) for Windows and install.  
   Verify with:
   ```powershell
   ngrok --version
   ```

2. In PowerShell (Windows, **not** WSL), run:
   ```powershell
   ngrok http 8000
   ```

3. You’ll get a public URL like:
   ```
   Forwarding  https://abc123.ngrok-free.app -> http://localhost:8000
   ```

4. Share the links:
   - Host: `https://abc123.ngrok-free.app/host/QUIZ123`
   - Player: `https://abc123.ngrok-free.app/player/QUIZ123`

> ⚠️ Without an ngrok account, links last ~2 hours. With a free account, you can use static subdomains and longer sessions.

---

## 🎯 Quick Start (One Command Workflow)

After making changes to the code, from your project folder:

```bash
docker build -t quiz_app . && docker run -p 8000:8000 quiz_app
```

Then in another PowerShell window:

```powershell
ngrok http 8000
```

Share the ngrok URL with your players 🎉.

---

## 🛠 Project Structure

```
Quiz_App/
├── app/
│   ├── main.py
│   ├── routers.py
│   ├── state.py
│   ├── templates/
│   │   ├── host.html
│   │   ├── player.html
│   │   └── index.html
│   └── static/
│       └── app.js
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 🧩 Tech Stack
- **FastAPI** (Python web framework)
- **WebSockets** for real-time buzzers
- **Jinja2** templating
- **Docker** for packaging
- **ngrok** for public tunneling

---

## 📜 License
MIT License – free to use and modify.
