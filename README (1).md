# 🧠 HoMM3 AI Opponent (AlphaGo-Style)

An AI-powered external brain for **Heroes of Might and Magic III**, using the open-source **VCMI engine**. This app watches game state, decides the best move using a Python agent, and outputs it to control your AI opponent like a boss.

---

## 🎮 How It Works
1. VCMI saves the current game state to `vcmi_game_state.json`
2. This AI app:
   - Reads that state
   - Feeds it into an agent
   - Outputs a move to `vcmi_ai_action.txt`
3. VCMI then executes that move (with a little modding magic)

---

## 🚀 Setup

### ✅ Requirements:
- Python 3.11+
- PyInstaller (only if building `.exe`)
- VCMI (with modded hooks to dump/read files)

### 📦 Install Python Dependencies:
```bash
pip install -r requirements.txt
```

---

## 🛠️ Build the Executable
To package this as a `.exe`:

```bash
pip install pyinstaller
pyinstaller --onefile homm3_ai_desktop.py
```

Your output will be in the `dist/` folder as `homm3_ai_desktop.exe`.

---

## 🔁 GitHub CI/CD Support

Already included! Push a release tag like `v1.0`, and GitHub Actions will:
- Build the `.exe`
- Upload it as a downloadable artifact

---

## 🧪 Example Game State (for Dev Testing)

```json
{
  "turn": 6,
  "ai_player": "Blue",
  "heroes": [{"name": "Solmyr", "pos": [4,7], "army": [5,3,1]}],
  "towns": [{"name": "Towerburg", "owner": "Blue"}]
}
```

---

## 📚 License
This project is released under the MIT License. Use it, mod it, profit (ethically).

---

## ✨ Author
Built with wizard-grade precision by **Joe Short**, supported by Maverick, your AI co-pilot. 🧙‍♂️