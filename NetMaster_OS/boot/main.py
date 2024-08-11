"""
            @author Nikhil Karmakar
            @project NetMaster_OS
            @date 11-08-2024
    
    NetMaster_OS Copyright (c) 2024 
    
    NetMaster_OS is an open-source firmware for the ESP32 (also works in ESP8266 but not recommended) microcontroller.
    For the first version, it's not going to use classes or OOPs, focusing on procedural programming instead.
    
    Code Structure and Flow:
    
    - **Imports:** The code starts with necessary imports for networking, machine control, and system utilities such as garbage collection and JSON handling.
    
    - **GPIO Setup:** Basic GPIO setup is done early in the code, defining constants for the LED and DHT11 sensor pins.
    
    - **Device Information:** The code initializes device-specific constants like `DEVICE_NAME` and network configuration parameters, setting up the core identity and connectivity options.
    
    - **Core Functions:**
        - `led_on_off()` and `led_blink()` provide basic LED control for visual feedback.
        - `wifi_connect()`, `wifi_search()`, and `wifi_ap()` handle WiFi management, including connecting to existing networks, scanning for available networks, and setting up an access point.
        - `boot_screen()` displays essential system information on startup, mimicking a Linux boot screen.
        - `cmd()` processes API commands sent via the web interface, primarily for WiFi control at this stage.
        - `host_website()` is responsible for hosting the web server, which listens for incoming HTTP requests and serves appropriate responses.
    
    - **Main Execution Flow:**
        - The `main()` function orchestrates the flow of the program, starting with GPIO initialization and network setup.
        - It calls `boot_screen()` to display system info and then starts the web server by calling `host_website()`.
        - The ESP32 remains in a loop listening for client connections, responding to API commands, and controlling hardware as instructed.
    
    - **Design Philosophy:** 
        - The code is structured in a simple, linear fashion, with functions serving specific tasks to maintain clarity and ease of debugging.
        - Future versions may introduce classes and OOP concepts as the project scales, but the initial approach emphasizes a straightforward, procedural methodology.
"""


import network,time,ubinascii,uos,socket,machine,ujson
import machine,dht,gc,_thread,ubinascii
from machine import Pin, unique_id

# GPIO PIN SETUP ACCORDING TO ESP32 
GPIO_LED = 2
GPIO_DHT11 = 4
led_pin = Pin(GPIO_LED, Pin.OUT)
sensor = dht.DHT11(DHT_PIN)
led_pin = Pin(GPIO_LED, Pin.OUT)

DEVICE_NAME = "Nikhil's NetMaster_OS"

# Manually Network setup
IP_ADDR = '192.168.1.1'
GATEWAY = IP_ADDR
SUBNET = '255.255.255.0'
DNS_ONE = '8.8.8.8'
DNS_TWO = '8.8.4.4'

# Define GPIO and other constants
def led_on_off(delay=2, times=2):
    for _ in range(times):
        led_pin.on()
        time.sleep(delay)
        led_pin.off()
        time.sleep(delay)

def led_blink():
    led_on_off(delay=0.2, times=10)

def led(type=0):
    switch = {
        0: led_on_off,   # Turn on and off with a 2-second delay
        1: led_blink     # Blink with a 0.4-second delay
    }
    func = switch.get(type)
    if func:
        func()
    else:
        print("Invalid type")

