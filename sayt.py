from flask import Flask, render_template, render_template_string, request, redirect

app = Flask(__name__)

# 1. Bosh sahifa
@app.route('/')
def home():
    return """
    <html>
        <head><title>ArcTrd Sec Lab</title></head>
        <body style='background:#111; color:#fff; text-align:center; padding:50px;'>
            <h1>ArcTrd CyberSecurity Local Lab</h1>
            <p>Simulyatsiya sahifalarini tekshirib ko'ring:</p>
            <a href='/fake-login' style='color:yellow;'>1. Fishing Sahifa Simulyatsiyasi</a><br><br>
            <a href='/malicious-download' style='color:red;'>2. Zararli Fayl Yuklash Simulyatsiyasi</a><br><br>
            <a href='/hidden-redirect' style='color:orange;'>3. Yashirin Yo'naltirish (Redirection)</a>
        </body>
    </html>
    """

# 2. FISHING SAHIFASI SIMULYATSIYASI
# Bu sahifada foydalanuvchi ma'lumotlarini o'g'irlaydigan soxta forma bor
@app.route('/fake-login', methods=['GET', 'POST'])
def fake_login():
    if request.method == 'POST':
        # Haqiqiy hakerlikda bu ma'lumotlar bazaga yoki telegram botga ketadi
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"\n[!!! LOGGED DATA !!!] Username: {username} | Password: {password}\n")
        return "Tizimda xatolik! Qaytadan urunib ko'ring."
        
    return """
    <body style='background:#f4f4f4; text-align:center; font-family:sans-serif;'>
        <div style='width:300px; margin:100px auto; padding:20px; border:1px solid #ccc; background:#fff;'>
            <h2>Blockchain Wallet Login</h2>
            <p style='color:red; font-size:12px;'>Xavfsizlikni yangilash uchun hamyon kalitini kiriting!</p>
            <form method='POST'>
                <input type='text' name='username' placeholder='Email yoki Hamyon manzili' required><br><br>
                <input type='password' name='password' placeholder='Parol / Private Key' required><br><br>
                <button type='submit' style='background:blue; color:white; width:100%; border:none; padding:10px;'>Verify Account</button>
            </form>
        </div>
    </body>
    """

# 3. ZARARLI FAYL YUKLASH SIMULYATSIYASI
# Bu sahifa rasm deb aldab, orqada shubhali ".exe" yoki ".bat" faylni yuklashni taklif qiladi
@app.route('/malicious-download')
def malicious_download():
    return """
    <body style='background:#111; color:#fff; text-align:center; padding:50px;'>
        <h1>Yutuqni qo'lga kiriting!</h1>
        <p>Quyidagi tugmani bosing va sovg'ani yuklab oling:</p>
        <a href='/security-test-zone' download='free_bitcoin_miner.exe' style='background:green; color:white; padding:15px; text-decoration:none;'>Yuklab olish (.EXE)</a>
    </body>
    """

# 4. YASHIRIN YO'NALTIRISH (Drive-by Redirect)
# Saytga kirgan zahoti foydalanuvchini boshqa shubhali saytga otib yuboradi
@app.route('/hidden-redirect')
def hidden_redirect():
    # Saytga kirganda avtomatik eicar test fayliga yo'naltiradi
    return redirect("https://secure.eicar.org/eicar.com.txt")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)