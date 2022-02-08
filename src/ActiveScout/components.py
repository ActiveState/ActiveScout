from datetime import datetime
from typing import (
    List,
    Optional,
    Callable,
)


class ActiveStateProduct:
    def __init__(
        self, name: str, regex: str, get_version_from_file: Optional[Callable] = None
    ) -> None:
        self.name: str = name
        self.regex: str = regex
        self.get_version_from_file: Optional[Callable] = get_version_from_file


class FoundProductInfo:
    def __init__(self, path: str, name: str, version: str) -> None:
        self.path: str = path
        self.name: str = name
        self.version: str = version

    def __str__(self) -> str:
        return f"{self.name} {self.version} {self.path}"

    def __repr__(self) -> str:
        return f"FoundProductInfo({self.name}, {self.version}, {self.path})"


class MachineSpecs:
    def __init__(self, mac: str, assigned_ip: str, machine_name: str, os: str) -> None:
        self.mac: str = mac
        self.assigned_ip: str = assigned_ip
        self.machine_name: str = machine_name
        self.os: str = os

    def __str__(self):
        return f"""
MAC address: {self.mac}
IP address: {self.assigned_ip}
Machine name: {self.machine_name}
OS: {self.os}
"""


class Summary:
    def __init__(
        self, installations: List, company_name: str = "", machine_tag: str = ""
    ) -> None:
        self.installations: List = installations
        self.company_name: str = company_name
        self.machine_tag: str = machine_tag
        self.machine_specs: MachineSpecs = MachineSpecs("", "", "", "")

    def displaydata(self):
        print(datetime.now().strftime("%Y/%d/%m %I:%M:%S %p"))
        print("Installations:")
        for installation in self.installations:
            print(f"  {installation}")
        print(f"Number of Installations: {len(self.installations)}")
        print("Company name:", self.company_name)
        print("Machine tag:", self.machine_tag)
        print(self.machine_specs)
