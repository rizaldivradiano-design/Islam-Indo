import json, os, requests, threading, time, random, sys, hashlib, base64
from datetime import datetime

CONFIG_FILE = "config.json"
DATA_FILE = "data.json"
SECRET = "islam-indo-rizal-2026"

def encrypt_data(data):
    j = json.dumps(data)
    k = hashlib.sha256(SECRET.encode()).digest()
    enc = bytes([ord(c) ^ k[i % len(k)] for i, c in enumerate(j)])
    return base64.b64encode(enc).decode()

def decrypt_data(s):
    try:
        enc = base64.b64decode(s.encode())
        k = hashlib.sha256(SECRET.encode()).digest()
        dec = "".join([chr(b ^ k[i % len(k)]) for i, b in enumerate(enc)])
        return json.loads(dec)
    except:
        return None

def banner():
    os.system("clear")
    print(r"""
  _____ _____ _ __ __
 |_ _/ ____| | | \/ |
   | | | (___ | | | \ / |
   | | \___ \| | | |\/| |
  _| |_ ____) | |____ | | | |
 |_____|_____/|______| |_| |_|
      Created by Rizal
    """)

def load_json(file, default):
    if file == DATA_FILE:
        if not os.path.exists(file):
            with open(file,'w') as f: f.write(encrypt_data(default))
            return default
        with open(file,'r') as f:
            d = decrypt_data(f.read())
            if d is None:
                print("⚠️ DATA XP DI-BOBOL! Reset jadi 0")
                time.sleep(2)
                with open(file,'w') as wf: wf.write(encrypt_data(default))
                return default
            return d
    else:
        if not os.path.exists(file):
            with open(file,'w') as f: json.dump(default,f,indent=2)
            return default
        with open(file,'r') as f: return json.load(f)

def save_json(file, data):
    if file == DATA_FILE:
        with open(file,'w') as f: f.write(encrypt_data(data))
    else:
        with open(file,'w') as f: json.dump(data,f,indent=2)

def auto_clear():
    print("\nPesan akan tertutup dalam 10 detik...")
    time.sleep(10)
    banner()
    print("Perintah:.khotbah.jadwalsholat.ngaji.xp.kuisislam.achievement.dk.setkota.clear.exit.reset")

def get_jadwal(kota_id="1210"):
    try:
        if str(kota_id).isdigit():
            url = f"https://api.myquran.com/v1/sholat/jadwal/{kota_id}/{datetime.now().strftime('%Y/%m/%d')}"
        else:
            url = f"http://api.aladhan.com/v1/timingsByCity?city={kota_id}&country=Indonesia&method=2"
        r = requests.get(url, timeout=10).json()
        if str(kota_id).isdigit():
            return r['data']['jadwal'], r['data']['lokasi']
        else:
            return r['data']['timings'], kota_id
    except:
        return None, None

def get_daftar_kota():
    try:
        r = requests.get("https://api.myquran.com/v1/sholat/kota/semua", timeout=10).json()
        return r['data']
    except:
        return [
            {"id":"1210","lokasi":"BANDAR LAMPUNG"},
            {"id":"1202","lokasi":"BANTEN"},
            {"id":"1301","lokasi":"JAKARTA"},
            {"id":"1211","lokasi":"LAMPUNG SELATAN"},
            {"id":"1221","lokasi":"LAMPUNG TENGAH"}
        ]

def get_rank(xp):
    if xp < 50: return "Pencari Hidayah"
    elif xp < 150: return "Pejuang Subuh"
    elif xp < 300: return "Penjaga Sholat"
    elif xp < 500: return "Ahlul Quran"
    else: return "Wali Santri"

def khotbah_pendek():
    data = [
        {"judul":"Khotbah Pendek: Jaga Sholat","isi":"Peliharalah sholat. QS Al-Baqarah 238. Sholat tiang agama, jangan tinggalkan."},
        {"judul":"Khotbah Pendek: Sabar","isi":"Jadikan sabar dan sholat sebagai penolongmu. QS Al-Baqarah 153. Allah bersama orang sabar."}
    ]
    return random.choice(data)

