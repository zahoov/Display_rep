import can
import os

os.system("sudo /sbin/ip link set can0 up type can bitrate " + str(250000))
bus = can.interface.Bus(channel='can0', bustype='socketcan_native', is_extended_id=True)

msg_data = [1, 0, 0, 0, 0, 0, 0, 0]

msg = can.Message(arbitration_id=0xCF00203, data=msg_data)

bus.send(msg)
