import sys
import os
import re
from datetime import datetime


def main():
    log_file_name = sys.argv[1]
    if not os.path.isfile(log_file_name):
        print("File path {} does not exist. Exiting...".format(log_file_name))
        sys.exit()

    try:
        log_file = open(log_file_name, "r", encoding="utf8")
        requests = {}
        for line in log_file:
            parse_line(line, requests)
        durations = calculate_durations(requests)

        print("id\tcorrelation_id\tduration")
        current_id = 0
        for correlation_id, duration in durations.items():
            print("{}\t{}\t{}".format(current_id, correlation_id, duration))
            current_id += 1
    finally:
        log_file.close()


def calculate_durations(requests):
    durations = {}
    for correlation_id, times in requests.items():
        duration = max(times) - min(times)
        durations[correlation_id] = duration.total_seconds()
    return durations


def parse_line(line, requests):
    regex = r'(.*)  INFO \[(.*),(.*),(.*),(.*)\]'
    compiled_regex = re.compile(regex)
    match = compiled_regex.search(line)
    if match is not None:
        time = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S.%f")
        base = match.group(3)
        if base is '':
            return
        if base not in requests:
            requests[base] = (time, None)
        elif requests[base][1] is None:
            requests[base] = (requests[base][0], time)
        else:
            raise Exception("Found duplicated value for {}".format(base))


if __name__ == "__main__":
    main()
