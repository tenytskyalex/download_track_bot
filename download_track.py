import telebot
import requests
import shutil
import time
from selenium import webdriver
import urllib3
from bs4 import BeautifulSoup
import glob,os


token = '791050097:AAGFQTBCj1idxWfC0sPpux_vHDwh75tJfXc'

#a = input()
#a = a.split()
#count = len(a)

load = []
bot = telebot.TeleBot(token)
closed = []
user_seans = 0
try:

    def download_music(url,chat_id):
        options = webdriver.ChromeOptions()
        prefs = {"download.default_directory" : 'F:/Games/MusicBot/'+chat_id, "directory_upgrade":True}
        options.add_experimental_option('prefs',prefs)
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)
        #load = driver.find_element_by_css_selector("a.playlist-btn-down no-ajaxy")
        #load.click()
        os.chdir('F:/Games/MusicBot/'+str(chat_id))
        while chat_id not in closed:
            for file in glob.glob("*.mp3"):
                closed.append(chat_id)
                time.sleep(1)
                driver.quit()
        closed.remove(chat_id)
    def get_url(url,chat_id=0):
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            soup = soup.find('div', { "class" : "playlist-btn"}).find('a', title="скачать")['href']
            download = "https://music.я.ws"+soup
            print(download)
            download_music(download,str(chat_id))
        except:
            bot.send_message(chat_id,"Не удалось найти песню")
            load.remove(chat_id)

    @bot.message_handler(content_types=['text'])
    def upload_music(message):
        if message.chat.id in load:
            bot.send_message(message.chat.id,"Дождитесь окончания загрузки")
        else:
            load.append(message.chat.id)
            bot.send_message(message.chat.id, "Ожидайте, это может занять до 30 секунд")
            search = ""
            a = message.text
            a = a.split()
            count = len(a)
            os.makedirs('F:/Games/MusicBot/'+str(message.chat.id), exist_ok=True)
            i = 0
            #soup = BeautifulSoup(page)
            while i < count:
                if i != count-1:
                    search += a[i].lower()+"-";
                else: search += a[i].lower()
                i += 1
     #       for i in closed:
    #            if i == message.chat.id:
                 #   break
                #else:
                    #closed.append(message.chat.id)
            url = "https://music.я.ws/search/"+search+"/"
            get_url(url,message.chat.id)
                    ##сюда вставлять
            os.chdir('F:/Games/MusicBot/'+str(message.chat.id))
            for file in glob.glob("*.mp3"):
                bot.send_audio(message.chat.id,audio = open('F:/Games/MusicBot/'+str(message.chat.id)+"/"+file, 'rb'))
                load.remove(message.chat.id)
                os.remove('F:/Games/MusicBot/'+str(message.chat.id)+"/"+file)
except Exception as e:
    print(e)
    bot.polling(none_stop=False, interval=0, timeout=20)
if __name__ == '__main__':
    bot.polling(none_stop=False, interval=0, timeout=20)


