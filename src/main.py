import os
import random
import logging
import multiprocessing

from dotenv import load_dotenv

from src.general import start_up, setup_engine, setup_recognizer, _listen, \
    validate_response, reply_to_greeting_message, init_youtube_client, say
from src.youtube import make_query, parse_response, play_song

load_dotenv()
USERNAME = os.getenv('_USERNAME')
names = ['robin', 'eloping', 'adobe', 'open']
invocation_responses = [
    'Tell me ' + USERNAME, 'What do you need?', 'Yes?', 'How can I help you?'
]


def setup():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [%(levelname)s] - %(message)s'
    )

    # Setup the engine
    _engine = setup_engine()
    _recognizer = setup_recognizer()

    # Initializers
    _youtube = init_youtube_client()

    return _engine, _recognizer, _youtube


if __name__ == '__main__':
    engine, recognizer, youtube = setup()
    logging.info('Setting up Robin...')

    # Start up Robin
    logging.info('Starting Robin...')
    start_up(engine)
    response = _listen(recognizer, engine, True)
    response = validate_response(response, recognizer, engine, False).lower()

    reply_to_greeting_message(engine, response)

    youtube_thread = None

    while True:
        response = validate_response(_listen(recognizer, engine, True),
                                     recognizer,
                                     engine, True).lower()

        if response:
            logging.info('While sleeping I heard: ' + response)
        else:
            logging.info('Completed on idle cycle')

        if any(_ in response for _ in names):
            say(engine, random.choice(invocation_responses))
            response = validate_response(_listen(recognizer, engine, True),
                                         recognizer,
                                         engine, True).lower()

            logging.info('The command is: ' + response)
            if 'play' in response:
                res = make_query(youtube, response)
                video_id = parse_response(res)

                youtube_thread = multiprocessing.Process(
                    target=play_song, args=(video_id,)
                )
                youtube_thread.start()

            if 'stop' in response or 'music' in response:
                if youtube_thread:
                    youtube_thread.terminate()
                    youtube_thread = None
