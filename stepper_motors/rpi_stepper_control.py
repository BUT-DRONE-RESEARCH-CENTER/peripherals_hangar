import serial
import time

# TODO: test the maximum safe feedrate for the motors
MAX_FEEDRATE = 1000  # Maximum feedrate for the CNC machine, units in mm/min (probably)


# Function to open the door
def open_door(ser):
    """
    This motion is stopped automatically by the GRBL firmware when the endstop is triggered.
    :param ser:
    :return:
    """
    # Move the motors towards the endstops
    send_gcode(ser, f"G1 X100 Y100 Z100 F{MAX_FEEDRATE}")  # Move X, Y, Z (and cloned A) axes
    # TODO: test if 100 is long enough distance, if not, increase it

# Function to close the door
def close_door(ser):
    send_gcode(ser, f"G1 X0 Y0 Z0 F{MAX_FEEDRATE}")


# Function to send G-code commands to GRBL and receive response
def send_gcode(ser, gcode):
    ser.write((gcode + '\n').encode())  # Send G-code command
    time.sleep(0.1)  # Wait for GRBL to process the command
    while ser.in_waiting > 0:  # Check for response
        response = ser.readline().decode().strip()
        print('GRBL Response:', response)
    return response


# Initialize the serial connection to the Arduino running GRBL
def initialize_grbl_connection(port='/dev/ttyUSB0', baudrate=115200):  # TODO: Check port and rate
    ser = serial.Serial(port, baudrate)
    time.sleep(2)  # Wait for the serial connection to establish
    ser.flushInput()  # Flush any startup messages
    return ser


# Main function to control the CNC machine
def control_motors():
    # Initialize GRBL connection
    ser = initialize_grbl_connection()

    # Wake up GRBL
    ser.write(b"\r\n\r\n")
    time.sleep(2)
    ser.flushInput()

    while True:
        # Enable hard limits to allow endstop switch behavior
        send_gcode(ser, "$21=1")  # Enable hard limits (end switches)

        # Optional: Invert limit switch pins if needed (only if using NC switches)
        # send_gcode(ser, "$5=1")  # Uncomment if limit switches need inversion

        # OPENING THE DOOR
        open_door(ser)

        # GRBL will automatically stop the motors when the endstop is triggered.

        time.sleep(5)

        # CLOSING THE DOOR
        close_door(ser)

    # Close the serial connection
    ser.close()


# Run the CNC control function
if __name__ == "__main__":
    control_motors()
