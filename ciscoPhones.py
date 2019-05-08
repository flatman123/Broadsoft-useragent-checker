#! /usr/bin/python3

import csv, re

csv_headers = [
                'Enterprise ID', ' Group ID', ' Device Name',
                ' Device Type', ' UCount', ' Line Ports',
                ' New DName', ' New DType', ' User Agent'
               ]

def cisco():
    cnt = 0
    phone_models = [
                    '504',
                    '112',
                    '3102'
                    ]

    ND_types = [
                'Cisco SPA 5XX',
                'Cisco-SPA-112',
                'Linksys SPA-3102'
                ]

    nw_device_type = {
                        '504': ND_types[0],
                        '112': ND_types[1],
                        '3102': ND_types[2]
                      }

    with open('<YOUR CSV FILE HERE>', 'r') as csv_file:
        contents = csv.DictReader(csv_file)

        with open('<YOUR CSV FILE HERE>', 'a', newline='') as matched_file:
            csv_writer = csv.DictWriter(matched_file, fieldnames=csv_headers, delimiter=',')
           # csv_writer.writeheader()

            for line in contents:
                for model in phone_models:
                    pattern = re.compile(rf"SPA{model}")
                    matches = pattern.finditer(str(pattern))

                    for match in matches:
                        if match.group(0) in line[' User Agent']:
                            line[' New DName'] = line[' Device Name']
                            line[' New DType'] = nw_device_type[model]
                            csv_writer.writerow(line)

    cnt += 1
    return cnt


def counter():
        cnt = 0
        true_false = None
        pattern = re.compile(r"(\d{3}|\d{4}|VOIP)-UA")

        with open('<YOUR CSV FILE HERE>') as count_entry:
            csv_counter = csv.DictReader(count_entry)

            for line in csv_counter:
                matches = pattern.finditer(line[' User Agent'])
                for match in matches:
                    if match.group(0) in line[' User Agent']:
                        true_false = True
                        print(line[' User Agent'])
                        cnt += 1
                    else:
                        true_false = False
                        print(true_false)
        return cnt

