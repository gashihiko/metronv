from playsound import playsound
# playsound=1.2.2 is required due to a bug in 1.3.0
import time
import wave
import contextlib
from pathlib import Path


class Wav:
    def __init__(self, path: str):
        self.path = path
        self.duration = self.calc_duration()

    def calc_duration(self):
        with contextlib.closing(wave.open(self.path, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / rate
            return duration

    def play(self):
        playsound(self.path)


class MetronV:
    rpm = 80

    def __init__(self, directory: str):
        self.dir = directory
        self.voice = dict()
        self.interval = dict()

        for i in range(1, self.rpm+1):
            self.voice[i] = Wav(f'{self.dir}/{i}.wav')
            self.interval[i] = 60 / self.rpm - self.voice[i].duration - 0.05 # 0.05 seconds of loss during each loop process
            if self.interval[i] < 0:
                self.interval[i] = 0

    def ready(self):
        for i in range(3, 0, -1):
            print(i)
            self.voice[i].play()
            interval = 1 - self.voice[i].duration
            if interval < 0:
                interval = 0
            time.sleep(interval)
        time.sleep(1)

    def count_up(self):
        for i in range(1, self.rpm+1):
            self.voice[i].play()
            time.sleep(self.interval[i])


if __name__ == '__main__':
    metan = MetronV(Path(__file__).parent.resolve() / 'numvoice')
    metan.ready()
    start = time.time()
    metan.count_up()
    print(f'{time.time() - start:.2f}')
