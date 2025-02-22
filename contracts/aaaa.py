from moralis import evm_api

api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjMzNmMzOWY0LWEwZWUtNDBlZS1hZDZiLTE4Y2Q2MDRlYjk4MyIsIm9yZ0lkIjoiNDMxNzc3IiwidXNlcklkIjoiNDQ0MTM4IiwidHlwZSI6IlBST0pFQ1QiLCJ0eXBlSWQiOiI0YzMxYjdmNy00MDNmLTQ3ZmItOTliNS1mYTAyY2Q2NDRmN2EiLCJpYXQiOjE3Mzk3MzQ0NzUsImV4cCI6NDg5NTQ5NDQ3NX0.6QyE8boCjJR5JR4O2H2prZatcPP-afFmZs99-F3IEmw"

from moralis import evm_api
import json

params = {
    "address": "0x30012Dc6f8a755584e6aA473116E774DE666ec32",
    "chain": "eth",
    "format": "decimal",
    "limit": 1,
    "token_addresses": [],
    "cursor": "",
    "normalizeMetadata": True,
}

result = []
for chain in ('eth', 'avax', 'polygon'):
    params['chain'] = chain
    result += [evm_api.nft.get_wallet_nfts(
    api_key=api_key,
    params=params,
    )]

# converting it to json because of unicode characters
print(json.dumps(result, indent=4))