import re
import uuid
import socket
import platform

from ActiveScout.components import MachineSpecs

"""
Machine spec:
    MAC address = mac
    assigned IP address = assigned_ip
    machine name = machine_name
    operating system = os
"""


def machine_specs():
    mac = ":".join(re.findall("..", "%012x" % uuid.getnode()))
    machine_name = socket.gethostname()
    assigned_ip = socket.gethostbyname(machine_name)
    os = platform.system() + platform.release()
    return MachineSpecs(
        mac=mac,
        assigned_ip=assigned_ip,
        machine_name=machine_name,
        os=os,
    )
