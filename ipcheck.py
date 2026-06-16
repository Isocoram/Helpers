import requests
import os
from dotenv import load_dotenv

load_dotenv("/home/lee/Desktop/iptracker/.env")

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

class IPchecker:

    def __init__(self, path: str) -> None:
        self.path = path
        self.ensure_directory()

    def ensure_directory(self) -> None:
        directory: str = os.path.dirname(self.path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def get_current_ip(self) -> str | None:
        try:
            respone: requests.Response = requests.get("https://api.ipify.org", timeout=10)
            return respone.text
        except:
            return None

    def get_last_ip(self) -> str | None:
        if not os.path.exists(self.path):
            return None
        file = open(self.path, "r")
        ip_data = file.read().strip()
        file.close()
        return ip_data

    def write_new_ip(self, ip: str):
        file = open(self.path, "w")
        file.write(ip)
        file.close()
    
    def check(self) -> None:
        current_ip: str | None = self.get_current_ip()
        last_ip: str | None = self.get_last_ip()

        if current_ip and current_ip != last_ip:
            self.write_new_ip(current_ip)
            print(f"IP updated to: {current_ip}")
            self.send_telegram_notification(str(current_ip))
    
    def send_telegram_notification(self, text: str) -> None:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}"
        requests.get(url)


if __name__ == "__main__":
    checker = IPchecker("/home/lee/Desktop/iptracker/last_ip.txt")
    checker.ensure_directory()
    checker.check()