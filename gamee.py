import requests
import json
import time
import subprocess
import threading
from urllib.parse import parse_qs

# URL dan headers
url = "https://api.service.gameeapp.com/"
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://dapp.fukduk.wtf',
    'priority': 'u=1, i',
    'referer': 'https://dapp.fukduk.wtf/',
    'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
}

# Fungsi untuk membaca initData dari file
def read_initdata_from_file(filename):
    initdata_list = []
    with open(filename, 'r') as file:
        for line in file:
            initdata_list.append(line.strip())
    return initdata_list

# Fungsi untuk mengambil nama dari init_data
def get_nama_from_init_data(auth_data):
    parsed_data = parse_qs(auth_data)
    user_data_json_str = parsed_data.get('user', [None])[0]

    if user_data_json_str:
        try:
            user_info = json.loads(user_data_json_str)

            first_name = user_info.get('first_name', '')
            last_name = user_info.get('last_name', '')
            username = user_info.get('username', '')

            # Combine first name, last name, and username in a specific format
            data = ""
            if first_name:
                data += first_name
            if last_name:
                data += " " + last_name
            if username:
                data += f" ({username})"

            return data.strip()
        except json.JSONDecodeError as e:
            return f"Invalid JSON format in user data: {e}"
    else:
        return "user data not found in the query parameters"

# Fungsi untuk melakukan claim
def claim(init_data):
    headers['--Webapp-init'] = init_data

    try:
        response = requests.post('https://rest.fukduk.wtf/api/farm/claim', headers=headers)
        return response
    except Exception as e:
        return f"An error occurred: {e}"

# Fungsi untuk menjalankan operasi untuk setiap initData
def process_initdata(init_data):
    try:
        print(init_data)
        nama = get_nama_from_init_data(init_data)
        print(f"Nama: {nama}")

        start_response = claim(init_data)
        print(start_response.text)
        if start_response.status_code == 200:
            print("Sukses Claim")
        else:
            print('Belum Waktunya Claim')
            time.sleep(3600)
        print("\n")
    except Exception as e:
        print(f"An error occurred: {e}")

# Fungsi utama
def main():
    initdata_file = "initdata.txt"
    while True:
        try:
            initdata_list = read_initdata_from_file(initdata_file)
            threads = []

            for init_data in initdata_list:
                thread = threading.Thread(target=process_initdata, args=(init_data.strip(),))
                threads.append(thread)
                thread.start()

            # Menunggu semua thread selesai
            for thread in threads:
                thread.join()

            # Delay sebelum membaca ulang file init
            time.sleep(3600)

        except KeyboardInterrupt:
            print("\nProcess interrupted by user. Exiting...")
            break

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        subprocess.run(["python3", "gamee.py"])
