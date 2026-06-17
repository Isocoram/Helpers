import requests
import os
from dotenv import load_dotenv
from datetime import datetime 

load_dotenv("/home/lee/Desktop/iptracker/.env")

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TIMEOUT = 10

class IPchecker:

    def __init__(self, logfile_path: str) -> None:
        self.path = logfile_path

    def get_current_ip(self) -> str | None:
        try:
            response: requests.Response = requests.get("https://api.ipify.org", timeout=TIMEOUT)
            return response.text
        except:
            return None

    def read_last_file_entry_ip(self) -> str | None:
        with open(self.path, "r") as file:
            total_lines = file.readlines()
            if not total_lines:
                return None
            last_line = total_lines[-1].strip()
            return total_lines[-1].split(" - ")[1] if " - " in last_line else None 
    
    def append_to_log_file(self, ip: str) -> None:
        current_time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        newline = "\n"
        with open(self.path, "a") as file:
            #   format needed otherwise split wont work and all ip checks will fail since ip will include newline etc
            file.write(f"{current_time} - {ip} - {newline}")

    def send_telegram_notification(self, text: str) -> None:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}"
        requests.get(url, timeout=TIMEOUT)
        
    def check(self) -> None:
        current_ip: str | None = self.get_current_ip()
        last_ip: str | None = self.read_last_file_entry_ip()
        if current_ip and current_ip != last_ip:
            self.append_to_log_file(current_ip)
            self.send_telegram_notification(str(current_ip))


if __name__ == "__main__":
    checker = IPchecker("/home/lee/Desktop/iptracker/ip_log_file.txt")
    #print(checker.read_last_file_entry_ip())
    #checker.append_to_log_file(checker.get_current_ip())
    #print(checker.read_last_file_entry_ip())
    checker.check()