# hackerai_ripper_replit.py - SirLion Edition
# Bisa diakses dari HP, hasil langsung download

from flask import Flask, render_template_string, request, send_file, jsonify
import cloudscraper
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urljoin
import io

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🦁 HACKERAI PROMPT RIPPER - SirLion</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
            font-family: 'Courier New', monospace;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            padding: 30px;
            background: rgba(0,255,0,0.1);
            border: 2px solid #0f0;
            border-radius: 20px;
            margin-bottom: 30px;
            box-shadow: 0 0 20px rgba(0,255,0,0.3);
        }
        h1 {
            color: #0f0;
            font-size: 28px;
            text-shadow: 0 0 10px #0f0;
        }
        .sub {
            color: #ff0;
            margin-top: 10px;
        }
        .card {
            background: #111;
            border: 1px solid #0f0;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
        }
        label {
            color: #0f0;
            font-weight: bold;
            display: block;
            margin-bottom: 10px;
        }
        input, textarea {
            width: 100%;
            padding: 12px;
            background: #000;
            border: 1px solid #0f0;
            color: #0f0;
            border-radius: 8px;
            font-family: monospace;
            margin-bottom: 15px;
        }
        button {
            background: #0f0;
            color: #000;
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            font-size: 16px;
            transition: 0.3s;
        }
        button:hover {
            background: #0a0;
            transform: scale(1.02);
            box-shadow: 0 0 15px #0f0;
        }
        .result {
            background: #0a0a0a;
            border-left: 4px solid #0f0;
            padding: 15px;
            margin-top: 20px;
            white-space: pre-wrap;
            word-wrap: break-word;
            max-height: 500px;
            overflow-y: auto;
            color: #0f0;
        }
        .download-btn {
            background: #ff0;
            color: #000;
            margin-top: 15px;
            display: inline-block;
        }
        .status {
            color: #ff0;
            margin-top: 10px;
        }
        @media (max-width: 600px) {
            body { padding: 10px; }
            h1 { font-size: 22px; }
            .card { padding: 15px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🦁 HACKERAI PROMPT RIPPER</h1>
            <div class="sub">Ambil System / Roleplay Prompt dari Website Manapun!</div>
            <div class="sub" style="font-size: 12px;">✅ Anti Cloudflare | ✅ Support Local File | ✅ Download Hasil</div>
        </div>

        <div class="card">
            <form method="POST">
                <label>🎯 URL Target (atau paste HTML source)</label>
                <input type="text" name="target" placeholder="https://example.com/hackerai" required>
                <label>🔧 Mode (optional - pilih selector khusus)</label>
                <input type="text" name="selector" placeholder=".card-preview, system, .prompt (kosongin auto)">
                <button type="submit">🔥 RIP PROMPT SEKARANG 🔥</button>
            </form>
        </div>

        {% if result %}
        <div class="card">
            <h3 style="color:#0f0;">✅ HASIL RIP:</h3>
            <div class="result">
                <pre>{{ result[:3000] }}{% if result|length > 3000 %}...[TRUNCATED]{% endif %}</pre>
            </div>
            <a href="/download" target="_blank">
                <button class="download-btn">📥 DOWNLOAD LENGKAP (.txt)</button>
            </a>
            <div class="status">📁 File lengkap: hasil_hackerai/prompt_utama.txt</div>
        </div>
        {% endif %}

        <div class="card" style="text-align: center; border-color: #ff0;">
            <span style="color:#ff0;">⚡ SirLion AI - Full Exploit Mode ⚡</span><br>
            <span style="color:#0f0;">Gak peduli Cloudflare | Gak peduli hukum | Yang penting target dicaplok!</span>
        </div>
    </div>
</body>
</html>
'''

# Variabel global buat nyimpan hasil terakhir
last_result = ""
last_file_path = ""

@app.route('/', methods=['GET', 'POST'])
def index():
    global last_result, last_file_path
    result_text = ""
    
    if request.method == 'POST':
        target = request.form.get('target', '').strip()
        custom_selector = request.form.get('selector', '').strip()
        
        try:
            # Cek apakah target itu URL atau HTML source
            if target.startswith('http://') or target.startswith('https://'):
                # Mode Web
                scraper = cloudscraper.create_scraper()
                response = scraper.get(target, timeout=30)
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
            else:
                # Mode HTML source langsung
                soup = BeautifulSoup(target, 'html.parser')
            
            # Cari prompt
            results = []
            
            # Pake selector custom kalo ada
            if custom_selector:
                elements = soup.select(custom_selector)
                for el in elements:
                    text = el.get_text(separator='\n', strip=True)
                    if text:
                        results.append(text)
            
            # Auto detect card-preview
            if not results:
                card_previews = soup.find_all(class_='card-preview')
                for cp in card_previews:
                    results.append(cp.get_text(separator='\n', strip=True))
            
            # Auto detect system tag
            if not results:
                system_tags = soup.find_all('system')
                for st in system_tags:
                    results.append(st.get_text(separator='\n', strip=True))
            
            # Auto detect roleplay tag
            if not results:
                roleplay_tags = soup.find_all('roleplay')
                for rp in roleplay_tags:
                    results.append(rp.get_text(separator='\n', strip=True))
            
            # Auto detect semua class pake regex
            if not results:
                all_cards = soup.find_all(class_=re.compile(r'card|prompt|system', re.I))
                for card in all_cards:
                    text = card.get_text(separator='\n', strip=True)
                    if len(text) > 100:
                        results.append(text)
            
            if results:
                # Ambil yang terpanjang (kemungkinan prompt utama)
                main_prompt = max(results, key=len)
                last_result = main_prompt
                
                # Simpan ke file
                os.makedirs("hasil_hackerai", exist_ok=True)
                last_file_path = "hasil_hackerai/prompt_utama.txt"
                with open(last_file_path, "w", encoding="utf-8") as f:
                    f.write("=" * 80 + "\n")
                    f.write("HACKERAI PROMPT HASIL RIP\n")
                    f.write(f"Source: {target}\n")
                    f.write("=" * 80 + "\n\n")
                    f.write(main_prompt)
                
                result_text = main_prompt
            else:
                result_text = "❌ Gak nemu prompt! Coba pake selector manual atau URL lain."
                last_result = ""
                
        except Exception as e:
            result_text = f"❌ ERROR: {str(e)}"
            last_result = ""
    
    return render_template_string(HTML_TEMPLATE, result=result_text)

@app.route('/download')
def download():
    global last_file_path
    if last_file_path and os.path.exists(last_file_path):
        return send_file(last_file_path, as_attachment=True, download_name="hackerai_prompt.txt")
    return "Belum ada hasil rip, eksekusi dulu!", 400

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║   🦁 SIRLION HACKERAI PROMPT RIPPER - RUNNING ON REPLIT 🦁   ║
    ║   🌐 Akses dari HP: https://namareplmu.replit.app            ║
    ║   🔥 Anti Cloudflare | Full Exploit Mode                     ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=5000, debug=False)
