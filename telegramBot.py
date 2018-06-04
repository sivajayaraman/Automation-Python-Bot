import requests
import tables
from bs4 import BeautifulSoup
import csv
def cricscore(last_chat_id):
	URL = "http://www.cricbuzz.com/cricket-match/live-scores"
	r = requests.get(URL)
	soup = BeautifulSoup(r.content, 'html5lib')
	p=1
	last_update = greet_bot.get_last_update()
	last_update_id = last_update['update_id']
	url_store=[]
	team=[]
	match_info=''
	table=soup.find('div', attrs = {'class':'cb-bg-white cb-col-100 cb-col'})
	for row in table.findAll('div', attrs = {'class':'cb-col cb-col-100 cb-lv-main'}):
		quote= {}
		quote['url']=row.a['href']
		url=row.a['href']
		name=row.a['title']
		match_info+=str(p)+'.'+name+'\n'
		p=p+1
		url_store.append(quote)
	greet_bot.send_message(last_chat_id,match_info)
	filename_url = 'current_matches_url.csv'
	with open(filename_url, 'wb') as f:
		w = csv.DictWriter(f,['url'])
		w.writeheader()
		for quote in url_store:
			w.writerow(quote)		    	        	    		       
	greet_bot.send_message(last_chat_id,"Enter the Match number")
	current_update_id=last_update_id
	while last_update_id==current_update_id:
		current_update= greet_bot.get_last_update()
		current_update_id = current_update['update_id']		
	match_no = int(current_update['message']['text'])
	if match_no>0 and match_no<=p:
		file = open(filename_url, 'r')
		t=1
		req_url="http://www.cricbuzz.com"
		for each in file:
			break
		for each in file:
			if t==match_no:
				req_url=req_url+each
				break
			t=t+1		
		r = requests.get(req_url)
		soup = BeautifulSoup(r.content, 'html5lib')
		table=soup.find('div', attrs = {'class':'page'})
		team1=0
		team2=0
		for row in table.findAll('div',attrs={'class':'cb-col cb-col-100 cb-min-tm cb-text-gray'}):
			team1=1
			greet_bot.send_message(last_chat_id,row.text)
		for row in table.findAll('div',attrs={'class':'cb-col cb-col-100 cb-min-tm'}):
			team2=1
			greet_bot.send_message(last_chat_id,row.text)
		for row in table.findAll('div',attrs={'class':'cb-text-rain'}):
			greet_bot.send_message(last_chat_id,row.text)	
		if team2==1 and team1==1:
			for row in table.findAll('div',attrs={'class':'cb-col cb-col-100 cb-min-stts cb-text-mom'}):
				greet_bot.send_message(last_chat_id,row.text)
			for row in table.findAll('div',attrs={'class':'cb-col cb-col-100 cb-min-stts cb-text-complete'}):
				greet_bot.send_message(last_chat_id,row.text)
		if team1==0 and team2==0:
			for row in table.findAll('div',attrs={'class':'cb-text-gray cb-font-16'}):
				team1=1
				greet_bot.send_message(last_chat_id,row.text)
			for row in table.findAll('span',attrs={'class':'cb-font-20 text-bold'}):
				team2=1
				greet_bot.send_message(last_chat_id,row.text)
			for row in table.findAll('div',attrs={'class':'cb-text-stump'}):
				greet_bot.send_message(last_chat_id,row.text)		
		if team1==0 and team2==0:
			greet_bot.send_message(last_chat_id,"Match not yet started! Stay tuned!")
	else:
			greet_bot.send_message(last_chat_id,"Select a valid match number!")
def googleSearch(last_chat_id,last_update_id):
	from googlesearch import search
	current_update_id=last_update_id
	greet_bot.send_message(last_chat_id,"Enter Your Query")
	while last_update_id==current_update_id:
		current_update= greet_bot.get_last_update()
		current_update_id = current_update['update_id']
	greet_bot.send_message(last_chat_id,"Searching in Google....")	
	query = current_update['message']['text']
	solution=''	
	for j in search(query, tld="co.in", num=5, stop=1, pause=2):
		greet_bot.send_message(last_chat_id,j)	
