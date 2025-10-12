import requests
from concurrent.futures import ThreadPoolExecutor
import os
import sys

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def check_internet_connection():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def check_proxy(proxy, save_file):
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }
    
    try:
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=5)
        if response.status_code in [200, 202, 500, 502, 503, 504]:
            detect_location(proxy, save_file)
            return True
    except requests.exceptions.RequestException:
        pass

    print(f" \033[1;37m[\033[1;31m★\033[1;37m] \033[1;37m{proxy} \033[1;31m× \033[1;31mDead")
    return False

def detect_location(proxy, save_file):
    ip_address = proxy.split(':')[0]
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success":
                print(f"\033[1;37m{proxy} \033[1;31m√ \033[1;37m{data['country']}/{data['city']} \033[1;31m√ \033[1;32mLive")
                with open(save_file, 'a') as f:
                    f.write(proxy + '\n')
            else:
                print(f"\033[1;37m[\033[1;31m+\033[1;37m] \033[1;31mFailed to detect location for proxy.")
    except requests.exceptions.RequestException:
        print(f"\033[1;37m[\033[1;31m+\033[1;37m] \033[1;31mFailed to detect location for proxy.")

def main():
    clear()
    if not check_internet_connection():
        print("\n\033[1;31mNo internet connection!")
        sys.exit(1)
    
    proxy_file = "Proxies.txt"
    if not os.path.exists(proxy_file):
        proxy_file = input("\033[1;32mEnter Proxy File: \033[1;33m")
    
    try:
        with open(proxy_file, 'r') as file:
            proxy_list = file.read().splitlines()
    except FileNotFoundError:
        print("\033[1;31mProxy file not found!")
        sys.exit(1)
    
    proxy_count = len(proxy_list)
    save_file = "working_proxies.txt"
    print(f" \033[1;31mTotal: \033[1;37m{proxy_count} \033[1;31mProxies in File")

    num_workers = 200
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        executor.map(lambda p: check_proxy(p, save_file), proxy_list)

    live_count = len(open(save_file).readlines()) if os.path.exists(save_file) else 0
    print(f" \033[1;31mProxy Checking Complete - Saved to \033[1;37m{save_file} \033[1;31mwith \033[1;37m{live_count} \033[1;31mLive Proxies")
    input(" Press Enter to exit")
    sys.exit()

if __name__ == "__main__":
    main()
