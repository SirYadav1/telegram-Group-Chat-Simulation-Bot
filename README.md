# 🤖 Telegram Group Chat Simulation Bot

A sophisticated multi-account Telegram bot that simulates natural group conversations with 6 different character personalities, powered by LLM.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## ✨ Features

- **6 Character Personalities**: Flirty Boy, Girl, Mature Guy, Curious Teen, and 2 Hustlers
- **Natural Group Dynamics**: Realistic conversations with character relationships
- **Multi-Account Management**: Easy add/remove/enable/disable accounts
- **LLM-Powered Responses**: Smart AI-generated replies with fallback system
- **Chat Logging**: JSON and CSV export of all conversations
- **Character-Based Starters**: Each personality has unique conversation openers

## 📋 Prerequisites

- Python 3.8 or higher
- Telegram account(s) - minimum 2, recommended 4-6
- Telegram API credentials (API ID & API Hash)
- VPS or local machine (for LLM server)

---

## 🚀 Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/SirYadav1/telegram-Group-Chat-Simulation-Bot.git
cd telegram-Group-Chat-Simulation-Bot
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Get Telegram API Credentials

1. Visit [https://my.telegram.org](https://my.telegram.org)
2. Login with your phone number
3. Go to "API Development Tools"
4. Create a new application
5. Copy your `API ID` and `API Hash`

**Repeat for each account you want to add!**

---

## 🖥️ LLM Server Setup

You need an LLM server to generate intelligent responses. Choose one option:

### Option A: VPS Setup (Recommended for 24/7 operation)

**1. Connect to your VPS:**
```bash
ssh root@your-vps-ip
```

**2. Install Python:**
```bash
apt update && apt upgrade -y
apt install python3 python3-pip git -y
```

**3. Create LLM Server:**
```bash
mkdir llm-server && cd llm-server
nano llm_server.py
```

**4. Add this code:**
```python
from flask import Flask, request, jsonify
from transformers import pipeline, set_seed
import torch

app = Flask(__name__)
set_seed(42)

# Load model (first run will download ~500MB)
print("Loading model...")
generator = pipeline(
    'text-generation',
    model='gpt2',
    device=0 if torch.cuda.is_available() else -1
)
print("Model loaded!")

@app.route('/v1/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        prompt = data.get('prompt', '')
        max_tokens = data.get('max_tokens', 20)
        temperature = data.get('temperature', 0.9)
        
        result = generator(
            prompt,
            max_length=len(prompt.split()) + max_tokens,
            temperature=temperature,
            num_return_sequences=1,
            do_sample=True
        )
        
        response_text = result[0]['generated_text'].replace(prompt, '').strip()
        return jsonify({'response': response_text})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

**5. Install dependencies:**
```bash
pip3 install flask transformers torch
```

**6. Run server:**
```bash
# Run in background
nohup python3 llm_server.py > llm.log 2>&1 &

# Check if running
netstat -tulpn | grep 5000

# View logs
tail -f llm.log
```

**7. Test server:**
```bash
curl -X POST http://YOUR_VPS_IP:5000/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello"}'
```

### Option B: Local Setup

Same steps as VPS but:
- Skip SSH connection
- Run on your local machine
- URL will be `http://localhost:5000/v1/chat`

---

## ⚙️ Bot Configuration

### 1. Update config.py

```python
# Edit config.py
nano config.py

# Update these lines:
LLM_API_URL = "http://YOUR_VPS_IP:5000/v1/chat"  # or localhost
LLM_API_KEY = "your-secret-key"  # Change this!
GROUP_ID = -1001234567890  # Your Telegram group ID (see below)
```

### 2. Get Your Group ID

**Method 1: Using Bot Father**
1. Add @RawDataBot to your group
2. It will show group ID
3. Remove the bot after

**Method 2: Using Script**
```python
# Create get_group_id.py
from telethon import TelegramClient

api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'
client = TelegramClient('temp_session', api_id, api_hash)

async def main():
    await client.start()
    async for dialog in client.iter_dialogs():
        if dialog.is_group:
            print(f"Group: {dialog.name}")
            print(f"ID: {dialog.id}\n")

with client:
    client.loop.run_until_complete(main())
```

Run: `python get_group_id.py`

---

## 🎮 Usage

### Starting the Bot

```bash
python main.py
```

You'll see this menu:
```
🤖 MAIN MENU
==================================================
1. Start Simulation
2. Manage Accounts
3. System Status
4. View Chat Logs
5. Exit
```

### First-Time Setup: Add Accounts

1. Select `2` (Manage Accounts)
2. Select `1` (Add New Account)
3. Enter details:
   ```
   Account name: Bot1
   API ID: 12345678
   API Hash: abcdef1234567890
   Phone number: +1234567890
   ```
4. Enter verification code from Telegram
5. ✅ Account added!

**Repeat for 2-6 accounts** (minimum 2 required)

### Running Simulation

1. Main Menu → `1` (Start Simulation)
2. Bot assigns personalities automatically:
   - **2 accounts**: Couple (Flirty Boy + Girl)
   - **3 accounts**: Couple + Curious Teen
   - **4 accounts**: Couple + Mentor-Student pair
   - **5 accounts**: Above + Hustler 1
   - **6+ accounts**: All 6 characters

3. First message is sent automatically
4. Bots respond to each other naturally
5. Press `Ctrl+C` to stop

### Example Conversation

```
🎬 Bot1 (Flirty Boy) started: 'hey beautiful whats up'
📨 Bot2 (Girl) received: 'hey beautiful whats up'
⌨️ Typing... (2.3s)
✅ Bot2 (Girl) replied: 'haha thanks'
📨 Bot1 (Flirty Boy) received: 'haha thanks'
⌨️ Typing... (3.1s)
✅ Bot1 (Flirty Boy) replied: 'wanna hang out'
...
```

---

## 🎭 Character System

| Character | Age | Personality | Example Messages |
|-----------|-----|-------------|------------------|
| **Flirty Boy** | 18-19 | Romantic, trying to impress girl | "hey beautiful", "thinking about you", "wanna meet up" |
| **Girl** | 18-19 | Sometimes interested, sometimes cold | "haha thanks", "busy rn", "maybe later", "aww sweet" |
| **Mature Guy** | 21 | Wise mentor, gives advice | "listen bro", "trust me", "from experience" |
| **Curious Teen** | 18 | Eager learner, asks questions | "how does that work", "teach me", "can you explain" |
| **Hustler 1** | 20 | Entrepreneur, business ideas | "new opportunity", "easy money", "lets start" |
| **Hustler 2** | 20 | Business partner, supportive | "sounds good", "whats the plan", "im down" |

### Character Dynamics

- **Flirty Boy ↔️ Girl**: Romantic tension, flirting
- **Mature Guy → Curious Teen**: Teaching/learning relationship
- **Hustler 1 ↔️ Hustler 2**: Business discussions, money-making

---

## 📊 Features Explained

### Account Management

```
💤 ACCOUNT MANAGEMENT
==================================================
1. Add New Account       → Add Telegram accounts
2. List All Accounts     → View all accounts
3. Delete Account        → Remove permanently
4. Enable/Disable        → Temporarily deactivate
5. Back to Main Menu
```

### System Status

Shows:
- Total accounts
- Active accounts
- Current personality assignments
- Character dynamics active in group

### Chat Logs

All conversations saved to:
- `chat_logs.json` - Structured JSON format
- `chat_logs.csv` - Excel-compatible format

View recent messages from menu option 4.

---

## 🔧 Configuration Options

Edit `config.py` to customize behavior:

```python
# Response Length
MIN_RESPONSE_WORDS = 3  # Minimum words in response
MAX_RESPONSE_WORDS = 6  # Maximum words (keep natural)

# Timing
BASE_COOLDOWN = 2        # Seconds between messages
RANDOM_DELAY_MIN = 2     # Min typing delay
RANDOM_DELAY_MAX = 4     # Max typing delay

# Probability
RESPONSE_PROBABILITY = 1.0  # 1.0 = always respond

# LLM Server
LLM_API_URL = "http://199.199.99.99:5000/v1/chat"
LLM_API_KEY = "Mygtafive"

# Telegram Group
GROUP_ID = -1002965648671
```

---

## 🛠️ Troubleshooting

### Problem: LLM server not responding

**Solution:**
```bash
# Check if server is running
netstat -tulpn | grep 5000

# Test connection
python test_llm.py

# View server logs
tail -f llm.log

# Restart server
pkill -f llm_server.py
nohup python3 llm_server.py > llm.log 2>&1 &
```

### Problem: Bot not sending messages

**Solutions:**
- ✅ Verify `GROUP_ID` is correct (must be negative)
- ✅ Check all accounts are members of the group
- ✅ Ensure accounts are marked as active
- ✅ Check Telegram rate limits (wait 1-2 minutes)

### Problem: Session errors

**Solution:**
```bash
# Delete old sessions
rm -rf sessions/*
rm accounts.json

# Re-add accounts from Main Menu
python main.py
```

### Problem: Responses are too formal/weird

**Solution:**
- LLM server needs better model (GPT-2 is basic)
- Fallback responses will be used more often
- Adjust temperature in `message_handler.py` (higher = more creative)

---

## 📁 Project Structure

```
telegram-bot-simulation/
│
├── main.py                    # 🚀 Main entry point & menu system
├── account_manager.py         # 👥 Account CRUD operations
├── bot_controller.py          # 🎮 Message handling & conversation flow
├── message_handler.py         # 🤖 LLM integration & response generation
├── personality_manager.py     # 🎭 Character personality system
├── chat_logger.py            # 📝 Conversation logging (JSON/CSV)
├── config.py                 # ⚙️ Configuration settings
├── requirements.txt          # 📦 Python dependencies
├── test_llm.py              # 🧪 LLM connection tester
│
├── accounts.json            # 💾 Account database (auto-generated)
├── sessions/                # 🔐 Telegram session files (auto-generated)
├── chat_logs.json          # 📊 Conversation logs (auto-generated)
└── chat_logs.csv           # 📈 CSV export (auto-generated)
```

### File Descriptions

| File | Purpose | Edit? |
|------|---------|-------|
| `main.py` | Menu system & application entry | ❌ No |
| `config.py` | Settings & configuration | ✅ Yes |
| `account_manager.py` | Account management logic | ❌ No |
| `bot_controller.py` | Message handling & responses | ❌ No |
| `personality_manager.py` | Character definitions | ⚠️ Advanced only |
| `message_handler.py` | LLM integration | ⚠️ Advanced only |
| `chat_logger.py` | Logging system | ❌ No |

---

## 🔒 Security & Privacy

### Important: Protect Your Data

Add to `.gitignore`:
```gitignore
# Sensitive files - NEVER commit these!
accounts.json
sessions/
*.session
chat_logs.*
*.csv
__pycache__/
*.pyc
.env
*.log

# Keep these
!requirements.txt
!README.md
```

### Best Practices

- 🔐 Never share `accounts.json` or session files
- 🔑 Change `LLM_API_KEY` from default
- 🚫 Don't commit API credentials to Git
- 🛡️ Use VPS firewall to restrict port 5000
- 📝 Regularly backup `accounts.json` (encrypted)

---

## 📈 Advanced Tips

### Improving Response Quality

1. **Use better LLM model:**
   ```python
   # In llm_server.py, replace gpt2 with:
   generator = pipeline('text-generation', model='gpt2-medium')
   # or gpt2-large (requires more RAM)
   ```

2. **Adjust temperature:**
   ```python
   # In message_handler.py, line with temperature:
   "temperature": 0.9,  # Lower = more conservative, Higher = more creative
   ```

3. **Fine-tune fallback responses:**
   Edit `message_handler.py` → `get_character_fallback()` function

### Running Multiple Groups

```python
# In config.py
GROUP_IDS = [-1001234567890, -1009876543210]

# In bot_controller.py, modify:
@client_data['client'].on(events.NewMessage(chats=GROUP_IDS))
```

### Auto-Restart on Crash

Create `run_bot.sh`:
```bash
#!/bin/bash
while true; do
    python3 main.py
    echo "Bot crashed. Restarting in 5 seconds..."
    sleep 5
done
```

Run: `chmod +x run_bot.sh && ./run_bot.sh`

---

## 🐛 Known Issues

| Issue | Workaround |
|-------|------------|
| Rate limiting after 20+ messages | Wait 60 seconds, Telegram auto-lifts |
| LLM server timeout | Increase timeout in `message_handler.py` |
| Duplicate messages | Clear `processed_messages` cache periodically |
| Session expired | Delete session file and re-add account |

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/SirYadav1/telegram-Group-Chat-Simulation-Bot.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**This bot is for educational purposes only.**

- ✅ Test in private groups only
- ❌ Do not spam public groups
- ⚠️ Automated messaging may violate Telegram ToS if misused
- 📚 Use responsibly and ethically
- 🔒 Respect privacy and data protection laws

**The authors are not responsible for misuse of this software.**

---

## 💬 Support

Need help?

- 📖 Read this README thoroughly
- 🔍 Check [Troubleshooting](#-troubleshooting) section
- 🐛 [Open an issue](https://github.com/yourusername/telegram-bot-simulation/issues)
- 💡 [View existing issues](https://github.com/yourusername/telegram-bot-simulation/issues?q=is%3Aissue)

---

## 🙏 Credits

Built with:
- [Telethon](https://github.com/LonamiWebs/Telethon) - Telegram client library
- [Transformers](https://github.com/huggingface/transformers) - LLM models
- [Flask](https://flask.palletsprojects.com/) - LLM server framework

---

## 📊 Statistics

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Accounts](https://img.shields.io/badge/Accounts-2--6-green)
![Characters](https://img.shields.io/badge/Characters-6-purple)
![Status](https://img.shields.io/badge/Status-Active-success)

---

**Made with ❤️ for realistic Telegram bot simulations**

⭐ Star this repo if you found it helpful!
