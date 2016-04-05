# -*- coding: UTF-8 -*-
import gspread, requests, schedule, time
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup

def job():
    scope = ['https://spreadsheets.google.com/feeds']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('tvReminder-9c2fc76b87b6.json', scope)

    gc = gspread.authorize(credentials)

    worksheet = gc.open("TV Progress").sheet1

    dlurl_cells = worksheet.range('E2:E62')
    note_cells = worksheet.range('F2:F62')
    update_cells = worksheet.range('G2:G62')

    # len(dlurl_cells)
    for x in xrange(len(dlurl_cells)):
        dlurl = dlurl_cells[x].value
        if dlurl is not '':
            resurl = dlurl.replace('/list','')

            try:
                # visit zimuzu.com
                r = requests.get(resurl)
                soup = BeautifulSoup(r.text, "html5lib")
                # print(soup.prettify())
                # process html
                note = soup.select(".resource-note")
                notestr = note[0].string
                replaceRawStr = unicode('說明：','utf-8')
                newNoteStr = notestr.replace(replaceRawStr,'')

                if not note_cells[x].value == newNoteStr:
                    note_cells[x].value = newNoteStr
                    update_cells[x].value = '***'

            except Exception, e:
                print e
                continue

    # Update in batch
    worksheet.update_cells(note_cells)
    worksheet.update_cells(update_cells)

if __name__ == '__main__':
    # schedule.every(4).hours.do(job)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    job()