def pnrStatus(last_chat_id,last_update_id):
	url="https://www.railyatri.in/pnr-status/"
	current_update_id=last_update_id
	greet_bot.send_message(last_chat_id,"Enter PNR Number")
	while last_update_id==current_update_id:
		current_update= greet_bot.get_last_update()
		current_update_id = current_update['update_id']
	greet_bot.send_message(last_chat_id,"Fetching Status....")	
	pnr=current_update['message']['text']
	if len(pnr)!=10:
		greet_bot.send_message(last_chat_id,"Retry with a valid PNR Number")
	else:	
		url=url+pnr
		r=requests.get(url)
		soup = BeautifulSoup(r.content, 'html5lib')
		table=soup.find('div', attrs = {'class':'pnr-search-result-info'})
		if not table:
			greet_bot.send_message(last_chat_id,"Retry with a valid PNR Number")
		else:
			train_booking='Booking Status:'
			train_name='Train Name:'
			train_from='From:'
			train_to='To:'
			train_date='Journey Date:'
			train_class='Class:'
			train_status='Current Status:'
			t=1
			for row in table.findAll('p',attrs={'class':'pnr-bold-txt'}):
				name=row.text
				if t==1:
					train_name=train_name+name
				elif t==2:
					train_from=train_from+name
				elif t==3:
					train_to=train_to+name
				elif t==4:
					train_date=train_date+name
				elif t==5:
					train_class=train_class+name
				t=t+1
			t=1	
			table=soup.find('div', attrs = {'id':'status'})	
			for row in table.findAll('p',attrs={'class':'pnr-bold-txt'}):
				if t==2:
					train_status=train_status+row.text
				elif t==1:
					train_booking=train_booking+row.text	
				t=t+1	
			pnr_info=train_booking+'\n'+train_status+'\n'+train_name+'\n'+train_from+'\n'+train_to+'\n'+train_date+'\n'+train_class
			greet_bot.send_message(last_chat_id,pnr_info)
class BotHandler:
    def __init__(self, token):
        self.token = 'token'
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json
    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp
    def get_last_update(self):
        get_result = self.get_updates()
        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]
        return last_update
greet_bot = BotHandler('token')  
greetings = ('hello', 'hi', 'greetings', 'sup','hey','hai','vanakkam','hey there','hey dere','dear','dr','dai','el','vanakam','dae','dude')  
def main():  
    new_offset = None
    while True:
		greet_bot.get_updates(new_offset)
		last_update = greet_bot.get_last_update()
		last_update_id = last_update['update_id']
		last_chat_text = last_update['message']['text']
		last_chat_id = last_update['message']['chat']['id']
		last_chat_name = last_update['message']['chat']['first_name']
		if last_chat_text.lower() in greetings :
			user_name='Hi '+ last_chat_name
			greet_bot.send_message(last_chat_id,user_name)
		elif last_chat_text.lower()=='bye' or last_chat_text.lower()=='tata' or last_chat_text.lower()=='cys' or last_chat_text.lower()=='see you soon':
			user_name='Bye! Have a Nice Day '+last_chat_name+'!'
			greet_bot.send_message(last_chat_id,user_name)  	
		elif last_chat_text.lower() =='score' or last_chat_text.lower() =='scores' or last_chat_text.lower() =='cricket':
			greet_bot.send_message(last_chat_id, 'Live Score Loading!')
			cricscore(last_chat_id)	
		elif last_chat_text.lower() == 'google' or last_chat_text.lower() == 'search':
			googleSearch(last_chat_id,last_update_id)
		elif last_chat_text.lower() == 'pnr':
			pnrStatus(last_chat_id,last_update_id)		
		new_offset=last_update_id + 1
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()