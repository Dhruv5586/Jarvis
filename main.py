import speech_recognition as sr
import webbrowser
import pyttsx3
import yt_dlp
import sys
recognizer = sr.Recognizer()
engine = pyttsx3.init()
print(sys.executable)
def speak(text):
    engine.say(text)
    engine.runAndWait()

def play_song(song_name):
    speak(f"Playing {song_name}")

    ydl_opts = {
        "quiet": True,
        "default_search": "ytsearch1",
        "format": "bestaudio",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(song_name, download=False)
        video_url = info["entries"][0]["webpage_url"]

    webbrowser.open(video_url)

def process(command):
    command = command.lower()

    if "open google" in command:
        webbrowser.open("https://google.com")

    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")

    elif command.startswith("play "):
        song = command.replace("play ", "").strip()
        play_song(song)

    else:
        speak("Command not recognized")

if __name__ == "__main__":
    speak("Initializing Jarvis")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source, duration=0.8)
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)

            wake_word = recognizer.recognize_google(audio)

            if wake_word.lower() == "jarvis":
                speak("Yes")

                with sr.Microphone() as source:
                    print("Jarvis active...")
                    audio = recognizer.listen(source)

                command = recognizer.recognize_google(audio)
                process(command)

        except sr.WaitTimeoutError:
            continue
        except Exception as e:
            print("Error:", e)
