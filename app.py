from flask import Flask, render_template, request, jsonify
import html
import urllib.parse

app = Flask(__name__, template_folder='templates')

FULLWIDTH_OFFSET = 0xFEE0
FULLWIDTH_CHARS = set('<>"\'/(){}[];:+%=&')
HTML_ENTITY_CHARS = set('<>"\'&')

def to_fullwidth(text, charset=FULLWIDTH_CHARS):
    return ''.join(chr(ord(c) + FULLWIDTH_OFFSET) if c in charset else c for c in text)

def to_html_entity(text, charset=None):
    return html.escape(text)

def to_unicode_escape(text):
    return ''.join('\\u{:04x}'.format(ord(c)) for c in text)

def to_utf8_urlencode(text):
    utf8_bytes = text.encode('utf-8')
    return urllib.parse.quote(utf8_bytes)

def to_math_double_struck(text):
    def convert(c):
        if '0' <= c <= '9':
            return chr(0x1D7D8 + ord(c) - ord('0'))
        elif 'A' <= c <= 'Z':
            return chr(0x1D538 + ord(c) - ord('A'))
        elif 'a' <= c <= 'z':
            return chr(0x1D552 + ord(c) - ord('a'))
        return c
    return ''.join(convert(c) for c in text)

def to_math_monospace(text):
    def convert(c):
        if '0' <= c <= '9':
            return chr(0x1D7F6 + ord(c) - ord('0'))
        elif 'A' <= c <= 'Z':
            return chr(0x1D670 + ord(c) - ord('A'))
        elif 'a' <= c <= 'z':
            return chr(0x1D68A + ord(c) - ord('a'))
        return c
    return ''.join(convert(c) for c in text)

def to_math_sans(text):
    def convert(c):
        if '0' <= c <= '9':
            return chr(0x1D7E2 + ord(c) - ord('0'))
        elif 'A' <= c <= 'Z':
            return chr(0x1D5A0 + ord(c) - ord('A'))
        elif 'a' <= c <= 'z':
            return chr(0x1D5BA + ord(c) - ord('a'))
        return c
    return ''.join(convert(c) for c in text)

def to_math_sans_bold(text):
    def convert(c):
        if '0' <= c <= '9':
            return chr(0x1D7EC + ord(c) - ord('0'))
        elif 'A' <= c <= 'Z':
            return chr(0x1D5D4 + ord(c) - ord('A'))
        elif 'a' <= c <= 'z':
            return chr(0x1D5EE + ord(c) - ord('a'))
        return c
    return ''.join(convert(c) for c in text)

def to_circled_negative(text):
    base_digit = {str(i): chr(0x24EA + i) for i in range(10)}
    base_alpha = {chr(i): chr(0x24B6 + i - 65) for i in range(65, 91)}
    base_alpha.update({chr(i): chr(0x24D0 + i - 97) for i in range(97, 123)})
    return ''.join(base_digit.get(c, base_alpha.get(c, c)) for c in text)

def to_parenthesized_digits(text):
    digit_map = {
        '0': '⑽', '1': '⑴', '2': '⑵', '3': '⑶', '4': '⑷',
        '5': '⑸', '6': '⑹', '7': '⑺', '8': '⑻', '9': '⑼'
    }
    alpha_map = {chr(i): f'({chr(i)})' for i in range(65, 91)}
    alpha_map.update({chr(i): f'({chr(i)})' for i in range(97, 123)})
    return ''.join(digit_map.get(c, alpha_map.get(c, c)) for c in text)

def to_subscript(text):
    mapping = {
        **{str(i): chr(0x2080 + i) for i in range(10)},
        'a': 'ₐ', 'e': 'ₑ', 'h': 'ₕ', 'i': 'ᵢ', 'j': 'ⱼ',
        'k': 'ₖ', 'l': 'ₗ', 'm': 'ₘ', 'n': 'ₙ', 'o': 'ₒ',
        'p': 'ₚ', 'r': 'ᵣ', 's': 'ₛ', 't': 'ₜ', 'u': 'ᵤ',
        'v': 'ᵥ', 'x': 'ₓ'
    }
    return ''.join(mapping.get(c, c) for c in text)

