from speedtest import Speedtest
from gauge import Gauge
import os
import sys
from queue import Queue
from threading import Thread
import time
from button import Button
import RPi.GPIO as GPIO
import neopixel
import board

def runTest(neopixels):
    queue = Queue() 
    speedtest = Speedtest(queue)
    speedtest.start()

    gauge = Gauge(neopixels)

    # read speed from test and update gauge
    (stage, _) = queue.get(True, 10)
    while not speedtest.isDone:
        try:
            (currentStage, speed) = queue.get(True, 4)

            # move gauge to 0 after the previous stage
            if (currentStage != stage):
                gauge.MoveToMbps(stage, 0)
                gauge.ResetLights()
                time.sleep(1)

            gauge.MoveToMbps(currentStage, speed)
            stage = currentStage
        except Exception:
            break


    speedtest.Complete()
    gauge.Complete()


def main(argv):
    GPIO.cleanup()

    # Single neopixel library instance
    maxPixels = 45
    neopixels = neopixel.NeoPixel(board.D18, maxPixels, brightness=0.5, auto_write=True, pixel_order=neopixel.RGB)

    button = Button()

    while True:
        # check button press blocking with timeout of 3 seconds
        if button.WaitForPress(3000):
            runTest(neopixels)

    button.Complete()

if __name__ == "__main__":
     main(sys.argv[1:])
