import argparse
import requests
import time
from urllib.parse import urlparse
import yaml


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "Path", help="Provide the path to the input YAML file.")
    args = parser.parse_args()
    print(args.Path)
    with open(args.Path, "r") as input:
        dict = yaml.safe_load(input)
    res = {}
    while True:
        try:
            for d in dict:
                # print(d.keys())
                key = urlparse(d["url"]).netloc
                # tuple where 0th is up and 1st is down counts
                if key not in res.keys():
                    res[key] = [0, 0]

                if health_check(d):
                    res[key][0] = res[key][0] + 1
                else:
                    res[key][1] = res[key][1] + 1
            print(res)
            # busy wait not ideal
            time.sleep(15)
        except KeyboardInterrupt:
            break


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
