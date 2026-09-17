import json, os, requests, time, random, sys, hashlib, base64
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
    print("================================\n ISLAM INDONESIA - by Rizal\n================================\n")

def load_json(file, default):
    if file == DATA_FILE:
        if not os.path.exists(file):
            with open(file,'w') as f: f.write(encrypt_data(default))
            return default
        with open(file,'r') as f:
            d = decrypt_data(f.read())
            if d is None:
                print("⚠️ DATA XP DI-BOBOL! Reset jadi 0\n")
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
    print("\nPesan akan tertutup dalam 10 detik...\n")
    time.sleep(10)
    banner()
    print("Perintah:\n.khotbah\n.jadwalsholat\n.sholat subuh/dzuhur/ashar/maghrib/isya\n.sholatcek\n.carasholat\n.kuisislam\n.xp\n.achievement\n.dk\n.setkota 1210\n.setngaji\n.clear\n.exit\n.reset\n")

def get_jadwal(kota_id="1210"):
    try:
        url = f"https://api.myquran.com/v1/sholat/jadwal/{kota_id}/{datetime.now().strftime('%Y/%m/%d')}"
        r = requests.get(url, timeout=10).json()
        return r['data']['jadwal'], r['data']['lokasi']
    except:
        return None, None

def get_daftar_kota():
    try:
        r = requests.get("https://api.myquran.com/v1/sholat/kota/semua", timeout=10).json()
        return r['data']
    except:
        return [{"id":"1210","lokasi":"BANDAR LAMPUNG"},{"id":"1301","lokasi":"JAKARTA"},{"id":"1211","lokasi":"LAMPUNG SELATAN"}]

def get_rank(xp):
    if xp < 50: return "Pencari Hidayah"
    elif xp < 150: return "Pejuang Subuh"
    elif xp < 300: return "Penjaga Sholat"
    elif xp < 500: return "Ahlul Quran"
    else: return "Wali Santri"

def get_khotbah_pendek_api():
    try:
        r = requests.get("https://khotbah-api.vercel.app/api/khotbah/random", timeout=10)
        if r.status_code == 200:
            d = r.json()
            return {"judul": d.get('judul','Khotbah Pendek API'), "isi": d.get('isi','')[:1500], "kuis_q": "Apa tema khotbah?", "kuis_a": "islam"}
    except: pass
    return {"judul":"Khotbah Pendek: Jaga Sholat","isi":"Peliharalah sholat. QS Al-Baqarah 238. Sholat tiang agama, jangan tinggalkan.","kuis_q":"Sholat tiang apa?","kuis_a":"agama"}

def get_khotbah_panjang_api():
    isi_api = ""
    judul_api = "Khotbah Jumat"
    try:
        r = requests.get("https://api.myquran.com/v1/khotbah/jumat", timeout=10).json()
        if r.get('data'):
            judul_api = r['data'].get('judul', judul_api)
            isi_api = r['data'].get('isi', '')
    except: pass
    if not isi_api:
        try:
            r = requests.get("https://raw.githubusercontent.com/renomureza/islamic-api/main/data/khotbah.json", timeout=10).json()
            pil = random.choice(r)
            judul_api = pil['judul']
            isi_api = pil['isi']
        except:
            isi_api = "Wahai jamaah, tingkatkan takwa kepada Allah. Jauhi judi online dan pinjol."

    full_isi = f"إِنَّ الْحَمْدَ لِلَّهِ نَحْمَدُهُ\n\nJamaah Jumat rahimakumullah,\n\nJudul Khotbah (API): {judul_api}\n\nMATERI DARI API:\n{isi_api}\n\nPENJELASAN LENGKAP:\n1. Takwa\nAllah berfirman QS Ali Imran 102: Hai orang beriman, bertakwalah sebenar-benar takwa.\n\n2. Isi Utama\n{isi_api}\n\nKita harus amalkan dalam hidup sehari-hari. Jika tentang sholat, jagalah. Jika tentang maksiat, jauhilah.\n\n3. Penutup\nSemoga Allah jaga keluarga kita dari judi online dan maksiat. Aamiin ya Rabbal Alamin.\n"
    return {"judul": judul_api, "isi": full_isi, "kuis_q": "Apa judul khotbah API tadi?", "kuis_a": judul_api.split()[0].lower()}

