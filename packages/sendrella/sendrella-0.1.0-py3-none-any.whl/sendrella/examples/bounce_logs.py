from sendrella import SendrellaClient

client = SendrellaClient(api_key="your_api_key_here")

logs = client.bounce.logs(page=1, per_page=5)

print("📑 Bounce Logs")
for log in logs.get("logs", []):
    print(f"- {log['email']} | Score: {log['bounce_score']} | Status: {log['status']} | Reason: {log['reason']}")
