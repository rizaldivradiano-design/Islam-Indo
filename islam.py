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
        return [{"id":"1210","lokasi":"BANDAR LAMPUNG"},{"id":"1301","lokasi":"JAKARTA"}]

def get_rank(xp):
    if xp < 50: return "Pencari Hidayah"
    elif xp < 150: return "Pejuang Subuh"
    elif xp < 300: return "Penjaga Sholat"
    elif xp < 500: return "Ahlul Quran"
    else: return "Wali Santri"

# === API KHOTBAH ===
def get_khotbah_pendek_api():
    try:
        r = requests.get("https://khotbah-api.vercel.app/api/khotbah/random", timeout=10)
        if r.status_code == 200:
            d = r.json()
            return {"judul": d.get('judul','Khotbah Pendek API'), "isi": d.get('isi','')[:1500], "kuis_q": "Apa tema khotbah ini?", "kuis_a": "islam"}
    except: pass
    return {"judul":"Khotbah Pendek: Jaga Sholat","isi":"Peliharalah sholat. QS Al-Baqarah 238. Sholat tiang agama.","kuis_q":"Sholat tiang apa?","kuis_a":"agama"}

def get_khotbah_panjang_api():
    isi_api = ""
    judul_api = "Khotbah Jumat"
    try:
        # API 1
        r = requests.get("https://api.myquran.com/v1/khotbah/jumat", timeout=10).json()
        if r.get('data'):
            judul_api = r['data'].get('judul', judul_api)
            isi_api = r['data'].get('isi', '')
    except: pass
    if not isi_api:
        try:
            # API 2 backup
            r = requests.get("https://raw.githubusercontent.com/renomureza/islamic-api/main/data/khotbah.json", timeout=10).json()
            pil = random.choice(r)
            judul_api = pil['judul']
            isi_api = pil['isi']
        except: pass
    if not isi_api:
        try:
            # API 3 Quran sebagai bahan khotbah
            r = requests.get("https://api.quran.gading.dev/surah/2", timeout=10).json()
            ayat = r['data']['verses'][random.randint(1,10)]['translation']['id']
            judul_api = "Khotbah Jumat: Pentingnya Takwa (API Quran)"
            isi_api = ayat
        except:
            isi_api = "Wahai jamaah, tingkatkan takwa kepada Allah."

    # BUNGKUS JADI FULL KHOTBAH JUMAT PANJANG
    full_isi = f"""
إِنَّ الْحَمْدَ لِلَّهِ نَحْمَدُهُ وَنَسْتَعِينُهُ وَنَسْتَغْفِرُهُ

Jamaah Jumat rahimakumullah,
Marilah kita bersyukur kepada Allah SWT dan meningkatkan takwa.

Judul Khotbah Hari Ini (dari API): {judul_api}

MATERI KHOTBAH DARI API:
{isi_api}

PENJELASAN LENGKAP:
Jamaah sekalian, apa yang disampaikan API tadi adalah inti sari ajaran Islam. Mari kita kembangkan.

1. Muqaddimah Takwa:
Allah berfirman: "Hai orang-orang yang beriman, bertakwalah kepada Allah sebenar-benar takwa kepada-Nya, dan janganlah sekali-kali kamu mati melainkan dalam keadaan beragama Islam." (QS Ali Imran 102)

2. Isi Utama:
{isi_api}

Kita sebagai muslim harus mengamalkan ini dalam kehidupan sehari-hari. Jangan hanya didengar, tapi diamalkan.

Jika ini tentang sholat, maka jagalah sholat 5 waktu. Jika tentang judi, jauhilah. Jika tentang orang tua, berbaktilah.

3. Penutup dan Doa:
Marilah kita tutup dengan doa. Semoga Allah memberikan kita hidayah, menjaga keluarga kita dari maksiat, dan memasukkan kita ke surga firdaus.

Semoga khotbah dari API ini bermanfaat. Ingat, ilmu tanpa amal bagaikan pohon tanpa buah.

Aamiin ya Rabbal Alamin.
"""
    return {"judul": judul_api, "isi": full_isi, "kuis_q": f"Apa judul khotbah API tadi?", "kuis_a": judul_api.split()[0].lower()}

