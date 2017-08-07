# -*- coding: UTF-8 -*-
'''
tested on python 2.7
Author: Yichen Lu
Email: me@yichen.Lu
www.yichen.lu
'''
import gspread
import requests
import schedule
import time
import datetime
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup


def job():
    scope = ['https://spreadsheets.google.com/feeds']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'tvReminder-9c2fc76b87b6.json', scope)

    gc = gspread.authorize(credentials)

    worksheet = gc.open("TV Progress").sheet1

    dlurl_cells = worksheet.range('E2:E62')
    note_cells = worksheet.range('F2:F62')
    update_cells = worksheet.range('G2:G62')

    isUpdate = 0

    # len(dlurl_cells)
    for x in xrange(len(dlurl_cells)):
        dlurl = dlurl_cells[x].value
        if dlurl is not '':
            resurl = dlurl.replace('/resource/list/', '/gresource/')
            # print(resurl)

            try:
                # visit zimuzu.com
                r = requests.get(resurl)
                soup = BeautifulSoup(r.text, "html5lib")

                # process html
                note = soup.select(".resource-tit > p")
                notestr = note[0].string
                # print notestr
                replaceRawStr = unicode('說明：', 'utf-8')
                newNoteStr = notestr.replace(replaceRawStr, '')
                # print(newNoteStr)

                if not note_cells[x].value == newNoteStr:
                    isUpdate = 1
                    note_cells[x].value = newNoteStr
                    now = datetime.datetime.now()
                    update_cells[x].value = now.strftime("%Y-%m-%d")

            except Exception as e:
                if str(e) == "list index out of range":
                    print(e)
                    isUpdate = 1
                    note_cells[x].value = "Download link may be broken"
                    update_cells[x].value = "Error"
                continue

    # Update in batch
    if isUpdate == 1:
        worksheet.update_cells(note_cells)
        worksheet.update_cells(update_cells)

if __name__ == '__main__':
    job()
    # schedule job
    schedule.every(3).hours.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