def wifi_connect(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print(f'Connecting to {ssid}...')
        wlan.connect(ssid, password)
        
        timeout = 5
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
    
    if wlan.isconnected():
        ip, subnet, gateway, dns = wlan.ifconfig()
        print(f'Connected to {ssid}.')
        print(f"IP address: {ip}")
        print(f"Subnet mask: {subnet}")
        print(f"Gateway: {gateway}")
        print(f"DNS server: {dns}")
        led(1)
        return True
    else:
        print(f'Failed to connect to {ssid}.')
        led(0)
        return False

def wifi_search():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    networks = wlan.scan()

    wifi_list = []
    
    for net in networks:
        ssid = net[0].decode('utf-8')
        rssi = net[3]
        security = net[4]

        if security == 0:
            security_str = "Open"
        elif security == 1:
            security_str = "WEP"
        elif security == 2:
            security_str = "WPA-PSK"
        elif security == 3:
            security_str = "WPA2-PSK"
        elif security == 4:
            security_str = "WPA/WPA2-PSK"
        else:
            security_str = "Unknown"

        wifi_list.append({
            "ssid": ssid,
            "rssi": rssi,
            "security": security_str
        })

    return wifi_list

def wifi_ap(ssid=DEVICE_NAME, password=''):
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    
    # Configure the access point
    ap.config(essid=ssid, password=password)
    
    # Manually set IP configuration
    ap.ifconfig((IP_ADDR, SUBNET, GATEWAY, DNS_ONE))
    
    while not ap.active():
        pass
    
    print('Access Point configured:')
    print('SSID:', ap.config('essid'))
    print('IP address:', ap.ifconfig()[0])
    print('Subnet mask:', ap.ifconfig()[1])
    print('Gateway:', ap.ifconfig()[2])
    print('DNS server:', ap.ifconfig()[3])


def url_decode(encoded_str):
    replace_blank = ['%20', '&']
    decoded_str = encoded_str
    for replacement in replace_blank:
        decoded_str = decoded_str.replace(replacement, ' ')
    return decoded_str

def cmd(command):
    command = url_decode(command)  # Decode URL-encoded characters
    print("DEBUG: ", command)
    help_message = """
    WIFI HELP
        wifi connect ssid=NAME password=PASSWORD
        wifi scan <a href='/cmd/wifi?scan'>wifi scan</a>
    """
    
    if command == "help":
        return help_message
    
    # Split the command into parts
    split_command = command.split()
    
    # Check for 'wifi' commands
    if len(split_command) > 1 and split_command[0] == 'wifi':
        if split_command[1] == 'connect':
            try:
                # Extract SSID and password from the command
                ssid, password = split_command[-2], split_command[-1]
                ssid = ssid.split('=')[1]
                password = password.split('=')[1]
                print("SSID: ",ssid,password)
                
                # Check if SSID is provided
                if not ssid:
                    return "SSID is required for connecting."
                
                # Try to connect to the WiFi
                result = wifi_connect(ssid, password)
                return "Connected successfully." if result else "Failed to connect."
            except Exception as e:
                return f"Error: {e}"
        elif split_command[1] == 'scan':
            # Perform WiFi scan and format the response as JSON
            wifi_list = wifi_search()
            return ujson.dumps(wifi_list)
        else:
            return "Invalid 'wifi' command. Type '/cmd=help' for a list of available commands."
    else:
        return "Invalid command. Type '/cmd=help' for a list of available commands."

def host_website():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    
    print('Listening on', addr)
    
    while True:
        cl, addr = s.accept()
        client_ip = addr[0]  # Get the client's IP address
        print(f'Client connected from IP: {client_ip}')
        
        cl_file = cl.makefile('rwb', 0)
        
        # Read the request line
        request_line = cl_file.readline().decode('utf-8').strip()
        print(f'Request Line: {request_line}')
        
        # Read the rest of the request (headers, etc.)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
        
        # Process request
        if request_line.startswith("GET /"):
            # Extract the path from the request line
            path = request_line.split(' ')[1]  # Split and get the path
            
            if path == "/":
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html\r\n"
                    "\r\n"
                    f"Welcome to {DEVICE_NAME.upper()}.<br>"
                    "<a href='/cmd/wifi?connect&ssid=Airtel_Zeus&password=TheBestWifi'>Connect to WiFi</a><br>"
                    "<a href='/cmd/wifi?scan'>Scan WiFi Networks</a><br>"
                    "<a href='/cmd/wifi?ap&name=MyAP&password=MyPassword'>Create WiFi AP</a><br>"
                    "<a href='/cmd=help'>Click here for help</a>"
                )
            elif path.startswith("/cmd/wifi"):
                # Extract the query string from the path
                if '?' in path:
                    query_string = path.split('?')[1]
                else:
                    query_string = ''
                
                # Debug output
                print("DEBUG[Query_cmd/wifi/]: %s" % query_string)
                
                # Pass the query string to the cmd function
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/json\r\n"
                    "\r\n" +
                    cmd('wifi ' + query_string)
                )
            else:
                response = (
                    "HTTP/1.1 404 Not Found\r\n"
                    "Content-Type: text/plain\r\n"
                    "\r\n"
                    "404 Not Found: The requested resource could not be found."
                )
        else:
            response = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/plain\r\n"
                "\r\n"
                "404 Not Found: The requested resource could not be found."
            )
        
        # Send the response
        cl.send(response.encode())
        cl.close()

def boot_screen():
    boot_screen_data = []
    chip_id = ubinascii.hexlify(machine.unique_id()).decode()
    free_ram = gc.mem_free()
    flash_size = uos.statvfs('/')[1] * uos.statvfs('/')[2]
    cpu_frequency = machine.freq()
    boot_screen_data.append("Device Name:", DEVICE_NAME)
    boot_screen_data.append("Chip ID:", chip_id)
    boot_screen_data.append(f"Free RAM: {free_ram} bytes ({free_ram / 1024:.2f} KB)")
    boot_screen_data.append(f"Flash Size: {flash_size} bytes ({flash_size / 1024:.2f} KB)")
    boot_screen_data.append(f"CPU Frequency: {cpu_frequency / 1_000_000} MHz")
    
    for data in boot_screen_data:
        print(data)
        time.sleep(0.250)


# mani() : is to be called organizedly 
# Its hosting own network as per The Device name
# InBuild led will on untill the host_website

def main():
    led_pin.on()
    print("System is booting up.....")
    # Configure as an access point
    wifi_ap()
    # wifi_connect()
    time.sleep(0.5)
    # Print boot screen
    boot_screen()
    time.sleep(1)
    # Start hosting the website
    print("WiFi AP is on. Connect to the network and access the website.")
    led_pin.off()
    host_website()

# Driver Code 
main()