import argparse


def arguments():
    parser = argparse.ArgumentParser(
        description="ActiveScout 2.0 ActiveState Software Audit"
    )
    parser.add_argument(
        "-o",
        "--org",
        help="Company organization name",
        required=True,
    )
    parser.add_argument(
        "-m",
        "--machinetag",
        help="Identifier to map installations with the machines",
        required=True,
    )
    parser.add_argument(
        "-l",
        "--log",
        help="Location of where to save report output",
        required=False,
    )
    parser.add_argument(
        "--telemetry",
        help="Enable sending callhome data [default=True]",
        dest="telemetry",
        action="store_true",
    )
    parser.add_argument(
        "--no-telemetry",
        help="Disable sending callhome data",
        dest="telemetry",
        action="store_false",
    )
    parser.set_defaults(telemetry=True)
    return parser.parse_args()