def khotbah_panjang():
    data = [
        {"judul":"Khotbah Panjang: Bahaya Judi Online","isi":"Jamaah rahimakumullah. Allah berfirman QS Al-Maidah 90: Hai orang beriman, sesungguhnya khamr, berjudi, berhala adalah keji termasuk perbuatan syaitan maka jauhilah. Judi online merusak keluarga, ekonomi, iman.","kuis_q":"QS Al-Maidah 90 melarang apa?","kuis_a":"judi"},
        {"judul":"Khotbah Panjang: Pentingnya Ngaji","isi":"Alhamdulillah. Iqra bismi rabbik. Selama kita hidup kita masih kategori mengaji. Menuntut ilmu wajib.","kuis_q":"Arti Iqra?","kuis_a":"bacalah"},
        {"judul":"Khotbah Panjang: Birrul Walidain","isi":"Dan Kami perintahkan berbuat baik kepada ibu bapak. QS Luqman 14. Ridho Allah ada pada ridho orang tua.","kuis_q":"QS Luqman 14 tentang apa?","kuis_a":"orang tua"}
    ]
    return random.choice(data)

def tanya_awal():
    banner()
    config = load_json(CONFIG_FILE, {})
    if "is_mengaji" not in config:
        print("=== SETUP AWAL ===")
        print("Ketik.dk untuk daftar kota")
        jwb = input("Apakah anda masih dalam kategori mengaji n/Y : ").lower().strip()
        is_mengaji = True if jwb == 'y' else False
        kota_input = input("Masukan ID kota contoh 1210 : ") or "1210"
        if kota_input.lower() == ".dk":
            for k in get_daftar_kota()[:60]:
                print(f"{k['lokasi'].lower()} : {k['id']}")
            kota_input = input("Masukan ID kota : ") or "1210"
        config = {"is_mengaji": is_mengaji, "kota_id": kota_input, "kota": kota_input}
        save_json(CONFIG_FILE, config)
        save_json(DATA_FILE, {"xp":0, "waktu_ngaji":"", "last_sholat":"", "kuis_benar":0})
        print(f"Disimpan! Mode {'NGAJI' if is_mengaji else 'NON-NGAJI'}")
        time.sleep(2)
        banner()
    return config

