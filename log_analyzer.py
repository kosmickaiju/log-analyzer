from tkinter import Tk
from tkinter.filedialog import askopenfilename
import re
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
    permitted_ips = []
    print(f"Analyzing: {filename}")
    with open(filename, "r") as f:
        for line in f:
            match = re.search(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", line)
            if match:
                ip = match.group()
                if ip not in permitted_ips:
                    print("POTENTIAL SUSPICIOUS IP >", ip)
            '''Example: detect failed SSH login attempts
            if "Failed password" in line:
                print("FAILED LOGIN >", line.strip())'''
def main():
    log_file = pick_file()
    analyze_log(log_file)
if __name__ == "__main__":
    main()