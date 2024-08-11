"""
            @author Nikhil Karmakar
            @project NetMaster_OS
            @date 12-08-2024
            
    Copyright (c) 2024 @author 

    This code is designed to interface with a DHT11 sensor connected to an ESP32 microcontroller. 
    It reads temperature and humidity data from the sensor and then hosts a web server on the ESP32. 
    The web server serves a webpage that displays the live sensor data. 

    The webpage continuously fetches the latest temperature and humidity readings from the ESP32 
    using an API endpoint provided by the server. The sensor data is updated in real-time on the webpage, 
    giving users a live view of the environmental conditions.
    
"""



import usocket as socket
from machine import Pin
import gc,ujson,machine,uos,ubinascii,time,_thread,dht,network

# Wi-Fi connection details
SSID = 'SSID'
PASSWORD = 'PASSWORD'

DEVICE_NAME = "Nikhils ESP32"
GPIO_DHT11 = 4  # D4 pin
GPIO_LED = 2

# Initialize DHT11 sensor
DHT_PIN = Pin(GPIO_DHT11)  # Replace with your correct GPIO pin
sensor = dht.DHT11(DHT_PIN)
led_pin = Pin(GPIO_LED, Pin.OUT)

# Manually Network setup
IP_ADDR = '192.168.1.1'
GATEWAY = IP_ADDR
SUBNET = '255.255.255.0'
DNS_ONE = '8.8.8.8'
DNS_TWO = '8.8.4.4'


# HTML webpage with basic CSS
# HTML content
HTML_PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Live Temperature and Humidity</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .backgroundColor {
            background-color: #2f2f2f;
        }
        .container {
            text-align: center;
            max-width: 550px;
            width: 100%;
        }
        h1 {
            color: #333;
        }
        .data-container {
            margin-top: 20px;
        }
        .data-item {
            color: white;
            font-size: 2em;
            background-color: #171717;
            border: 1px solid #ddd;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            font: "Hawaii 5-0, sans-serif";
        }
        .wifi-connected {
            color: green;
        }
        .wifi-disconnected {
            color: red;
        }
    </style>
</head>
<body class="backgroundColor">
    <div class="container backgroundColor">
        <i id="wifiIcon" class="fa fa-wifi fa-2x wifi-disconnected"></i>
        <h1 style="color: white;">Temp & Humidity</h1>
        <div class="data-container">
            <div id="heat" class="data-item">Fetching temperature...</div>
            <div id="humi" class="data-item">Fetching humidity...</div>
        </div>
    </div>
    <script>
        const wifiIcon = document.getElementById('wifiIcon');

        let lastDataReceivedTime = Date.now();

        function resetDataIfNoUpdate() {
            const currentTime = Date.now();
            if (currentTime - lastDataReceivedTime >= 3000) {
                updateUI({
                    temperature: '0',
                    humidity: '0'
                });
                wifiIcon.classList.remove('wifi-connected');
                wifiIcon.classList.add('wifi-disconnected');
            }
        }

        const API_URL = '/dht11';

        function fetchData() {
            const xhr = new XMLHttpRequest();
            xhr.open('GET', API_URL, true);
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    lastDataReceivedTime = Date.now();
                    console.log("Received data:", xhr.responseText);
                    try {
                        const rawData = JSON.parse(xhr.responseText);
                        console.log("Parsed data:", rawData);
                        const modifiedData = {
                            temperature: rawData['temperature'] !== undefined ? `${rawData['temperature']}°C` : 'N/A',
                            humidity: rawData['humidity'] !== undefined ? `${rawData['humidity']}%` : 'N/A'
                        };
                        updateUI(modifiedData);
                        wifiIcon.classList.remove('wifi-disconnected');
                        wifiIcon.classList.add('wifi-connected');
                    } catch (error) {
                        console.error("Error parsing data:", error);
                    }
                } else {
                    wifiIcon.classList.remove('wifi-connected');
                    wifiIcon.classList.add('wifi-disconnected');
                }
            };
            xhr.send();
        }

        setInterval(fetchData, 1000);
        setInterval(resetDataIfNoUpdate, 1000);

        function updateUI(data) {
            document.getElementById('heat').innerText = `Temperature: ${data.temperature}`;
            document.getElementById('humi').innerText = `Humidity: ${data.humidity}`;
        }
    </script>
</body>
</html>
"""

# Error page HTML
ERROR_PAGE = """<!DOCTYPE html>
<html>
<head>
    <title>404 Not Found</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        h1 { font-size: 50px; color: #FF6347; }
        p { font-size: 20px; }
    </style>
</head>
<body>
    <h1>404</h1>
    <p>Page not found</p>
</body>
</html>
"""

def led_on_off(delay=2, times=2):
    for _ in range(times):
        led_pin.on()
        time.sleep(delay)
        led_pin.off()
        time.sleep(delay)

def connect_wifi(ssid, password):
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
        return True
    else:
        print(f'Failed to connect to {ssid}.')
        return False

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

def read_dht11():
    try:
        sensor.measure()  # Trigger a measurement
        temp = sensor.temperature()  # Get the temperature in Celsius
        humi = sensor.humidity()  # Get the humidity percentage
        return temp, humi
    except OSError as e:
        print('Failed to read sensor.')
        return None, None

def host_socket():
    """Host the main web server on the ESP32."""
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(5)
    print('Hosting web server on', addr)

    while True:
        cl, addr = s.accept()
        print('Client connected from', addr)
        request = cl.recv(1024)
        request = str(request)

        if 'GET /dht11' in request:
            temp, humi = read_dht11()
            if temp is not None and humi is not None:
                # Prepare JSON response
                response = {
                    'temperature': temp,
                    'humidity': humi
                }
                response = ujson.dumps(response)
                http_response = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n' + response
            else:
                response = 'Failed to retrieve data from sensor.'
                http_response = 'HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\n\r\n' + response
        elif 'GET /' in request:
            # Serve the HTML content
            http_response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + HTML_PAGE
        else:
            # Handle 404 Not Found
            http_response = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n' + ERROR_PAGE

        cl.send(http_response)
        cl.close()


def start_server():
    """Start the web server."""
    _thread.start_new_thread(host_socket, ())

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

# Main function
def main():
    print("Starting.........")
    led_pin.on()
    boot_screen()
    time.sleep(1)
    wifi_ap() # Host its own network 
    # Or, U can configure the Wifi ssid and password
    # connect_wifi(SSID, PASSWORD)
    
    time.sleep(1)
    start_server()
    led_pin.off()

# Run the main function
main()