def main():
    config = tanya_awal()
    data = load_json(DATA_FILE, {"xp":0, "waktu_ngaji":"", "last_sholat":"", "kuis_benar":0})
    print("Bot Jalan!.khotbah.jadwalsholat.ngaji.xp.kuisislam.achievement.dk.setkota.clear.exit")
    while True:
        try:
            cmd = input("\n> ").strip()
            low = cmd.lower()
            if low == "clear" or low == ".clear":
                banner()
                print("Perintah:.khotbah.jadwalsholat.ngaji.xp.kuisislam.achievement.dk.setkota.clear.exit")
                continue
            if low == ".dk":
                print("\nDaftar Kota:")
                for k in get_daftar_kota():
                    print(f"{k['lokasi'].lower()} : {k['id']}")
                auto_clear()
                continue
            if low.startswith(".setkota"):
                try:
                    id_baru = cmd.split(" ")[1]
                    config["kota_id"] = id_baru
                    config["kota"] = id_baru
                    save_json(CONFIG_FILE, config)
                    print(f"Kota diganti ke {id_baru}")
                except:
                    print("Format:.setkota 1210")
                auto_clear()
                continue
            if low == "exit" or low == ".exit":
                print("Keluar Barakallah")
                sys.exit(0)
            if low == ".reset":
                for f in [CONFIG_FILE, DATA_FILE]:
                    if os.path.exists(f): os.remove(f)
                print("Reset Jalankan ulang")
                break
            elif low == ".jadwalsholat":
                timings, lokasi = get_jadwal(str(config.get("kota_id","1210")))
                if timings:
                    print(f"\nJadwal {lokasi}")
                    for k,v in timings.items():
                        print(f"{k}: {v}")
                else:
                    print("Gagal cek ID kota.dk dulu")
                auto_clear()
                continue
            elif low == ".khotbah":
                print("\nPilihan\n1. Khotbah pendek +10 xp\n2. Khotbah panjang +20 xp\n3. Khotbah panjang dan kuis +50 xp")
                pil = input("Pilih 1/2/3 : ").strip()
                if pil == "1":
                    kh = khotbah_pendek()
                    print(f"\n{kh['judul']}\n\n{kh['isi']}")
                    if config["is_mengaji"]:
                        data["xp"] += 10
                        save_json(DATA_FILE, data)
                        print(f"\n+10 XP Total {data['xp']} Rank {get_rank(data['xp'])}")
                elif pil == "2":
                    kh = khotbah_panjang()
                    print(f"\n{kh['judul']}\n\n{kh['isi']}")
                    if config["is_mengaji"]:
                        data["xp"] += 20
                        save_json(DATA_FILE, data)
                        print(f"\n+20 XP Total {data['xp']} Rank {get_rank(data['xp'])}")
                elif pil == "3":
                    kh = khotbah_panjang()
                    print(f"\n{kh['judul']}\n\n{kh['isi']}\n\n--- KUIS ---\n{kh['kuis_q']}")
                    jawab = input("Jawaban lu : ").lower().strip()
                    if kh['kuis_a'] in jawab:
                        print("MasyaAllah benar")
                        if config["is_mengaji"]:
                            data["xp"] += 50
                            save_json(DATA_FILE, data)
                            print(f"+50 XP Total {data['xp']} Rank {get_rank(data['xp'])}")
                    else:
                        print(f"Belum tepat Jawaban {kh['kuis_a']} tetap +20 XP")
                        if config["is_mengaji"]:
                            data["xp"] += 20
                            save_json(DATA_FILE, data)
                auto_clear()
                continue
            elif low == ".kuisislam":
                soal = [
                    {"q":"Rukun Islam ada berapa?","a":"5"},
                    {"q":"Malam Lailatul Qadar di bulan apa?","a":"ramadhan"},
                    {"q":"Nabi pertama siapa?","a":"adam"},
                    {"q":"Kitab umat Islam?","a":"quran"},
                    {"q":"Sholat pertama?","a":"subuh"},
                    {"q":"Arah kiblat ke kota?","a":"mekkah"},
                    {"q":"Puasa wajib bulan apa?","a":"ramadhan"}
                ]
                s = random.choice(soal)
                print(f"\n[KUIS ISLAM] {s['q']}")
                jwb = input("Jawaban: ").lower().strip()
                if s['a'] in jwb:
                    data["xp"] += 15
                    data["kuis_benar"] = data.get("kuis_benar",0)+1
                    save_json(DATA_FILE, data)
                    print(f"Bener +15 XP Total {data['xp']} Rank {get_rank(data['xp'])}")
                else:
                    print(f"Salah Jawaban {s['a']}")
                auto_clear()
                continue
            elif low == ".achievement":
                xp = data["xp"]
                rank = get_rank(xp)
                print(f"\n=== ACHIEVEMENT ===\nRank: {rank}\nXP: {xp}\nKuis benar: {data.get('kuis_benar',0)}\n\nBadge:")
                if xp >= 10: print("✅ Pertama Ngaji")
                if xp >= 50: print("✅ Rajin Sholat")
                if data.get('kuis_benar',0) >= 1: print("✅ Cerdas Islami")
                if xp >= 100: print("✅ Istiqomah")
                if xp >= 300: print("✅ Ahlul Quran Unlock")
                if xp >= 500: print("✅ Wali Santri")
                if xp < 10: print("Belum ada ayo ngaji dulu")
                auto_clear()
                continue
            elif low == ".ngaji":
                if config["is_mengaji"]:
                    data["xp"] += 10
                    save_json(DATA_FILE, data)
                    print(f"Barakallah +10 XP Total {data['xp']} Rank {get_rank(data['xp'])}")
                    auto_clear()
                continue
            elif low == ".xp":
                print(f"XP {data['xp']} Rank {get_rank(data['xp'])} Kota {config.get('kota_id')}")
                auto_clear()
                continue
        except KeyboardInterrupt:
            print("\nKetik.clear atau.exit")
            continue
        except Exception as e:
            print(f"Error {e}")
            continue

if __name__ == "__main__":
    main()