from tkinter import Tk
from tkinter.filedialog import askopenfilename
from datetime import datetime
import re
import json

def load_config():
    with open("config.json") as f:
        return json.load(f)

config = load_config()
permitted_ips = config["permitted_ips"]
permitted_login_hours = config["allowed_login_hours"]
start_hour = permitted_login_hours["start"]
end_hour = permitted_login_hours["end"]

def pick_file():
    Tk().withdraw()
    filename = askopenfilename(
        title="Select a log file",
        filetypes=[("Log files", "*.log *.txt"), ("All files", "*.*")]
    )
    if not filename:
        print("No file selected.")
        exit()
    return filename

def analyze_log(filename):
    print(f"Analyzing: {filename}")
    with open(filename, "r") as f:
        for line in f:
            ip_match = re.search(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", line)
            if ip_match:
                ip = ip_match.group()
                if ip not in permitted_ips:
                    print("POTENTIAL SUSPICIOUS IP >", ip)
            time_match = re.search(r"\d{4}-\d{2}-\d{2} (\d{2}):\d{2}:\d{2}", line)
            if not time_match:
                return
            hour = int(time_match.group(1))
            if hour < start_hour or hour >= end_hour:
                print("POTENTIAL UNUSUAL LOGIN TIME >", time_match.group(0))
            
def main():
    log_file = pick_file()
    analyze_log(log_file)

if __name__ == "__main__":
    main()