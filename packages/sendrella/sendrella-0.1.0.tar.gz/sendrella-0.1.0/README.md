# Sendrella Python SDK

The official Python SDK for [Sendrella](https://sendrella.com) — a modern infrastructure for secure and intelligent email communication.

It enables effortless integration with the Sendrella API to perform:

- ✉️ Email bounce checks  
- 🛡️ Disposable (temporary) email detection  
- 📊 Credit tracking  
- 🔐 API key validation  

---

## 📦 Installation

Install directly via Git:

```bash
pip install git+https://github.com/Salman0x01/sendrella-python-sdk.git
```

Or clone this repo and install locally:

```bash
git clone https://github.com/Salman0x01/sendrella-python-sdk.git
cd sendrella-python-sdk
pip install .
```

---

## 🔑 Authentication

Every API call requires a valid Sendrella API key.

### 🔐 Get your key:
1. Log in to [Sendrella Dashboard](https://sendrella.com/dashboard)
2. Copy your API key
3. Use it in the SDK like this:

```python
from sendrella import SendrellaClient

client = SendrellaClient(api_key="your_api_key_here")
```

---

## 🚀 Usage Examples

### 📬 Check Email Bounce

```python
result = client.bounce.check("hello@example.com")
print(result["status"])          # valid / warn / risky / invalid / error
print(result["bounce_score"])    # Score between 0–100
print(result["confidence_indicators"])
```

---

### 📑 Retrieve Bounce Logs

```python
logs = client.bounce.logs(page=1, status="risky")
for log in logs["logs"]:
    print(log["email"], "-", log["status"], "(", log["bounce_score"], ")")
```

---

### 🛡️ Check Disposable Email

```python
result = client.temp_mail.check("user@mailinator.com")
if result.get("is_disposable"):
    print("❌ Disposable email detected")
else:
    print("✅ Clean email")
```

---

### 📂 View Temp Mail Logs

```python
logs = client.temp_mail.logs(page=1)
for log in logs["logs"]:
    print(log["email"], "-", log["status"], "via", log["detection_method"])
```

---

### 💳 Fetch Credits

```python
credits = client.utils.credits()
print("Available:", credits["available_credits"])
print("Used:", credits["all_time_used"])
print("Total:", credits["all_time_credits"])
```

---

### 🔐 Validate API Key

```python
info = client.utils.validate_key()
if info.get("success"):
    print("Authenticated as:", info.get("name"))
else:
    print("Invalid or expired API key")
```

---

## 🧪 Running Tests

```bash
# Run all tests
pytest -v tests/

# Or run one
pytest -v tests/test_bounce.py
```

Make sure to set your API key:

```bash
set SENDRELLA_API_KEY=your_api_key_here   # Windows
export SENDRELLA_API_KEY=your_api_key_here  # Linux/macOS
```

---

## 📚 Supported Endpoints

| Feature           | Method                      | Path                        |
|------------------|-----------------------------|-----------------------------|
| Bounce Check      | `client.bounce.check()`     | `/bounce/check`             |
| Bounce Logs       | `client.bounce.logs()`      | `/bounce/logs`              |
| Disposable Check  | `client.temp_mail.check()`  | `/tempmail/check`           |
| Temp Logs         | `client.temp_mail.logs()`   | `/tempmail/logs`            |
| Get Credits       | `client.utils.credits()`    | `/utils/credits`            |
| Validate API Key  | `client.utils.validate_key()`| `/token/validate`           |

---

## 🛠️ Error Handling

All errors are wrapped in custom exceptions:

- `SendrellaError` (base)
- `AuthenticationError`
- `BadRequestError`
- `ServerError`
- `TimeoutError`
- `NotFoundError`

Example:

```python
from sendrella.exceptions import AuthenticationError

try:
    result = client.bounce.check("email@example.com")
except AuthenticationError:
    print("Invalid API key or permission denied.")
```

---

## 📄 License

MIT License © 2025 [Your Name or Company]

---

## ❤️ Contributing

PRs welcome! Please submit bug fixes, improvements, or new endpoints with test coverage.

---

## 🔗 Useful Links

- [Official Website](https://sendrella.com)
- [API Docs](https://swagger.sendrella.com)
- [Support](https://sendrella.com/contact)

