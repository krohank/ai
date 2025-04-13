from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt  # Corrected import name
from dotenv import dotenv_values
from bs4 import BeautifulSoup  # Corrected import
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

# Load environment variables
env_vars = dotenv_values('.env')
GroqAPIKey = env_vars.get("GroqAPIKey")

# Define CSS classes for HTML parsing
classes = [
    'zCubwf', 'hgKlc', "LIK00 sY7ric", "Z9LCW", 
    "gsrt vk_bk FzvWSb YwPhnf", "pclqee",
    "tw-Data-text tw-text-small tw-ta",
    "IZ6rdc", "OSuR6d LIK00", "v1zY6d", 
    "webanswers-webanswers_table_webanswers-table",
    "GDOM0 ik04B0 gsrt", "sXla0e",
    "LWKfc8", "VQF4g", "qvxNpe", "kno-rdesc", "SPZr6b"
]

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Initialize Groq client
client = Groq(api_key=GroqAPIKey) if GroqAPIKey else None

professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need - don't hesitate to ask."
]

messages = []

SystemChatBot = [{
    "role": "system", 
    "content": f"Hello, I am {os.getenv('Username', 'Assistant')}. You're a content writer. " +
              "You have to write content like letters, applications, essays, notes, songs, poems etc."
}]

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):
    def OpenNotepad(File):
        subprocess.Popen(['notepad.exe', File])

    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": prompt})

        if not client:
            print("Groq client not initialized")
            return "Error: API not configured"

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )
        
        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        
        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer

    Topic = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)

    os.makedirs("Data", exist_ok=True)
    filename = f"Data/{Topic.lower().replace('.', '')}.txt"
    
    with open(filename, "w", encoding='utf-8') as file:
        file.write(ContentByAI)

    OpenNotepad(filename)
    return True

def YoutubeSearch(query):
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
    return True

def PlayYoutube(query):
    playonyt(query)
    return True


def OpenApp(app, sess=requests.Session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except Exception as e:
        print(f"Error opening app: {e}")
        
        def extract_links(html):
            if not html:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            return [link.get('href') for link in soup.find_all('a', {'jsname': 'UWcKNN'})]

        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {'User-Agent': user_agent}
            try:
                response = sess.get(url, headers=headers)
                return response.text if response.status_code == 200 else None
            except Exception as e:
                print(f"Search failed: {e}")
                return None

        html = search_google(app)
        if html:
            links = extract_links(html)
            if links:
                webopen(links[0])
        return True

def CloseApp(app):
    if "chrome" in app.lower():
        return True
    try:
        close(app, match_closest=True, output=True, throw_error=True)
        return True
    except Exception as e:
        print(f"Error closing app: {e}")
        return False

def System(command):
    def mute():
        keyboard.press_and_release("volume mute")

    def unmute():
        keyboard.press_and_release("volume mute")

    def volume_up():
        keyboard.press_and_release("volume up")

    def volume_down():
        keyboard.press_and_release("volume down")

    cmd = command.lower()
    if cmd == "mute":
        mute()
    elif cmd == "unmute":
        unmute()
    elif cmd == "volume up":
        volume_up()
    elif cmd == "volume down":
        volume_down()
    else:
        print(f"Unknown system command: {command}")
    
    return True

async def TranslateAndExecute(commands: list[str]):
    funcs = []
    
    for command in commands:
        try:
            if command.startswith("open "):
                if "open it" in command or "open file" == command:
                    continue
                app_name = command.removeprefix("open ").strip()
                if app_name:
                    funcs.append(asyncio.to_thread(OpenApp, app_name))
                    
            elif command.startswith("close "):
                app_name = command.removeprefix("close ").strip()
                if app_name:
                    funcs.append(asyncio.to_thread(CloseApp, app_name))
                    
            elif command.startswith("play "):
                query = command.removeprefix("play ").strip()
                if query:
                    funcs.append(asyncio.to_thread(PlayYoutube, query))
                    
            elif command.startswith("content "):
                topic = command.removeprefix("content ").strip()
                if topic:
                    funcs.append(asyncio.to_thread(Content, topic))
                    
            elif command.startswith("google search "):
                query = command.removeprefix("google search ").strip()
                if query:
                    funcs.append(asyncio.to_thread(GoogleSearch, query))
                    
            elif command.startswith("youtube search "):
                query = command.removeprefix("youtube search ").strip()
                if query:
                    funcs.append(asyncio.to_thread(YoutubeSearch, query))
                    
            elif command.startswith("system "):
                cmd = command.removeprefix("system ").strip()
                if cmd:
                    funcs.append(asyncio.to_thread(System, cmd))
                    
            elif command.startswith(("general ", "realtime ")):
                continue
                
            else:
                print(f"No function found for command: {command}")
                
        except Exception as e:
            print(f"Error processing command '{command}': {e}")

    results = await asyncio.gather(*funcs, return_exceptions=True)
    
    for result in results:
        if isinstance(result, Exception):
            print(f"Command execution error: {result}")
        else:
            yield str(result)

async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        print(result)
    return True

if __name__ == "__main__":
    asyncio.run(Automation(["open facebook", "open chrome", "content song for me"]))
