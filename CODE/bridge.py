import serial
import time

# Configure these ports for your system
ESP32_PORT = 'COM5'    # ESP32's serial port
ARDUINO_PORT = 'COM7'  # Display Arduino's serial port
BAUD_RATE = 9600

def main():
    # Initialize serial connections
    esp32 = serial.Serial(ESP32_PORT, BAUD_RATE, timeout=1)
    arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
    
    # Allow ports to initialize
    time.sleep(2)
    
    print("Bridge script running. Press Ctrl+C to exit.")
    
    try:
        while True:
            # Read line from ESP32
            if esp32.in_waiting:
                line = esp32.readline().decode('utf-8').strip()
                
                # Check for detection line
                if line.startswith("Detected: "):
                    label = line.split("Detected: ")[1]
                    print(f"Forwarding: {label}")
                    
                    # Send to Arduino display
                    arduino.write(f"{label}\n".encode('utf-8'))
                    
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        esp32.close()
        arduino.close()

if __name__ == "__main__":
    main()