import requests
import random
import asyncio
import re
from datetime import datetime
from config import LLM_API_URL, LLM_API_KEY

class MessageHandler:
    def __init__(self, personality_manager):
        self.personality_manager = personality_manager
        self.conversation_history = []
        self.account_response_history = {}
        
    async def generate_response(self, account_name, message_context, original_message=""):
        """Generate character-appropriate response"""
        
        character_key = self.personality_manager.assigned_personalities.get(account_name, "curious_teen")
        character = self.personality_manager.get_character_info(character_key)
        
        # Detect who sent the message (for relationship dynamics)
        sender_character = self.detect_sender_character(original_message)
        
        # Try LLM
        for attempt in range(2):
            response = await self.call_character_llm(
                account_name,
                character,
                sender_character,
                original_message,
                attempt
            )
            
            if response and self.is_valid_character_response(response, account_name, original_message):
                self.track_response(account_name, response)
                print(f"✅ {account_name} ({character['name']}): {response}")
                return response
        
        # Character-based fallback
        fallback = self.get_character_fallback(character_key, original_message, sender_character)
        self.track_response(account_name, fallback)
        return fallback
    
    def detect_sender_character(self, message):
        """Detect which character likely sent the message"""
        msg_lower = message.lower()
        
        # Girl indicators
        if any(w in msg_lower for w in ['aww', 'cute', 'sweet', 'maybe later', 'busy']):
            return "girl"
        
        # Flirty boy indicators
        if any(w in msg_lower for w in ['beautiful', 'pretty', 'wanna hang', 'thinking about you']):
            return "flirty_boy"
        
        # Mature guy indicators
        if any(w in msg_lower for w in ['listen', 'trust me', 'from experience', 'heres the trick']):
            return "mature_guy"
        
        # Curious teen indicators (questions)
        if '?' in message or any(w in msg_lower for w in ['how', 'why', 'what', 'can you explain']):
            return "curious_teen"
        
        # Hustler indicators
        if any(w in msg_lower for w in ['money', 'business', 'opportunity', 'earning', 'investment']):
            return "hustler"
        
        return "unknown"
    
    async def call_character_llm(self, account_name, character, sender_character, original_message, attempt):
        """Call LLM with character-specific prompt"""
        
        recent = self.account_response_history.get(account_name, [])
        
        # Character-specific response style
        character_styles = {
            "flirty_boy": {
                "examples": "hey beautiful | you look nice | wanna hang out | thinking of you",
                "tone": "flirty and trying to impress"
            },
            "girl": {
                "examples": "haha thanks | maybe later | busy rn | aww thats sweet | not interested",
                "tone": "sometimes interested, sometimes cold"
            },
            "mature_guy": {
                "examples": "listen bro | heres the thing | trust me | from my experience",
                "tone": "wise and helpful"
            },
            "curious_teen": {
                "examples": "how does that work | can you teach me | really bro | i dont get it",
                "tone": "curious and asking questions"
            },
            "hustler_1": {
                "examples": "new opportunity bro | easy money | lets start this | dropshipping idea",
                "tone": "entrepreneur mindset"
            },
            "hustler_2": {
                "examples": "sounds good | whats the plan | im down | how much investment",
                "tone": "supportive hustler"
            }
        }
        
        char_key = character.get('name', 'Curious Teen').lower().replace(' ', '_')
        style = character_styles.get(char_key, character_styles["curious_teen"])
        
        # Build relationship-aware prompt
        relationship_context = ""
        if char_key == "girl" and sender_character == "flirty_boy":
            relationship_context = "A boy is flirting with you. Sometimes show interest, sometimes be cold."
        elif char_key == "flirty_boy" and sender_character == "girl":
            relationship_context = "The girl you like replied. Keep flirting but be cool."
        elif char_key == "curious_teen" and sender_character == "mature_guy":
            relationship_context = "The mature guy is sharing wisdom. Ask follow-up questions."
        elif char_key == "mature_guy" and sender_character == "curious_teen":
            relationship_context = "The teen asked something. Give helpful advice."
        
        prompt = f"""Friend group chat. You're a {character['age']} year old.

{relationship_context}

They said: "{original_message}"

Your vibe: {style['tone']}

How you talk:
{style['examples']}

Reply naturally (3-5 words):"""

        try:
            response = requests.post(
                LLM_API_URL,
                headers={"Authorization": LLM_API_KEY},
                json={
                    "prompt": prompt,
                    "max_tokens": 12,
                    "temperature": 0.9,
                    "top_p": 0.85,
                    "frequency_penalty": 2.0,
                    "presence_penalty": 1.5
                },
                timeout=8
            )
            
            if response.status_code == 200:
                result = response.json()
                reply = result.get('response', '').strip()
                return self.clean_response(reply)
        
        except:
            pass
        
        return None
    
    def clean_response(self, text):
        """Clean response"""
        if not text:
            return ""
        
        # Remove emojis
        text = re.sub(r'[^\x00-\x7F]+', '', text)
        
        # Remove hashtags
        text = re.sub(r'#\w+', '', text)
        
        # Clean
        text = text.strip('"\'`')
        text = ' '.join(text.split())
        
        # Word limit
        words = text.split()
        if len(words) > 5:
            text = ' '.join(words[:5])
        
        # Remove incomplete endings
        text = text.rstrip(',')
        bad_endings = [' the', ' a', ' to', ' of', ' in', ' and', ' or']
        for ending in bad_endings:
            if text.lower().endswith(ending):
                words = text.split()
                text = ' '.join(words[:-1])
        
        return text.strip()
    
    def is_valid_character_response(self, response, bot_name, original_message):
        """Validate response"""
        if not response or len(response.strip()) < 2:
            return False
        
        # Word count
        words = response.split()
        if len(words) < 2 or len(words) > 5:
            return False
        
        # No formal words
        formal = ['indeed', 'perhaps', 'absolutely', 'marvelous', 'wonderful']
        if any(word in response.lower() for word in formal):
            return False
        
        # No rule leaks
        if 'rule' in response.lower() or 'example' in response.lower():
            return False
        
        # No copying
        original_words = set(original_message.lower().split())
        response_words = set(response.lower().split())
        if len(original_words.intersection(response_words)) >= 2:
            return False
        
        # No repetition
        recent = self.account_response_history.get(bot_name, [])
        if response.lower() in recent[-2:]:
            return False
        
        return True
    
    def get_character_fallback(self, character_key, original_message, sender_character):
        """Character-specific fallbacks"""
        
        msg_lower = original_message.lower()
        
        # FLIRTY BOY fallbacks
        if character_key == "flirty_boy":
            if sender_character == "girl":
                return random.choice(["you look nice", "wanna meet up", "thinking about you", "hey beautiful"])
            else:
                return random.choice(["yeah bro", "sounds cool", "im good"])
        
        # GIRL fallbacks
        elif character_key == "girl":
            if sender_character == "flirty_boy":
                # 60% ignore, 40% respond positively
                if random.random() < 0.6:
                    return random.choice(["busy rn", "maybe later", "not now", "lol okay"])
                else:
                    return random.choice(["haha thanks", "aww sweet", "sure why not"])
            else:
                return random.choice(["yeah", "okay cool", "sounds good"])
        
        # MATURE GUY fallbacks
        elif character_key == "mature_guy":
            if sender_character == "curious_teen" or '?' in original_message:
                return random.choice(["listen bro", "heres the thing", "trust me", "from experience"])
            else:
                return random.choice(["makes sense", "true that", "i agree"])
        
        # CURIOUS TEEN fallbacks
        elif character_key == "curious_teen":
            if sender_character == "mature_guy":
                return random.choice(["how does that work", "can you explain", "teach me bro", "really"])
            else:
                return random.choice(["interesting", "nice", "cool bro"])
        
        # HUSTLER 1 fallbacks
        elif character_key == "hustler_1":
            if any(w in msg_lower for w in ['money', 'business', 'idea']):
                return random.choice(["new opportunity bro", "easy money method", "lets do this", "im thinking dropshipping"])
            else:
                return random.choice(["yeah man", "sounds good", "im down"])
        
        # HUSTLER 2 fallbacks
        elif character_key == "hustler_2":
            if any(w in msg_lower for w in ['opportunity', 'business', 'start']):
                return random.choice(["whats the plan", "how much investment", "im interested", "lets try it"])
            else:
                return random.choice(["cool bro", "makes sense", "true"])
        
        # Default
        return random.choice(["yeah", "okay", "cool"])
    
    def track_response(self, bot_name, response):
        """Track responses"""
        if bot_name not in self.account_response_history:
            self.account_response_history[bot_name] = []
        
        self.account_response_history[bot_name].append(response.lower())
        
        if len(self.account_response_history[bot_name]) > 5:
            self.account_response_history[bot_name].pop(0)
    
    async def get_delay_time(self):
        """Typing delay"""
        return random.uniform(2, 4)
    
    def update_conversation_history(self, message, sender, message_id=None):
        """Track conversation"""
        self.conversation_history.append({
            'sender': sender,
            'message': message,
            'timestamp': datetime.now()
        })
        
        if len(self.conversation_history) > 5:
            self.conversation_history.pop(0)
    
    def get_conversation_context(self, limit=2):
        """Get context"""
        return ""
    
    def should_respond(self, message_id):
        return True
    
    def mark_responded(self, message_id):
        pass
