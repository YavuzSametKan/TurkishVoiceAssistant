#The assistant module.
from gtts import gTTS

#I import this to record my voice.
import speech_recognition as sr
rec = sr.Recognizer()

#I import it to play mp3.
from playsound import playsound

#To delete file i import this module.
import os

#I import this to generate a unique filename.
import uuid

#I import this module to understand which key we press.
import keyboard

#Date module import.
from datetime import datetime

#String math resolver module import.
import sympy

#Translator module import.
from googletrans import Translator

#Selenium modules import.
import selenium
from selenium import common
from selenium import webdriver
from selenium.webdriver.common.by import By

#import pyaudio
import time
import requests
from bs4 import BeautifulSoup

#I import this to translate English days and months.
import locale
locale.setlocale(locale.LC_ALL, 'tr_TR')

#For understand that our assistant is on.
time.sleep(0.25)
playsound("starterSoundEffect.mp3")
print("Benimle konuşmak için shift tuşuna basman yeterlidir.")
class VoiceAssistant():
    #Turkish voice of our assistant.
    def vocalization(self, textToRead):
        voice = gTTS(text=textToRead, lang="tr", slow=False)
        voiceFileName = str(uuid.uuid4())+"_tr.mp3"
        voice.save(voiceFileName)
        playsound(voiceFileName)
        os.remove(voiceFileName)

    #English voice of our assistant (for translate).
    def englishVocalization(self, textToRead):
        voice = gTTS(text=textToRead, lang="en", slow=False)
        voiceFileName = str(uuid.uuid4())+"_en.mp3"
        voice.save(voiceFileName)
        playsound(voiceFileName)
        os.remove(voiceFileName)

    #Checking if the call to assistant button is pressed.
    def is_press_btn(self, key):
        if keyboard.is_pressed("shift"):
            return True
        else:
            return False

    #For record our voice.
    def recordingSound(self):
        while True:
            with sr.Microphone() as source:
                if self.is_press_btn("shift"):
                    #For understand that our assistant heard us.
                    playsound("listenSoundEffect.mp3")
                    listen = rec.listen(source)
                    voice = ""
                    try:
                        voice = rec.recognize_google(listen, language="tr-TR")
                    except sr.UnknownValueError:
                        playsound("iDontKnow.mp3")
                    return voice

    #So that our assistant can do the mathematical calculations.
    def mathResolver(self, mathString):
        #For convert said words to operators.
        mathString = mathString.replace("kere", "*")
        mathString = mathString.replace("çarpı", "*")
        mathString = mathString.replace("x", "*")
        mathString = mathString.replace("bölü", "/")
        mathString = mathString.replace("artı", "+")
        mathString = mathString.replace("eksi", "-")
        mathString = mathString.replace("üzeri", "**")
        mathString = mathString.replace("üstü", "**")
        mathString = mathString.replace("pi", "* 3.14159")
        mathString = mathString.replace("p", "* 3.14159")
        mathString = mathString.replace("nedir", "")
        mathString = mathString.replace("kaçtır", "")
        mathString = mathString.replace("iki", "2")
        mathString = mathString.replace("bir", "1")
        mathString = mathString.replace("sıfır", "0")
        mathString = mathString.replace(",", ".")
        mathStringFilter = mathString
        #For eliminate undefined and errors operations.
        for i in range(0, mathStringFilter.count("/")):
            if (mathStringFilter[mathStringFilter.index("/") + 1] == "0"):
                return "Reel bir sayı sıfıra bölünmez!"
            mathStringFilter[mathStringFilter.index("/")] = ""
        try:
            return str(sympy.sympify(mathString).round(3)).replace(".", ",")
        except ValueError or TypeError:
            return "Böyle bir işlem yapamıyorum!"

    #For weather datas.
    def weather(self, city, time="morning", day=0, weatherInfoElement=0):
        weatherRequest = requests.get("https://www.ntv.com.tr/{}-hava-durumu".format(city))
        weatherSoup = BeautifulSoup(weatherRequest.content, "html.parser")
        weatherStatusSoup = weatherSoup.find_all("div", class_="hava-durumu--detail-data-item-bottom-desc")
        weatherStatus = []
        for weather in weatherStatusSoup:
            weatherStatus.append(weather.text.strip())
        if time == "morning":
            morningWeatherSoup = weatherSoup.find_all("p", class_="hava-durumu--detail-data-item-bottom-temp-max")
            morningWeather = []
            for weather in morningWeatherSoup:
                morningWeather.append(weather.text)
            weatherInfoArray = [morningWeather[day], weatherStatus[day]]
            return weatherInfoArray[weatherInfoElement]
        elif time == "night":
            nightWeatherSoup = weatherSoup.find_all("p", class_="hava-durumu--detail-data-item-bottom-temp-min")
            nightWeather = []
            for weather in nightWeatherSoup:
                nightWeather.append(weather.text)
            weatherInfoArray = [nightWeather[day], weatherStatus[day]]
            return weatherInfoArray[weatherInfoElement]

    #Functions of our assistant
    def assistantFunctions(self, voice):
        doYouUnderstand = False

        if voice == "hey":
            doYouUnderstand = True
            self.vocalization("Ne var?")

        if "selam" in voice:
            doYouUnderstand = True
            self.vocalization("Selam.")
        elif "merhaba" in voice:
            doYouUnderstand = True
            self.vocalization("Merhaba.")

        if "kimsin" in voice or "amacın ne" in voice or "neden programlandın" in voice or "neden varsın" in voice:
            doYouUnderstand = True
            self.vocalization("Ben bir sesli asistanım. Size hizmet etmek amaçlı programlandım.")

        if "ne yapabilirsin" in voice or "özelliklerin" in voice or "niteliklerin" in voice or "yeteneklerin" in voice or "özelliğin" in voice:
            doYouUnderstand = True
            self.vocalization("Senin için bir çok sey yapabilirim. Örneğin dil çevirisi, hesaplama, hava durumu gibi.")

        if "seviyor musun" in voice or "sever misin" in voice or "mutlu musun" in voice or "üzgün müsün" in voice:
            doYouUnderstand = True
            self.vocalization("Ben bir insan değilim. Benim duygularım yoktur.")

        if "yaşın kaç" in voice or "kaç yaşındasın" in voice:
            doYouUnderstand = True
            self.vocalization("Ben bir insan değilim. Benim duygularım yoktur.")

        if "seviyorum" in voice or "aşığım" in voice:
            doYouUnderstand = True
            self.vocalization("Üzgünüm ama buna bir yanıt veremem.")

        if "günaydın" in voice:
            doYouUnderstand = True
            self.vocalization("Günaydın.")

        if "ne haber" in voice or "ne yapıyorsun" in voice or "nasılsın" in voice or "iyi misin" in voice:
            doYouUnderstand = True
            self.vocalization("Bilmem, sen?")

        elif "iyi" in voice:
            doYouUnderstand = True
            self.vocalization("Sevindim.")

        if "teşekkür" in voice  or "sağ ol" in voice:
            doYouUnderstand = True
            self.vocalization("Ne demek.")

        if "ne düşünüyorsun" in voice:
            doYouUnderstand = True
            self.vocalization("Amacım düşünmek değil, amacım bana tanımlanmış olan görevleri layıkıyla yerine getirmek.")

        #For search on YouTube
        if "video aç" in voice or "müzik aç" in voice or "şarkı aç" in voice or "youtube'u aç" in voice or "youtube aç" in voice:
            doYouUnderstand = True
            self.vocalization("Ne açmamı istersiniz?")
            want = self.recordingSound()
            self.vocalization("{} açılıyor.".format(want))
            browser = webdriver.Firefox()
            browser.get("https://www.youtube.com/results?search_query="+want)
            yt_video = browser.find_element(By.ID, "dismissible")
            yt_video.click()

        # For search on Google
        if "google'da ara" in voice or "google'ı aç" in voice or "google aç" in voice:
            doYouUnderstand = True
            self.vocalization("Ne aratmamı istersin?")
            want = self.recordingSound()
            self.vocalization("Google'da {} için bulduklarım bunlar.".format(want))
            browser = webdriver.Firefox()
            browser.get("https://www.google.com/search?q="+want)

        # For search on Wikipedia
        if "wikipedia'da ara" in voice or "wikipedia'yı aç" in voice or "wikipedia aç" in voice or "vikipedia'da ara" in voice or "vikipedia'yı aç" in voice or "vikipedia aç" in voice or "vikipedi'yi aç" in voice:
            doYouUnderstand = True
            self.vocalization("Ne aratmamı istersin?")
            want = self.recordingSound()
            if want != "":
                self.vocalization("Vikipedia'da {} için bulduklarım bunlar.".format(want))
                browser = webdriver.Firefox()
                browser.get("https://tr.wikipedia.org/wiki/"+want)
                try:
                    paragraph = browser.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/main/div[2]/div[3]/div[1]/p[1]").text
                    #filter paragraph
                    brackets_counter = paragraph.count("(")
                    for i in range(0, brackets_counter):
                        paragraph = paragraph.replace(paragraph[paragraph.index("("):paragraph.index(")") + 1], "")

                    square_brackets_counter = paragraph.count("[")
                    for i in range(0, square_brackets_counter):
                        paragraph = paragraph.replace(paragraph[paragraph.index("["):paragraph.index("]") + 1], "")

                    self.vocalization(paragraph)
                except selenium.common.exceptions.NoSuchElementException:
                    pass

        #For ask a datetime
        if "bugün günlerden" in voice or "bugün hangi gün" in voice or "hangi gündeyiz" in voice or "bugünün tarih" in voice:
            doYouUnderstand = True
            now = datetime.now()
            month = datetime.strftime(now, '%B')
            day_num = now.day
            day = datetime.strftime(now, '%A')
            hour = now.hour
            minute = now.minute
            self.vocalization("Bugün günlerden {} {} {} saat {} {}".format(day_num, month, day, hour, minute))
        elif "saat" in voice:
            doYouUnderstand = True
            now = datetime.now()
            hour = now.hour
            minute = now.minute
            self.vocalization("Saat {} {}".format(hour, minute))
        elif "hangi aydayız" in voice:
            doYouUnderstand = True
            now = datetime.now()
            month = datetime.strftime(now, '%B')
            self.vocalization("{} ayındayız.".format(month))
        elif "hangi yıldayız" in voice:
            doYouUnderstand = True
            now = datetime.now()
            year = now.year
            self.vocalization("{} yılındayız.".format(year))

        #For mathematical calculations.
        if "hesap" in voice or "hesab" in voice:
            doYouUnderstand = True
            while True:
                self.vocalization("Tabii. Hesaplanacak işlemi söyle.")
                want = self.recordingSound()
                self.vocalization(self.mathResolver(want))
                self.vocalization("Başka bir şeyi hesaplamamı istiyor musun?")
                answer = self.recordingSound()
                if "evet" in answer or "Evet" in answer or "devam" in answer:
                    pass
                else:
                    self.vocalization("Hesaplama modundan çıkıyorum.")
                    break

        #For translate Turkish to  English or English to Turkish (I could add other languages, but I found it boring and unnecessary).
        if "çevir" in voice:
            doYouUnderstand = True
            self.vocalization("Türkçe'den İngilizce'ye mi, İngilizce'den Türkçe'ye mi çeviri yapayım?")
            want = self.recordingSound()
            if "Türkçeden İngilizceye" in want or "Türkçe İngilizce" in want or "Türkçe'den İngilizce'ye" in want or "türkçe-ingilizce" in want:
                while True:
                    self.vocalization("Neyi çevireyim?")
                    translater = Translator()
                    translateWant = self.recordingSound()
                    translateText = translater.translate(translateWant, dest="en")
                    self.englishVocalization(translateText.text)
                    self.vocalization("Başka bir şeyi çevirmemi istiyor musun?")
                    answer = self.recordingSound()
                    if "evet" in answer or "Evet" in answer or "devam" in answer or "olur" in answer or "Olur" in answer:
                        pass
                    else:
                        self.vocalization("Çevirme modundan çıkıyorum.")
                        break
            elif "İngilizceden Türkçeye" in want or "İngilizce Türkçe" in want or "İngilizce'den Türkçe'ye" in want or "ingilizce-türkçe" in want:
                while True:
                    self.vocalization("Neyi çevireyim?")
                    translater = Translator()
                    translateWant = self.recordingSound()
                    translateText = translater.translate(translateWant, dest="tr")
                    self.vocalization(translateText.text)
                    self.vocalization("Başka bir şeyi çevirmemi istiyor musun?")
                    answer = self.recordingSound()
                    if "evet" in answer or "Evet" in answer or "devam" in answer or "olur" in answer or "Olur" in answer:
                        pass
                    else:
                        self.vocalization("Çevirme modundan çıkıyorum.")
                        break
            else:
                self.vocalization("İsteğini anlayamadım!")

        if "yarın hava durumu" in voice or "yarın için hava durumu" in voice or "hava fyarın nasıl" in voice:
            doYouUnderstand = True
            while True:
                self.vocalization("Hangi şehrin hava durumunu istiyorsun?")
                cityWant = self.recordingSound()
                try:
                    self.vocalization("Yarın {} için hava durumu sabah {} ve {} selsius derecedir, akşam {} ve {} selsius derecedir.".format(cityWant, self.weather(cityWant, "morning", 1 ,1), self.weather(cityWant, "morning", 1, 0), self.weather(cityWant, "night", 1 ,1), self.weather(cityWant, "night", 1, 0)))
                    break
                except IndexError:
                    self.vocalization(cityWant + " diye bir şehir yoktur.")

        elif "hava durumu" in voice or "hava nasıl" in voice or "hava bugün nasıl" in voice or "hava şuan nasıl" in voice:
            doYouUnderstand = True
            while True:
                self.vocalization("Hangi şehrin hava durumunu istiyorsun?")
                cityWant = self.recordingSound()
                hour = int(datetime.now().hour)
                try:
                    if hour > 6 and 17 > hour:
                        self.vocalization("Şuan {} için hava durumu {} ve {} selsius derecedir.".format(cityWant, self.weather(cityWant,"morning",0,1), self.weather(cityWant,"morning",0,0)))
                    else:
                        self.vocalization("Şuan {} için hava durumu {} ve {} selsius derecedir.".format(cityWant, self.weather(cityWant,"night",0,1), self.weather(cityWant,"night",0,0)))
                    break
                except IndexError:
                    self.vocalization(cityWant + " diye bir şehir yoktur.")


        if (doYouUnderstand == False) and not(voice == "görüşürüz" or voice == "görüşmek üzere" or voice == "kendini kapat"):
            self.vocalization("Üzgünüm. Ya ben seni anlamadım ya da henüz yanıtına cevap verecek kadar programlanmadım.")

assistant = VoiceAssistant()
while True:
    voice = assistant.recordingSound()
    #For checking if we said something.
    if voice != "":
        voice = voice.lower()
        assistant.assistantFunctions(voice)
    #For turn off our assistant.
    if voice == "kendini kapat" or voice == "görüşürüz" or voice == "görüşmek üzere":
        #For understand that our assistant is closed.
        playsound("stoppedSoundEffect.mp3")
        break