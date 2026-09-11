# 👋 Hi, I'm Erhan Emir

🛠️ **Maker & Developer** — Embedded Systems, IoT, Web & Mobile  
📍 Turkey | 🌐 [erhanemir.github.io](https://erhanemir.github.io)

---

### 🐍 Autonomous Snake (live in this README)

<p align="center">
  <a href="https://github.com/ErhanEmir/ErhanEmir/actions/workflows/snake.yml">
    <img src="snake.svg" alt="Autonomous Snake Game" width="600"/>
  </a>
</p>

<p align="center">
  <sub>🟢 Snake • 🍎 Food • 🧱 Walls • Auto-playing via Hamiltonian path</sub>
</p>

---

### 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| **Embedded** | C/C++, Arduino, ESP32/ESP8266, LoRa, FreeRTOS |
| **PCB & CAD** | EasyEDA, KiCad, Fusion 360, Tinkercad, 3D Printing |
| **Backend** | Python, FastAPI, Django, Linux, Docker, GitHub Actions |
| **Frontend** | HTML/CSS/JS (vanilla), TypeScript, React (basics) |
| **Mobile** | Dart, Flutter, Cross-platform apps |
| **Tools** | Git, GitHub, VS Code, PlatformIO, KiCad |

---

### 📦 Featured Projects

| Project | Description | Stack |
|---------|-------------|-------|
| **[indir-gitsin](https://github.com/ErhanEmir/indir-gitsin)** | Multi-platform video/image downloader (TikTok, Instagram, YouTube, Pinterest…) | Python, CLI, yt-dlp wrapper |
| **[erhanemir.github.io](https://github.com/ErhanEmir/erhanemir.github.io)** | Personal portfolio — typing animation, terminal, mouse glow, error pages | HTML, CSS, JS (vanilla) |

---

### 📊 GitHub Stats

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=ErhanEmir&show_icons=true&theme=tokyonight&hide_border=true&count_private=true" height="150"/>
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=ErhanEmir&layout=compact&theme=tokyonight&hide_border=true" height="150"/>
</p>

---

### 📫 Connect

[![GitHub](https://img.shields.io/badge/GitHub-ErhanEmir-181717?logo=github)](https://github.com/ErhanEmir)
[![Instagram](https://img.shields.io/badge/Instagram-erhanemir.32-E4405F?logo=instagram)](https://instagram.com/erhanemir.32)
[![Email](https://img.shields.io/badge/Email-erhanemir32@hotmail.com-D14836?logo=gmail)](mailto:erhanemir32@hotmail.com)

---

<details>
<summary>🤖 How the snake works</summary>

The snake follows a **Hamiltonian cycle** — a path that visits every cell exactly once before returning to start. This guarantees:
- ✅ Never hits itself
- ✅ Eventually eats every food
- ✅ Runs forever without human input

The SVG is regenerated every 6 hours via GitHub Actions (`.github/workflows/snake.yml`).
</details>