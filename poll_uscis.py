from pyquery import PyQuery as pq
import requests
import os
import sys
import os.path
import re

import time

MAC = 0

STATUS_OK = 0
STATUS_ERROR = -1
FILENAME_LASTSTATUS = os.path.join(sys.path[0], "LAST_STATUS_{0}.txt")

# ----------------- SETTINGS -------------------

def poll_optstatus(casenumber):
    """
    poll USCIS case status given receipt number (casenumber)
    Args:
        param1: casenumber the case receipt number

    Returns:
        a tuple (status, details) containing status and detailed info
    Raise:
        error:
    """
    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language':
        'en-US, en; q=0.8, zh-Hans-CN; q=0.5, zh-Hans; q=0.3',
        'Cache-Control': 'no-cache',
        'Connection': 'Keep-Alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'egov.uscis.gov',
        'Referer': 'https://egov.uscis.gov/casestatus/mycasestatus.do',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
    }
    url = "https://egov.uscis.gov/casestatus/mycasestatus.do"
    data = {"appReceiptNum": casenumber, 'caseStatusSearchBtn': 'CHECK+STATUS'}

    res = requests.post(url, data=data, headers=headers)
    doc = pq(res.text)
    status = doc('h1').text()
    code = STATUS_OK if status else STATUS_ERROR
    details = doc('.text-center p').text()
    return (code, status, details)

def main():
    
    while True:
        print("Starting the loop")
        casenumber = ""
        code, status, detail = poll_optstatus(casenumber)
        if code == STATUS_ERROR:
            print("The case number %s is invalid." % casenumber)
            return
        print(f'code: {code}')
        print(f'status: {status}')
        print(f'detail: {detail}')
        

        file1 = open("status.txt","r")
        line = file1.readline()
        print(f'line: {line}')
        file1.close()

        if status not in line:
            print(f'Not same')
            file2 = open("status.txt","w")
            file2.write(status)
            file2.close()

            if MAX:
                cmd = "osascript sendIMsg.scpt -{0} -{1}".format(YOUR_NUMBER_HERE,status)
                os.system(cmd)

        else:
            print(f'Same status')

        print(f"Waiting for next call in: ",end="")
        for i in range(0,5):
            print(f'{5-i} ',end="")
            time.sleep(5)

        print("")



if __name__ == '__main__':
    main()
