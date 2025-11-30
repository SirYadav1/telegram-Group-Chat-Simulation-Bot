"""
6 Character Personality System - Natural Group Dynamics
REPLACE your personality_manager.py with this
"""
import random

class PersonalityManager:
    def __init__(self):
        self.assigned_personalities = {}
        
        # 6 FIXED CHARACTERS with roles and dynamics
        self.six_characters = {
            # COUPLE (Flirty Dynamic)
            "flirty_boy": {
                "name": "Flirty Boy",
                "age": "18-19",
                "role": "ladki ke piche pada rahta hai",
                "style": "flirty, romantic, trying to impress",
                "examples": "hey beautiful | you look nice today | wanna hang out | thinking about you"
            },
            "girl": {
                "name": "Girl", 
                "age": "18-19",
                "role": "kabhi bhaw deti hai, kabhi ignore karti hai",
                "style": "sometimes flirty back, sometimes cold, mood-based",
                "examples": "haha thanks | maybe later | busy right now | aww thats sweet"
            },
            
            # MENTOR-STUDENT (Gyan Dynamic)
            "mature_guy": {
                "name": "Mature Guy",
                "age": "21",
                "role": "gyani, experienced, gives advice",
                "style": "wise, helpful, shares knowledge and tips",
                "examples": "listen bro | heres the trick | trust me | from experience"
            },
            "curious_teen": {
                "name": "Curious Teen",
                "age": "18",
                "role": "questions puchta hai, seekhna chahta hai",
                "style": "asks questions, eager to learn, innocent",
                "examples": "how does that work | can you explain | really | teach me bro"
            },
            
            # HUSTLER FRIENDS (Earning/Business Dynamic)
            "hustler_1": {
                "name": "Hustler 1",
                "age": "20",
                "role": "naye business ideas, earning methods discuss karta hai",
                "style": "entrepreneur mindset, talks about money, opportunities",
                "examples": "new opportunity bro | easy money method | lets start something | affiliate marketing"
            },
            "hustler_2": {
                "name": "Hustler 2",
                "age": "20", 
                "role": "partner in crime, discusses side hustles",
                "style": "supportive, also into making money, realistic",
                "examples": "sounds good | whats the plan | im down | investment needed"
            }
        }
    
    def assign_personalities(self, account_names):
        """Assign personalities based on account count"""
        self.assigned_personalities = {}
        
        if not account_names:
            return {}
        
        num_accounts = len(account_names)
        
        # Priority order based on count
        if num_accounts == 2:
            # COUPLE: Flirty Boy + Girl
            priority = ["flirty_boy", "girl"]
        
        elif num_accounts == 3:
            # COUPLE + CURIOUS TEEN
            priority = ["flirty_boy", "girl", "curious_teen"]
        
        elif num_accounts == 4:
            # COUPLE + MENTOR-STUDENT
            priority = ["flirty_boy", "girl", "mature_guy", "curious_teen"]
        
        elif num_accounts == 5:
            # COUPLE + MENTOR-STUDENT + HUSTLER 1
            priority = ["flirty_boy", "girl", "mature_guy", "curious_teen", "hustler_1"]
        
        else:  # 6+
            # ALL 6 CHARACTERS
            priority = ["flirty_boy", "girl", "mature_guy", "curious_teen", "hustler_1", "hustler_2"]
        
        # Assign personalities
        for i, account_name in enumerate(account_names):
            if i < len(priority):
                character_key = priority[i]
                self.assigned_personalities[account_name] = character_key
            else:
                # Extra accounts get random
                character_key = random.choice(list(self.six_characters.keys()))
                self.assigned_personalities[account_name] = character_key
        
        return self.assigned_personalities
    
    def get_character_info(self, character_key):
        """Get full character details"""
        return self.six_characters.get(character_key, self.six_characters["curious_teen"])
    
    def get_personality_prompt(self, account_name, original_message, mood="normal"):
        """Generate character-based prompt"""
        
        character_key = self.assigned_personalities.get(account_name, "curious_teen")
        character = self.get_character_info(character_key)
        
        # Build natural prompt based on character
        prompt = f"""You are {character['name']} (age {character['age']}) in a friend group chat.

Your role: {character['role']}
Your style: {character['style']}

Someone said: "{original_message}"

How you talk:
{character['examples']}

Reply naturally (3-5 words max). Sound like a real {character['age']} year old:"""

        return prompt
    
    def get_assigned_personalities(self):
        return self.assigned_personalities
    
    def show_personality_assignment(self):
        """Display character assignments"""
        if not self.assigned_personalities:
            print("🎭 No characters assigned yet")
            return
        
        print("\n🎭 CHARACTER ASSIGNMENTS")
        print("="*60)
        for account, character_key in self.assigned_personalities.items():
            character = self.get_character_info(character_key)
            print(f"👤 {account:15} → {character['name']:15} (Age: {character['age']}, Role: {character['role'][:30]}...)")
        
        print("\n💬 GROUP DYNAMICS:")
        chars = list(self.assigned_personalities.values())
        
        if "flirty_boy" in chars and "girl" in chars:
            print("   💕 Couple Dynamic: Flirty Boy ↔️ Girl (romantic tension)")
        
        if "mature_guy" in chars and "curious_teen" in chars:
            print("   🎓 Mentor-Student: Mature Guy → Curious Teen (teaching/learning)")
        
        if "hustler_1" in chars or "hustler_2" in chars:
            print("   💰 Hustler Friends: Discuss business, earning, opportunities")