# examples/check_bounce.py

from sendrella import SendrellaClient

client = SendrellaClient(api_key="your_api_key_here")

result = client.bounce.check("hello@example.com")

print("Status:", result.get("status"))
print("Bounce Score:", result.get("bounce_score"))
print("Reason:", result.get("reason"))
print("Confidence Signals:", result.get("confidence_indicators"))
