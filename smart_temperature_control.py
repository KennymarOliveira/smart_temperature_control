import os
import sys
import serial
import struct
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6 import uic

'''
    THIS PROGRAM JUST MONITORS THE TEMPERATURE AND PRESENCE, BECAUSE I HAD NO TEMPERATURE CONTROL DEVICE TO TEST IT, BUT IT CAN BE IMPLEMENTED LATER
'''

VERSION = "0.1-alpha"

class TempMonitorMenu(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('temp_monitor_menu.ui', self)
        self.setWindowTitle(f'Temp Monitor v{VERSION}')

        # The setup button opens the configuration window
        self.setup_window = TempMonitorSetup()
        self.setup_button.clicked.connect(self.show_setup_window)

        # The start button opens the execution window
        self.execution_window = TempMonitorExecution()
        self.start_button.clicked.connect(self.show_execution_window)

    def show_setup_window(self):
        self.setup_window.show()
        self.hide()

    def show_execution_window(self):
        self.execution_window.show()
        self.hide()

class TempMonitorSetup(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('temp_monitor_setup.ui', self)
        self.setWindowTitle(f'Temp Monitor v{VERSION}')

        # Default values
        self.COM = 3
        self.temperature = 25
        self.read_setup_file()

        # Set default values for the fields
        self.com_port_text.setText(str(self.COM))
        self.temperature_text.setText(str(self.temperature))

        # Connect text change signals to validation functions
        self.com_port_text.textChanged.connect(self.validate_com_port)
        self.temperature_text.textChanged.connect(self.validate_temperature)

        # The OK button closes the setup window and opens the execution window
        self.ok_button.clicked.connect(self.show_menu_window)

    def read_setup_file(self):
        if os.path.exists('setup.txt'):
            with open('setup.txt', 'r') as setup_file:
                lines = setup_file.readlines()
                for line in lines:
                    line = line.strip()
                    if line.startswith('com_port='):
                        self.COM = int(line.split('=')[1])
                    elif line.startswith('temperature='):
                        self.temperature = int(line.split('=')[1])

    def update_setup_file(self):
        try:
            with open('setup.txt', 'w') as setup_file:
                setup_file.write(f'com_port={self.COM}\n')
                setup_file.write(f'temperature={self.temperature}')
        except Exception as e:
            print("Error updating setup.txt configuration file:", e)

    def validate_com_port(self, text):
        try:
            if not text:
                self.com_port_label.setStyleSheet("QLabel { color: red; }")
            elif not text.isdigit():
                self.com_port_label.setStyleSheet("QLabel { color: white; }")
                self.com_port_text.setText(text[:-1])
            else:
                self.com_port_label.setStyleSheet("QLabel { color: white; }")
                self.COM = int(text)
                self.update_setup_file()
        except Exception as e:
            print("Error updating com_port:", e)

    def validate_temperature(self, text):
        try:
            if not text:
                self.set_temperature_label.setStyleSheet("QLabel { color: red; }")
            elif not text.isdigit():
                self.set_temperature_label.setStyleSheet("QLabel { color: white; }")
                self.temperature_text.setText(text[:-1])
            else:
                self.set_temperature_label.setStyleSheet("QLabel { color: white; }")
                self.temperature = int(text)
                self.update_setup_file()
        except Exception as e:
            print("Error updating temperature:", e)

    def show_menu_window(self):
        if self.com_port_text.text() and self.temperature_text.text():
            menu_window.show()
            self.close()

class TempMonitorExecution(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('temp_monitor_execution.ui', self)
        self.setWindowTitle(f'Temp Monitor v{VERSION}')

        # Set initial information
        self.com_port.setText("None")
        self.presence.setText("None")
        self.target_temperature.setText("None")
        self.temperature.setText("None")
        self.start_stop_button.setText("Start")
        self.status.setText("None")

        # The back button opens the menu window
        self.back_button.clicked.connect(self.show_menu_window)

        # The Start/Stop button starts or stops the thread execution
        self.start_stop_button.clicked.connect(self.start_stop_button_handler)

        # Thread configuration
        self.Thread_1 = Thread_1()
        self.Thread_1.info_update_signal.connect(self.info_update_slot)

    def info_update_slot(self, com_port, presence, temperature, target_temperature):
        str_presence = "HIGH" if presence == "1" else "LOW"
        str_status = "ON" if temperature != target_temperature else "OFF"

        self.com_port.setText(com_port)
        self.presence.setText(str_presence)
        self.temperature.setText(temperature)
        self.target_temperature.setText(target_temperature)
        self.status.setText(str_status)

    def start_stop_button_handler(self):
        if not self.Thread_1.isRunning():
            self.Thread_1.start()
            self.start_stop_button.setText("Stop")
        else:
            self.Thread_1.stop()
            self.start_stop_button.setText("Start")

    def show_menu_window(self):
        menu_window.show()
        self.close()

class Thread_1(QThread):
    info_update_signal = pyqtSignal(str, str, str, str)

    def __init__(self):
        super().__init__()
        self.ThreadActive = True
        self.mutex = QMutex()
        
        self.COM = 3
        self.target_temperature = 25
        self.presence = None
        self.temperature = None

        if os.path.exists('setup.txt'):
            with open('setup.txt', 'r') as setup_file:
                lines = setup_file.readlines()
                for line in lines:
                    line = line.strip()
                    if line.startswith('com_port='):
                        self.COM = int(line.split('=')[1])
                    elif line.startswith('temperature='):
                        self.target_temperature = int(line.split('=')[1])

    def run(self):
        serial_info = serial.Serial(f'COM{self.COM}', 9600, timeout=0.2)
        if not serial_info.isOpen():
            serial_info.open()
        serial_info.write(struct.pack('B', self.target_temperature))

        while self.ThreadActive:
            if serial_info.in_waiting > 0:
                info = serial_info.readline().decode('utf-8').strip()

                '''

                    THIS INFO CAN BE USED TO CONTROL ANOTHER DEVICE WITH THE FOLLOWING STRUCTURE:

                    presence_str, temperature_str = info.split(",")
                    self.presence = presence_str
                    self.temperature = temperature_str
                    if self.presence == "1" and self.temperature != self.target_temperature:
                        # Send command to adjust temperature
                    
                '''

                try:
                    presence_str, temperature_str = info.split(",")
                    self.presence = presence_str
                    self.temperature = temperature_str
                    self.info_update_signal.emit(str(self.COM), self.presence, self.temperature, str(self.target_temperature))
                except ValueError:
                    print("Received information is not properly formatted")

    def stop(self):
        with QMutexLocker(self.mutex):
            self.ThreadActive = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu_window = TempMonitorMenu()
    menu_window.show()
    sys.exit(app.exec())
