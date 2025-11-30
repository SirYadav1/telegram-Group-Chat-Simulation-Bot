import asyncio
import json
import os
from telethon import TelegramClient
from telethon.sessions import StringSession
import random

class AccountManager:
    def __init__(self):
        self.accounts_file = 'accounts.json'
        self.sessions_dir = 'sessions'
        self.accounts = []
        self.active_accounts = []
        
        # Create sessions directory if not exists
        os.makedirs(self.sessions_dir, exist_ok=True)
        self.load_accounts()
    
    def load_accounts(self):
        """Load accounts from JSON file"""
        try:
            with open(self.accounts_file, 'r', encoding='utf-8') as f:
                self.accounts = json.load(f)
            print(f"✅ Loaded {len(self.accounts)} accounts from file")
        except FileNotFoundError:
            self.accounts = []
            print("📝 No existing accounts file found. Starting fresh.")
    
    def save_accounts(self):
        """Save accounts to JSON file"""
        with open(self.accounts_file, 'w', encoding='utf-8') as f:
            json.dump(self.accounts, f, indent=4, ensure_ascii=False)
        print(f"💾 Saved {len(self.accounts)} accounts to file")
    
    async def create_new_account(self):
        """Interactive account creation"""
        print("\n" + "="*50)
        print("➕ ADD NEW ACCOUNT")
        print("="*50)
        
        # Get account details
        name = input("Account name: ").strip()
        if not name:
            print("❌ Account name is required!")
            return None
        
        # Check if name already exists
        if any(acc['name'] == name for acc in self.accounts):
            print("❌ Account with this name already exists!")
            return None
        
        api_id = input("API ID: ").strip()
        if not api_id.isdigit():
            print("❌ API ID must be a number!")
            return None
        
        api_hash = input("API Hash: ").strip()
        if not api_hash:
            print("❌ API Hash is required!")
            return None
        
        phone = input("Phone number (with country code): ").strip()
        if not phone:
            print("❌ Phone number is required!")
            return None
        
        print(f"\n📝 Creating account: {name}...")
        
        try:
            # Create session
            session = StringSession()
            client = TelegramClient(session, int(api_id), api_hash)
            
            # Start client and get authorization
            await client.start(phone=phone)
            
            # Get user info
            me = await client.get_me()
            session_string = session.save()
            
            # Save session to file
            session_filename = f"{self.sessions_dir}/{name}.session"
            with open(session_filename, 'w', encoding='utf-8') as f:
                f.write(session_string)
            
            # Create account object
            account = {
                'name': name,
                'api_id': int(api_id),
                'api_hash': api_hash,
                'phone': phone,
                'user_id': me.id,
                'username': me.username or '',
                'first_name': me.first_name or '',
                'session_file': session_filename,
                'session_string': session_string,
                'is_active': True
            }
            
            # Add to accounts list
            self.accounts.append(account)
            self.save_accounts()
            
            print(f"✅ Account '{name}' created successfully!")
            print(f"   👤 User ID: {me.id}")
            print(f"   📞 Phone: {phone}")
            print(f"   💾 Session: {session_filename}")
            
            await client.disconnect()
            return account
            
        except Exception as e:
            print(f"❌ Failed to create account: {e}")
            return None
    
    async def initialize_accounts(self):
        """Initialize all active accounts"""
        self.active_accounts = []
        
        for account in self.accounts:
            if not account.get('is_active', True):
                continue
                
            try:
                # Load session from file
                if os.path.exists(account['session_file']):
                    with open(account['session_file'], 'r', encoding='utf-8') as f:
                        session_string = f.read().strip()
                else:
                    session_string = account['session_string']
                
                # Create client
                client = TelegramClient(
                    StringSession(session_string),
                    account['api_id'],
                    account['api_hash']
                )
                
                await client.start()
                
                # Verify connection
                me = await client.get_me()
                
                client_data = {
                    'client': client,
                    'name': account['name'],
                    'user_id': me.id,
                    'phone': account['phone'],
                    'username': me.username or '',
                    'session_file': account['session_file']
                }
                
                self.active_accounts.append(client_data)
                print(f"✅ {account['name']} initialized successfully")
                
            except Exception as e:
                print(f"❌ Failed to initialize {account['name']}: {e}")
        
        print(f"🎯 Total active accounts: {len(self.active_accounts)}")
        return self.active_accounts
    
    def delete_account(self, account_name):
        """Delete an account"""
        account_to_delete = None
        
        for account in self.accounts:
            if account['name'] == account_name:
                account_to_delete = account
                break
        
        if not account_to_delete:
            print(f"❌ Account '{account_name}' not found!")
            return False
        
        # Remove session file
        try:
            if os.path.exists(account_to_delete['session_file']):
                os.remove(account_to_delete['session_file'])
                print(f"🗑️  Deleted session file: {account_to_delete['session_file']}")
        except Exception as e:
            print(f"⚠️  Could not delete session file: {e}")
        
        # Remove from accounts list
        self.accounts = [acc for acc in self.accounts if acc['name'] != account_name]
        self.save_accounts()
        
        print(f"✅ Account '{account_name}' deleted successfully!")
        return True
    
    def toggle_account_status(self, account_name, status):
        """Enable/disable an account"""
        for account in self.accounts:
            if account['name'] == account_name:
                account['is_active'] = status
                self.save_accounts()
                action = "enabled" if status else "disabled"
                print(f"✅ Account '{account_name}' {action}")
                return True
        
        print(f"❌ Account '{account_name}' not found!")
        return False
    
    def get_account_count(self):
        return len(self.accounts)
    
    def get_active_account_count(self):
        return len([acc for acc in self.accounts if acc.get('is_active', True)])
    
    def list_accounts(self):
        """Display all accounts with details"""
        if not self.accounts:
            print("📭 No accounts found!")
            return
        
        print(f"\n📋 ACCOUNTS LIST ({len(self.accounts)} total, {self.get_active_account_count()} active)")
        print("="*80)
        for i, account in enumerate(self.accounts, 1):
            status = "✅ ACTIVE" if account.get('is_active', True) else "❌ DISABLED"
            print(f"{i:2d}. {account['name']:15} | {account['phone']:15} | {account['user_id']:10} | {status}")
    
    async def disconnect_all(self):
        """Disconnect all active clients"""
        for client_data in self.active_accounts:
            try:
                await client_data['client'].disconnect()
                print(f"🔌 Disconnected {client_data['name']}")
            except Exception as e:
                print(f"⚠️  Error disconnecting {client_data['name']}: {e}")
        
        self.active_accounts = [] 