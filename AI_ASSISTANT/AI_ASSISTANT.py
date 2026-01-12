import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import threading


r = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 150)

def speak(text):
    def run():
        try:
            engine.say(text)
            engine.runAndWait()
        except:
            pass
    threading.Thread(target=run).start()

def smart_reply(command):
    command = command.lower().strip()

    if "can you hear me" in command or "are you listening" in command:
        speak("Yes boss, I can hear you clearly.")
        return

    apps = {
        "facebook": "https://facebook.com",
        "instagram": "https://instagram.com",
        "whatsapp": "https://web.whatsapp.com",
        "tiktok": "https://www.tiktok.com",
        "twitter": "https://twitter.com",
        "x": "https://twitter.com",
        "snapchat": "https://snapchat.com",
        "linkedin": "https://linkedin.com",
        "reddit": "https://reddit.com",
        "github": "https://github.com"
    }

    for app, url in apps.items():
        if f"open {app}" in command:
            speak(f"Yes boss, opening {app}")
            webbrowser.open(url)
            return

    if "open youtube" in command:
        speak("Yes boss, opening YouTube")
        webbrowser.open("https://youtube.com")
        return

    if "open google" in command:
        speak("Yes boss, opening Google")
        webbrowser.open("https://google.com")
        return

    if "who is" in command or "what is" in command:
        topic = command.replace("who is", "").replace("what is", "").strip()
        try:
            summary = wikipedia.summary(topic, sentences=2, auto_suggest=False)
            speak("Yes boss, here is what I found")
            speak(summary)
        except:
            speak("Sorry boss, I couldn't find that topic.")
        return

    chat = {
        "hello": "Hello boss, how can I help you today?",
        "hi": "Hi boss! Hope you are having a great day!",
        "how are you": "I am always fine when I am with you boss!",
        "what's up": "Just assisting my boss, you know!",
        "thanks": "You are welcome boss!",
        "thank you": "You are welcome boss!",
        "good morning": "Good morning boss! Have a great day!",
        "good night": "Good night boss! Sleep well!",
        "bye": "Goodbye boss! Talk to you soon!",
        "i am fine": "Glad to hear that boss!",
        "i am tired": "Take some rest boss, you deserve it!",
        "i am hungry": "Do you want me to suggest something to eat, boss?",
        "i am happy": "That's great boss! Happiness is important!",
        "i am sad": "Don't worry boss, everything will be fine. I'm here!",
        "what are you doing": "Just assisting my boss, as always!",
        "tell me a joke": "Why did the computer go to the doctor? Because it had a virus!",
        "good afternoon": "Good afternoon boss!",
        "good evening": "Good evening boss!",
        "how is the weather": "I cannot check live weather yet, but I hope it's nice outside!",
        "i need help": "I am here boss! Tell me what you need."
    }

    for phrase, reply in chat.items():
        if phrase in command:
            speak(reply)
            return

    speak("Sorry boss, I didn't understand that. I am learning every day.")

def command():
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            print("Listening... Say something!")
            audio = r.listen(source, timeout=6, phrase_time_limit=5)
            text = r.recognize_google(audio)
            print("You said:", text)
            return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not get that.")
        return ""
    except sr.RequestError:
        print("Google Speech Recognition error.")
        speak("Boss, internet is not working properly.")
        return ""
    except OSError:
        print("MIC ERROR: No usable microphone found")
        speak("Boss, your microphone is not working. Please check it.")
        return ""
    except Exception as e:
        print("Error:", e)
        return ""

speak("Hello! I am your AI assistant. How can I help you today?")
while True:
    cmd = command()
    if cmd:
        if "quit" in cmd or "exit" in cmd:
            speak("Goodbye boss!")
            break
        smart_reply(cmd)
