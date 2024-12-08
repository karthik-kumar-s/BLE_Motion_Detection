import asyncio
from bleak import BleakScanner
import numpy as np

# Motion threshold for determining whether the device is moving or stationary
MOTION_THRESHOLD = 50

# Function to parse accelerometer data from BLE packets
def parse_accelerometer_data(packet: bytes):
    """
    Extracts accelerometer data (X, Y, Z) from a BLE packet and converts it to signed integers.
    The accelerometer data is assumed to start at position 26 and ends at position 38 in the packet.

    Args:
    - packet (bytes): The raw BLE packet containing the accelerometer data.

    Returns:
    - dict: A dictionary containing X, Y, and Z accelerometer values, or None if parsing fails.
    """
    try:
        # Convert the packet to a hexadecimal string for easier processing
        hex_packet = packet.hex()
        
        # Ensure the packet is long enough to contain accelerometer data
        if len(hex_packet) < 38:
            raise ValueError("Packet is too short to contain accelerometer data")

        # Extract the X, Y, and Z values from the correct byte positions
        x = int(hex_packet[26:30], 16)
        y = int(hex_packet[30:34], 16)
        z = int(hex_packet[34:38], 16)

        # Convert the values to signed integers (since they are 16-bit)
        if x > 32767:
            x -= 65536
        if y > 32767:
            y -= 65536
        if z > 32767:
            z -= 65536

        return {"x": x, "y": y, "z": z}

    except (ValueError, IndexError) as e:
        print(f"Error parsing accelerometer data: {e}")
        return None

# Function to detect motion based on accelerometer data
def detect_motion(accel_data):
    """
    Detects motion by calculating the variance of accelerometer data. If variance is above the threshold,
    the device is considered "moving"; otherwise, it is "stationary".

    Args:
    - accel_data (dict): The accelerometer data (X, Y, Z values).

    Returns:
    - str: "Moving" if variance exceeds the threshold, "Stationary" otherwise.
    """
    try:
        # Calculate the variance of the accelerometer values (X, Y, Z)
        variance = np.var(list(accel_data.values()))
        
        # If the variance is above the threshold, consider the device to be moving
        return "Moving" if variance > MOTION_THRESHOLD else "Stationary"
    except Exception as e:
        print(f"Error detecting motion: {e}")
        return "Error"

# Function to parse iBeacon data (UUID, major, minor values)
def parse_ibeacon_data(packet: bytes):
    """
    Parses iBeacon data, extracting the UUID, major, and minor values.

    Args:
    - packet (bytes): The raw BLE iBeacon packet.

    Returns:
    - dict: A dictionary containing UUID, major, and minor values, or None if parsing fails.
    """
    try:
        # Convert the packet to a hexadecimal string for easier manipulation
        hex_packet = packet.hex()

        # Ensure the packet is long enough to contain iBeacon data (at least 56 characters)
        if len(hex_packet) < 56:
            print(f"Error: iBeacon packet is too short: {hex_packet}")
            return None

        # iBeacon UUID is typically 16 bytes starting at position 16 to 32
        uuid = hex_packet[16:48]
        
        # The major and minor values are 2 bytes each (position 48-52 for major, 52-56 for minor)
        major = int(hex_packet[48:52], 16) if hex_packet[48:52] else None
        minor = int(hex_packet[52:56], 16) if hex_packet[52:56] else None

        # Return the parsed iBeacon data
        return {"uuid": uuid, "major": major, "minor": minor}

    except Exception as e:
        print(f"Error parsing iBeacon data: {e}")
        return None

# Main function to scan for BLE devices and process their packets
async def scan_and_detect():
    """
    This function scans for nearby BLE devices and processes the manufacturer data
    to detect motion based on accelerometer data, or simply parse iBeacon data.
    """
    try:
        print("Scanning for BLE devices...")

        # Scan for BLE devices nearby
        devices = await BleakScanner.discover()

        # If no devices are found, print a message and exit
        if not devices:
            print("No BLE devices found.")
            return

        # Loop through each detected device
        for device in devices:
            print(f"Found device: {device.name}, Address: {device.address}")

            # Access the advertisement data (which includes manufacturer data)
            advertisement = device.advertisement if hasattr(device, 'advertisement') else device.metadata
            manufacturer_data = advertisement.get('manufacturer_data', {})

            # Process each manufacturer's data if available
            if manufacturer_data:
                for key, value in manufacturer_data.items():
                    print(f"Processing packet from {device.name or 'Unknown'}: {value.hex()}")

                    # First, attempt to parse accelerometer data
                    accel_data = parse_accelerometer_data(value)
                    if accel_data:
                        # If accelerometer data is parsed successfully, detect motion
                        print(f"Accelerometer Data: {accel_data}")
                        status = detect_motion(accel_data)
                        print(f"Motion Status: {status}")
                    else:
                        # If no accelerometer data is found, try to parse iBeacon data
                        print("No accelerometer data found. Attempting to parse iBeacon data...")
                        ibeacon_data = parse_ibeacon_data(value)
                        if ibeacon_data:
                            print(f"iBeacon Data: {ibeacon_data}")
                        else:
                            print("Failed to parse iBeacon data.")
    except Exception as e:
        # If there is an error during scanning or packet processing, print an error message
        print(f"Error during BLE scanning or processing: {e}")

# Main entry point for the script
if __name__ == "__main__":
    try:
        # Run the scan and detect function asynchronously
        asyncio.run(scan_and_detect())
    except KeyboardInterrupt:
        # Handle user interruption (Ctrl+C)
        print("\nScan interrupted by user.")
    except Exception as e:
        # Handle any unexpected errors that occur during execution
        print(f"Unexpected error: {e}")
