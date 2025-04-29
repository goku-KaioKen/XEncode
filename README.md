# 🧪 XEncode

**XEncode** is a simple but powerful web tool designed for security researchers and bug bounty hunters to **obfuscate XSS payloads** using various encoding techniques — ideal for **WAF/IDS bypass testing** and input filter evasion.

---

## ✨ Features

- 🧠 **Real-time encoding** as you type
- 🔁 **Throttled updates** for smooth UX
- 🧩 **Multiple encodings**:
  - Full-width Unicode encoding
  - HTML entity encoding
  - Unicode escape encoding (`\uXXXX`)
  - Full-width + UTF-8 URL encoding
- 📋 **Copy to clipboard** (per field or all at once)
- 🖼️ Clean and responsive UI with scroll support for large payloads
- 🔒 Secure localhost-only deployment via Apache/Docker

---

## 🛠️ Encoding Techniques

| Type | Example |
|------|---------|
| **Full-width** | `<` → `＜` |
| **HTML Entities** | `<` → `&lt;` |
| **Unicode Escape** | `<` → `\u003c` |
| **UTF-8 URL** | `＜` → `%EF%BC%9C` |

---

## 🚀 Usage

### 🧪 Locally (Python)

```bash
pip install flask
python app.py
# Visit http://127.0.0.1:5000
```

### 🐳 Docker

```bash
docker-compose up --build
# Or bind securely to localhost via 127.0.0.1:5000
```

### 🔐 Production Behind Apache

Use Apache reverse proxy to expose it over HTTPS:
```apache
<VirtualHost *:443>
    ServerName encoder.yourdomain.com
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/
    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/yourcert.pem
    SSLCertificateKeyFile /etc/ssl/private/yourkey.pem
</VirtualHost>
```

---

## 📦 Deployment Structure

```
xss_encoder_webapp/
├── app.py                  # Flask app
├── Dockerfile              # Lightweight Python image
├── docker-compose.yml      # Run and expose app
└── templates/
    └── index.html          # UI with JS/CSS/UX polish
```

---

## 🎯 Example Payload

Paste your raw payload:

```html
<script>alert(1)</script>
```

And instantly get:

- Full-width:
  ```
  ＜ｓｃｒｉｐｔ＞ａｌｅｒｔ（１）＜／ｓｃｒｉｐｔ＞
  ```
- HTML entity:
  ```
  &lt;script&gt;alert(1)&lt;/script&gt;
  ```
- Unicode escape:
  ```
  \u003c\u0073\u0063\u0072\u0069...
  ```

---

## 💡 Use Cases

- Bypassing naive HTML filters
- Testing XSS payload handling
- Evading blacklists and regex-based WAFs

---

## 📜 License

MIT — use, modify, and share freely. Attribution appreciated.
