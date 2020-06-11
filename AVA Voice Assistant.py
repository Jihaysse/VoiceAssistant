from gtts import gTTS
import speech_recognition as sr
from pygame import mixer
from io import BytesIO
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import urllib.parse
import bs4
import chromedriver_binary
import re
import webbrowser
import datetime
import time
import requests
import json
from geopy.distance import geodesic
from opencage.geocoder import OpenCageGeocode

listen = False
my_name = 'Julien'
api_key = 'f43fe96b2191441cbd0c4832d50a8f8a'
geocoder = OpenCageGeocode(api_key)

def talk(audio):
    print(audio)
    for line in audio.splitlines():
        mp3 = BytesIO()
        text_to_speech = gTTS(text=audio, lang='fr')
        text_to_speech.write_to_fp(mp3)
        mp3.seek(0)
        mixer.init()
        mixer.music.load(mp3)
        mixer.music.play()



def myCommand():
    #Initialize the recognizer 
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        # print('Ava est prête...')
        r.pause_threshold = 2
        #wait for 2 seconds to let the recognizer adjust the  
        #energy threshold based on the surrounding noise level 
 
        print("Patientez svp...")   
        # listen for 1 seconds and create the ambient noise energy level   
        r.adjust_for_ambient_noise(source, duration=1)  
        r.dynamic_energy_threshold = True 
        print("Ava est prête!")
        #listens for the user's input
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio, language="fr-FR").lower()
        print('Tu as dis: ' + command + '\n')
        time.sleep(1)

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('Je n\'ai pas compris ta demande.')
        command = myCommand()

    return command

def activate(command):
    if 'ava' in command:       
        talk('Je t\'écoute, {}'.format(my_name))
        time.sleep(2)
        listen = True
        print(listen)
        while listen == True:
            ava(myCommand())
    else:
        print('Je suis désactivée. Prononce \"Ava\" pour m\'activer.')


def ava(command):

    errors=[
        "Je ne comprends pas ce que tu veux dire",
        "Que veux-tu dire?",
        "Je n'ai pas compris",
    ]

    if 'bonjour' in command:
        talk('Bonjour! Je suis Ava. Comment puis-je t\'aider?')
        time.sleep(3)
        

    elif 'google' in command:
        reg_ex = re.search('(.*) google (.*)', command)
        search_for = command.split("google",1)[1]
        url = 'https://www.google.com/'
        if reg_ex:
            subgoogle = reg_ex.group(1)
            url = url + 'r/' + subgoogle
        talk('D\'accord!')
        driver = webdriver.Chrome()
        driver.get('http://www.google.com')
        search = driver.find_element_by_name('q') # finds search
        search.send_keys(str(search_for)) #sends search keys 
        search.send_keys(Keys.RETURN) #hits enter
        return activate(myCommand())

    elif 'wikipedia' in command or 'wikipédia' in command:
        reg_ex = re.search('(.*) wikip[ée]dia (.+)', command)
        if reg_ex: 
            query = command.split("wikipédia",1)[1] 
            response = requests.get("https://fr.wikipedia.org/wiki/" + query)
            if response is not None:
                html = bs4.BeautifulSoup(response.text, 'html.parser')
                title = html.select("#firstHeading")[0].text
                paragraphs = html.select("p")
                for para in paragraphs:
                    print (para.text)
                intro = '\n'.join([ para.text for para in paragraphs[0:3]])
                mp3name = 'speech.mp3'
                language = 'fr-FR'
                myobj = gTTS(text=intro, lang=language, slow=False)   
                myobj.save(mp3name)
                mixer.init()
                mixer.music.load("speech.mp3")
                mixer.music.play()

    elif 'youtube' in command:
        reg_ex = re.search('youtube (.+)', command)
        if reg_ex:
            domain = command.split('youtube',1)[1] 
            query_string = urllib.parse.urlencode({"search_query" : domain})
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
            webbrowser.open("http://www.youtube.com/watch?v={}".format(search_results[0]))
            return activate(myCommand()) 

    elif 'distance' in command:        
        reg_ex = re.search('distance (.+)', command)
        if reg_ex:
            my_city_split = command.split(' et ')
            my_city_join = "".join(my_city_split[0])
            my_city = my_city_join.split('entre ')[1]
            destination = command.split('et',1)[1]
            query = my_city
            print(my_city)
            
    elif 'stop' in command:
        mixer.music.stop()
        return activate(myCommand)
    else:
        error = random.choice(errors)
        talk(error)





#loop to continue executing multiple commands
while listen == False:
    activate(myCommand())
   