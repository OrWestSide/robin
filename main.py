from general import start_up, setup_engine, setup_recognizer, _listen, \
    validate_response


if __name__ == '__main__':
    # Setup the engine
    engine = setup_engine()
    recognizer = setup_recognizer()

    # Start up Robin
    start_up(engine)
    response = _listen(recognizer, engine)
    response = validate_response(response, recognizer, engine)
