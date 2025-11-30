"""
Updated config.py - Optimized for slow LLM server
REPLACE your config.py with this
"""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
LLM_API_URL = "http://159.195.20.30:5000/v1/chat"
LLM_API_KEY = "Mygtafive"

# Group Configuration
GROUP_ID = -1002919456671  # Your group ID

# Message Response Settings
MIN_RESPONSE_WORDS = 3  # Minimum 3 words
MAX_RESPONSE_WORDS = 6  # Maximum 6 words (STRICT)
RESPONSE_PROBABILITY = 1.0

# Message Timing Configuration
BASE_COOLDOWN = 2  # Faster
RANDOM_DELAY_MIN = 2
RANDOM_DELAY_MAX = 4  # Shorter delays

# Message Rules
MIN_MESSAGE_LENGTH = 3
ALLOWED_LANGUAGES = ['en', 'ru']

# Mood System
ENABLE_MOOD_SYSTEM = True
MOOD_CHANGE_CHANCE = 0.30  # 30% chance

# Available Personality Types
PERSONALITY_TYPES = [
    "aggressive", "cool", "humorous", "casual", "friendly",
    "serious", "curious", "sarcastic", "enthusiastic"
]