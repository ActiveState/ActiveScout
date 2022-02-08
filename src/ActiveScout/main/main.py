import os
import csv

from ActiveScout.prodsearch import find_as_products
from ActiveScout.components import Summary
from ActiveScout.arguments import arguments
from ActiveScout.specs import machine_specs
from ActiveScout.tracker import report_callhome


def main() -> None:
    args = arguments()
    print(
        "ActiveScout scanning in progress. This may take a couple minutes, please wait..."
    )
    summary = Summary([prod for prod in find_as_products()])
    summary.company_name = args.org
    summary.machine_tag = args.machinetag
    summary.machine_specs = machine_specs()
    result: list = [
        len(summary.installations),
        summary.company_name,
        summary.machine_tag,
        summary.machine_specs,
    ]

    if args.log:
        if os.path.exists(args.log):
            logpath = os.path.join(args.log, "ActiveScoutReport.csv")
            print("Output will be saved to: {}".format(logpath))
            header = [
                "num_install",
                "company_name",
                "machine_tag",
                "mac_address",
                "assigned_ip",
                "machine_name",
                "operating_system",
            ]
            csvdata = [
                len(summary.installations),
                summary.company_name,
                summary.machine_tag,
                summary.machine_specs.mac,
                summary.machine_specs.assigned_ip,
                summary.machine_specs.machine_name,
                summary.machine_specs.os,
            ]
            with open(logpath, "w") as file:
                wr = csv.writer(file, quoting=csv.QUOTE_ALL)
                wr.writerow(header)
                wr.writerow(csvdata)
        else:
            print(
                "The directory '{}' does not exist, please rerun to get CSV report.".format(
                    args.log
                )
            )

    if args.telemetry:
        print("Sending Callhome data")
        report_callhome(*result)
    else:
        print("Callhome is disabled")
    summary.displaydata()


if __name__ == "__main__":
    main()
