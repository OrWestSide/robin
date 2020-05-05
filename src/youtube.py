import vlc
import pafy
import time
import logging
import multiprocessing
from general import init_youtube_client


def make_query(_youtube, query):
    _req = _youtube.search().list(q=query, part='snippet', type='video')
    return _req.execute()


def parse_response(resp):
    try:
        return resp['items'][0]['id']['videoId']
    except KeyError:
        return '0'


def play_song(_id):
    url = 'https://www.youtube.com/watch?v=' + str(_id)
    logging.info('Video url: ' + url)

    video = pafy.new(url)
    best = video.getbest()
    play_url = best.url

    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(play_url)
    media.get_mrl()
    player.set_media(media)
    player.play()

    time.sleep(1.5)
    duration = player.get_length() / 1000
    time.sleep(duration)


if __name__ == '__main__':
    youtube = init_youtube_client()

    q = input('Enter the song you want to play: ')

    res = make_query(youtube, q)
    video_id = parse_response(res)

    youtube_process = None
    if video_id != '0':
        youtube_process = multiprocessing.Process(
            target=play_song, args=(video_id,)
        )
        youtube_process.start()

    q = input('Stop music? (y/n) ')

    if q == 'y' and youtube_process is not None:
        youtube_process.terminate()
