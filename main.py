import subprocess
import os
from subprocess import Popen
import threading
import sys
from pydub import AudioSegment
from pydub.playback import play

HOME_DIR = os.environ['HOME']
MP3_1_DIR = HOME_DIR + '/mp3/build1.mp3'
MP3_2_DIR = HOME_DIR + '/mp3/build2.mp3'
MP3_3_DIR = HOME_DIR + '/mp3/build3.mp3'


class Ridocker:

    def __init__(self):
        self.stop_event = threading.Event() #停止させるかのフラグ

        #スレッドの作成と開始
        self.thread_1 = threading.Thread(target=self.exec)
        self.thread_2 = threading.Thread(target=self.run_mp3, args=(MP3_1_DIR,))
        self.thread_3 = threading.Thread(target=self.retry)

    def run_mp3(self, path):
        sound = AudioSegment.from_file(path, 'mp3')
        play(sound)

    def exec(self):
        cmd = "docker-compose build"
        popen = Popen(cmd, shell=True)
        popen.wait()
        self.stop()

    def retry(self):
        sound = AudioSegment.from_file(MP3_2_DIR, 'mp3')
        while not self.stop_event.is_set():
            play(sound)

    def stop(self):
        self.stop_event.set()
        self.thread_3.join()    #スレッドが停止するのを待つ
        self.run_mp3(MP3_3_DIR)

if __name__ == '__main__':
    h = Ridocker()
    
    h.thread_2.start()
    h.thread_2.join()
    h.thread_3.start()
    h.thread_1.start()