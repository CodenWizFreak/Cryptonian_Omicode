import requests

# Aptos Testnet API Endpoint
NODE_URL = "https://fullnode.devnet.aptoslabs.com/v1"

def connect_wallet(wallet_address: str):
    """Check if the wallet address exists on Aptos blockchain"""
    try:
        response = requests.get(f"{NODE_URL}/accounts/{wallet_address}")
        
        if response.status_code == 200:
            print("✅ Wallet connected successfully!")
            return response.json()
        else:
            print(f"❌ Wallet connection failed: {response.json().get('message', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"❌ Wallet connection failed: {e}")
        return None

def get_transaction_history(wallet_address: str):
    """Fetch past transactions of the given Aptos wallet address"""
    try:
        response = requests.get(f"{NODE_URL}/accounts/{wallet_address}/transactions")
        
        if response.status_code == 200:
            transactions = response.json()
            if transactions:
                print("\n📜 **Past Transactions:**")
                for txn in transactions[:5]:  # Show last 5 transactions
                    print(f"🔹 Txn Hash: {txn['hash']}, Type: {txn['type']}, Time: {txn['timestamp']}")
            else:
                print("ℹ️ No transactions found.")
        else:
            print(f"❌ Failed to retrieve transactions: {response.json().get('message', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Error fetching transactions: {e}")

if __name__ == "__main__":
    wallet_address = input("Enter your Aptos wallet address: ").strip()
    account_info = connect_wallet(wallet_address)
    
    if account_info:
        print("\n🆔 **Account Info:**")
        print(account_info)
        get_transaction_history(wallet_address)
