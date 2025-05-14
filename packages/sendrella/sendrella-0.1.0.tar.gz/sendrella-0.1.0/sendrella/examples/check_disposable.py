# examples/check_disposable.py

from sendrella import SendrellaClient

client = SendrellaClient(api_key="your_api_key_here")

result = client.temp_mail.check("user@mailinator.com")

if result.get("is_disposable"):
    print("⚠️ Disposable detected")
else:
    print("✅ Not disposable")
