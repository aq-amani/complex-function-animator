import os
import subprocess
import configparser
from datetime import datetime

def main():
    config = configparser.ConfigParser()
    config.read('./config.ini')

    FRAMES_PATH = config['GLOBAL']['FRAMES_PATH']
    VIDEO_PATH = config['GLOBAL']['VIDEO_PATH']

    video_filename = datetime.now().strftime("%Y%m%d_%H%M%S")

    start_time = datetime.now()
    print(f'{start_time.strftime("%Y-%m-%d %H:%M:%S")} Creating video from frames using ffmpeg..')

    subprocess.call(['ffmpeg', '-r', '30', '-f', 'image2', '-i', f'{FRAMES_PATH}%d.png', '-qscale', '0', f'{VIDEO_PATH}{video_filename}.avi', '-hide_banner', '-loglevel', 'error'])
    finish_time = datetime.now()
    print(f'{finish_time.strftime("%Y-%m-%d %H:%M:%S")} Done.')

if __name__ == '__main__':
    main()
