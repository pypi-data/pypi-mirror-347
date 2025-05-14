# examples/get_credits.py

from sendrella import SendrellaClient

client = SendrellaClient(api_key="your_api_key_here")

credits = client.utils.credits()
print("Credits:", credits.get("available_credits"))
