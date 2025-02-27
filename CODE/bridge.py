import serial
import time

# Configure these ports for your system
ESP32_PORT = 'COM5'    # ESP32's serial port
# ARDUINO_PORT = 'COM7'  # Display Arduino's serial port
BAUD_RATE = 9600

def main():
    try:
        # Initialize serial connection to the ESP32 with hardware flow control turned off
        esp32 = serial.Serial(
            port=ESP32_PORT,
            baudrate=BAUD_RATE,
            timeout=2,       # Increased timeout for proper reading
            rtscts=False,    # Disable RTS/CTS hardware flow control
            dsrdtr=False     # Disable DSR/DTR hardware flow control
        )
        # Disable DTR and RTS to prevent the ESP32 from auto-resetting on port open
        esp32.setDTR(False)
        esp32.setRTS(False)
        
        # Allow extra time for the ESP32 to boot and start sending data
        time.sleep(5)
        # Clear any stale data in the input buffer
        esp32.reset_input_buffer()

        # --- Uncomment these lines when ready to connect to the Arduino display ---
        # arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
        # time.sleep(2)  # Allow the Arduino port to initialize
        # ----------------------------------------------------------------------------

        print("Bridge script running. Press Ctrl+C to exit.")
        print(f"Connected to ESP32 on {ESP32_PORT}")
        # If using Arduino, you can un-comment the next line:
        # print(f"Connected to Arduino on {ARDUINO_PORT}")
        
        while True:
            if esp32.in_waiting > 0:
                raw_data = esp32.readline()  # Read raw bytes from ESP32
                try:
                    line = raw_data.decode('utf-8').strip()
                except UnicodeDecodeError:
                    # Fallback decoding if needed
                    line = raw_data.decode('latin1').strip()
                
                if line:  # If there's valid data
                    print(f"Received from ESP32: {line}")
                    # --- Forward to Arduino display (uncomment when needed) ---
                    # print(f"Forwarding to Arduino: {line}")
                    # arduino.write(f"{line}\n".encode('utf-8'))
                    # ----------------------------------------------------------------
            else:
                print("No data waiting from ESP32.")
            time.sleep(1)  # Slow down loop to avoid flooding the console

    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'esp32' in locals() and esp32.is_open:
            esp32.close()  # Close the ESP32 serial connection cleanly
            print("ESP32 serial port closed.")
        # --- If using Arduino, close its connection as well ---
        # if 'arduino' in locals() and arduino.is_open:
        #     arduino.close()
        #     print("Arduino serial port closed.")

if __name__ == "__main__":
    main()
