# Treat Yourself to a Hack Day: Make a Physical Speedtest Gauge

Sure you love taking a Speedtest, but have you ever seen the results manifest in a 3D statue that lives on your desk? Now’s your chance. This repo contains everything you need to construct and program an ethernet-enabled physical Speedtest Gauge. All you’ll need to build it is access to a 3D printer, some affordable and easy-to-find parts, and a basic working knowledge of both electronics and command line interface (CLI) tools. Then you can proudly display your Speedtest gauge on your desk or gift it to a friend who also loves to nerd out over networks. Either way, you’ll have the most fun setup for measuring network throughput in town.

![Speedtest Gauge](gauge.jpg?raw=true "Speedtest Gauge")

## Components you’ll need
The total cost of all the components below is around $65, and the project will take about two or three hours to complete, not counting the time to 3D print the enclosure. 

This project requires the following components to work:

* A soldering iron. A basic one should do fine. 
* [Jumper wires](https://smile.amazon.com/REXQualis-120pcs-Breadboard-Arduino-Raspberry/dp/B072L1XMJR) to connect the various components together.
* A stepper motor. This project used [this model](https://smile.amazon.com/ELEGOO-28BYJ-48-ULN2003-Stepper-Arduino/dp/B01CP18J4A/) but feel free to upgrade to a better one. The limitation of this one is that the max speed is slow and so the gauge needle is not very quick.
* Programmable LED lights. This project uses [three neopixel ring lights](https://www.adafruit.com/product/1768). Note that you will need three of these to form the full gauge. You can find cheaper versions of this ring elsewhere.
* Physical buttons. A good candidate for buttons are these [mini push buttons](https://smile.amazon.com/gp/product/B0752RMB7Q/). 
* A [Raspberry Pi](https://www.adafruit.com/category/105). This drives the LED lights as well as the motor and runs the actual test. 
* A good [power source](https://smile.amazon.com/Raspberry-Power-Supply-Off-Switch/dp/B083JCL6H2) for the Raspberry Pi. 
* The 3D-printed housing. The housing and needle are where you finally get to put everything together. The STL printable files can be found on this GitHub project. 
* The free [Speedtest CLI](https://www.speedtest.net/apps/cli). The latest version of the official Speedtest CLI is used to actually run the network performance test. 
* Unbuffer. This is needed to parse the Speedtest CLI output. You can install it by running ```apt-get install expect```

## How to assemble your Speedtest gauge

* Step 1: Print out the housing using a 3D printer. The instructions can be found in this GitHub project. 

* Step 2: Attach the stepper motor to the center of the 3D-printed housing. Then attach the stepper motor driver to the motor, attach the +5V and GND on the controller to the appropriate Raspberry Pi GPIO pin. 

* Step 3: Attach the needle to the tip of the stepper motor. You can snap them together with some glue. 

* Step 4: Connect the controller to the Raspberry Pi with the following GPIO mappings:

    > IN1 to GPIO17
    > IN2 to GPIO22
    > IN3 to GPIO23
    > IN4 to GPIO24

* Step 5: Solder the neopixel rings per [this guide](https://learn.adafruit.com/neopixel-60-ring-clock/circuit-diagram) on Adafruit. Note that we will be using three segments only. After that, connect the +5V and GND on the neopixel lights to the +5V and GND on the Raspberry Pi. Then connect the data line to GPIO18 on the Raspberry Pi. 

* Step 6: Inset the neopixel ring into the gauge indent. You can use sticky tape or soft glue to hold it in place. 

* Step 7: Insert the button in the button hold in the bottom left corner of the front housing. Solder two wires to the connections at the back of the button and attach one lead to GPIO1 (3.3v) on the Raspberry Pi and the other to GPIO10.

* Step 8: Use the extra space in the back where the Raspberry Pi ports are accessible to pass through the power cable and plug it into the Raspberry Pi. 

## Use the software to run Speedtest

The software you’ll need to power your new Speedtest gauge is available on this [GitHub repository](https://github.com/hashfunction/speedtest-gauge) and can be downloaded for non-commercial use. The main sections control the LED lights, the stepper motor and run the CLI test. You can pull this code on the Raspberry Pi and set it to run on startup. Make sure you set the SD Card to read-only mode to prevent data corruption due to reboots.

The following components control the gauge: 

* speedtest.py. This runs the Speedtest CLI app and parses and returns the speed measurements as well as the current stage
* gauge.py. This class takes in the current speed and calculates and moves the needle to the angle represented by the speed. It also lights up the LED based on the position of the needle. 
* button.py. This simple wrapper handles events from the button, which runs the test. 
* run.py. The root file listens to the button events and coordinates between the Speedtest and gauge movement. 


To set up the gauge, load the repo on the device and run the code below. Note that sudo is required to access the GPIO ports on the Raspberry Pi. 

```sudo python3 run.py```

Note that you can use the src/speedtest_bootup.service (change the script location) to always start the software on reboot. 

There you have it! Your very own Speedtest gauge. Share your pictures with us on Twitter or Facebook using the hashtag #SpeedtestGauge.


