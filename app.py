from flask import Flask, render_template, request, jsonify
import re
import html
import urllib.parse
import itertools

app = Flask(__name__, template_folder='templates')

FULLWIDTH_OFFSET = 0xFEE0
FULLWIDTH_CHARS = set('<>"\'/(){}[];:+%=&')
HTML_ENTITY_CHARS = set('<>"\'&')

def to_fullwidth(text, charset=FULLWIDTH_CHARS):
    return ''.join(chr(ord(c) + FULLWIDTH_OFFSET) if c in charset else c for c in text)

def to_html_entity(text, charset=None):
    return html.escape(text)

def to_full_html_entities(text):
    return ''.join(f'&#{ord(c)};' for c in text)

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

def to_circled_with_separator(text):
    parts = text.split('.')
    if not all(part.isdigit() for part in parts):
        return text

    def circle_digits(segment):
        return ''.join(
            '\u24EA' if d == '0' else chr(0x2460 + int(d) - 1) for d in segment
        )

    return '⨀'.join(circle_digits(part) for part in parts)

def to_circled_negative_final_zero(text):
    parts = text.split('.')
    final = parts[-1]
    return '.'.join(parts[:-1]) + '.' + ''.join(chr(0x24FF) if c == '0' else c for c in final)

def to_circled_with_fullwidth_dots(text):
    """Encodes IPs using circled digits with fullwidth dots (．). Returns original if not a valid IPv4 address."""
    parts = text.split('.')
    if len(parts) != 4 or not all(part.isdigit() for part in parts):
        return text

    def circled_segment(segment):
        result = ''
        for d in segment:
            if d == '0':
                result += '\u24EA'  # circled zero
            elif d in '123456789':
                result += chr(0x245F + int(d))  # circled 1–9
            else:
                return segment  # fallback on bad char
        return result

    try:
        return '．'.join(circled_segment(part) for part in parts)
    except Exception:
        return text

def to_rock_dots(text):
    return '∵'.join(text.split('.'))

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

def get_circled_options(octet):
    per_digit = ''.join(chr(0x2460 + int(d) - 1) if d != '0' else '\u24EA' for d in str(octet))
    options = [per_digit]

    if 100 <= octet <= 999:
        first_two = octet // 10
        last_digit = octet % 10
        if 10 <= first_two <= 20:
            compound = chr(0x2469 + first_two - 10)
            if last_digit != 0:
                compound += chr(0x2460 + last_digit - 1)
            options.append(compound)
    elif 10 <= octet <= 20:
        options.append(chr(0x2469 + octet - 10))

    return options

def generate_ipv6_mapped_combinations(ipv4):
    octets = list(map(int, ipv4.split('.')))
    options = [get_circled_options(o) for o in octets]
    combinations = list(itertools.product(*options))
    results = []
    for combo in combinations:
        part = '。'.join(combo)  # Use ideographic dot
        results.append(f"::ⓕⓕⓕⓕ:{part}")
    return results


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
                'Full HTML Entities': to_full_html_entities(payload),
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
                'Circled with ⨀': to_circled_with_separator(payload),
                'Circled (neg ending ⓿)': to_circled_negative_final_zero(payload),
                'Circled with Fullwidth Dots (Only Valid for IPs)': to_circled_with_fullwidth_dots(payload),
                'Rock Dots': to_rock_dots(payload),
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
                'Replacement Char Appended (U+FFFD)': append_replacement_char(payload),
            }
            # Bundle all IPv6 mixed encodings into one block
            cleaned_payload = payload.strip("[] ")
            if cleaned_payload.startswith("::ffff:") and re.match(r"::ffff:\d+\.\d+\.\d+\.\d+$", cleaned_payload):
                ipv4 = cleaned_payload.split(":ffff:")[-1].strip('[] ')
                octet_parts = [part.strip('[] ') for part in ipv4.split('.')]
                octets = list(map(int, octet_parts))
                combos = generate_ipv6_mapped_combinations('.'.join(map(str, octets)))
                joined_combos = '\n'.join(f'[{c}]' for c in combos)
                encoded['Mixed IPv6 Mapped IPv4 Variant (Unicode + Circle)'] = joined_combos
            else:
                encoded['Mixed IPv6 Mapped IPv4 Variant (Unicode + Circle)'] = "⚠ Not an IPv6-mapped IPv4 address (expected format: ::ffff:x.x.x.x)"

        return jsonify(encoded)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)