def tanya_awal():
    banner()
    config = load_json(CONFIG_FILE, {})
    if "is_mengaji" not in config:
        print("=== SETUP AWAL ===")
        jwb = input("Apakah anda masih kategori mengaji n/Y : ").lower().strip()
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
            if low in ["clear",".clear"]:
                banner()
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
                    save_json(CONFIG_FILE, config)
                    print(f"Kota diganti ke {id_baru}")
                except:
                    print("Format:.setkota 1210")
                auto_clear()
                continue
            if low in ["exit",".exit"]:
                print("Keluar Barakallah")
                sys.exit(0)
            if low == ".reset":
                for f in [CONFIG_FILE, DATA_FILE]:
                    if os.path.exists(f): os.remove(f)
                print("Reset! Jalankan ulang")
                break
            elif low == ".jadwalsholat":
                timings, lokasi = get_jadwal(str(config.get("kota_id","1210")))
                if timings:
                    print(f"\nJadwal {lokasi}")
                    for k,v in timings.items():
                        print(f"{k}: {v}")
                else:
                    print("Gagal cek,.dk dulu")
                auto_clear()
                continue
            elif low == ".khotbah":
                print("\nPilihan\n1. Khotbah pendek (API) +10 xp [auto 10 detik]\n2. Khotbah panjang FULL API +20 xp [tunggu.selesaibaca]\n3. Khotbah panjang API + kuis +50 xp [tunggu.selesaibaca]")
                pil = input("Pilih 1/2/3 : ").strip()
                if pil == "1":
                    print("\nMengambil khotbah pendek dari API...")
                    kh = get_khotbah_pendek_api()
                    print(f"\n{kh['judul']}\n\n{kh['isi']}")
                    if config["is_mengaji"]:
                        data["xp"] += 10
                        save_json(DATA_FILE, data)
                        print(f"\n+10 XP Total {data['xp']} Rank {get_rank(data['xp'])}")
                    auto_clear()
                elif pil in ["2","3"]:
                    print("\nMengambil khotbah panjang dari API...")
                    kh = get_khotbah_panjang_api()
                    print(f"\n{kh['judul']}\n\n{kh['isi']}")
                    print("\n" + "="*60)
                    print("Ketik.selesaibaca setelah selesai membaca khotbah")
                    print("="*60)
                    while True:
                        s = input().lower().strip()
                        if s == ".selesaibaca":
                            break
                        else:
                            print("Ketik.selesaibaca jika sudah selesai")
                    if pil == "2":
                        if config["is_mengaji"]:
                            data["xp"] += 20
                            save_json(DATA_FILE, data)
                            print(f"\nBarakallah sudah baca khotbah API +20 XP Total {data['xp']} Rank {get_rank(data['xp'])}")
                    else:
                        print(f"\n--- KUIS API ---\n{kh['kuis_q']}")
                        jawab = input("Jawaban lu : ").lower().strip()
                        if kh['kuis_a'].lower() in jawab.lower() or jawab.lower() in kh['kuis_a'].lower():
                            print("MasyaAllah benar")
                            if config["is_mengaji"]:
                                data["xp"] += 50
                                save_json(DATA_FILE, data)
                                print(f"+50 XP Total {data['xp']}")
                        else:
                            print(f"Belum tepat, jawaban {kh['kuis_a']} tetap +20 XP")
                            if config["is_mengaji"]:
                                data["xp"] += 20
                                save_json(DATA_FILE, data)
                    banner()
                continue
            elif low == ".kuisislam":
                soal = [{"q":"Rukun Islam ada berapa?","a":"5"},{"q":"Puasa wajib bulan apa?","a":"ramadhan"}]
                s = random.choice(soal)
                print(f"\n[KUIS ISLAM] {s['q']}")
                jwb = input("Jawaban: ").lower().strip()
                if s['a'] in jwb:
                    data["xp"] += 15
                    data["kuis_benar"] = data.get("kuis_benar",0)+1
                    save_json(DATA_FILE, data)
                    print(f"Bener +15 XP Total {data['xp']}")
                else:
                    print(f"Salah, jawaban {s['a']}")
                auto_clear()
                continue
            elif low == ".achievement":
                print(f"\nRank: {get_rank(data['xp'])} | XP: {data['xp']}")
                auto_clear()
                continue
            elif low == ".xp":
                print(f"XP {data['xp']} Rank {get_rank(data['xp'])}")
                auto_clear()
                continue
        except KeyboardInterrupt:
            continue
        except Exception as e:
            print(f"Error {e}")
            continue

if __name__ == "__main__":
    main()