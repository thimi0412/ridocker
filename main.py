import subprocess
from subprocess import Popen
import threading
import sys
from pydub import AudioSegment
from pydub.playback import play

class Hoge():

    def __init__(self):
        self.stop_event = threading.Event() #停止させるかのフラグ
        self.inc_event = threading.Event()  #刻み幅を増やすかのフラグ

        #スレッドの作成と開始
        self.thread_1 = threading.Thread(target=self.exec)
        self.thread_2 = threading.Thread(target=self.run_mp3, args=('mp3/build1.mp3',))
        self.thread_3 = threading.Thread(target=self.run_mp3, args=('mp3/build2.mp3',))
        self.thread_4 = threading.Thread(target=self.retry)
        self.thread_1.start()
        self.thread_2.start()
        self.thread_2.join()
        self.thread_3.start()
        self.thread_3.join()
        self.thread_4.start()

    def run_mp3(self, path):
        sound = AudioSegment.from_file(path, 'mp3')
        play(sound)

    def exec(self):
        cmd = "docker-compose build --no-cache"
        popen = Popen(cmd, shell=True)
        popen.wait()
        self.stop()

    def retry(self):
        sound = AudioSegment.from_file('mp3/build3.mp3', 'mp3')
        while not self.stop_event.is_set():
            play(sound)

    def stop(self):
        self.stop_event.set()
        self.thread_4.join()    #スレッドが停止するのを待つ
        self.run_mp3('mp3/build4.mp3')

    def inc(self):
        """targetで出力する数字の刻み幅を増やすフラグを立てる"""
        self.inc_event.set()

if __name__ == '__main__':
    h = Hoge()