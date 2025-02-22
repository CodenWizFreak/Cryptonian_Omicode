
from aptos_sdk.account import Account
from aptos_sdk.async_client import RestClient
from aptos_sdk.transactions import TransactionPayload, EntryFunction
from aptos_sdk.authenticator import Authenticator
from aptos_sdk.bcs import Serializer
from typing import List, Dict, Optional, Tuple
import json
import os
from dataclasses import dataclass

@dataclass
class WalletConnection:
    address: str
    wallet_type: str
    connected: bool
    balance: Optional[float] = None

class AptosContract:
    def __init__(self):
        self.client = RestClient("https://fullnode.mainnet.aptoslabs.com/v1")
        self.account = None
        self.module_address = "0x1"  # Replace with your deployed module address
        self.nft_collection_name = "Cryptonian_Achievements"
        
    async def connect_wallet(self, wallet_type: str, connection_data: Dict) -> Tuple[bool, Optional[str]]:
        """
        Enhanced wallet connection for Aptos wallets.
        
        Args:
            wallet_type: Type of wallet ("petra", "martian", "pontem")
            connection_data: Dictionary containing wallet-specific connection data
            
        Returns:
            Tuple[bool, Optional[str]]: (Success status, Error message if any)
        """
        try:
            if wallet_type not in ["petra", "martian", "pontem"]:
                return False, "Unsupported wallet type"

            if "address" not in connection_data:
                return False, "No address provided"

            try:
                # If private key is provided (for development/testing)
                if "private_key" in connection_data:
                    self.account = Account.load_key(connection_data["private_key"])
                else:
                    # For production: use wallet's provided address
                    self.account = Account.load_address(connection_data["address"])

                # Verify account
                await self.client.account(self.account.address())
                
                # Store wallet connection info
                self.wallet_connection = WalletConnection(
                    address=self.account.address(),
                    wallet_type=wallet_type,
                    connected=True
                )
                
                # Get initial balance
                balance = await self.get_balance()
                if balance is not None:
                    self.wallet_connection.balance = float(balance) / 1e8  # Convert to APT
                
                return True, None

            except Exception as e:
                return False, f"Failed to verify Aptos account: {str(e)}"

        except Exception as e:
            return False, f"Wallet connection failed: {str(e)}"

    def disconnect_wallet(self) -> None:
        """Disconnects the current wallet."""
        self.account = None
        self.wallet_connection = None

    def get_wallet_info(self) -> Optional[WalletConnection]:
        """Returns current wallet connection information."""
        return self.wallet_connection

    async def verify_wallet_connection(self) -> bool:
        """Verifies if the wallet connection is still valid."""
        if not self.wallet_connection or not self.wallet_connection.connected:
            return False
            
        try:
            await self.client.account(self.account.address())
            return True
        except:
            return False

    def transfer(self, receiver: str, amount: float) -> Optional[str]:
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

    async def mint_achievement_nft(self, achievement_data: Dict) -> Optional[str]:
        """Mints an NFT for a completed achievement."""
        if not self.account:
            return None
        try:
            # Create NFT metadata
            metadata = {
                "name": f"Cryptonian Achievement: {achievement_data['title']}",
                "description": achievement_data['description'],
                "image": achievement_data['image_url'],
                "attributes": {
                    "category": achievement_data['category'],
                    "difficulty": achievement_data['difficulty'],
                    "score": achievement_data['score'],
                    "timestamp": achievement_data['timestamp']
                }
            }
            
            # Prepare transaction payload for NFT minting
            payload = EntryFunction.natural(
                f"{self.module_address}::cryptonian_nft",
                "mint_achievement",
                [],
                [
                    self.nft_collection_name,
                    metadata["name"],
                    metadata["description"],
                    metadata["image"],
                    json.dumps(metadata["attributes"])
                ]
            )
            
            txn = await self.client.create_bcs_transaction(self.account, payload)
            signed_txn = await self.client.sign_bcs_transaction(self.account, txn)
            txn_hash = await self.client.submit_bcs_transaction(signed_txn)
            return txn_hash
        except Exception as e:
            print(f"NFT minting failed: {e}")
            return None

    async def reward_tokens(self, user_address: str, amount: int, reason: str) -> Optional[str]:
        """Rewards tokens to users for completing activities."""
        if not self.account:
            return None
        try:
            payload = EntryFunction.natural(
                f"{self.module_address}::cryptonian_token",
                "reward_tokens",
                [],
                [user_address, amount, reason]
            )
            
            txn = await self.client.create_bcs_transaction(self.account, payload)
            signed_txn = await self.client.sign_bcs_transaction(self.account, txn)
            txn_hash = await self.client.submit_bcs_transaction(signed_txn)
            return txn_hash
        except Exception as e:
            print(f"Token reward failed: {e}")
            return None

    async def update_dynamic_nft(self, token_id: str, new_metadata: Dict) -> Optional[str]:
        """Updates a dynamic NFT based on user progress."""
        if not self.account:
            return None
        try:
            payload = EntryFunction.natural(
                f"{self.module_address}::cryptonian_nft",
                "update_nft_metadata",
                [],
                [token_id, json.dumps(new_metadata)]
            )
            
            txn = await self.client.create_bcs_transaction(self.account, payload)
            signed_txn = await self.client.sign_bcs_transaction(self.account, txn)
            txn_hash = await self.client.submit_bcs_transaction(signed_txn)
            return txn_hash
        except Exception as e:
            print(f"NFT update failed: {e}")
            return None

    async def get_user_achievements(self, address: str) -> List[Dict]:
        """Retrieves all NFT achievements for a user."""
        try:
            resources = await self.client.get_account_resources(address)
            nft_store = next(
                (r for r in resources if "cryptonian_nft" in r["type"]),
                None
            )
            if not nft_store:
                return []
            
            return nft_store["data"]["achievements"]
        except Exception as e:
            print(f"Error fetching achievements: {e}")
            return []

    async def create_marketplace_listing(self, token_id: str, price: float) -> Optional[str]:
        """Lists an NFT on the marketplace."""
        if not self.account:
            return None
        try:
            payload = EntryFunction.natural(
                f"{self.module_address}::cryptonian_marketplace",
                "list_nft",
                [],
                [token_id, int(price * 1e8)]
            )
            
            txn = await self.client.create_bcs_transaction(self.account, payload)
            signed_txn = await self.client.sign_bcs_transaction(self.account, txn)
            txn_hash = await self.client.submit_bcs_transaction(signed_txn)
            return txn_hash
        except Exception as e:
            print(f"Marketplace listing failed: {e}")
            return None

    async def purchase_nft(self, listing_id: str) -> Optional[str]:
        """Purchases an NFT from the marketplace."""
        if not self.account:
            return None
        try:
            payload = EntryFunction.natural(
                f"{self.module_address}::cryptonian_marketplace",
                "purchase_nft",
                [],
                [listing_id]
            )
            
            txn = await self.client.create_bcs_transaction(self.account, payload)
            signed_txn = await self.client.sign_bcs_transaction(self.account, txn)
            txn_hash = await self.client.submit_bcs_transaction(signed_txn)
            return txn_hash
        except Exception as e:
            print(f"NFT purchase failed: {e}")
            return None

    def get_transaction_history(self) -> List[Dict]:
        """Retrieves transaction history for the connected wallet."""
        if not self.account:
            return []
        try:
            transactions = self.client.get_account_transactions(self.account.address())
            return [
                {
                    "Hash": tx["hash"],
                    "Timestamp": tx["timestamp"],
                    "Type": tx["payload"]["function"],
                    "Amount": tx["payload"]["arguments"][1] if "arguments" in tx["payload"] else None
                } 
                for tx in transactions
            ]
        except Exception as e:
            print(f"Error fetching transactions: {e}")
            return []
