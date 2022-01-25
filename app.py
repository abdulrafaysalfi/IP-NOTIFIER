from csv import DictReader, DictWriter
from dataclasses import fields
from datetime import datetime
import requests
from win10toast import ToastNotifier

URL = 'https://api.ipify.org?format=json'
DATE_FORMAT = "DATE(YYYY-MM-DD)"
fields = ["IP ADDRESS", DATE_FORMAT]

def get_ip_address():
    ip_address = requests.get(URL).json()
    return ip_address["ip"]

def write_ip_to_file(row):
    with open('./ip.csv','a',newline='') as file:
        writer = DictWriter(file,delimiter=',',lineterminator="\n",fieldnames=fields)
        if file.tell() == 0:
            writer.writeheader()
        if not check_in_file(row):
            writer.writerow(row)
            print("1 new IP Address Added to file.")
            return "1 new IP Address Added to file."
        else:
            print("IP Already Exist.")
            return "IP Already Exist."
def check_in_file(row):
    file = open("./ip.csv")
    reader = DictReader(file, fieldnames=fields)
    data = list(reader)[1:]
    if not any(d["IP ADDRESS"] == row["IP ADDRESS"] and d[DATE_FORMAT] == row[DATE_FORMAT]  for d in data):
        return False
    else:
        return True

if __name__=="__main__":
    row = {"IP ADDRESS":get_ip_address(),DATE_FORMAT:str(datetime.now())[:10]}
    toast = ToastNotifier()
    toast.show_toast("IP NOTIFIER",write_ip_to_file(row) + f"\nIP is {get_ip_address()}",duration=20)
