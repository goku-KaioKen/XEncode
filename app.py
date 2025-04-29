from flask import Flask, render_template, request, jsonify
import html
import urllib.parse
import os

app = Flask(__name__, template_folder='templates')

FULLWIDTH_OFFSET = 0xFEE0
FULLWIDTH_CHARS = set('<>"\'/(){}[];:+%=')
HTML_ENTITY_CHARS = set('<>"\'&')

def to_fullwidth(text, charset=FULLWIDTH_CHARS):
    return ''.join(chr(ord(c) + FULLWIDTH_OFFSET) if c in charset else c for c in text)

def to_html_entity(text, charset=HTML_ENTITY_CHARS):
    return ''.join(html.escape(c) if c in charset else c for c in text)

def to_unicode_escape(text):
    return ''.join('\\u{:04x}'.format(ord(c)) for c in text)

def to_utf8_urlencode(text):
    utf8_bytes = text.encode('utf-8')
    return urllib.parse.quote(utf8_bytes)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    payload = request.form.get('payload', '')
    encoded = {
        'fullwidth': to_fullwidth(payload),
        'html_entity': to_html_entity(payload),
        'unicode_escape': to_unicode_escape(payload),
        'utf8_urlencode': to_utf8_urlencode(to_fullwidth(payload))
    }
    return jsonify(encoded)

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    app.run(host='127.0.0.1', port=5000, debug=False)
