from aptos_sdk.account import Account
from aptos_sdk.client import RestClient
from aptos_sdk.transactions import TransactionPayload
from aptos_sdk.authenticator import Authenticator
import os

class AptosContract:
    def __init__(self):
        self.client = RestClient("https://fullnode.mainnet.aptoslabs.com/v1")
        self.account = None

    def connect_wallet(self, private_key: str):
        """Connects to the Aptos wallet using a private key."""
        try:
            self.account = Account.load_key(private_key)
            return True
        except Exception as e:
            print(f"Wallet connection failed: {e}")
            return False

    def get_balance(self):
        """Fetches the account balance."""
        if not self.account:
            return None
        try:
            account_info = self.client.account(self.account.address())
            return int(account_info["balances"][0]["amount"])
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return None

    def transfer(self, receiver: str, amount: float):
        """Transfers APT tokens to another wallet."""
        if not self.account:
            return None
        try:
            txn_payload = TransactionPayload("0x1::coin::transfer", [receiver, int(amount * 1e8)])
            txn = self.client.create_transaction(self.account, txn_payload)
            signed_txn = self.client.sign_transaction(self.account, txn)
            txn_hash = self.client.submit_transaction(signed_txn)
            return txn_hash
        except Exception as e:
            print(f"Transfer failed: {e}")
            return None

    def get_transaction_history(self):
        """Retrieves transaction history for the connected wallet."""
        if not self.account:
            return []
        try:
            transactions = self.client.get_account_transactions(self.account.address())
            return [
                {"Hash": tx["hash"], "Timestamp": tx["timestamp"], "Amount": tx["payload"]["arguments"][1]} 
                for tx in transactions
            ]
        except Exception as e:
            print(f"Error fetching transactions: {e}")
            return []

