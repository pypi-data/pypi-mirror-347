import re

keywords = {
    "اگر": "if",
    "وگرنه": "else",
    "تا وقتی که": "while",
    "برای": "for",
    "در غیر این صورت": "elif",
    "در حین": "while",
    "در": "in",
    "تعریف": "def",
    "چاپ": "print",
    "برگردان": "return",
    "برگرداندن": "yield",
    "و": "and",
    "یا": "or",
    "نه": "not",
    "درست": "True",
    "نادرست": "False",
    "هیچ": "None",
    "کلاس": "Class",
}

def convert_farsi_numbers_to_english(text):
    farsi_to_english_numbers = {
        '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
        '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'
    }
    for farsi, english in farsi_to_english_numbers.items():
        text = text.replace(farsi, english)
    return text

def translate(code):
    # ذخیره رشته‌های داخل " " یا ' '
    string_matches = list(re.finditer(r'(["\'])(?:(?=(\\?))\2.)*?\1', code))
    strings = {}
    for i, match in enumerate(string_matches):
        key = f"__STR_{i}__"
        strings[key] = match.group(0)
        code = code.replace(match.group(0), key)

    # تبدیل کلمات کلیدی
    for fa, en in sorted(keywords.items(), key=lambda x: -len(x[0])):
        code = code.replace(fa, en)

    # تبدیل اعداد فارسی
    code = convert_farsi_numbers_to_english(code)

    # برگرداندن رشته‌ها سر جاشون
    for key, original in strings.items():
        code = code.replace(key, original)

    return code