def get_cara_sholat(jenis="semua"):
    p = {
        "subuh": "=== SHOLAT SUBUH 2 RAKAAT ===\nNiat: Ushalli fardha subhi rak'ataini...\n1. Takbir Allahu Akbar\n2. Al-Fatihah + surat pendek\n3. Ruku (Subhana rabbiyal adzhimi 3x)\n4. I'tidal\n5. Sujud (Subhana rabbiyal a'la 3x)\n6. Duduk diantara 2 sujud\n7. Sujud lagi\n8. Rakaat 2 ulangi\n9. Tahiyat akhir + Qunut + Salam\n",
        "dzuhur": "=== DZUHUR 4 RAKAAT ===\nNiat: Ushalli fardha dzuhri arba'a raka'atin...\n",
        "ashar": "=== ASHAR 4 RAKAAT ===\nNiat: Ushalli fardha ashri arba'a raka'atin...\n",
        "maghrib": "=== MAGHRIB 3 RAKAAT ===\nNiat: Ushalli fardha maghribi tsalatsa raka'atin...\n",
        "isya": "=== ISYA 4 RAKAAT ===\nNiat: Ushalli fardha isya'i arba'a raka'atin...\n",
        "wudhu": "=== CARA WUDHU ===\n1. Niat\n2. Tangan 3x\n3. Kumur 3x\n4. Hidung 3x\n5. Muka 3x\n6. Tangan sampai siku 3x\n7. Usap kepala\n8. Telinga\n9. Kaki 3x\n"
    }
    if jenis.lower() in p:
        return p[jenis.lower()]
    else:
        return "Pilihan:\n.carasholat subuh\n.carasholat dzuhur\n.carasholat ashar\n.carasholat maghrib\n.carasholat isya\n.carasholat wudhu\n"

def catat_sholat(jenis, data):
    hari_ini = datetime.now().strftime("%Y-%m-%d")
    if "sholat_log" not in data:
        data["sholat_log"] = {}
    if hari_ini not in data["sholat_log"]:
        data["sholat_log"][hari_ini] = []
    if jenis in data["sholat_log"][hari_ini]:
        return False, f"Lu udah catat sholat {jenis} hari ini bre, jangan 2x 😅\n"
    data["sholat_log"][hari_ini].append(jenis)
    data["xp"] += 25
    bonus = ""
    if len(data["sholat_log"][hari_ini]) == 5:
        data["xp"] += 50
        bonus = "\n🔥 MASYAALLAH 5 WAKTU LENGKAP HARI INI! +50 BONUS XP!\n"
    else:
        bonus = f"\nProgress hari ini: {len(data['sholat_log'][hari_ini])}/5 waktu\n"
    save_json(DATA_FILE, data)
    return True, f"Barakallah sholat {jenis} dicatat! +25 XP\n{bonus}Total XP: {data['xp']}\nRank: {get_rank(data['xp'])}\n"

def tanya_awal():
    banner()
    config = load_json(CONFIG_FILE, {})
    if "is_mengaji" not in config:
        print("=== SETUP AWAL ===\nKetik.dk untuk daftar kota\n")
        jwb = input("Apakah anda masih kategori mengaji n/Y : ").lower().strip()
        is_mengaji = True if jwb == 'y' else False
        kota_input = input("Masukan ID kota contoh 1210 : ") or "1210"
        if kota_input.lower() == ".dk":
            for k in get_daftar_kota()[:60]:
                print(f"{k['lokasi'].lower()} : {k['id']}")
            kota_input = input("Masukan ID kota : ") or "1210"
        config = {"is_mengaji": is_mengaji, "kota_id": kota_input, "kota": kota_input}
        save_json(CONFIG_FILE, config)
        save_json(DATA_FILE, {"xp":0, "waktu_ngaji":"", "last_sholat":"", "kuis_benar":0, "sholat_log":{}})
        print(f"\nDisimpan! Mode {'NGAJI' if is_mengaji else 'NON-NGAJI'}\n")
        time.sleep(2)
        banner()
    return config

