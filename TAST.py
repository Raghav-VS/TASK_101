import machine
import dht
import time
import urequests

# WiFi credentials
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"

# ThingSpeak API key
THINGSPEAK_API_KEY = "YOUR_THINGSPEAK_API_KEY"

# DHT sensor setup
DHT_PIN = 2  # Pin connected to the DHT sensor
dht_sensor = dht.DHT22(machine.Pin(DHT_PIN))

# Sampling interval (in seconds)
SAMPLING_INTERVAL = 30  # 30 seconds

def connect_to_wifi():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            pass
    print("WiFi connected:", wlan.ifconfig())

def send_to_thingspeak(temperature, humidity):
    url = "https://api.thingspeak.com/update"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = "api_key=" + THINGSPEAK_API_KEY + "&field1=" + str(temperature) + "&field2=" + str(humidity)
    response = urequests.post(url, data=payload, headers=headers)
    print("Response:", response.text)
    response.close()

def read_sensor_data():
    dht_sensor.measure()
    temperature = dht_sensor.temperature()
    humidity = dht_sensor.humidity()
    return temperature, humidity

def main():
    connect_to_wifi()

    while True:
        try:
            temperature, humidity = read_sensor_data()
            print("Temperature:", temperature, "°C, Humidity:", humidity, "%")
            send_to_thingspeak(temperature, humidity)
            time.sleep(SAMPLING_INTERVAL)
        except Exception as e:
            print("Error:", e)

if _name_ == "_main_":
    main()