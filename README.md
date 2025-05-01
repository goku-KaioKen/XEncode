# 🧪 XEncode

**XEncode** is a powerful web-based payload obfuscation tool for security researchers, red teamers, and bug bounty hunters. It helps bypass WAFs and input filters by transforming XSS and SSRF payloads using exotic and lesser-known Unicode, encoding, and IP obfuscation tricks.

---

## ✨ Features

- 🧠 **Real-time encoding** as you type
- 💣 **Three distinct modes**:
  - `XSS Mode` — Obfuscate HTML/script payloads
  - `SSRF Mode` — Evade SSRF filters with exotic Unicode and RTL tricks
  - `IP Obfuscation Mode` — Generate all known valid representations of an IP
- 📋 **Per-field copy** and **Copy ALL** support
- 🏹 **IPv6-mapped IPv4 encodings** with multiple combinations (including bracketed form `[::ffff:x.x.x.x]`)

---

## 🛠️ Encoding Techniques

### XSS Mode
| Type                    | Example                              |
|-------------------------|--------------------------------------|
| Full-width Unicode      | `<` → `＜`                           |
| HTML Entities (basic)   | `<` → `&lt;`                        |
| HTML Entities (numeric) | `<` → `&#60;` or `&#x3c;`           |
| Unicode Escape          | `<` → `\u003c`                     |
| UTF-8 URL (Fullwidth)  | `＜` → `%EF%BC%9C`                  |

### SSRF Mode
| Encoding                           | Example                                 |
|------------------------------------|-----------------------------------------|
| Math Double-Struck                 | 𝟠𝟙.𝟜.𝟙𝟚𝟜.𝟙𝟘                           |
| Math Monospace                     | 𝟾𝟷.𝟺.𝟷𝟸𝟺.𝟷𝟶                           |
| Math Sans                          | 𝟪𝟣.𝟦.𝟣𝟤𝟦.𝟣𝟢                           |
| Math Sans Bold                     | 𝟴𝟭.𝟰.𝟭𝟮𝟰.𝟭𝟬                           |
| Circled (alpha+num)               | ⓲⓫.⓮.⓫⓬⓮.⓫⓪                           |
| Circled with ⨀ Separator           | ⑧①⨀④⨀①②④⨀①⓪                          |
| Circled with Fullwidth Dots       | ①⑨②．①⑥⑧．①．①                         |
| Circled (neg ending ⓿)            | 81.4.124.1⓿                             |
| IPv6 Mixed Encodings               | [::ⓕⓕⓕⓕ:①⑥⑨。②⑤④。⑯⑨。②⑤⑤]       |
| Rock Dots                         | 81∵4∵124∵10                             |
| Parenthesized Digits             | ⑻⑴.⑷.⑴⑵⑷.⑴⓪                          |
| Subscript Digits                 | ₈₁.₄.₁₂₄.₁₀                           |
| Superscript Digits               | ⁸¹.⁴.¹²⁴.¹⁰                           |
| Small Caps                       | ꜱᴇʀᴠᴇʀᴏʙᴊᴇᴄᴛ                         |
| Faux Cyrillic                   | ЅΣЯѴΣЯФБЈΣCТ                           |
| Homoglyph Swap                  | ѕеrvеrіntеrnаl                         |
| Zalgo / Combining Marks          | 8̀1́.̂4̀.́1̂2̀4́.̂1̀0́                   |
| RTL Override                     | ‮10.124.4.81                       |
| Zero Width (ZWSP)               | 8​1​.​4​.​1​2​4​.​1​0                   |
| Replacement Char Injected       | 8�1�.�4�.�1�2�4�.�1�0                  |
| Replacement Char Appended       | 81.4.124.10�                           |

### IP Obfuscation Mode
Generates all valid representations of an IP address like:

| Variant               | Output Example                |
|-----------------------|-------------------------------|
| Decimal               | `http://192.168.1.1`          |
| Class B               | `http://192.168.257`          |
| Class A               | `http://192.11010305`         |
| DWORD (unsigned)      | `http://3232235777`           |
| Dotted Hex            | `http://0xc0.0xa8.0x1.0x1`     |
| Packed Hex            | `http://0xc0a80101`           |
| Hybrid Hex 1          | `http://0xc0.0xa80101`         |
| Hybrid Hex 2          | `http://0xc0.0xa8.0x0101`      |
| Dotted Octal          | `http://0300.0250.01.01`       |
| Padded Octal          | `http://0300.0250.0001.0001`   |
| Packed Octal          | `http://030052000401`         |
| Percent Encoding      | `http://%31%39%32...`          |
| Mixed Hex/Octal       | `http://192.0xa8.0001.0x1`     |
| Unicode (Circled)     | `http://①⑨②．①⑥⑧．①．①`     |
| IPv6-mapped IPv4     | `http://[::ffff:192.168.1.1]`     |

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

### 🔐 Behind Apache
Use Apache reverse proxy to expose via HTTPS:
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

## 📦 Project Structure
```
xencode/
├── app.py              # Flask backend with encoder logic
├── Dockerfile
├── docker-compose.yml
└── templates/
    └── index.html      # Frontend UI with dynamic logic
```

---

## 🎯 Example
Paste your payload:
```html
<script>alert(1)</script>
```

And instantly get:
- `＜ｓｃｒｉｐｔ＞ａｌｅｒｔ（１）＜／ｓｃｒｉｐｔ＞`
- `&lt;script&gt;alert(1)&lt;/script&gt;`
- `&#60;&#115;&#99;&#114;&#105;&#112;&#116;&#62;alert(1)&#60;/script&#62;`
- `\u003c\u0073\u0063\u0072...`
- `%EF%BC%9C%EF%BD%93%EF%BD...`

---

## 💡 Use Cases
- Obfuscating payloads for WAF/IDS testing
- XSS/SSRF encoding permutations
- Input filter bypass fuzzing
- Unicode transformation attack research

---

## 📜 License
MIT — free to use, improve, and distribute. Attribution appreciated.

## Credits

Built by a hacker for hackers by gokuKaioKen