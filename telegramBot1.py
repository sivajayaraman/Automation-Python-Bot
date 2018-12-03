from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler
import requests
import tables
from bs4 import BeautifulSoup
import csv
def start(bot, update):
	msg='Welcome to MyBot()'+'\n'+'1.Enter "score" to know Cricket Score.'+'\n'+'2.Enter "search" to Google Search.'+'\n'+'3.Enter "pnr" to know PNR Status.'+'\n'+'4.Enter "meaning" to know Synonyms of your word.'
	bot.send_message(chat_id=update.message.chat_id, text=msg)
def echo(bot,update):
	query=update.inline_query.query
	print query
	if choice.lower()=='score':
		print 1
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
		bot.send_message(chat_id=update.message.chat_id, text=match_info)
		last_update=choice
		current_update=choice
		while last_update==current_update:
			current_update= update.message.text		
		match_no = current_update
		print match_no
		if match_no>0 and match_no<=p:
			req_url="http://www.cricbuzz.com"
			req_url=req_url+url_store[match_no-1]
			print req_url
			r = requests.get(req_url)
			soup = BeautifulSoup(r.text, 'html.parser')
			table=soup.find(class_='page')
			team1=0
			team2=0
			for row in table.find_all(class_='cb-col cb-col-100 cb-min-tm cb-text-gray'):
				team1=1
				bot.send_message(chat_id=update.message.chat_id, text=row.text)
			for row in table.find_all(class_='cb-col cb-col-100 cb-min-tm'):
				team2=1
				bot.send_message(chat_id=update.message.chat_id, text=row.text)
			for row in table.find_all(class_='cb-text-rain'):
				bot.send_message(last_chat_id,row.text)	
			if team2==1 and team1==1:
				for row in table.find_all(class_='cb-col cb-col-100 cb-min-stts cb-text-mom'):
					bot.send_message(chat_id=update.message.chat_id, text=row.text)
				for row in table.find_all(class_='cb-col cb-col-100 cb-min-stts cb-text-complete'):
					bot.send_message(chat_id=update.message.chat_id, text=row.text)
			if team1==0 and team2==0:
				for row in table.find_all(class_='cb-text-gray cb-font-16'):
					team1=1
					bot.send_message(chat_id=update.message.chat_id, text=row.text)
				for row in table.find_all(class_='cb-font-20 text-bold'):
					team2=1
					bot.send_message(chat_id=update.message.chat_id, text=row.text)
				for row in table.find_all(class_='cb-text-stump'):
					bot.send_message(chat_id=update.message.chat_id, text=row.text)		
			if team1==0 and team2==0:
				bot.send_message(chat_id=update.message.chat_id, text="Match not yet started! Stay tuned!")
		else:
			bot.send_message(chat_id=update.message.chat_id, text="Select a valid match number!")
	elif choice.lower()=='pnr':
		last_update=choice
		current_update=choice
		url="https://www.railyatri.in/pnr-status/"
		bot.send_message(chat_id=update.message.chat_id, text="Enter PNR Number")
		while last_update==current_update:
			current_update=update.message.text
		bot.send_message(chat_id=update.message.chat_id, text="Fetching Status....")	
		pnr=current_update
		print current_update
		if len(pnr)!=10:
			bot.send_message(chat_id=update.message.chat_id, text="Retry with a valid PNR Number")
		else:	
			url=url+pnr
			r=requests.get(url)
			soup = BeautifulSoup(r.text, 'html.parser')
			table=soup.find(class_='pnr-search-result-info')
			if not table:
				bot.send_message(chat_id=update.message.chat_id, text="Retry with a valid PNR Number")
			else:
				train_booking='Booking Status:'
				train_name='Train Name:'
				train_from='From:'
				train_to='To:'
				train_date='Journey Duration:'
				train_class='Date:'
				t=1
				for row in table.find_all(class_='pnr-bold-txt'):
					name=row.text
					if t==1:
						train_name=train_name+name
					elif t==2:
						train_from=train_from+name
					elif t==3:
						train_to=train_to+name
					elif t==4 or t==5:
						train_date=train_date+name
					elif t==6:
						train_class=train_class+name
					t=t+1
				t=1	
				table=soup.find(id='status')	
				for row in table.find_all(class_='col-xs-4'):
					if t==1 or t==2:	
						t=t+1
						continue	
					if t%3!=0:
						train_booking=train_booking+row.text
						train_booking=train_booking.replace('\n', ' ').replace('\r', '')
						train_booking.rstrip
					t=t+1
				pnr_info=train_booking+'\n'+train_name+'\n'+train_from+'\n'+train_to+'\n'+train_date+'\n'+train_class
				bot.send_message(chat_id=update.message.chat_id, text=pnr_info)
	elif choice.lower()=='search':
		from googlesearch import search
		current_update=choice
		last_update=choice
		bot.send_message(chat_id=update.message.chat_id, text="Enter Your Query")
		while last_update==current_update:
			current_update = update.message.text
		bot.send_message(chat_id=update.message.chat_id, text="Searching in Google....")	
		query = current_update
		print query
		solution=''	
		for j in search(query, tld="co.in", num=5, stop=1, pause=2):
			bot.send_message(chat_id=update.message.chat_id, text=j)	
	elif choice.lower()=='meaning':
		i=1
		errorMsg='Meaning for the Word was not found.'+'\n'+'This may be due to one of the following reasons:'+'\n'+'  1)Misspelled Word'+'\n'+'  2)Compund Word'+'\n'+'Retry with a valid word!'
		url='http://www.dictionary.com/browse/'
		current_update=choice
		last_update=choice
		bot.send_message(chat_id=update.message.chat_id, text="Enter Word to be searched")
		while last_update==current_update:
			current_update = update.message.text	
		word=current_update
		meaning='Meaning of '+ word + ':' + '\n'
		url=url+word+'?s=t'
		r=requests.get(url)
		soup = BeautifulSoup(r.text, 'html.parser')
		table=soup.find(class_='css-zw8qdz e10vl5dg3')
		if not table:
			bot.send_message(chat_id=update.message.chat_id, text=errorMsg)
		else:
			for row in table.find_all(class_='css-4x41l7 e10vl5dg6'):
				meaning=meaning+str(i)+'.'+row.text+'\n'
				i=i+1
			bot.send_message(chat_id=update.message.chat_id, text=meaning)				
updater=Updater(token = '604449506:AAGdN1Sco2yj5hW7DM3dEmmP5IJKHP_y_lQ')
dispatcher=updater.dispatcher
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)