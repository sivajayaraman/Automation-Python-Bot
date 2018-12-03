import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import requests
import tables
from bs4 import BeautifulSoup
import csv
update_id = None
def main():
    global update_id
    bot = telegram.Bot('token')
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None
    while True:
        try:
            for update in bot.get_updates(offset=update_id, timeout=25):
                update_id = update.update_id + 1
                if update.message.text.lower() == 'meaning':
                    update.message.reply_text("Enter Word to be searched:")
                    echo(bot)
                elif update.message.text.lower() == 'score':
                    URL = "http://www.cricbuzz.com/cricket-match/live-scores"
                    r = requests.get(URL)
                    soup = BeautifulSoup(r.text, 'html.parser')
                    p=1
                    url_store=[]
                    match_info=''
                    table=soup.find(class_='cb-bg-white cb-col-100 cb-col')
                    for row in table.find_all(class_='cb-col cb-col-100 cb-lv-main'):
                        url=row.a['href']
                        url_store.append(url)
                        name=row.a['title']
                        match_info+=str(p)+'.'+name+'\n'
                        p=p+1    
                    match_info=match_info+'\n'+"Enter the match number"
                    update.message.reply_text(match_info)
                    match(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            update_id += 1
def echo(bot):
    global update_id
    errorMsg='Meaning for the Word was not found.'+'\n'+'This may be due to one of the following reasons:'+'\n'+'  1)Misspelled Word'+'\n'+'  2)Compund Word'+'\n'+'Retry with a valid word!'
    url='http://www.dictionary.com/browse/'
    for update in bot.get_updates(offset=update_id, timeout=25):
        update_id = update.update_id + 1
        if update.message:
            word=update.message.text
            i=1
            meaning='Meaning of '+ word + ':' + '\n'
            url=url+word.lower()
            r=requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            table=soup.find(class_="css-zw8qdz e1hk9ate4")
            if not table:
                update.message.reply_text(errorMsg)
            else:
                for row in table.find_all(class_="css-2oywg7 e1q3nk1v3"):
                    meaning=meaning+str(i)+'.'+row.text+'\n'
                    i=i+1
                update.message.reply_text(meaning)
        break
def match(bot):
    global update_id
    URL = "http://www.cricbuzz.com/cricket-match/live-scores"
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    url_store=[]
    p=1
    table=soup.find(class_='cb-bg-white cb-col-100 cb-col')
    for row in table.find_all(class_='cb-col cb-col-100 cb-lv-main'):
        url=row.a['href']
        url_store.append(url)
        p=p+1
    print url_store                 
    for update in bot.get_updates(offset=update_id, timeout=25):
        update_id = update.update_id + 1
        if update.message:
            match_no=int(update.message.text)
            if match_no>0 and match_no<=p:
                req_url="http://www.cricbuzz.com"
                req_url=req_url+url_store[match_no-1]
                r = requests.get(req_url)
                soup = BeautifulSoup(r.text, 'html.parser')
                table=soup.find(class_='page')
                team1=0
                team2=0
                for row in table.find_all(class_='cb-col cb-col-100 cb-min-tm cb-text-gray'):
                    team1=1
                    update.message.reply_text(row.text)
                for row in table.find_all(class_='cb-col cb-col-100 cb-min-tm'):
                    team2=1
                    update.message.reply_text(row.text)
                for row in table.find_all(class_='cb-text-rain'):
                    bot.send_message(last_chat_id,row.text) 
                if team2==1 and team1==1:
                    for row in table.find_all(class_='cb-col cb-col-100 cb-min-stts cb-text-mom'):
                        update.message.reply_text(row.text)
                    for row in table.find_all(class_='cb-col cb-col-100 cb-min-stts cb-text-complete'):
                        update.message.reply_text(row.text)
                if team1==0 and team2==0:
                    for row in table.find_all(class_='cb-text-gray cb-font-16'):
                        team1=1
                        update.message.reply_text(row.text)
                    for row in table.find_all(class_='cb-font-20 text-bold'):
                        team2=1
                        update.message.reply_text(row.text)
                    for row in table.find_all(class_='cb-text-stump'):
                        update.message.reply_text(row.text)     
                if team1==0 and team2==0:
                    update.message.reply_text("Match not yet started! Stay tuned!")
            else:
                update.message.reply_text("Select a valid match number!")
            break                      
if __name__ == '__main__':
    main()
