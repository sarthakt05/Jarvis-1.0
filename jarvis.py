import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser as wb
import os
import pyautogui
import psutil
import pyjokes

r = sr.Recognizer()
engine = pyttsx3.init()  # This will call the initial function of the pyttsx3 module
# female voice
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id)


def speak(audio):
    # This is a predefined function that converts the text specified into speech
    engine.say(audio)
    engine.runAndWait()  # This will wait till it has finished speaking


def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("The current time is")
    speak(Time)


def convertMonth(month):
    if(month == 1):
        return "January"
    elif(month == 2):
        return "February"
    elif(month == 3):
        return "March"
    elif(month == 4):
        return "April"
    elif(month == 5):
        return "May"
    elif(month == 6):
        return "June"
    elif(month == 7):
        return "July"
    elif(month == 8):
        return "August"
    elif(month == 9):
        return "September"
    elif(month == 10):
        return "October"
    elif(month == 11):
        return "November"
    elif(month == 12):
        return "December"


def date():
    year = str(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = str(datetime.datetime.now().day)
    month = convertMonth(month)
    speak("The current date is")
    speak(day+month+year)


def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        greet = "Good morning"
    elif hour >= 12 and hour <= 16:
        greet = "Good afternoon"
    elif hour > 16 and hour <= 20:
        greet = "Good evening"
    else:
        greet = "Welcome back"
    speak(greet + " sir")
    time()
    date()
    speak("Jarvis at your sevice. How can I help you")


def takeCommand():
    try:
        with sr.Microphone() as source:  # input coming from the micrphone which is the source
            print("Listening..")
            # wait for 0.5 second and then start listening audio
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(query)
    except Exception as e:
        print(e)
        speak("Unable to understand. Say that again please")
        return "None"

    return query


def sendEmail(to, content):
    # as gmail usually uses 587 port
    server = smtplib.SMTP('smtp.gmail.com', 587)

    # for checking the connection with gmail
    server.ehlo()
    server.starttls()

    # then we login to our account
    server.login('snavneet561@gmail.com', 'singh@navneet01')

    server.sendmail('snavneet561@gmail.com', to, content)

    # to close our session from smtplib
    server.close


def screenshot():
    img = pyautogui.screenshot()
    img.save(
        "C:\\Users\\HP\\Documents\\navneet\\personal\\Jarvis AI assistant\\ss.png")


def cpu():
    usage = str(psutil.cpu_percent())
    speak("CPU is at " + usage)
    battery = psutil.sensors_battery()
    speak("Battery is at ")
    speak(battery.percent)


def joke():
    speak(pyjokes.get_joke())


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
        if "time" in query:
            time()
        elif "date" in query:
            date()
        elif "wikipedia" in query:
            speak("Searching...")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=2)
            print(result)
            speak(result)

        elif 'hi' in query or 'hello' in query:
            speak('Hello sir, how may I help you?')

        elif 'thanks' in query or 'thank you' in query:
            speak('I am happy I could help you')

        elif 'bye' in query:
            speak('Bye sir, see you next time')

        elif "send email" in query:
            try:
                speak("What message should I send?")
                content = takeCommand()
                speak("Please tell the email ID of the receiver")
                to = takeCommand()
                sendEmail(to, content)
                speak("Email has been sent!!")
            except Exception as e:
                print(e)
                speak("Unable to send the email")
        elif "google search" in query:
            speak("What should I search?")
            chromepath = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
            search = takeCommand().lower()
            wb.get(chromepath).open_new_tab(search + ".com")
        elif "logout" in query:
            os.system("shutdown -l")
        elif "shutdown" in query:
            os.system("shutdown /s /t 1")
        elif "restart" in query:
            os.system("shutdown /r /t 1")
        elif "play songs" in query:
            songs_dir = "C:\\Users\\HP\\Music"
            # return the list of songs in that directory
            songs = os.listdir(songs_dir)
            os.startfile(os.path.join(songs_dir, songs[0]))
        elif "remember that" in query:
            speak("What should I remember?")
            data = takeCommand()
            speak("You said me to remember that" + data)
            remember = open("data.txt", "w")
            remember.write(data)
            remember.close()
        elif "do you remember anything" in query:
            remember = open("data.txt", "r")
            speak("You said me to remember that " + remember.read())

        elif 'timer' in query or 'stopwatch' in query:

            speak("For how many minutes?")
            timesec = takeCommand()
            timesec = timesec.replace('minutes', '')
            timesec = timesec.replace('minute', '')
            timesec = timesec.replace('for', '')
            timesec = float(timesec)
            timesec = timesec * 60
            speak(f'I will remind you in {timesec} seconds')

            time.sleep(timesec)
            speak('Your time has been finished sir')

        elif "screenshot" in query:
            screenshot()
            speak("Done")
        elif "cpu" in query:
            cpu()
        elif "joke" in query:
            joke()
        elif "offline" in query:
            quit()
