"""
Complete main.py - Copy-paste this ENTIRE file
"""
import asyncio
import sys
from account_manager import AccountManager
from personality_manager import PersonalityManager
from message_handler import MessageHandler
from bot_controller import BotController
from chat_logger import ChatLogger

class TelegramSimulation:
    def __init__(self):
        self.account_manager = AccountManager()
        self.personality_manager = PersonalityManager()
        self.message_handler = MessageHandler(self.personality_manager)
        self.chat_logger = ChatLogger()
        self.controller = BotController(
            self.account_manager,
            self.personality_manager,
            self.message_handler,
            self.chat_logger
        )
    
    async def add_new_account(self):
        """Add new account interactively"""
        await self.account_manager.create_new_account()
    
    def delete_account_interactive(self):
        """Delete account interactively"""
        if not self.account_manager.accounts:
            print("❌ No accounts to delete!")
            return
        
        self.account_manager.list_accounts()
        account_name = input("\nEnter account name to delete: ").strip()
        
        if account_name:
            confirm = input(f"Are you sure you want to delete '{account_name}'? (y/N): ").strip().lower()
            if confirm == 'y':
                self.account_manager.delete_account(account_name)
    
    def toggle_account_interactive(self):
        """Enable/disable account interactively"""
        if not self.account_manager.accounts:
            print("❌ No accounts found!")
            return
        
        self.account_manager.list_accounts()
        account_name = input("\nEnter account name: ").strip()
        
        if account_name:
            current_status = any(acc['name'] == account_name and acc.get('is_active', True) for acc in self.account_manager.accounts)
            new_status = not current_status
            action = "enable" if new_status else "disable"
            
            confirm = input(f"Are you sure you want to {action} '{account_name}'? (y/N): ").strip().lower()
            if confirm == 'y':
                self.account_manager.toggle_account_status(account_name, new_status)
    
    async def manage_accounts_menu(self):
        """Account management menu"""
        while True:
            print("\n" + "="*50)
            print("👤 ACCOUNT MANAGEMENT")
            print("="*50)
            print("1. Add New Account")
            print("2. List All Accounts")
            print("3. Delete Account")
            print("4. Enable/Disable Account")
            print("5. Back to Main Menu")
            
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == '1':
                await self.add_new_account()
            elif choice == '2':
                self.account_manager.list_accounts()
            elif choice == '3':
                self.delete_account_interactive()
            elif choice == '4':
                self.toggle_account_interactive()
            elif choice == '5':
                break
            else:
                print("❌ Invalid option!")
    
    async def start_simulation(self):
        """Start the group simulation"""
        active_accounts = [acc for acc in self.account_manager.accounts if acc.get('is_active', True)]
        
        if len(active_accounts) < 2:
            print("❌ Need at least 2 active accounts to start simulation!")
            return
        
        # Assign personalities based on active accounts
        active_account_names = [acc['name'] for acc in active_accounts]
        self.personality_manager.assign_personalities(active_account_names)
        
        # Show assignment
        self.personality_manager.show_personality_assignment()
        
        print(f"\n🚀 Starting simulation with {len(active_accounts)} accounts...")
        await self.controller.start_simulation()
        
        # Keep simulation running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            await self.controller.stop_simulation()
    
    def show_status(self):
        """Show current system status"""
        total_accounts = self.account_manager.get_account_count()
        active_accounts = self.account_manager.get_active_account_count()
        
        print("\n📊 SYSTEM STATUS")
        print("="*30)
        print(f"📦 Total Accounts: {total_accounts}")
        print(f"✅ Active Accounts: {active_accounts}")
        print(f"🎭 Personalities Ready: {len(self.personality_manager.get_assigned_personalities())}")
        
        if self.personality_manager.get_assigned_personalities():
            print("\n🎭 Current Personality Assignment:")
            for account, personality in self.personality_manager.get_assigned_personalities().items():
                print(f"   👤 {account} → {personality}")
    
    async def main(self):
        """Main application loop"""
        print("🚀 TELEGRAM GROUP SIMULATION")
        print("   Advanced Account Management System")
        print("="*55)
        
        while True:
            print("\n" + "="*50)
            print("🤖 MAIN MENU")
            print("="*50)
            print("1. Start Simulation")
            print("2. Manage Accounts")
            print("3. System Status")
            print("4. View Chat Logs")
            print("5. Exit")
            
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == '1':
                await self.start_simulation()
            elif choice == '2':
                await self.manage_accounts_menu()
            elif choice == '3':
                self.show_status()
            elif choice == '4':
                # View logs implementation
                logs = self.chat_logger.get_logs(limit=10)
                if logs:
                    print("\n📝 RECENT CHAT LOGS:")
                    for log in logs:
                        print(f"[{log['timestamp']}] {log['account']} ({log['personality']}): {log['message']}")
                else:
                    print("📭 No chat logs yet.")
            elif choice == '5':
                print("👋 Exiting...")
                await self.account_manager.disconnect_all()
                break
            else:
                print("❌ Invalid option!")

# Run the application
if __name__ == "__main__":
    simulation = TelegramSimulation()
    
    try:
        asyncio.run(simulation.main())
    except KeyboardInterrupt:
        print("\n🛑 Program interrupted by user")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        sys.exit(1)