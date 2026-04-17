from telethon.sync import TelegramClient
from telethon.errors import PhoneCodeInvalidError
from time import sleep
import os
import uuid

phone_numbers = '+998907296181'.split(",")  
api_id = 20715400
api_hash = '2d71f4a218d45286d6dc1bef7764487a'

BASE_SESSION_NAME = "base"

RETRY_DELAY = 5  

for number in phone_numbers:
    number = number.strip()
    if not number:
        continue

    attempt = 0
    print(f"\n--- {number} uchun urinuvlarni boshlash ---")

    while True:
        attempt += 1
        print(f"\nUrinuv #{attempt} — {number}")

        client = TelegramClient(BASE_SESSION_NAME, api_id, api_hash)
        try:
            try:
                client.connect()
            except Exception as e:
                print(f"[{number}] client.connect() xatosi: {e}")
                try:
                    client.disconnect()
                except:
                    pass
                sleep(RETRY_DELAY)
                continue

            try:
                client.send_code_request(number)
                print(f"[{number}] Code request sent.")
            except Exception as e:
                print(f"[{number}] Code request yuborishda xatolik: {e}")
                try:
                    client.disconnect()
                except:
                    pass

                try:
                    original = BASE_SESSION_NAME + ".session"
                    if os.path.exists(original):
                        rand_name = f"session_{uuid.uuid4().hex[:8]}.session"
                        os.rename(original, rand_name)
                        print(f"[{number}] {original} -> {rand_name}")
                        journal_orig = original + "-journal"
                        if os.path.exists(journal_orig):
                            journal_new = rand_name + "-journal"
                            os.rename(journal_orig, journal_new)
                            print(f"[{number}] {journal_orig} -> {journal_new}")
                except Exception as e2:
                    print(f"[{number}] Session rename xatosi: {e2}")

                sleep(RETRY_DELAY)
                continue

            try:
                client.sign_in(number, 12345)
                print(f"[{number}] Successfully signed in ✓")
                try:
                    client.disconnect()
                except:
                    pass

                try:
                    original = BASE_SESSION_NAME + ".session"
                    if os.path.exists(original):
                        rand_name = f"session_{uuid.uuid4().hex[:8]}.session"
                        os.rename(original, rand_name)
                        print(f"[{number}] {original} -> {rand_name}")
                        journal_orig = original + "-journal"
                        if os.path.exists(journal_orig):
                            journal_new = rand_name + "-journal"
                            os.rename(journal_orig, journal_new)
                            print(f"[{number}] {journal_orig} -> {journal_new}")
                except Exception as e2:
                    print(f"[{number}] Session rename xatosi (success): {e2}")

                print(f"[{number}] Kirish muvaffaqiyatli, keyingi amallarni bajarish uchun chiqyapmiz.")
                break  
            except PhoneCodeInvalidError:
                print(f"[{number}] Invalid code. Serverdan yuborilgan kod 12345 bilan mos emas.")
            except Exception as e:
                print(f"[{number}] sign_in xatosi: {e}")

        finally:
            try:
                client.disconnect()
            except:
                pass

            try:
                original = BASE_SESSION_NAME + ".session"
                if os.path.exists(original):
                    rand_name = f"session_{uuid.uuid4().hex[:8]}.session"
                    os.rename(original, rand_name)
                    print(f"[{number}] (post-attempt) {original} -> {rand_name}")
                    journal_orig = original + "-journal"
                    if os.path.exists(journal_orig):
                        journal_new = rand_name + "-journal"
                        os.rename(journal_orig, journal_new)
                        print(f"[{number}] (post-attempt) {journal_orig} -> {journal_new}")
                else:
                    print(f"[{number}] (post-attempt) {original} topilmadi.")
            except Exception as e:
                print(f"[{number}] (post-attempt) session rename xatosi: {e}")

        sleep(RETRY_DELAY)

    print(f"[{number}] Bajarildi — keyingi raqamga o'tiladi (agar mavjud bo'lsa).")

print("\nBarcha raqamlar qayta ishlandi.")
