import requests
import time
from datetime import datetime, timedelta
from colorama import init, Fore

# Inisialisasi Colorama
init(autoreset=True)

# Informasi Channel dan Nama Bot
script_name = "GetGems"
telegram_channel = "https://t.me/ugdairdrop"

# Membaca account_id dari file teks
def get_account_id():
    with open('id.txt', 'r') as file:
        return file.read().strip()

# Konfigurasi akun
account_id = get_account_id()

# Waktu terakhir klaim
last_claim_time = None

# Fungsi untuk menampilkan informasi header
def print_header():
    print(f"{Fore.BLUE}=============================")
    print(f"{Fore.YELLOW} {script_name} Auto Claim")
    print(f"{Fore.YELLOW}  Channel: {telegram_channel}")
    print(f"{Fore.BLUE}=============================")


# Fungsi untuk menampilkan menu pilihan awal
def print_menu():
    print(f"{Fore.YELLOW}Silahkan pilih tindakan yang ingin dilakukan:")
    print(f"{Fore.GREEN}1. Auto claim (setiap 6 jam)")
    print(f"{Fore.GREEN}2. Auto complete tasks\n")

# Fungsi untuk memilih aksi awal
def choose_action():
    print_menu()
    choice = input(f"{Fore.YELLOW}Masukkan pilihan (1/2): ")
    if choice == '1':
        auto_claim()
    elif choice == '2':
        auto_complete_tasks()
    else:
        print(f"{Fore.RED}Pilihan tidak valid. Silahkan pilih 1 atau 2.")

# Fungsi untuk menampilkan informasi klaim berikutnya
def display_next_claim_time():
    global last_claim_time
    if last_claim_time is not None:
        next_claim_time = last_claim_time + timedelta(hours=6)
        time_left = next_claim_time - datetime.now()
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"{Fore.YELLOW}Next claim in: {hours:02}:{minutes:02}:{seconds:02}")
    else:
        print(f"{Fore.YELLOW}Next claim time is not yet initialized.")

# Fungsi untuk klaim token
def claim_token():
    global last_claim_time
    url = f"https://dolphin-app-2-qkmuv.ondigitalocean.app/api/account/{account_id}/claim"
    response = requests.put(url)
    if response.status_code == 200:
        last_claim_time = datetime.now()
        print(f"{Fore.GREEN}Successfully claimed token")
        display_next_claim_time()
    elif response.status_code == 400:
        print(f"{Fore.RED}Failed to claim token: Token already claimed")
    else:
        print(f"{Fore.RED}Failed to claim token: {response.status_code} - {response.text}")

# Fungsi untuk mengecek dan menyelesaikan tugas
def check_and_complete_tasks():
    url = f"https://dolphin-app-2-qkmuv.ondigitalocean.app/api/tasks/{account_id}"
    response = requests.get(url)
    if response.status_code == 200:
        tasks_data = response.json()
        if "taskScopes" in tasks_data:
            for scope in tasks_data["taskScopes"]:
                for task in scope.get("tasks", []):
                    print_task(task)
                    if not task.get("isCompleted", True):
                        complete_task(task["id"])
        else:
            print(f"{Fore.RED}Unexpected tasks format: {tasks_data}")
    else:
        print(f"{Fore.RED}Failed to fetch tasks: {response.status_code} - {response.text}")

# Fungsi untuk menampilkan tugas dengan format yang menarik
def print_task(task):
    status = "Selesai" if task['isCompleted'] else "Belum"
    print(f"""
    {Fore.MAGENTA}----------------------------
    {Fore.YELLOW}ID : {task['id']} | {task['locales'].get('en', 'No description')} | {status}
    {Fore.MAGENTA}----------------------------
    """)

# Fungsi untuk menyelesaikan tugas tertentu
def complete_task(task_id):
    url = f"https://dolphin-app-2-qkmuv.ondigitalocean.app/api/tasks/{account_id}/complete/{task_id}"
    response = requests.put(url)
    if response.status_code == 200:
        print(f"{Fore.GREEN}Successfully completed task {task_id}")
    else:
        print(f"{Fore.RED}Failed to complete task {task_id}: {response.status_code} - {response.text}")

# Fungsi untuk auto claim token (setiap 6 jam sekali)
def auto_claim():
    global last_claim_time
    while True:
        if last_claim_time is None or (datetime.now() - last_claim_time) >= timedelta(hours=6):
            claim_token()
            time.sleep(1)  # Tunggu 1 detik setelah klaim sebelum memeriksa lagi
        else:
            print(f"{Fore.YELLOW}Token telah di-claim dalam 6 jam terakhir. Tunggu hingga waktunya.")
            time.sleep(60)  # Tunggu 1 menit sebelum memeriksa lagi

# Fungsi untuk auto complete tasks
def auto_complete_tasks():
    check_and_complete_tasks()

# Fungsi untuk mengecek data pengguna
def check_user_data():
    url = f"https://dolphin-app-2-qkmuv.ondigitalocean.app/api/account/{account_id}"
    response = requests.get(url)
    if response.status_code == 200:
        user_data = response.json()
        print_user_data(user_data)
    else:
        print(f"{Fore.RED}Failed to fetch user data: {response.status_code} - {response.text}")

# Fungsi untuk menampilkan data pengguna dengan format yang menarik
def print_user_data(user_data):
    print(f"""
    {Fore.YELLOW}============== USER DATA ==============
    {Fore.GREEN}Name          : {user_data['firstName']}{user_data['lastName']}
    {Fore.GREEN}Username      : {user_data['username']}
    {Fore.GREEN}GG Points     : {user_data['ggPoints']}
    {Fore.YELLOW}========================================
    """)

# Fungsi utama untuk menjalankan semua tugas
def main():
    print_header()
    check_user_data()
    choose_action()

# Jalankan skrip utama
if __name__ == "__main__":
    main()
