from src.general import start_up, setup_engine, setup_recognizer, _listen, \
    validate_response, reply_to_greeting_message


if __name__ == '__main__':
    # Setup the engine
    engine = setup_engine()
    recognizer = setup_recognizer()

    # Start up Robin
    start_up(engine)
    response = _listen(recognizer, engine)
    response = validate_response(response, recognizer, engine).lower()

    reply_to_greeting_message(engine, response)