def to_superscript(text):
    mapping = {
        **{str(i): chr(0x2070 + i) for i in range(10)},
        'a': 'ᵃ', 'b': 'ᵇ', 'c': 'ᶜ', 'd': 'ᵈ', 'e': 'ᵉ',
        'f': 'ᶠ', 'g': 'ᵍ', 'h': 'ʰ', 'i': 'ⁱ', 'j': 'ʲ',
        'k': 'ᵏ', 'l': 'ˡ', 'm': 'ᵐ', 'n': 'ⁿ', 'o': 'ᵒ',
        'p': 'ᵖ', 'r': 'ʳ', 's': 'ˢ', 't': 'ᵗ', 'u': 'ᵘ',
        'v': 'ᵛ', 'w': 'ʷ', 'x': 'ˣ', 'y': 'ʸ', 'z': 'ᶻ'
    }
    return ''.join(mapping.get(c, c) for c in text)

def to_small_caps(text):
    mapping = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ',
        'f': 'ꜰ', 'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ',
        'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ',
        'p': 'ᴘ', 'q': 'q', 'r': 'ʀ', 's': 'ꜱ', 't': 'ᴛ',
        'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'z'
    }
    return ''.join(mapping.get(c, c) for c in text)

def to_faux_cyrillic(text):
    mapping = {'A': 'Д', 'B': 'Ɓ', 'C': 'Ͼ', 'D': 'Ԁ', 'E': 'Σ', 'F': 'Ғ', 'G': 'Ɠ',
               'H': 'Ћ', 'I': 'І', 'J': 'Ј', 'K': 'Ҡ', 'L': 'Ŀ', 'M': 'М', 'N': 'И',
               'O': 'Ф', 'P': 'Р', 'Q': 'Ⴓ', 'R': 'Я', 'S': 'Ѕ', 'T': 'Т', 'U': 'Ц',
               'V': 'Ѵ', 'W': 'Ш', 'X': 'Ж', 'Y': 'Ұ', 'Z': 'Ȥ'}
    return ''.join(mapping.get(c.upper(), c) for c in text)

def to_zero_width(text):
    return '\u200b'.join(text)

def to_combining_marks(text):
    combining = ['\u0300', '\u0301', '\u0302']  # grave, acute, circumflex
    return ''.join(c + combining[i % len(combining)] for i, c in enumerate(text))

def to_rtl_override(text):
    return '\u202E' + text[::-1]

def to_homoglyph_swap(text):
    glyphs = {
        'a': 'а', 'c': 'ϲ', 'e': 'е', 'i': 'і', 'j': 'ј', 'o': 'о',
        'p': 'р', 's': 'ѕ', 'x': 'х', 'y': 'у', 'A': 'Α', 'B': 'Β',
        'C': 'С', 'E': 'Е', 'H': 'Н', 'I': 'І', 'J': 'Ј', 'K': 'Κ',
        'M': 'М', 'O': 'О', 'P': 'Р', 'S': 'Ѕ', 'T': 'Т', 'X': 'Χ', 'Y': 'Υ'
    }
    return ''.join(glyphs.get(c, c) for c in text)

def to_replacement_char(text):
    """Inserts U+FFFD (�) between each character."""
    return '\uFFFD'.join(text)

def append_replacement_char(text):
    """Appends U+FFFD (�) to the end of the input — useful after domain names."""
    return text + '\uFFFD'

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    try:
        payload = request.form.get('payload', '')
        mode = request.form.get('mode', 'xss')
        encoded = {}

        if mode == 'xss':
            encoded = {
                'Full-Width': to_fullwidth(payload),
                'HTML Entity': to_html_entity(payload),
                'Unicode Escape': to_unicode_escape(payload),
                'Unicode Normalization': to_utf8_urlencode(to_fullwidth(payload))
            }
        elif mode == 'ssrf':
            encoded = {
                'Math Double-Struck': to_math_double_struck(payload),
                'Math Monospace': to_math_monospace(payload),
                'Math Sans': to_math_sans(payload),
                'Math Sans Bold': to_math_sans_bold(payload),
                'Circled (alpha+num)': to_circled_negative(payload),
                'Parenthesized (alpha+num)': to_parenthesized_digits(payload),
                'Subscript (alpha+num)': to_subscript(payload),
                'Superscript (alpha+num)': to_superscript(payload),
                'Small Caps': to_small_caps(payload),
                'Faux Cyrillic': to_faux_cyrillic(payload),
                'Zero Width (ZWSP)': to_zero_width(payload),
                'Combining Marks (Zalgo)': to_combining_marks(payload),
                'RTL Override': to_rtl_override(payload),
                'Homoglyph Swap': to_homoglyph_swap(payload),
                'Replacement Char Injected (U+FFFD)': to_replacement_char(payload),
                'Replacement Char Appended (U+FFFD)': append_replacement_char(payload)
            }
        return jsonify(encoded)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)