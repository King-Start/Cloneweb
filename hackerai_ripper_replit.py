from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>SirLion Prompt Ripper</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #0a0a0a; color: #0f0; font-family: monospace; padding: 20px; }
        input, button { background: #111; color: #0f0; border: 1px solid #0f0; padding: 10px; margin: 5px; width: 80%; }
        .result { background: #111; padding: 15px; margin-top: 20px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1>🦁 SirLion Prompt Ripper</h1>
    <form method="POST">
        <input type="text" name="url" placeholder="https://target.com" required>
        <button type="submit">🔥 RIP PROMPT 🔥</button>
    </form>
    {% if result %}
        <div class="result"><pre>{{ result }}</pre></div>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        url = request.form.get('url')
        if not url.startswith('http'):
            url = 'https://' + url
        
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(r.text, 'html.parser')
            text = soup.get_text()
            
            # Cari prompt
            keywords = ['kamu adalah', 'Anda adalah', 'system', 'roleplay', 'prompt', 'HACKERAI']
            found = []
            for line in text.split('\n'):
                for kw in keywords:
                    if kw.lower() in line.lower():
                        found.append(line)
                        break
            
            result = f"Ditemukan {len(found)} baris prompt:\n\n" + "\n".join(found[:50])
        except Exception as e:
            result = f"Error: {str(e)}"
    
    return render_template_string(HTML_FORM, result=result)

if __name__ == '__main__':
    # ★ INI KUNCI AGAR WEBVIEW MUNCUL ★
    app.run(host='0.0.0.0', port=8080, debug=False)
