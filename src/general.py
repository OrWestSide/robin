import pyttsx3
import datetime
import random
import pytz
import os
import speech_recognition as sr

from dotenv import load_dotenv


load_dotenv()
USERNAME = os.getenv('_USERNAME')
RATE = int(os.getenv('RATE'))
VOLUME = float(os.getenv('VOLUME'))
TIMEZONE = os.getenv('TIMEZONE')


def setup_engine() -> pyttsx3.engine:
    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', RATE)
    engine.setProperty('volume', VOLUME)

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    return engine


def setup_recognizer():
    return sr.Recognizer()


def start_up(_engine: pyttsx3.engine):
    _hour = datetime.datetime.now(pytz.timezone(TIMEZONE)).hour
    greeting = 'Good morning '
    if 12 < _hour < 20:
        greeting = 'Good afternoon '
    elif _hour >= 20:
        greeting = 'Good evening '

    question = 'How are things going?' \
        if random.random() > 0.5 else\
        'How are you today?'

    _engine.say(greeting + USERNAME + '. ' + question)
    _engine.runAndWait()


def validate_response(response, recognizer, _engine) -> str:
    while not response:
        response = _listen(recognizer, _engine)
    return response


def _listen(r, en):
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en')
    except sr.UnknownValueError:
        say(en, 'I could not understand what you said. Do you want to repeat?')
        return None
    return query


def say(_engine, saying):
    _engine.say(saying)
    _engine.runAndWait()
