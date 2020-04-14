from src.general import start_up, setup_engine, setup_recognizer, _listen, \
    validate_response, say

tired = ['tired', 'long']
sad = ['not', 'bad']
happy = ['ok', 'great']

if __name__ == '__main__':
    # Setup the engine
    engine = setup_engine()
    recognizer = setup_recognizer()

    # Start up Robin
    start_up(engine)
    response = _listen(recognizer, engine)
    response = validate_response(response, recognizer, engine).lower()

    if 'no' not in response and 'yes' not in response:
        _need = 'If you need anything just call me by my name.'
        if any(_ in response for _ in tired):
            say(engine, 'You should get some rest. ' + _need)
        elif any(_ in response for _ in happy):
            say(engine, 'This is good. ' + _need)
        elif any(_ in response for _ in sad):
            say(engine, 'These are the days that you need to shine. ' + _need)