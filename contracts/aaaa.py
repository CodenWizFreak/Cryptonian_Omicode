# Copyright © Aptos Foundation
# SPDX-License-Identifier: Apache-2.0

import asyncio
from aptos_sdk.account import Account
from aptos_sdk.async_client import FaucetClient, IndexerClient, RestClient
import os

# Configuration
FAUCET_URL = os.getenv("APTOS_FAUCET_URL", "https://faucet.devnet.aptoslabs.com")
FAUCET_AUTH_TOKEN = os.getenv("FAUCET_AUTH_TOKEN")
INDEXER_URL = os.getenv("APTOS_INDEXER_URL", "https://api.devnet.aptoslabs.com/v1/graphql")
NODE_URL = os.getenv("APTOS_NODE_URL", "https://api.devnet.aptoslabs.com/v1")

async def main():
    rest_client = RestClient(NODE_URL)
    faucet_client = FaucetClient(FAUCET_URL, rest_client, FAUCET_AUTH_TOKEN)

    if INDEXER_URL and INDEXER_URL != "none":
        indexer_client = IndexerClient(INDEXER_URL)
    else:
        indexer_client = None

    # Prompt user for input
    print("Welcome to the Aptos Wallet Interaction Script!")
    print("You can either:")
    print("1. Generate a new account.")
    print("2. Use an existing account by providing your private key.")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        # Generate a new account
        user_account = Account.generate()
        print("\n=== New Account Generated ===")
        print(f"Private Key: {user_account.private_key.hex()}")
        print(f"Public Key (Address): {user_account.address()}")
    elif choice == "2":
        # Use an existing account
        private_key_hex = input("Enter your private key (64-character hex string): ").strip()
        try:
            user_account = Account.load_key(private_key_hex)
            print("\n=== Account Loaded ===")
            print(f"Public Key (Address): {user_account.address()}")
        except Exception as e:
            print(f"Error: Invalid private key. {e}")
            await rest_client.close()
            return
    else:
        print("Invalid choice. Exiting.")
        await rest_client.close()
        return

    # Fund the user's account
    print("\n=== Funding Account ===")
    await faucet_client.fund_account(user_account.address(), 100_000_000)
    print(f"Account funded with 100,000,000 coins.")

    # Display initial balance
    print("\n=== Initial Balance ===")
    balance = await rest_client.account_balance(user_account.address())
    print(f"Balance: {balance}")

    # Transfer coins to another address
    print("\n=== Transfer Coins ===")
    recipient_address = input("Enter the recipient's address: ").strip()
    amount = int(input("Enter the amount to transfer: ").strip())

    try:
        txn_hash = await rest_client.bcs_transfer(user_account, recipient_address, amount)
        await rest_client.wait_for_transaction(txn_hash)
        print(f"Transaction successful! Hash: {txn_hash}")
    except Exception as e:
        print(f"Transaction failed: {e}")

    # Display final balance
    print("\n=== Final Balance ===")
    balance = await rest_client.account_balance(user_account.address())
    print(f"Balance: {balance}")

    # Query transaction history using Indexer (if enabled)
    if indexer_client:
        print("\n=== Transaction History ===")
        query = """
            query TransactionsQuery($account: String) {
              account_transactions(
                limit: 20
                where: {account_address: {_eq: $account}}
              ) {
                transaction_version
                coin_activities {
                  amount
                  activity_type
                  coin_type
                  entry_function_id_str
                  owner_address
                  transaction_timestamp
                }
              }
            }
        """
        variables = {"account": f"{user_account.address()}"}
        data = await indexer_client.query(query, variables)
        transactions = data["data"]["account_transactions"]
        if transactions:
            for txn in transactions:
                print(f"Transaction Version: {txn['transaction_version']}")
                for activity in txn["coin_activities"]:
                    print(f"  Activity: {activity['activity_type']}, Amount: {activity['amount']}")
        else:
            print("No transactions found.")

    await rest_client.close()


if __name__ == "__main__":
    asyncio.run(main())