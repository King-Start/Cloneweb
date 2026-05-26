#!/usr/bin/env python3
# SIRLION IMPACT ELEMEN RIPPER - BISA LIAT SEMUA KONTEN TERHAMBAT

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os
import base64

G = '\033[92m'
R = '\033[91m'
Y = '\033[93m'
B = '\033[94m'
W = '\033[0m'

banner = f"""
{R}╔══════════════════════════════════════════════════════════════╗
{R}║{W}   🦁 SIRLION IMPACT ELEMEN RIPPER - TEMBUS APAPUN 🦁     {R}║
{R}║{Y}   "Bisa liat dan ambil elemen yang ke-hidden/clicable"    {R}║
{R}╚══════════════════════════════════════════════════════════════╝{W}
"""
print(banner)

url = input(f"{B}[?]{W} Masukkan URL target: ")
if not url.startswith("http"):
    url = "https://" + url

# Setup Chrome biar bisa jalan di Termux/Replit/Server
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # Mode headless biar gak popup
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")

print(f"{Y}[!]{W} Memulai browser...")

# Pake undetected-chromedriver kalo perlu (biar gak kedetek bot)
try:
    from undetected_chromedriver import Chrome
    driver = Chrome(options=chrome_options)
    print(f"{G}[✓]{W} Mode undetected AKTIF!")
except:
    driver = webdriver.Chrome(options=chrome_options)
    print(f"{Y}[!]{W} Mode biasa, mungkin kena deteksi")

driver.get(url)
time.sleep(3)

print(f"{G}[✓]{W} Halaman loaded: {driver.title}")

# ============================================================
# AUTO SCROLL KE BAWAH (biar semua konten ke-load)
# ============================================================
print(f"{Y}[!]{W} Auto scroll untuk load semua konten...")
last_height = driver.execute_script("return document.body.scrollHeight")
scroll_count = 0
while scroll_count < 10:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    scroll_count += 1
    print(f"  Scroll ke-{scroll_count}")

# ============================================================
# CARI SEMUA ELEMEN YANG MUNGKIN NYIMPAH KONTEN
# ============================================================
print(f"\n{Y}[!]{W} Mencari elemen impact...")

impact_selectors = [
    "button", "a", ".clickable", "[onclick]", 
    "[data-toggle]", "[data-target]", ".accordion",
    ".dropdown", ".collapse", ".modal-trigger",
    ".tab", ".nav-link", ".show-more", ".load-more",
    ".read-more", ".expand", "[data-bs-toggle]",
    "div[class*='hidden']", "div[class*='collapse']",
    "div[style*='display: none']", "div[style*='visibility: hidden']"
]

all_buttons = []
for selector in impact_selectors:
    elements = driver.find_elements(By.CSS_SELECTOR, selector)
    for el in elements:
        if el.is_displayed() and el.is_enabled():
            all_buttons.append(el)

print(f"{G}[✓]{W} Ditemukan {len(all_buttons)} elemen interaktif")

# ============================================================
# EKSEKUSI KLIK PADA SEMUA BUTTON (buat reveal konten)
# ============================================================
clicked = 0
for i, btn in enumerate(all_buttons[:30]):  # Maks 30 biar gak overload
    try:
        text = btn.text[:50] if btn.text else "no-text"
        print(f"  Mencoba klik {i+1}: {text}...")
        
        # Scroll ke elemen
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        
        # Klik pake JS (lebih ampuh)
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(1)
        clicked += 1
    except:
        pass

print(f"{G}[✓]{W} Berhasil klik {clicked} elemen")

# ============================================================
# AMBIL SEMUA TEKS YANG KELIHATAN (termasuk yang baru muncul)
# ============================================================
print(f"\n{Y}[!]{W} Mengambil semua konten yang terlihat...")

visible_text = driver.execute_script("""
    let elements = document.querySelectorAll('body *');
    let visible = [];
    for(let el of elements) {
        let style = window.getComputedStyle(el);
        if(style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0') {
            let text = el.innerText?.trim();
            if(text && text.length > 50 && !visible.some(v => v.includes(text.substring(0,100)))) {
                visible.push(text);
            }
        }
    }
    return visible;
""")

# ============================================================
# SCREENSHOT - BIAR LU BISA LIAT IMPACT ELEMENNYA
# ============================================================
print(f"\n{Y}[!]{W} Mengambil screenshot...")
os.makedirs("hasil_impact", exist_ok=True)

# Screenshot full page
screenshot_path = "hasil_impact/full_page.png"
driver.save_screenshot(screenshot_path)
print(f"{G}[✓]{W} Screenshot full page: {screenshot_path}")

# Screenshot per elemen penting (biar liat detail)
for i, btn in enumerate(all_buttons[:10]):
    try:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.3)
        elem_screenshot = f"hasil_impact/element_{i+1}.png"
        btn.screenshot(elem_screenshot)
        print(f"  Screenshot elemen {i+1} tersimpan")
    except:
        pass

# ============================================================
# SIMPAN HASIL TEKS
# ============================================================
with open("hasil_impact/semua_konten.txt", "w", encoding="utf-8") as f:
    f.write("=" * 80 + "\n")
    f.write(f"HASIL IMPACT RIP DARI: {url}\n")
    f.write("=" * 80 + "\n\n")
    for i, text in enumerate(visible_text, 1):
        f.write(f"\n{'─' * 40}\n")
        f.write(f"KONTEN KE-{i}\n")
        f.write(f"{'─' * 40}\n")
        f.write(text)
        f.write("\n")

print(f"\n{G}[✓]{W} Total {len(visible_text)} konten tersimpan")

# ============================================================
# EKSTRAK PROMPT / SYSTEM (pake regex)
# ============================================================
full_text = "\n".join(visible_text)

prompt_patterns = [
    r'kamu (?:adalah|sekarang menjadi|akan menjadi).*?(?=\n\n|\Z)',
    r'system prompt:.*?(?=\n\n|\Z)',
    r'roleplay.*?(?=\n\n|\Z)',
    r'kamu adalah asisten.*?(?=\n\n|\Z)',
    r'Anda adalah.*?(?=\n\n|\Z)',
    r'prompt:.*?(?=\n\n|\Z)',
]

import re
all_prompts = []
for pattern in prompt_patterns:
    matches = re.findall(pattern, full_text, re.IGNORECASE | re.DOTALL)
    all_prompts.extend(matches)

if all_prompts:
    with open("hasil_impact/prompt_ditemukan.txt", "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("PROMPT YANG DITEMUKAN\n")
        f.write("=" * 80 + "\n\n")
        for i, p in enumerate(all_prompts, 1):
            f.write(f"\n--- PROMPT {i} ---\n")
            f.write(p.strip())
            f.write("\n")
    print(f"{G}[✓]{W} Ditemukan {len(all_prompts)} prompt!")

# ============================================================
# SELESAI
# ============================================================
print(f"\n{G}{'='*60}{W}")
print(f"{G}✅ SELESAI!{W}")
print(f"{Y}📁 Hasil di folder: hasil_impact/{W}")
print(f"  - full_page.png (screenshot full)")
print(f"  - element_X.png (screenshot per elemen)")
print(f"  - semua_konten.txt (semua teks)")
if all_prompts:
    print(f"  - prompt_ditemukan.txt (prompt yang keextrak)")
print(f"{G}{'='*60}{W}")

driver.quit()
