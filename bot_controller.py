"""
Character-Based Bot Controller with Natural Starters
REPLACE your bot_controller.py with this
"""
import asyncio
import random
from telethon import events
from config import GROUP_ID

class BotController:
    def __init__(self, account_manager, personality_manager, message_handler, chat_logger):
        self.account_manager = account_manager
        self.personality_manager = personality_manager
        self.message_handler = message_handler
        self.chat_logger = chat_logger
        self.is_running = False
        self.processed_messages = {}
        
        # Character-specific conversation starters
        self.character_starters = {
            "flirty_boy": [
                "hey beautiful whats up",
                "thinking about you",
                "you free today",
                "wanna hang out"
            ],
            "girl": [
                "hey guys",
                "whats everyone doing",
                "bored",
                "anyone online"
            ],
            "mature_guy": [
                "listen guys important thing",
                "got some advice",
                "heres a good tip",
                "trust me on this"
            ],
            "curious_teen": [
                "can someone explain this",
                "how does that work",
                "guys i have question",
                "teach me something new"
            ],
            "hustler_1": [
                "guys new opportunity",
                "found easy money method",
                "lets start something",
                "business idea guys"
            ],
            "hustler_2": [
                "whats the plan today",
                "any new ideas",
                "im down for anything",
                "lets make some money"
            ]
        }
    
    async def start_simulation(self):
        """Start character-based simulation"""
        self.is_running = True
        self.processed_messages = {}
        
        print("🚀 Starting character-based simulation...")
        
        # Initialize accounts
        clients = await self.account_manager.initialize_accounts()
        
        if not clients:
            print("❌ No active clients!")
            return
        
        # Assign characters
        active_names = [acc['name'] for acc in self.account_manager.accounts if acc.get('is_active', True)]
        self.personality_manager.assign_personalities(active_names)
        
        # Show character assignments
        self.personality_manager.show_personality_assignment()
        
        # Setup handlers
        for client_data in clients:
            self.setup_handlers(client_data)
        
        # Start conversation
        await asyncio.sleep(3)
        await self.initiate_character_conversation()
        
        print("✅ Character simulation started!")
        print("💬 Natural group dynamics active...")
    
    def setup_handlers(self, client_data):
        """Setup message handlers"""
        
        @client_data['client'].on(events.NewMessage(chats=GROUP_ID))
        async def message_handler(event):
            if not self.is_running:
                return
            
            if event.sender_id == client_data['user_id']:
                return
            
            message_text = event.message.text
            message_id = event.message.id
            
            if not message_text or len(message_text.strip()) < 2:
                return
            
            # Duplicate prevention
            response_key = f"{client_data['name']}_{message_id}"
            if response_key in self.processed_messages:
                return
            
            self.processed_messages[response_key] = True
            
            # Clean old entries
            if len(self.processed_messages) > 50:
                keys = list(self.processed_messages.keys())
                for old_key in keys[:20]:
                    del self.processed_messages[old_key]
            
            # Get character info
            character_key = self.personality_manager.assigned_personalities.get(client_data['name'], "curious_teen")
            character = self.personality_manager.get_character_info(character_key)
            
            print(f"\n📨 {client_data['name']} ({character['name']}) received: '{message_text}'")
            
            # Typing delay
            delay = await self.message_handler.get_delay_time()
            print(f"⌨️ Typing... ({delay:.1f}s)")
            await asyncio.sleep(delay)
            
            # Generate response
            response = await self.message_handler.generate_response(
                client_data['name'],
                "",
                original_message=message_text
            )
            
            if response and len(response.strip()) > 2:
                try:
                    await client_data['client'].send_message(GROUP_ID, response)
                    print(f"✅ {client_data['name']} ({character['name']}) replied: '{response}'")
                    
                    # Update history
                    self.message_handler.update_conversation_history(
                        message_text,
                        f"User_{event.sender_id}",
                        message_id
                    )
                    self.message_handler.update_conversation_history(
                        response,
                        client_data['name'],
                        None
                    )
                    
                    # Log
                    self.chat_logger.log_message(
                        client_data['name'],
                        response,
                        character['name']
                    )
                    
                except Exception as e:
                    print(f"❌ Error: {e}")
            else:
                print(f"⚠️ Empty response")
    
    async def initiate_character_conversation(self):
        """Start conversation with character-appropriate message"""
        if not self.account_manager.active_accounts:
            return
        
        # Choose starter based on priority
        assignments = self.personality_manager.assigned_personalities
        
        # Priority: Flirty Boy > Curious Teen > Hustler 1 > Others
        priority_order = ["flirty_boy", "curious_teen", "hustler_1", "mature_guy", "girl", "hustler_2"]
        
        starter_account = None
        starter_character = None
        
        for char_key in priority_order:
            for account_name, assigned_char in assignments.items():
                if assigned_char == char_key:
                    # Find corresponding account
                    for acc in self.account_manager.active_accounts:
                        if acc['name'] == account_name:
                            starter_account = acc
                            starter_character = char_key
                            break
                    break
            if starter_account:
                break
        
        if not starter_account:
            starter_account = random.choice(self.account_manager.active_accounts)
            starter_character = assignments.get(starter_account['name'], "curious_teen")
        
        # Get character-appropriate starter
        starters = self.character_starters.get(starter_character, ["hey everyone"])
        starter_message = random.choice(starters)
        
        try:
            await starter_account['client'].send_message(GROUP_ID, starter_message)
            
            character = self.personality_manager.get_character_info(starter_character)
            print(f"\n🎬 {starter_account['name']} ({character['name']}) started: '{starter_message}'")
            
            # Track
            self.message_handler.update_conversation_history(
                starter_message,
                starter_account['name'],
                None
            )
            
            # Log
            self.chat_logger.log_message(
                starter_account['name'],
                starter_message,
                character['name']
            )
            
        except Exception as e:
            print(f"❌ Error starting: {e}")
    
    async def stop_simulation(self):
        """Stop simulation"""
        self.is_running = False
        print("🛑 Stopping...")
        await self.account_manager.disconnect_all()
        print("✅ Disconnected")