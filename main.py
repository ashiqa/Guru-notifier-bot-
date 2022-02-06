import requests , bs4
import pytz
import time 
from datetime import datetime
from jaagteraho import keep_alive

# to start the thread
keep_alive()

IST = pytz.timezone('Asia/Kolkata')
raw_TS =datetime.now(IST)
curr_date = raw_TS.strftime("%d-%m-%Y")
curr_time = raw_TS.strftime("%H:%M:%S") #24Hr

# Auth for telegram bot 
telegram_auth_token = "5285918762:AAHtv2YsSeq4PlQ6EdghkVbY0fYAGUveIb4"                      
# Telegram group name
telegram_group_id = "technocrats_notify"


#msg=f"Message received on {curr_date} at {curr_time}"

def send_message_on_telegram():
  
  res = requests.get('https://www.guru.com/d/jobs/c/programming-development/sc/web-development-design/ssc/web-development/bud/fixed/')

  # Catches errors 
  res.raise_for_status()
 
  #parse it in beautiful soup
  soupObj=bs4.BeautifulSoup(res.text, 'html.parser')
  
  #iterate thro list obj
  for i in range(4,20):
      job=soupObj.find_all('li')[i]
      if(job is None):
          continue

      header=job.find('div',class_="jobRecord__meta")
      if(header is None):
          continue
      
      #extract name/desc and link 
      companyTitle=job.find('h2',class_="jobRecord__title jobRecord__title--changeVisited")
      if(companyTitle is None):
          continue

      companyTag=companyTitle.find('a')
      if(companyTag is None):
          continue

      link='https://www.guru.com'+companyTag['href'] ;
      companyName=companyTag.text ;
      
      #extract time
      time_details=header.text.split() 
      unit=time_details[2]
      time_posted=time_details[1]

      #extract price
      budget=job.find('div',class_="jobRecord__budget")
      if(budget is None):
          continue 
      price =budget.text

      #display 
      if(unit=="mins" ):
          
          message=f" {time_posted}{unit} ago  {price} {companyName}  {link} "
          
          telegram_api_url=f"https://api.telegram.org/bot{telegram_auth_token}/sendMessage?chat_id=@{telegram_group_id}&text={message}"
          
          tel_response=requests.get(telegram_api_url)

          if tel_response.status_code == 200:
            print("INFO : Notification sent")
          else:
            print("ERROR : Can't send")

#bot runs every 5 min
while(True):
  send_message_on_telegram()
  time.sleep(3600) 