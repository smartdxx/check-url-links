import json
import base64
import time
import requests
from colorama import Fore, Style, init

# Ranglarni ishga tushirish
init(autoreset=True)

# !!! BU YERGA O'ZINGIZNING VIRUSTOTAL API KALITINGIZNI YOZING !!!
API_KEY = "Your_VirusTotal_Api_Key_Paste_Here"

def advanced_local_analyze(url):
    """ Sayt tarkibini o'zi yuklab olib, ichidagi kodlarni tahlil qiluvchi funksiya """
    print(f"\n{Fore.BLUE}[*] Ichki chuqurlashtirilgan statik tahlil boshlandi...")
    try:
        # Sayt kodini yuklab olish
        response = requests.get(url, timeout=5)
        html_content = response.text.lower()
        
        # 1. Fishing indikatorlari
        phishing_words = ["private key", "wallet", "login", "password", "verify account", "update now"]
        found_phishing = [w for w in phishing_words if w in html_content]
        
        # 2. Zararli fayl indikatorlari
        malware_indicators = [".exe", ".bat", ".dmg", "miner", "free_bitcoin"]
        found_malware = [m for m in malware_indicators if m in html_content]
        
        # Xulosani chiqarish
        print(f"{Fore.CYAN}--- STATIK TAHLIL NATIJALARI ---")
        if found_phishing:
            print(f"{Fore.RED}[!] FISHING XAVFI: Sayt ichida maxfiy ma'lumotlarni so'rovchi elementlar bor: {found_phishing}")
        
        if found_malware:
            print(f"{Fore.RED}[!] MALWARE XAVFI: Sayt foydalanuvchiga shubhali dasturlarni yuklashni taklif qilmoqda: {found_malware}")
            
        if not found_phishing and not found_malware:
            print(f"{Fore.GREEN}[+] Mahalliy tahlil: Sahifa kodida shubhali kontent aniqlanmadi.")
        print(f"{Fore.CYAN}---------------------------------")
            
    except Exception as e:
        print(f"{Fore.RED}[!] Sayt tarkibini mustaqil o'qib bo'lmadi (Ehtimol local yoki ommaviy havola emas): {e}")


def check_url(url):
    """ VirusTotal API orqali global tekshirish funksiyasi """
    print(f"\n{Fore.BLUE}[*] Havola tekshirilmoqda: {url}")
    
    # Avval o'zimiz yaratgan ichki statik tahlilni ishga tushiramiz (Siz so'ragan antivirus qismi)
    advanced_local_analyze(url)
    
    # So'ngra VirusTotal global bazasidan qidiramiz
    url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
    headers = {
        "accept": "application/json",
        "x-apikey": API_KEY
    }
    
    scan_url = f"https://www.virustotal.com/api/v3/urls"
    data = {"url": url}
    
    try:
        response = requests.post(scan_url, data=data, headers=headers)
        if response.status_code == 401:
            print(f"{Fore.RED}[!] Xato: API kalit noto'g'ri yoki kiritilmagan!")
            return
        
        print(f"\n{Fore.YELLOW}[*] VirusTotal global antiviruslar bazasidan ma'lumotlar olinmoqda...")
        time.sleep(1) 
        
        report_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
        report_response = requests.get(report_url, headers=headers)
        
        if report_response.status_code == 200:
            result = report_response.json()
            stats = result['data']['attributes']['last_analysis_stats']
            results = result['data']['attributes']['last_analysis_results']
            
            print(f"\n{Fore.CYAN}=== GLOBAL BAZA NATIJALARI ===")
            print(f"{Fore.GREEN}Toza (Harmless): {stats.get('harmless', 0)}")
            print(f"{Fore.WHITE}Shubhali (Suspicious): {stats.get('suspicious', 0)}")
            print(f"{Fore.RED}Zararli (Malicious): {stats.get('malicious', 0)}")
            print(f"{Fore.YELLOW}Fishing: {stats.get('phishing', 0)}")
            print(f"{Fore.CYAN}==============================\n")
            
            if stats.get('malicious', 0) > 0 or stats.get('suspicious', 0) > 0:
                print(f"{Fore.RED}[!] Diqqat! Global motorlar xavf aniqladi:")
                for engine, details in results.items():
                    if details['category'] in ['malicious', 'suspicious']:
                        print(f"  - {Fore.YELLOW}{engine}{Fore.RESET}: {details['result']} ({details['category']})")
            else:
                print(f"{Fore.GREEN}[+] Global baza: Havola xavfsiz deb topildi.")
                
        else:
            print(f"{Fore.RED}[!] Global hisobotni olib bo'lmadi. Kod: {report_response.status_code}")
            
    except Exception as e:
        print(f"{Fore.RED}[!] Global tekshiruvda xatolik: {str(e)}")


if __name__ == "__main__":
    print(f"{Fore.MAGENTA}=== smartdxx URL Scanner (Hybrid Mode) ===")
    if API_KEY == "YOUR_VIRUSTOTAL_API_KEY_HERE":
        print(f"{Fore.RED}[!] Iltimos, kod ichiga shaxsiy VirusTotal API kalitingizni kiriting!")
    else:
        while True:
            target_url = input(f"\n{Fore.GREEN}Tekshirish uchun URL kiriting (chiqish uchun 'q'): {Fore.RESET}").strip()
            if target_url.lower() == 'q':
                print(f"{Fore.MAGENTA}Dastur yakunlandi.")
                break
            if not target_url.startswith(("http://", "https://")):
                target_url = "https://" + target_url
            check_url(target_url)
