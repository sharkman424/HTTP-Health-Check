import argparse
import requests
import time
from urllib.parse import urlparse
import yaml


def main():
    # use argparse to get the path to input yaml
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "Path", help="Provide the path to the input YAML file.")
    args = parser.parse_args()
    # open and ingest input yaml
    with open(args.Path, "r") as input:
        dict_list = yaml.safe_load(input)
    res = {}
    while True:
        try:
            for d in dict_list:
                key = urlparse(d["url"]).netloc
                # list where 0th is UP count and 1st is DOWN count
                if key not in res.keys():
                    # then we initialize an empty list to track UP and DOWN counts
                    res[key] = [0, 0]

                if health_check(d):
                    # Endpoint is UP
                    res[key][0] = res[key][0] + 1
                else:
                    # Endpoint is DOWN
                    res[key][1] = res[key][1] + 1
            # log current availability percentages to stdout
            print_ap(res)
            # busy wait 15 seconds (not ideal)
            time.sleep(15)
        except KeyboardInterrupt:
            # allow user to CTRL+C to stop the execution
            break


"""
Helper function to calculate, format and print the availability percentages
to standard out after each pass through the list of endpoints.
"""


def print_ap(map: dict):
    for key in map.keys():
        up = map[key][0]
        down = map[key][1]
        total = up + down
        ap = 100 * (up / total)
        print(f"{key} has {round(ap)}% availabilty percentage")


"""
Helper function that ensures the necessary components for the HTTP requests
are initialized, makes the HTTP request, and determines whether or not the 
response from the endpoint meets the criteria for UP (<500ms latency and a status
code in [200,299]) or if the endpoint is DOWN
"""


def health_check(block: dict):
    # default behavior
    if 'method' not in block.keys():
        block['method'] = "GET"

    if 'headers' not in block.keys():
        block['headers'] = None

    if 'body' not in block.keys():
        block['body'] = None

    response = requests.request(
        block["method"], block["url"], headers=block['headers'], json=block['body'])
    # convert time delta to seconds then to ms
    latency = response.elapsed.total_seconds() * 1000
    code = response.status_code
    if latency < 500 and code >= 200 and code <= 299:
        # then the endpoint is UP
        return True
    # else endpoint is DOWN
    return False


if __name__ == "__main__":
    main()
