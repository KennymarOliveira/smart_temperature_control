## This project has the general objective of developing an automated temperature control system of a room/location, using presence sensors PIR, DHT11 temperature and humidity sensors and an Arduino UNO board.

### How it works?

The system constantly monitors data from both sensors and identifies if there is someone in the room/location. If there is, the system verifies a pre-defined temperature to adjust the room temperature according to it.

**Note:** The room temperature control could not be finished yet, because I do not have access to any temperature control device at this moment, but it will be added. There is already a part of the code in the "smart_temperature_control.py" file.

### How to use it to monitor?

- Download the latest release, run and set the COM port in the setup window according to your COM Port in the Arduino IDE. [Tutorial here.](https://support.arduino.cc/hc/en-us/articles/4406856349970-Select-board-and-port-in-Arduino-IDE)
- Set your target temperature in the setup window.
- Copy the code in the file "smart_temperature_control.cpp" to your Arduino IDE and run.
- Start the execution to see the colected data.
