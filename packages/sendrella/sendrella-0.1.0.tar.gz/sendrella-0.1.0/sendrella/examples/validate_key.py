from sendrella import SendrellaClient

client = SendrellaClient(api_key="your_api_key_here")

info = client.utils.validate_key()

print("🔐 API Key Validation")
print("Success:", info.get("success"))
print("Account Name:", info.get("name"))
