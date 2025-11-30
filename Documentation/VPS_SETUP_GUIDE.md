# 🖥️ VPS Setup Guide - Complete Tutorial

This guide will walk you through setting up the LLM server on a VPS from scratch.

## 📋 What You Need

- VPS with minimum:
  - **RAM**: 2GB (4GB recommended)
  - **Storage**: 10GB
  - **OS**: Ubuntu 20.04 or 22.04
- SSH access credentials
- Basic terminal knowledge

## 🚀 Part 1: LLM Server Setup

### Step 1: Connect to VPS

```bash
# Replace with your VPS IP and credentials
ssh root@YOUR_VPS_IP
# Enter password when prompted
```

### Step 2: Update System

```bash
# Update package lists
apt update

# Upgrade existing packages
apt upgrade -y

# Install essential tools
apt install -y python3 python3-pip git nano curl wget
```

### Step 3: Create Project Directory

```bash
# Create directory for LLM server
mkdir -p /root/llm-server
cd /root/llm-server
```

### Step 4: Create LLM Server File

```bash
nano llm_server.py
```

**Copy and paste this code:**

```python
"""
Simple LLM Server for Telegram Bot
Port: 5000
Endpoint: /v1/chat
"""

from flask import Flask, request, jsonify
from transformers import pipeline, set_seed
import torch
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
set_seed(42)

# Global variable for model
generator = None

def load_model():
    """Load the language model"""
    global generator
    try:
        logger.info("🔄 Loading GPT-2 model (this may take a few minutes)...")
        
        # Check if CUDA is available
        device = 0 if torch.cuda.is_available() else -1
        device_name = "GPU" if device == 0 else "CPU"
        
        logger.info(f"📍 Using device: {device_name}")
        
        generator = pipeline(
            'text-generation',
            model='gpt2',  # ~500MB download on first run
            device=device
        )
        
        logger.info("✅ Model loaded successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    if generator is None:
        return jsonify({'status': 'loading'}), 503
    return jsonify({'status': 'healthy'}), 200

@app.route('/v1/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        # Parse request
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        prompt = data.get('prompt', '')
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400
        
        max_tokens = data.get('max_tokens', 20)
        temperature = data.get('temperature', 0.9)
        
        logger.info(f"📨 Received prompt: {prompt[:50]}...")
        
        # Generate response
        result = generator(
            prompt,
            max_length=len(prompt.split()) + max_tokens,
            temperature=temperature,
            num_return_sequences=1,
            do_sample=True,
            pad_token_id=generator.tokenizer.eos_token_id
        )
        
        # Extract generated text (remove prompt)
        full_text = result[0]['generated_text']
        response_text = full_text.replace(prompt, '').strip()
        
        logger.info(f"✅ Generated response: {response_text[:50]}...")
        
        return jsonify({'response': response_text})
        
    except Exception as e:
        logger.error(f"❌ Error generating response: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info("🚀 Starting LLM Server...")
    
    # Load model on startup
    if not load_model():
        logger.error("Failed to load model. Exiting...")
        exit(1)
    
    logger.info("🌐 Server ready on port 5000")
    logger.info("📡 Endpoint: http://0.0.0.0:5000/v1/chat")
    
    # Run server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )
```

**Save and exit:**
- Press `Ctrl + X`
- Press `Y`
- Press `Enter`

### Step 5: Install Python Dependencies

```bash
# Install required packages
pip3 install flask transformers torch

# This will download ~2GB of dependencies
# Wait patiently...
```

### Step 6: Test Server (First Run)

```bash
# Run server manually first time
python3 llm_server.py

# You should see:
# 🔄 Loading GPT-2 model...
# 📍 Using device: CPU
# ✅ Model loaded successfully!
# 🌐 Server ready on port 5000
```

**First run will download the model (~500MB)**

Keep terminal open and test from another terminal:

```bash
# From your local machine or another SSH session
curl -X POST http://YOUR_VPS_IP:5000/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, how are you?"}'

# Expected output:
# {"response":"I am doing well, thank you!"}
```

If it works, press `Ctrl + C` to stop the server.

### Step 7: Run Server in Background

```bash
# Run server in background (survives terminal close)
nohup python3 llm_server.py > llm_server.log 2>&1 &

# Check if running
ps aux | grep llm_server.py

# View logs
tail -f llm_server.log

# To stop viewing logs: Ctrl + C
```

### Step 8: Configure Firewall (Optional but Recommended)

```bash
# Install UFW firewall
apt install -y ufw

# Allow SSH (IMPORTANT - don't lock yourself out!)
ufw allow 22/tcp

# Allow LLM server port
ufw allow 5000/tcp

# Enable firewall
ufw --force enable

# Check status
ufw status
```

### Step 9: Auto-Start on Reboot (Optional)

Create systemd service:

```bash
nano /etc/systemd/system/llm-server.service
```

Add this content:

```ini
[Unit]
Description=LLM Server for Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/llm-server
ExecStart=/usr/bin/python3 /root/llm-server/llm_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
# Reload systemd
systemctl daemon-reload

# Enable auto-start
systemctl enable llm-server

# Start service
systemctl start llm-server

# Check status
systemctl status llm-server

# View logs
journalctl -u llm-server -f
```

**Useful commands:**
```bash
systemctl stop llm-server     # Stop server
systemctl restart llm-server  # Restart server
systemctl status llm-server   # Check status
```

---

## 🤖 Part 2: Bot Setup (Local Machine)

### Step 1: Download Project

