from datetime import datetime
from logging.config import listen
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # 1 = male, 0 = female
activationWord = 'computer'  # Single word, activation!

# Configure browser
# Set the path
chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))


def speak(text, rate=120):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()


def parseCommand():
    listener = sr.Recognizer()
    print('Listening for a command')

    with sr.Microphone() as source:
        listener.pause_threshold = 2
        input_speech = listener.listen(source)

    try:
        print('Recognizing speech...')
        query = listener.recognize_google(input_speech, language='en_gb')
        print(f'The input speech was: {query}')
    except Exception as exception:
        print('I did not quite catch that')
        speak('I did not quite catch that')
        print(exception)
        return 'None'

    return query


def search_wikipedia(query=''):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print('No Wikipedia result')
        return 'No result received'
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummery = str(wikiPage.summary)
    return wikiSummery


# Main loop
if __name__ == '__main__':
    speak('I am rita, your digital assistant. How can I help you?')

    while True:
        # Parse as a list
        query = parseCommand().lower().split()

        if query[0] == activationWord:
            query.pop(0)

            # List commands
            if query[0] == 'say':
                if 'hello' in query:
                    speak('Greetings, all.')
                else:
                    query.pop(0)  # Remove say
                    speech = ' '.join(query)
                    speak(speech)

        # Navigation
        if query[0] == 'go' and query[1] == 'to':
            speak('Opening...')
            query = ' '.join(query[2:])
            webbrowser.get('chrome').open_new(query)

        # Wikipedia
        if query[0] == 'wikipedia':
            query = ' '.join(query[1:])
            speak('Querying the universal data bank.')
            speak(search_wikipedia(query))

        # Note recording
        if query[0] == 'log':
            speak('Ready to record your note')
            newNote = parseCommand().lower()
            now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            with open('note_%s.txt' % now, 'w') as newFile:
                newFile.write(newNote)
            speak('Note written')

        if query[0] == 'exit':
            speak('Goodbye')
            break
