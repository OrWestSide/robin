import pyttsx3
import datetime
import random
import pytz
import os
import speech_recognition as sr

from apiclient import discovery
from dotenv import load_dotenv

load_dotenv()
USERNAME = os.getenv('_USERNAME')
RATE = int(os.getenv('RATE'))
VOLUME = float(os.getenv('VOLUME'))
TIMEZONE = os.getenv('TIMEZONE')
API_KEY = os.getenv('GOOGLE_API_KEY')

tired = ['tired', 'long', 'tiring']
sad = ['not', 'bad']
happy = ['ok', 'great', 'fine']


def setup_engine() -> pyttsx3.engine:
    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', RATE)
    engine.setProperty('volume', VOLUME)

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    return engine


def setup_recognizer() -> sr.Recognizer:
    return sr.Recognizer()


def start_up(_engine: pyttsx3.engine):
    _hour = datetime.datetime.now(pytz.timezone(TIMEZONE)).hour
    greeting = 'Good morning '
    if 12 < _hour < 20:
        greeting = 'Good afternoon '
    elif _hour >= 20:
        greeting = 'Good evening '

    question = 'How are things going?' \
        if random.random() > 0.5 else \
        'How are you today?'

    msg = greeting + USERNAME + '. ' + question
    say(_engine, msg)


def validate_response(response: str,
                      recognizer: sr.Recognizer,
                      _engine: pyttsx3.engine,
                      sleep: bool) -> str:
    while not response:
        response = _listen(recognizer, _engine, sleep)
    return response


def reply_to_greeting_message(engine: pyttsx3.engine, response: str):
    _need = 'If you need anything just call me by my name.'
    if any(_ in response for _ in tired):
        say(engine, 'You should get some rest. ' + _need)
    elif any(_ in response for _ in happy):
        say(engine, 'This is good. ' + _need)
    elif any(_ in response for _ in sad):
        say(engine, 'These are the days you need to shine. ' + _need)
    else:
        say(engine, 'Some days I just do not understand you. Anyway. ' + _need)


def _listen(r: sr.Recognizer, en: pyttsx3.engine, sleep: bool):
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en')
    except sr.UnknownValueError:
        if not sleep:
            say(en, 'I could not understand what you said. Do you want to '
                    'repeat?')
        return None
    return query


def init_youtube_client():
    return discovery.build('youtube', 'v3', developerKey=API_KEY)


def say(_engine: pyttsx3.engine, saying: str):
    _engine.say(saying)
    _engine.runAndWait()
