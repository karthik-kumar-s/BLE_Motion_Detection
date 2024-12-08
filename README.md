# **BLE Motion Detection App**

## **Overview**
This Python application scans for **BLE devices** broadcasting accelerometer data and determines whether the device (tag) is **"Moving"** or **"Stationary"**. The app processes BLE packets containing accelerometer data, extracts X, Y, and Z values, and uses variance analysis to detect motion.

## **Features**
- **Real-time BLE scanning**: Discovers BLE devices broadcasting accelerometer data.
- **Accelerometer parsing**: Extracts X, Y, Z values from BLE packets.
- **Motion detection**: Determines motion status based on variance analysis of accelerometer data.

## **Compatibility**
- **Operating Systems**: 
  - Linux
  - macOS 
- **Hardware Requirements**: 
  - BLE-compatible Bluetooth adapter.

## **Prerequisites**
1. **Python 3.9 or later** installed.
2. **BLE-compatible Bluetooth adapter**.

### **Install Python**:
Make sure Python 3.9 or later is installed. You can check your Python version using:
```bash
python3 --version


If Python is not installed, follow these steps:

##For Ubuntu (Linux):
sudo apt update
sudo apt install python3 python3-pip

##For macOS:
macOS usually comes with Python 2.7 pre-installed, but you'll need to install Python 3:

1.Install Homebrew if you don't have it:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

2.Install Python 3 via Homebrew:
brew install python

##Install Required Libraries:
requirements.txt

##Installation Steps
1. Clone the Repository:
If you're starting from a GitHub repository, clone it first:
git clone https://github.com/karthik-kumar-s/BLE_Motion_Detection.git
cd ble-motion-detection

2. Install Dependencies:
Install all necessary Python dependencies:
pip install -r requirements.txt

3. Run the App:
Once everything is installed, you can start the app. Use the following command to scan for BLE devices:
python ble_motion_detection.py

4. Verify BLE Devices:
The app will list the devices it finds in the output:

Scanning for BLE devices...
Found device: JODUE5981F, Address: FC:B0:DE:E5:98:1F
Processing packet from Unknown: <Packet Hex>
Accelerometer Data: {'x': 1369, 'y': 4896, 'z': -17736}
Motion Status: Moving

5. Debugging:
If no BLE devices are found:

Ensure your Bluetooth adapter is correctly connected and functional.
Run bluetoothctl (on Linux) or check Bluetooth settings (on macOS) to ensure the adapter is properly enabled.

6. Testing with Real-Time Hardware:
To test with real hardware:

i)Enable Bluetooth on your device.
ii)Start the BLE device with accelerometer data broadcasting.
iii)Run the script to start scanning and detecting motion.

##Troubleshooting##
No Devices Found:
Ensure that your Bluetooth adapter is enabled and properly connected.
On Linux, you can run sudo rfkill unblock bluetooth if Bluetooth is blocked.
On macOS, make sure the Bluetooth adapter is turned on in System Preferences > Bluetooth.
Deprecation Warning:
If you see warnings related to device.metadata being deprecated, the script is compatible with future versions of Bleak by using device.advertisement (as explained in earlier fixes).

**Conclusion**
This app helps in detecting motion from BLE devices broadcasting accelerometer data. It works on Linux and macOS and is easily testable with real-time hardware. Just make sure to have a BLE-compatible adapter and the necessary Python libraries installed.


