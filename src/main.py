from src.general import start_up, setup_engine, setup_recognizer, _listen, \
    validate_response, reply_to_greeting_message, init_youtube_client


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
            print('invoked')