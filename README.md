# 🧪 XEncode

**XEncode** is a payload obfuscation tool for security researchers and bug bounty hunters. It provides real-time, browser-based encoding of payloads for **XSS**, **SSRF**, and other filter-evasion techniques — all with a clean UI and secure backend.

---

## ✨ Features

- 🧠 **Real-time encoding** with input throttling
- 🔁 Toggle between **XSS** and **SSRF** encoding modes
- 📋 **Copy buttons** for each encoding and a global "Copy All"

---

## 🧩 Encoding Techniques

### 🔹 XSS Mode
| Type                        | Example             |
|-----------------------------|---------------------|
| Full-width Unicode          | `<` → `＜`          |
| HTML Entities               | `<` → `&lt;`        |
| Unicode Escape              | `<` → `\u003c`     |
| UTF-8 URL (Full-width)      | `＜` → `%EF%BC%9C`   |

### 🔸 SSRF Mode
Includes obfuscation variants that can bypass filters, regexes, or normalization-based checks:

- **Math-based Unicode styles**: Sans, Bold, Monospace, Double-struck
- **Visual Trickery**:
  - Zero-width injectors (U+200B)
  - RTL override (U+202E)
  - Unicode combining marks (Zalgo-style)
- **Unicode Lookalikes**:
  - Homoglyph swaps (Latin → Cyrillic)
  - Faux Cyrillic, Small Caps
- **Numeric Manipulation**:
  - Circled digits (⓪⑨)
  - Full-width digits (０１２)
  - Subscript / Superscript
- **Filter Confusion**:
  - Unicode replacement char (�, U+FFFD) injection/appending

---

## 🎯 Usage

### 🔬 Local (Python)
```bash
pip install flask
python app.py
# Visit http://127.0.0.1:5000
```

### 🐳 Docker
```bash
docker-compose up --build
# Exposed securely at http://127.0.0.1:5000
```

### 🔐 Production (Apache Reverse Proxy)
```apache
<VirtualHost *:443>
    ServerName encoder.example.com
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/
    SSLEngine on
    SSLCertificateFile /path/fullchain.pem
    SSLCertificateKeyFile /path/key.pem
</VirtualHost>
```

---

## 📦 Project Structure

```
XEncode/
├── app.py                 # Flask backend
├── templates/
│   └── index.html         # UI + dynamic rendering
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🔍 Example Payloads

Input:
```html
<script>alert(1)</script>
```

Encodings:
- **Full-width**: `＜ｓｃｒｉｐｔ＞ａｌｅｒｔ（１）＜／ｓｃｒｉｐｔ＞`
- **HTML Entity**: `&lt;script&gt;alert(1)&lt;/script&gt;`
- **Unicode Escape**: `\u003c\u0073\u0063...`

---

## 🧠 Use Cases

- Bypassing XSS filters and input sanitizers
- SSRF WAF/regex filter bypasses
- Red team payload mutation
- Fuzzing backend normalization behaviors
- Filter evasion in CTFs or bug bounty targets

---

## 📜 License

MIT — free for all uses. Contributions and suggestions are welcome!

## Credits

Built by a hacker for hackers by gokuKaioKen