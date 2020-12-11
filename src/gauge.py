import sys
import time
import RPi.GPIO as GPIO
import array as arr
import time
import board
import neopixel
from stage import Stage

class Gauge:
    pixelPin = board.D18
    numPixels = 45
    # number of degrees each LED light occupies in the ring
    pixelWidthAngle = 6

    gaugeNumbers = arr.array('d',[0, 20, 75,  300, 500])
    gaugeAngles = arr.array('d', [0, 50, 134, 222, 270])

    # Stepper motor settings
    stepPins = [17,22,23,24]

    # motor rated at 4096 steps in 360 degrees
    stepAngle = 360 / float(4096)
    waitTime = 2/float(1000)

    # half step sequence for stepper
    seq = [[1,0,0,1],
       [1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1]]

    # Color scheme
    downloadGaugeColorA = (1, 163, 229)
    downloadGaugeColorB = (25, 191, 120)

    uploadGaugeColorA = (107, 50, 149)
    uploadGaugeColorB = (233, 123, 206)

    latencyGaugeColorA = (235, 221, 80)
    latencyGaugeColorB = (31, 164, 233)

    def __init__(self, pixels):
        GPIO.setmode(GPIO.BCM)

        self.pixels = pixels

        for pin in self.stepPins:
          GPIO.setup(pin,GPIO.OUT)
          GPIO.output(pin, False)

        self.currentPixelNum = 0
        self.currentPixelAngle = 0
        self.currentAngle = 0
        self.stepCount = len(self.seq)

        self.__ShowColorWheel()

    def __ShowColorWheel(self):
        colorA = self.latencyGaugeColorA
        colorB = self.latencyGaugeColorB
        for i in range (0, self.numPixels):
            self.pixels[i] = (self.__GetColorFromRange(i, 0, self.numPixels, colorA[0], colorB[0]), 
                              self.__GetColorFromRange(i, 0, self.numPixels, colorA[1], colorB[1]), 
                              self.__GetColorFromRange(i, 0, self.numPixels, colorA[2], colorB[2]))
            self.pixels.show()
            time.sleep(0.024)

        for i in range (0, self.numPixels):
            self.pixels[i] = (0,0,0)
            self.pixels.show()
            time.sleep(0.024)

    def __GetColorValue(self, index, currentPixel, stage):
        colorA = self.downloadGaugeColorA if stage is Stage.Download else self.uploadGaugeColorA
        colorB = self.downloadGaugeColorB if stage is Stage.Download else self.uploadGaugeColorB
        return self.__GetColorFromRange(currentPixel, 0, self.numPixels, colorA[index], colorB[index])

    def __GetColorFromRange(self, value, leftMin, leftMax, rightMin, rightMax):
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        valueScaled = float(value - leftMin) / float(leftSpan)
        return int(rightMin + (valueScaled * rightSpan))

    def MoveToMbps(self, stage, speed):
        newAngle = self.__calculateAngleFromMbps(speed)
        # bail if the difference is small to prevent needle from jittering
        if (abs(self.currentAngle - newAngle) < 6):
            return

        stepCounter = 0
        stepAngleCurrent = 0

        dir = -1 if self.currentAngle > newAngle else 1
        shouldBreak = False

        # move the needle and colors to the right place
        while True:
          for pin in range(0, 4):
            xpin = self.stepPins[pin]
            if self.seq[stepCounter][pin]!=0:
              GPIO.output(xpin, True)
            else:
              GPIO.output(xpin, False)

          #increment angle for 1 step
          self.currentAngle += self.stepAngle * dir
          #set to next step
          stepCounter += dir

          self.__updateLights(dir, stage)

          if (dir < 0 and self.currentAngle <= newAngle):
              shouldBreak = True
          elif (dir > 0 and self.currentAngle > newAngle):
              shouldBreak = True

          if (stepCounter>=self.stepCount):
            stepCounter = 0
            if shouldBreak:
                break
          if (stepCounter<0):
            stepCounter = self.stepCount+dir
            if shouldBreak:
                break

          # Wait before moving on
          time.sleep(self.waitTime)

    def __updateLights(self, dir, stage):
        if (abs(self.currentAngle - self.currentPixelAngle) >= self.pixelWidthAngle):
            self.pixels[self.currentPixelNum] = (self.__GetColorValue(0, self.currentPixelNum, stage), self.__GetColorValue(1, self.currentPixelNum, stage), self.__GetColorValue(2, self.currentPixelNum, stage)) if dir == 1 else (0,0,0)

            self.pixels.show()
            self.currentPixelNum += dir
            self.currentPixelNum = min(self.numPixels-1, self.currentPixelNum)
            self.currentPixelAngle = self.currentAngle

    def __calculateAngleFromMbps(self, mbps): 
      if (mbps <= 0):
        return self.gaugeAngles[0]

      indexLow = 0
      for i in range(len(self.gaugeNumbers)):
        if (self.gaugeNumbers[i] > mbps):
          indexLow = max(0, i-1)
          break

      indexHigh = min(len(self.gaugeAngles), indexLow+1)
      A = self.gaugeNumbers[indexLow]
      B = self.gaugeNumbers[indexHigh]
      C = self.gaugeAngles[indexLow]
      D = self.gaugeAngles[indexHigh]

      angle = C + (mbps - A) * (D - C) / (B - A)
      angle = min(angle, self.gaugeAngles[len(self.gaugeAngles)-1])
      
      return angle

    def Complete(self):
        self.MoveToMbps(Stage.Upload, 0)
        self.ResetLights()

    def ResetLights(self):
        for i in range(0, self.numPixels):
            self.pixels[i] = (0,0,0)

        self.pixels.show()


