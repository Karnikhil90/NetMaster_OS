### NetMaster_OS

NetMaster_OS is an open-source firmware designed for the ESP32 microcontroller (and optionally for the ESP8266, though it's not recommended). The project, developed by Nikhil Karmakar, focuses on providing a powerful yet easy-to-use platform for managing and controlling various functionalities of the ESP32 via a web interface.

#### Overview

NetMaster_OS is built with the intention of allowing full control of the ESP32 through a web-based API. The current version focuses on setting up and managing WiFi connections, controlling GPIO pins, and reading sensor data (like from the DHT11). As the project evolves, the goal is to add more advanced features, including support for additional sensors, software updates over-the-air (OTA), and integration with an SD card module for data storage.

#### Features

- **WiFi Management:**  
  - Connect to a WiFi network using SSID and password via an API.
  - Scan for available WiFi networks and retrieve their SSID, RSSI, and security status.
  - Set up the ESP32 as a WiFi access point with a custom SSID.

- **GPIO Control:**  
  - Basic control of GPIO pins, such as turning an LED on and off, with options for different blink patterns.

- **Boot Screen:**  
  - Displays vital system information at startup, including device name, chip ID, available RAM, flash size, and CPU frequency.

- **Web Interface:**  
  - Hosts a simple website directly on the ESP32, providing links to various WiFi commands and system functionalities.
  - API-based command execution through a web interface.

#### Future Development

- **API Expansion:**  
  - Addition of more commands to the existing API, allowing for broader control of the ESP32.
  
- **Sensor Integration:**  
  - Support for additional sensors, easily configurable through the web interface.

- **SD Card Module Support:**  
  - Integration with an SD card module to enable data storage and retrieval, adding more flexibility to the system.

- **Over-the-Air (OTA) Updates:**  
  - Enabling firmware updates over WiFi, allowing for easy deployment of new features and bug fixes without requiring a physical connection to the device.

#### Requirements

To use and develop for NetMaster_OS, you will need the following:

1. **Thonny IDE:**  
   Thonny is a user-friendly IDE that simplifies the process of writing, running, and debugging MicroPython code on microcontrollers like the ESP32.

   Download Thonny from the official website: [Thonny.org](https://thonny.org)

2. **MicroPython Firmware:**  
   NetMaster_OS is based on MicroPython, a lean implementation of Python 3 designed to run on microcontrollers. You'll need to flash your ESP32 with MicroPython before uploading the NetMaster_OS code.

   You can download the latest MicroPython firmware from the official site: [MicroPython.org](https://micropython.org)

3. **ESP32 Microcontroller:**  
   This project is designed primarily for the ESP32 microcontroller. An ESP8266 may work, but it's not recommended due to performance limitations.

#### How to Use

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/YourGitHubUsername/NetMaster_OS.git
   cd NetMaster_OS
   ```

2. **Flash MicroPython Firmware:**
   Use `esptool.py` or a similar tool to flash the MicroPython firmware onto your ESP32. You can also use the Thonny IDE to manage this process.

3. **Upload the Code Using Thonny:**
   Open the NetMaster_OS project in Thonny and upload the code to your ESP32.

4. **Boot and Connect:**
   Upon booting, the ESP32 will attempt to connect to a predefined WiFi network or create an access point. You can then connect to the network and access the web interface.

5. **Control and Configure:**
   Use the web interface to execute commands, control GPIO pins, and manage the WiFi connections. More features will be added as the project evolves.

#### Contributing

Feel free to fork this repository and contribute to the development of NetMaster_OS. Whether it's bug fixes, new features, or documentation improvements, your contributions are welcome!

#### License

This project is licensed under the Apache License 2.0. Please see the `LICENSE` file for more details.

