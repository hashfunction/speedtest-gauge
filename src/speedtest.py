import sys
import time
import subprocess
import os
import re
from stage import Stage
from queue import Queue
from threading import Thread

class Speedtest(Thread):
    def __init__(self,queue):
        super(Speedtest, self).__init__()
        self.queue = queue
        self.isDone = False

    def run(self):
        stage = Stage.Download
        
        self.process = subprocess.Popen(['unbuffer', "speedtest"], bufsize=0, shell=False, stdout=subprocess.PIPE, universal_newlines=True)

        while True:
            output = ""
            try:
              output = self.process.stdout.read(30)
            except Exception as e:
              #ignore any errors reading
              print(e)
              pass

            if self.process.poll() != None:
                break

            if output != '':

                dlResult = re.search("Download:(.*)Mbps", output)
                ulResult = re.search("Upload:(.*)Mbps", output)

                if (ulResult and ulResult.group(1)):
                    if (stage == Stage.Download):
                        stage = Stage.Upload
                    self.__invoke(ulResult, stage)

                if (dlResult and dlResult.group(1)):
                    self.__invoke(dlResult, stage)

        self.isDone = True

    def __invoke(self, result, stage):
        spd = float(result.group(1).strip())
        self.queue.put((stage, spd))

    def Complete(self):
        if self.process:
            self.process.terminate()

