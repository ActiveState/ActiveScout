## ActiveScout 2.0

An easy to use tool that scans the current system to detect all ActiveState products including Python, Perl, and Tcl.

### Requirements
Available via ActiveState Platform Project [ActiveScout](https://platform.activestate.com/ActiveState/ActiveScout) or by locally cloning this repo and running with Python 3.7 and greater (requires `python3 setup.py install` to be run). This will generally work without root/Admin access, but if hidden folders or directories are locked down to root/Admin, then these permissions will be required when running ActiveScout. 

### Usage
`activescout -o companyName -m machineTag -l $(pwd)`

- Pass in `--no-telemetry` if users do not wish to send the data back to ActiveState, otherwise telemetry is enabled by default.

- Pass in `-l` to specify where to save a CSV report file containing the following data:
    - Total number of installations
    - Company Name
    - Machine Tag
    - MAC address
    - Assigned IP address
    - Machine Name
    - Operating System
