import tkinter as tk
from tkinter import messagebox
import json
import os
import threading
import mail_downloader

CONFIG_FILE = "config.json"

def save_credentials(email, password):
    config = {"email": email, "password": password}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def load_credentials():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("UYARI: config.json dosyası bozuk veya boş. Varsayılan ayarlar kullanılacak.")
            return {"email": "", "password": ""}
    return {"email": "", "password": ""}


def start_process():
    email = email_entry.get()
    password = password_entry.get()

    if not email or not password:
        messagebox.showerror("Hata", "Lütfen e-posta ve şifre giriniz.")
        return

    try:
        # Doğrulama testi yapalım (bağlantı kontrolü)
        imap = mail_downloader.test_login(email, password)
        imap.logout()
    except Exception as e:
        messagebox.showerror("Bağlantı Hatası", f"Giriş başarısız: {str(e)}")
        return

    save_credentials(email, password)
    messagebox.showinfo("Başarılı", "Giriş başarılı. Sistem başlatıldı.")
    
    # Arka planda mail sistemini başlat
    def run_mail_loop():
        mail_downloader.start_with_credentials(email, password)

    threading.Thread(target=run_mail_loop, daemon=True).start()

# Arayüz oluştur
root = tk.Tk()
root.title("Mail İndirme ve Photoshop Otomasyonu")
root.geometry("400x200")

tk.Label(root, text="Mail Adresi").pack()
email_entry = tk.Entry(root, width=40)
email_entry.pack()

tk.Label(root, text="Şifre").pack()
password_entry = tk.Entry(root, show="*", width=40)
password_entry.pack()

tk.Button(root, text="Start", command=start_process).pack(pady=10)

# Kayıtlı bilgi varsa doldur
creds = load_credentials()
email_entry.insert(0, creds.get("email", ""))
password_entry.insert(0, creds.get("password", ""))

root.mainloop()
