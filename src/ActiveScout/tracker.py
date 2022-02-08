import http.client

from ActiveScout.components import MachineSpecs


def report_callhome(
    num_install: int, company_name: str, machine_tag: str, machinespecs: MachineSpecs
):

    httpHost: str = "activescout.s3.amazonaws.com"
    url: str = "/tracker/pixel"
    head: str = "?num_install=" + str(num_install)
    head += "&company_name=" + company_name
    head += "&machine_tag=" + machine_tag
    head += "&mac=" + machinespecs.mac
    head += "&assigned_ip=" + machinespecs.assigned_ip
    head += "&machine_name=" + machinespecs.machine_name
    head += "&os=" + machinespecs.os

    # remove whitespace in request
    final = (url + head).replace(" ", "")
    conn = http.client.HTTPConnection(httpHost)
    conn.request("HEAD", final)
    res = conn.getresponse()
    print(res.status, res.reason)
    conn.close()