def main():
    config = tanya_awal()
    data = load_json(DATA_FILE, {"xp":0, "waktu_ngaji":"", "last_sholat":"", "kuis_benar":0, "sholat_log":{}})
    print("Bot Jalan!\nPerintah:\n.khotbah\n.jadwalsholat\n.sholat subuh\n.sholatcek\n.carasholat\n.kuisislam\n.xp\n.achievement\n.dk\n.setkota\n.setngaji\n.clear\n.exit\n")
    while True:
        try:
            cmd = input("\n> ").strip()
            low = cmd.lower()
            if low in ["clear",".clear"]:
                banner()
                continue
            if low == ".dk":
                print("\nDaftar Kota:\n")
                for k in get_daftar_kota():
                    print(f"{k['lokasi'].lower()} : {k['id']}")
                auto_clear()
                continue
            if low.startswith(".setkota"):
                try:
                    id_baru = cmd.split(" ")[1]
                    config["kota_id"] = id_baru
                    save_json(CONFIG_FILE, config)
                    print(f"\nKota diganti ke {id_baru}\n")
                except:
                    print("\nFormat:.setkota 1210\n")
                auto_clear()
                continue
            if low == ".setngaji":
                print(f"\nMode sekarang: {'NGAJI' if config.get('is_mengaji') else 'NON-NGAJI'}\n")
                jwb = input("Ganti mode? n/Y : ").lower().strip()
                if jwb == 'y':
                    config["is_mengaji"] = not config.get("is_mengaji", True)
                    save_json(CONFIG_FILE, config)
                    print(f"\nMode diganti jadi {'NGAJI' if config['is_mengaji'] else 'NON-NGAJI'}\n")
                auto_clear()
                continue
            if low in ["exit",".exit"]:
                print("\nKeluar Barakallah\n")
                sys.exit(0)
            if low == ".reset":
                for f in [CONFIG_FILE, DATA_FILE]:
                    if os.path.exists(f): os.remove(f)
                print("\nReset! Jalankan ulang\n")
                break
            elif low == ".jadwalsholat":
                timings, lokasi = get_jadwal(str(config.get("kota_id","1210")))
                if timings:
                    print(f"\nJadwal {lokasi}\n")
                    for k,v in timings.items():
                        print(f"{k}: {v}")
                else:
                    print("\nGagal cek,.dk dulu\n")
                auto_clear()
                continue
            elif low.startswith(".sholat") and not low.startswith(".sholatcek"):
                parts = cmd.split(" ")
                if len(parts) < 2:
                    print("\nCara hidupin sholat:\n.sholat subuh\n.sholat dzuhur\n.sholat ashar\n.sholat maghrib\n.sholat isya\n\nContoh abis sholat subuh ketik.sholat subuh\n+25 XP, 5 waktu lengkap bonus +50\nCek.sholatcek\n")
                else:
                    jenis = parts[1].lower()
                    if jenis not in ["subuh","dzuhur","ashar","maghrib","isya"]:
                        print("\nJenis salah! Pilih subuh/dzuhur/ashar/maghrib/isya\n")
                    else:
                        ok, msg = catat_sholat(jenis, data)
                        print(f"\n{msg}\n")
                        data = load_json(DATA_FILE, data)
                auto_clear()
                continue
            elif low == ".sholatcek":
                hari_ini = datetime.now().strftime("%Y-%m-%d")
                log = data.get("sholat_log", {}).get(hari_ini, [])
                print(f"\n=== SHOLAT HARI INI {hari_ini} ===\n")
                for s in ["subuh","dzuhur","ashar","maghrib","isya"]:
                    status = "✅" if s in log else "❌"
                    print(f"{status} {s}\n")
                print(f"Progress {len(log)}/5\n")
                if len(log) == 5:
                    print("MASYAALLAH LENGKAP!\n")
                auto_clear()
                continue
            elif low.startswith(".carasholat"):
                parts = cmd.split(" ")
                jenis = parts[1] if len(parts) > 1 else "semua"
                print(f"\n{get_cara_sholat(jenis)}\n")
                if config.get("is_mengaji"):
                    data["xp"] += 5
                    save_json(DATA_FILE, data)
                    print(f"+5 XP belajar sholat Total {data['xp']}\n")
                print("================================\nKetik.selesaibaca setelah selesai membaca khotbah\n================================\n")
                while True:
                    s = input().lower().strip()
                    if s == ".selesaibaca":
                        break
                banner()
                continue
            elif low == ".khotbah":
                print("\nPilihan:\n1. Khotbah pendek (API) +10 xp\n2. Khotbah panjang FULL API +20 xp\n3. Khotbah panjang API + kuis +50 xp\n")
                pil = input("Pilih 1/2/3 : ").strip()
                if pil == "1":
                    print("\nMengambil khotbah pendek dari API...\n")
                    kh = get_khotbah_pendek_api()
                    print(f"\n{kh['judul']}\n\n{kh['isi']}\n")
                    if config.get("is_mengaji"):
                        data["xp"] += 10
                        save_json(DATA_FILE, data)
                        print(f"+10 XP Total {data['xp']} Rank {get_rank(data['xp'])}\n")
                    auto_clear()
                elif pil in ["2","3"]:
                    print("\nMengambil khotbah panjang dari API...\n")
                    kh = get_khotbah_panjang_api()
                    print(f"\n{kh['judul']}\n\n{kh['isi']}\n")
                    print("================================\nKetik.selesaibaca setelah selesai membaca khotbah\n================================\n")
                    while True:
                        s = input().lower().strip()
                        if s == ".selesaibaca":
                            break
                    if pil == "2":
                        if config.get("is_mengaji"):
                            data["xp"] += 20
                            save_json(DATA_FILE, data)
                            print(f"\nBarakallah +20 XP Total {data['xp']} Rank {get_rank(data['xp'])}\n")
                    else:
                        print(f"\n--- KUIS API ---\n{kh['kuis_q']}\n")
                        jawab = input("Jawaban lu : ").lower().strip()
                        if kh['kuis_a'].lower() in jawab.lower():
                            print("\nMasyaAllah benar\n")
                            if config.get("is_mengaji"):
                                data["xp"] += 50
                                save_json(DATA_FILE, data)
                        else:
                            print(f"\nBelum tepat, jawaban {kh['kuis_a']} tetap +20 XP\n")
                            if config.get("is_mengaji"):
                                data["xp"] += 20
                                save_json(DATA_FILE, data)
                    banner()
                continue
            elif low == ".kuisislam":
                soal = [{"q":"Rukun Islam ada berapa?","a":"5"},{"q":"Puasa wajib bulan apa?","a":"ramadhan"}]
                s = random.choice(soal)
                print(f"\n[KUIS ISLAM] {s['q']}\n")
                jwb = input("Jawaban: ").lower().strip()
                if s['a'] in jwb:
                    data["xp"] += 15
                    data["kuis_benar"] = data.get("kuis_benar",0)+1
                    save_json(DATA_FILE, data)
                    print(f"\nBener +15 XP Total {data['xp']}\n")
                else:
                    print(f"\nSalah, jawaban {s['a']}\n")
                auto_clear()
                continue
            elif low == ".xp":
                print(f"\nXP {data['xp']} Rank {get_rank(data['xp'])}\n")
                auto_clear()
                continue
            elif low == ".achievement":
                print(f"\n=== ACHIEVEMENT ===\nRank: {get_rank(data['xp'])}\nXP: {data['xp']}\nKuis benar: {data.get('kuis_benar',0)}\n")
                hari_ini = datetime.now().strftime("%Y-%m-%d")
                log = data.get("sholat_log", {}).get(hari_ini, [])
                print(f"Sholat hari ini {len(log)}/5\n")
                auto_clear()
                continue
        except KeyboardInterrupt:
            print("\nKetik.clear atau.exit\n")
            continue
        except Exception as e:
            print(f"\nError {e}\n")
            continue

if __name__ == "__main__":
    main()