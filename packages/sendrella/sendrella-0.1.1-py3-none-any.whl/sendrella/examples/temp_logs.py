from sendrella import SendrellaClient

client = SendrellaClient(api_key="your_api_key_here")

logs = client.temp_mail.logs(page=1, per_page=5)

print("📑 Temp Email Logs")
for log in logs.get("logs", []):
    print(f"- {log['email']} ({log['domain']}) → {log['status']} via {log['detection_method']}")
