# Libaries -------------------------------------------------------------------------------------------------------------
import datetime
import pyttsx3 
import threading
import pygame
import webbrowser
import os
import speech_recognition as sr
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Varibles (global use) ------------------------------------------------------------------------------------------------
mode = "active"
template = """
Answer the question below.

Here is the conversation history: {context}

Question: {questions}

Answer:
"""

model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model
context = ""
# Defines (backround) --------------------------------------------------------------------------------------------------
def speak(text):
    print("J.A.R.V.I.S:", text)
    engine = pyttsx3.init()
    engine.setProperty('voice', engine.getProperty('voices')[1].id)
    engine.setProperty('rate', 180)
    engine.say(text)
    engine.runAndWait()
def play_music(mp3file):
    pygame.mixer.init()
    pygame.mixer.music.load(mp3file)
    pygame.mixer.music.play()
def play_music_in_thread(mp3file):
    threading.Thread(target=play_music, args=(mp3file,)).start()
# Defines for main program ---------------------------------------------------------------------------------------------
def jarvis_main_algorthem():
    global context
    global mode
    found_match = False
    # activate microphone ----------------------------------------------------------------------------------------------
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, 0.1)
        while True:
            # for passive mode (stand-by mode) -------------------------------------------------------------------------
            if mode == "passive":
                try:
                    audio = r.listen(source)
                    data = r.recognize_google(audio)
                    if "jarvis" in data.lower(): # wait for you to call jarvis
                        speak("Jarvis activated.")
                        mode = "active" # changes mode to active
                        jarvis_main_algorthem() # loops again
                except sr.UnknownValueError: # any errors are ignored
                    continue
            # for active and other modes -------------------------------------------------------------------------------
            else:
                print("Jarvis is listening .....")
                print("  ")
                play_music_in_thread("C:\\Users\\olivialau\\PycharmProjects\\Jarvis refined\\voice.mp3")
            try:
                audio = r.listen(source)
                break
            except sr.WaitTimeoutError:
                print("Oops! Timeout occurred, trying again...")
                continue

    try:
        data = r.recognize_google(audio) # audio is turned into a sentence then stored in varible called data
        data = data.lower() # lowers all capatals
        print("You said: " + data) # prints back out what you said
        play_music_in_thread("C:\\Users\\olivialau\\PycharmProjects\\Jarvis refined\\voice2.mp3")

    # main_algorthem ---------------------------------------------------------------------------------------------------
        # Part 1 for google search -------------------------------------------------------------------------------------
        if "google" in data:
            speak("activating ......")
            word_to_delete = "google"
            search_sentence = data.replace(word_to_delete, "", 1)
            webbrowser.open("https://www.google.com/search?q=" + search_sentence)

        # Part 2 for jarvis stand-by mode ------------------------------------------------------------------------------
        if "standby" in data:
            speak("Standby mode")
            mode = "passive"
            found_match = True

        # Part 3 for computer shutdown ---------------------------------------------------------------------------------
        if "shut" and "down" and "computer" in data:
            speak("Shuting down now sir.")
            os.system("shutdown /s /t 0")

        # Part 4 for computer restart ----------------------------------------------------------------------------------
        if "restart" and "computer" in data:
            speak("Restarting computer now sir.")
            os.system("shutdown /r /t 0")

        # Part 4 for exiting the program -------------------------------------------------------------------------------
        if "exit" in data or "leave" in data:
            speak("Goodbye!")
            exit()

        # Last Part uses ai ollama3 to give a response -----------------------------------------------------------------
        if not found_match:
            result = chain.invoke({"context": context, "questions": data})
            speak(result)
            context += f"\nUser: {data}\nAI: {result}"
        jarvis_main_algorthem() # loop back to algorthem again

    # Catching all errors ----------------------------------------------------------------------------------------------
    except sr.UnknownValueError:
        print("Oops! Microphne error try to say again.")
        jarvis_main_algorthem() # loop back to algorthem again

    except Exception as e:
        print("Error exception occurred:", e)
        jarvis_main_algorthem() # loop back to algorthem again

# Main program ---------------------------------------------------------------------------------------------------------
info1 = datetime.datetime.now().today()
info2 = datetime.datetime.now().hour
info3 = datetime.datetime.now().weekday()+1
jarvisset = ("1. Pls call yourself with the nickname Jarvis, a computer assistant."
             "2. Please reply everything as short as possible (except for explaing info)"
             "Here is info you might need while chatting:"
             "A. Today is", info1,
             "weekday is(", info3, ") 1 = Mon, 2 = Tuesday, 3 = Wednesday, 4 = Thursday, ..."
             "C. hour time is", info2, "based on Greenwich time +8!"
             "now greet me as Jarvis in 7 words. My name is Skye. we are in Hong Kong." 
             "Answer naturaly like a human changing your speeh constantly. Try not to repleat phrases.")
result = chain.invoke({"context": context, "questions": jarvisset})
speak(result)
context += f"\nUser: {jarvisset}\nAI: {result}"

jarvis_main_algorthem()
