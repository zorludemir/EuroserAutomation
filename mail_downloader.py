import imaplib
import email
from email.header import decode_header
import os
import schedule
import time
import subprocess

USERNAME = "seninmailin@yandex.com"
PASSWORD = "dpmqvmqqcchxmwkr"
DOWNLOAD_FOLDER = "downloads"
SAVED_FOLDER = "saved"
PHOTOSHOP_PATH = r"C:\Program Files\Adobe\Adobe Photoshop 2024\Photoshop.exe"  # Kendi Photoshop yolunu yaz
SCRIPT_PATH = os.path.abspath("process_with_photoshop.jsx")

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(SAVED_FOLDER, exist_ok=True)

def test_login(email, password):
    imap = imaplib.IMAP4_SSL("imap.yandex.com")
    imap.login(email, password)
    return imap

def start_with_credentials(email, password):
    global USERNAME, PASSWORD
    USERNAME = email
    PASSWORD = password
    check_new_emails()
    schedule.every(5).minutes.do(check_new_emails)
    while True:
        schedule.run_pending()
        time.sleep(1)

def check_new_emails():
    print("Yeni mailler kontrol ediliyor...")

    imap = imaplib.IMAP4_SSL("imap.yandex.com")
    imap.login(USERNAME, PASSWORD)
    imap.select("INBOX")

    status, messages = imap.search(None, "UNSEEN")

    new_files_downloaded = False

    for num in messages[0].split():
        status, data = imap.fetch(num, "(RFC822)")
        email_message = email.message_from_bytes(data[0][1])

        for part in email_message.walk():
            if part.get_content_disposition() == "attachment":
                filename = part.get_filename()
                if filename:
                    filename = decode_header(filename)[0][0]
                    if isinstance(filename, bytes):
                        filename = filename.decode()

                    if filename.lower().endswith(".png"):
                        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
                        if not os.path.exists(filepath):  # Aynı dosya daha önce inmediyse
                            with open(filepath, "wb") as f:
                                f.write(part.get_payload(decode=True))
                            print(f"Downloaded: {filepath}")
                            new_files_downloaded = True

    imap.logout()

    # Yeni dosya indirildiyse Photoshop çalıştır
    if new_files_downloaded:
        print("Photoshop başlatılıyor ve dosyalar işleniyor...")
        subprocess.call([PHOTOSHOP_PATH, "-r", SCRIPT_PATH])
    else:
        print("Yeni dosya bulunamadı, Photoshop başlatılmadı.")

