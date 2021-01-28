# This debug script tool can be used to find out the board version of your ODrive (in the case of defective/missing printing on the physical board) without performing and executing any possibly breaking firmware-based changes/upgrades/actions
# Mangled from the inner functions of the odrive Python library to expose some of the inner workings/methods/variables for debugging purposes
# Created by James Raphael Tiovalen (2021)

import odrive
from odrive.dfuse import DfuDevice
from odrive.utils import Event
import usb.core
import threading
import time

# Define helper functions
def get_fw_version_string(fw_version):
    if (fw_version[0], fw_version[1], fw_version[2]) == (0, 0, 0):
        return "[unknown version]"
    else:
        return "v{}.{}.{}{}".format(fw_version[0], fw_version[1], fw_version[2], "-dev" if fw_version[3] else "")

def get_hw_version_string(hw_version):
    if hw_version == (0, 0, 0):
        return "[unknown version]"
    else:
        return "v{}.{}{}".format(hw_version[0], hw_version[1], ("-" + str(hw_version[2]) + "V") if hw_version[2] > 0 else "")

# Define your ODrive's serial number here, if necessary
serial_number = ""
app_shutdown_token = Event()
find_odrive_cancellation_token = Event(app_shutdown_token)

devices = [None, None]

def find_device_in_dfu_mode(serial_number, cancellation_token):
    """
    Polls libusb until a device in DFU mode is found
    """
    while not cancellation_token.is_set():
        params = {} if serial_number == None else {'serial_number': serial_number}
        stm_device = usb.core.find(idVendor=0x0483, idProduct=0xdf11, **params)
        if stm_device != None:
            return stm_device
        time.sleep(1)
    return None

# Start background thread to scan for ODrives in DFU mode
def find_device_in_dfu_mode_thread():
    devices[0] = find_device_in_dfu_mode(serial_number, find_odrive_cancellation_token)
    find_odrive_cancellation_token.set()
t = threading.Thread(target=find_device_in_dfu_mode_thread)
t.daemon = True
t.start()

# Scan for ODrives not in DFU mode
# We only scan on USB because DFU is only implemented over USB
# Find any ODrives that are currently connected to the system (or the one with the specified serial number, if any)
devices[1] = odrive.find_any("usb", serial_number, find_odrive_cancellation_token, app_shutdown_token, timeout=30)
find_odrive_cancellation_token.set()

device = devices[0] or devices[1]

if isinstance(device, usb.core.Device):
    serial_number = device.serial_number
    dfudev = DfuDevice(device)

    # Read hardware version from one-time-programmable memory (512 Byte OTP)
    otp_sector = [s for s in dfudev.sectors if s['name'] == 'OTP Memory' and s['addr'] == 0x1fff7800][0]
    otp_data = dfudev.read_sector(otp_sector)
    if otp_data[0] == 0:
        otp_data = otp_data[16:]
    if otp_data[0] == 0xfe:
        hw_version = (otp_data[3], otp_data[4], otp_data[5])
    else:
        hw_version = (0, 0, 0)

else:
    serial_number = device.__channel__.usb_device.serial_number
    dfudev = None
    # Read hardware version as reported from firmware
    hw_version_major = device.hw_version_major if hasattr(device, 'hw_version_major') else 0
    hw_version_minor = device.hw_version_minor if hasattr(device, 'hw_version_minor') else 0
    hw_version_variant = device.hw_version_variant if hasattr(device, 'hw_version_variant') else 0
    hw_version = (hw_version_major, hw_version_minor, hw_version_variant)

# Read firmware version
fw_version_major = device.fw_version_major if hasattr(device, 'fw_version_major') else 0
fw_version_minor = device.fw_version_minor if hasattr(device, 'fw_version_minor') else 0
fw_version_revision = device.fw_version_revision if hasattr(device, 'fw_version_revision') else 0
fw_version_prerelease = device.fw_version_prerelease if hasattr(device, 'fw_version_prerelease') else True
fw_version = (fw_version_major, fw_version_minor, fw_version_revision, fw_version_prerelease)

# Report and print the relevant ODrive's board version (hw_version, with an accompanying fw_version) to the terminal console or display screen
print("Found ODrive of serial number {} with board/hardware version {} and firmware version {}{}.".format(
                serial_number,
                get_hw_version_string(hw_version),
                get_fw_version_string(fw_version),
                " in DFU mode" if dfudev is not None else ""))
