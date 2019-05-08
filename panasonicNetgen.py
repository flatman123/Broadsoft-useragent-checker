#! /usr/bin/python3

import csv, re

csv_headers = [
                'Enterprise ID', ' Group ID', ' Device Name',
                ' Device Type', ' UCount', ' Line Ports',
                ' New DName', ' New DType', ' User Agent'
               ]

def pana_net():
    cnt = 0
    phone_models = [
                    '600',
                    '500',
                    'HX4E'
                    ]

    ND_types = [
                'Panasonic KX-TGP500',
                'Linksys SPA-2102',
                'HX4E',
                'Panasonic KX-TGP600'
                ]

    nw_device_type = {
                        '600': ND_types[3],
                        '500': ND_types[0],
                        'HX4E': ND_types[1]
                      }

    with open('<YOUR CSV FILE HERE>', 'r') as csv_file:
        contents = csv.DictReader(csv_file)

        with open('<YOUR CSV FILE HERE>', 'a', newline='') as matched_file:
            csv_writer = csv.DictWriter(matched_file, fieldnames=csv_headers, delimiter=',')
           # csv_writer.writeheader()

            for line in contents:
                for model in phone_models:
                    pattern = re.compile(rf"(KX-TGP{model}|{model}-\d\w)")
                    matches = pattern.finditer(line[' User Agent'])

                    for match in matches:
                        if match.group(0) in line[' User Agent']:
                            line[' New DName'] = line[' Device Name']
                            line[' New DType'] = nw_device_type[model]
                            csv_writer.writerow(line)

    cnt += 1
    return cnt












