#!/usr/bin/env python3
# SIRLION SIMPLE RIPPER - PAKAI INI AJA BOSQUE

import requests
from bs4 import BeautifulSoup
import re
import os

url = input("Masukkan URL target: ")
if not url.startswith("http"):
    url = "https://" + url

print(f"Mengambil data dari {url}...")

headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Ambil SEMUA teks dari halaman
semua_teks = soup.get_text(separator='\n', strip=True)

# Cari prompt (pake kata kunci umum)
kata_kunci = ['kamu adalah', 'Anda adalah', 'system', 'roleplay', 'prompt', 'jailbreak', 'HACKERAI']

hasil = []
for line in semua_teks.split('\n'):
    for keyword in kata_kunci:
        if keyword.lower() in line.lower():
            hasil.append(line)
            break

# Simpan
os.makedirs("hasil_rip", exist_ok=True)
with open("hasil_rip/prompt_ditemukan.txt", "w", encoding="utf-8") as f:
    for h in hasil:
        f.write(h + "\n\n")

print(f"Selesai! Ditemukan {len(hasil)} baris prompt")
print(f"File: hasil_rip/prompt_ditemukan.txt")