```bash
# On your local machine
git clone https://github.com/SirYadav1/telegram-Group-Chat-Simulation-Bot
cd telegram-bot-simulation
```

### Step 2: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### Step 3: Configure Bot

Edit `config.py`:

```python
# Update these lines
LLM_API_URL = "http://YOUR_VPS_IP:5000/v1/chat"
LLM_API_KEY = "your-secret-key-change-this"
GROUP_ID = -1001234567890  # Your group ID
```

### Step 4: Test LLM Connection

```bash
# Test if bot can reach LLM server
python test_llm.py

# Expected output:
# 🔍 Testing LLM Server Connection...
# ✅ LLM Server is WORKING!
# Response: (some generated text)
```

If this fails, check:
- VPS IP is correct
- Port 5000 is open in firewall
- LLM server is running: `systemctl status llm-server`

### Step 5: Get Group ID

Add @RawDataBot to your Telegram group, it will show the group ID. Then remove it.

Or use this script:

```python
# Create get_group_id.py
from telethon import TelegramClient

api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'

client = TelegramClient('temp', api_id, api_hash)

async def main():
    await client.start()
    print("\n📋 Your Groups:\n")
    async for dialog in client.iter_dialogs():
        if dialog.is_group:
            print(f"Name: {dialog.name}")
            print(f"ID: {dialog.id}\n")

with client:
    client.loop.run_until_complete(main())
```

Run: `python get_group_id.py`

### Step 6: Run Bot

```bash
python main.py
```

Follow on-screen instructions to:
1. Add accounts (minimum 2)
2. Start simulation

---

## 🔧 Troubleshooting

### Problem: "Connection refused" when testing LLM

**Solution:**
```bash
# On VPS, check if server is running
systemctl status llm-server

# If not running, start it
systemctl start llm-server

# Check firewall
ufw status
ufw allow 5000/tcp
```

### Problem: Model loading takes forever

**Solution:**
- First run downloads ~500MB model
- Check VPS internet speed
- Wait 5-10 minutes
- View progress: `tail -f llm_server.log`

### Problem: Server crashes with "Out of memory"

**Solution:**
```bash
# Your VPS has low RAM, use smaller model
# Edit llm_server.py, change line:
model='distilgpt2'  # Much smaller, faster
```

### Problem: Can't connect to VPS

**Solution:**
```bash
# Check SSH is running
systemctl status ssh

# Check firewall allows SSH
ufw allow 22/tcp
```

### Problem: Server stops after closing terminal

**Solution:**
```bash
# Don't use python3 llm_server.py directly
# Use one of these methods:

# Method 1: nohup
nohup python3 llm_server.py > llm_server.log 2>&1 &

# Method 2: systemd (recommended)
systemctl start llm-server
```

---

## 📊 Monitoring

### Check Server Status

```bash
# Server status
systemctl status llm-server

# Resource usage
htop

# Network connections
netstat -tulpn | grep 5000

# View logs
tail -f /root/llm-server/llm_server.log
# or
journalctl -u llm-server -f
```

### Check Bot Status

```bash
# On local machine
python main.py
# Select option 3: System Status
```

---

## 🚀 Performance Tips

### Use Better Model (if VPS has 4GB+ RAM)

```python
# In llm_server.py, change:
model='gpt2-medium'  # Better quality, needs 2GB+ RAM
# or
model='gpt2-large'   # Best quality, needs 4GB+ RAM
```

### Enable GPU Acceleration (if VPS has GPU)

```bash
# Install CUDA-enabled PyTorch
pip3 install torch --extra-index-url https://download.pytorch.org/whl/cu118

# Server will automatically use GPU
```

### Optimize Response Time

```python
# In llm_server.py, add caching:
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_generate(prompt):
    # ... generation code
```

---

## 🔒 Security Checklist

- ✅ Changed default `LLM_API_KEY` in config.py
- ✅ Firewall configured (UFW)
- ✅ Only necessary ports open (22, 5000)
- ✅ Strong SSH password or key-based auth
- ✅ Regular backups of `accounts.json`
- ✅ `.gitignore` configured properly

---

## 📈 Scaling Up

### Run Multiple LLM Servers

```bash
# Server 1: Port 5000
python3 llm_server.py

# Server 2: Port 5001
# Edit llm_server.py port, then:
python3 llm_server_2.py

# In bot config.py, use load balancing
```

### Run Bot on VPS Too

```bash
# On VPS
cd /root/telegram-bot
git clone https://github.com/SirYadav1/telegram-Group-Chat-Simulation-Bot
pip3 install -r requirements.txt
nohup python3 main.py &
```

---

## 💡 Cost Optimization

### Free/Cheap VPS Options

1. **Oracle Cloud** - Free tier: 1GB RAM, always free
2. **Google Cloud** - $300 credit for 90 days
3. **AWS** - Free tier: 1 year
4. **Hetzner** - €3.79/month for 2GB RAM
5. **DigitalOcean** - $4/month for 1GB RAM

### Reduce Costs

- Use `distilgpt2` model (smaller, faster)
- Stop server when not needed
- Use local LLM server (free)

---

## ✅ Final Checklist

Before going live:

- [ ] LLM server running on VPS
- [ ] Server responds to curl test
- [ ] `test_llm.py` passes
- [ ] Bot config.py updated
- [ ] Minimum 2 accounts added
- [ ] Tested in private group first
- [ ] Firewall configured
- [ ] Auto-restart enabled
- [ ] Logs monitoring set up

---

**🎉 You're all set! Happy botting!**

For issues, check main README troubleshooting section.
