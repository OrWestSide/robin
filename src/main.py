from src.general import start_up, setup_engine, setup_recognizer, _listen, \
    validate_response, reply_to_greeting_message, init_youtube_client, say
from src.youtube import make_query, parse_response, play_song


if __name__ == '__main__':
    # Setup the engine
    engine = setup_engine()
    recognizer = setup_recognizer()

    # Initializers
    youtube = init_youtube_client()

    # Start up Robin
    start_up(engine)
    response = _listen(recognizer, engine, True)
    response = validate_response(response, recognizer, engine, False).lower()

    reply_to_greeting_message(engine, response)

    while True:
        response = validate_response(_listen(recognizer, engine, True),
                                     recognizer,
                                     engine, True).lower()

        print(response)
        if 'robin' in response:
            say(engine, 'Tell me Orestis')
            response = validate_response(_listen(recognizer, engine, True),
                                         recognizer,
                                         engine, True).lower()
            print(response)
            if 'play' in response:
                res = make_query(youtube, response)
                video_id = parse_response(res)
                play_song(video_id)


            print('invoked')