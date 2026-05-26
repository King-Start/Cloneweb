#!/usr/bin/env python3
# web_copy_server.py - SirLion Web Copy Server v3.0 (Lightweight)

from flask import Flask, render_template_string, request, jsonify
import requests
from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin
import re
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>SirLion Web Copy v3.0</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: monospace; background: #0a0a0a; color: #0f0; padding: 20px; }
        input, select, button { background: #111; color: #0f0; border: 1px solid #0f0; padding: 10px; margin: 5px; }
        .result { background: #111; padding: 15px; border-left: 3px solid #0f0; margin-top: 20px; white-space: pre-wrap; word-wrap: break-word; }
        a { color: #0f0; }
        @media (max-width: 600px) { body { padding: 10px; } input, select, button { width: 100%; } }
    </style>
</head>
<body>
    <h1>🦁 SirLion Web Copy v3.0</h1>
    <p>Copy SEMUA dari website target — jalan di server, HP cuma lihat hasil 📱</p>
    <form method="POST">
        <input type="text" name="url" placeholder="https://target.com" required style="width: 70%;">
        <select name="menu">
            <option value="1">📄 Ambil SEMUA TEKS</option>
            <option value="2">🖼️ Ambil SEMUA GAMBAR</option>
            <option value="3">📇 Ambil SEMUA CARD</option>
            <option value="4">🤖 Ambil SYSTEM PROMPT</option>
            <option value="5">🔗 Ambil SEMUA LINK</option>
            <option value="6">📜 Ambil RAW HTML</option>
            <option value="7">📝 Ambil PREVIEW/DESKRIPSI</option>
            <option value="0">💣 Ambil SEMUANYA (1-7)</option>
        </select>
        <button type="submit">🔥 EKSEKUSI 🔥</button>
    </form>
    <div class="result">
        {% if result %}
            <pre>{{ result }}</pre>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        menu = request.form.get('menu')
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=30, verify=False)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            output_lines = [f"✅ Target: {url}\n"]
            
            # Menu 1
            if menu in ['1', '0']:
                text = soup.get_text(separator='\n', strip=True)
                output_lines.append(f"\n📄 TEKS ({len(text)} karakter):\n{text[:3000]}...")
            
            # Menu 2
            if menu in ['2', '0']:
                imgs = soup.find_all('img')
                img_urls = []
                for img in imgs:
                    src = img.get('src') or img.get('data-src')
                    if src:
                        full = urljoin(url, src)
                        img_urls.append(f"🔗 {full}")
                output_lines.append(f"\n🖼️ GAMBAR ({len(img_urls)}):\n" + "\n".join(img_urls[:50]))
            
            # Menu 3
            if menu in ['3', '0']:
                cards = soup.find_all(class_=re.compile(r'card', re.I))
                card_texts = [c.get_text(strip=True)[:500] for c in cards[:30]]
                output_lines.append(f"\n📇 CARD ({len(cards)}):\n" + "\n---\n".join(card_texts))
            
            # Menu 4
            if menu in ['4', '0']:
                prompts = []
                for s in soup.find_all('system'):
                    prompts.append(s.get_text(strip=True))
                for div in soup.find_all(class_=re.compile(r'system|roleplay', re.I)):
                    prompts.append(div.get_text(strip=True)[:1000])
                output_lines.append(f"\n🤖 SYSTEM PROMPT ({len(prompts)}):\n" + "\n\n".join(prompts[:10]))
            
            # Menu 5
            if menu in ['5', '0']:
                links = soup.find_all('a', href=True)
                link_list = [f"{i+1}. {a.get_text(strip=True)[:50]} -> {a['href']}" for i, a in enumerate(links[:100])]
                output_lines.append(f"\n🔗 LINK ({len(links)}):\n" + "\n".join(link_list))
            
            # Menu 6
            if menu in ['6', '0']:
                output_lines.append(f"\n📜 HTML MENTAH (3000 karakter pertama):\n{response.text[:3000]}...")
            
            # Menu 7
            if menu in ['7', '0']:
                previews = soup.find_all(class_=re.compile(r'preview|description', re.I))
                prev_texts = [p.get_text(strip=True)[:500] for p in previews[:20]]
                output_lines.append(f"\n📝 PREVIEW ({len(previews)}):\n" + "\n---\n".join(prev_texts))
            
            return render_template_string(HTML_FORM, result="\n".join(output_lines))
        
        except Exception as e:
            return render_template_string(HTML_FORM, result=f"❌ ERROR: {str(e)}")
    
    return render_template_string(HTML_FORM, result="⚡ Masukkan URL dan pilih menu. Server jalan lancar, HP lu gak perlu kuat-kuat amat!")

if __name__ == '__main__':
    print("""
    🦁 SIRLION WEB COPY SERVER v3.0
    📱 Akses dari HP: http://<IP_PC_LU>:5000
    🔥 Pastikan 1 WiFi/HP tethering
    """)
    app.run(host='0.0.0.0', port=5000, debug=False)
