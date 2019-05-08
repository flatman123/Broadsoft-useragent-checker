#! /usr/bin/python3

import csv, re, time
import ciscoPhones, panasonicNetgen


not_match = []
csv_headers = [
                "Enterprise ID", " Group ID", " Device Name",
                " Device Type", " UCount", " Line Ports",
                " New DName", " New DType", " User Agent"
               ]

phone_models = [
                "300", "310", "335", "301", "321",
                "401", "411", "410", "560", "330",
                "500", "600", "400", "8800", "501",
                "311", "450", "550", "331", "6000",
                "5000", "8500", "650", "601", "7000"
                #"VOIP"
                ]
            # Removed the following models from list

                ## "T21P", "T41P", "T41S", "T48S", "T48G", , "VOIP"

MAC_prefix = [
                "VVX201", "VXX300", "VVX301", "VVX310", "VVX311", "VVX400",
                "VVX401", "VVX410", "VVX411", "VVX500", "VVX501", "VVX600", "VVX601",
                "IP300", "IP320", "IP321", "IP330", "IP331", "IP335", "IP430", "IP450",
                "IP500", "IP501", "IP550", "IP601", "IP650", "IP4000", "IP6000",
                "IP5000", "IP7000", "IP8000", "IP600"
                ]

NDtypes = [
            "Polycom_VVX300", "Polycom_VVX410", "Polycom_VVX500",
            "Polycom-321", "Polycom_VVX500", "Polycom-601",
            "Polycom-550", "Polycom-450", "Polycom-8000",
            "Polycom-6000", "Panasonic KX-TGP500",
            "Polycom_VVX401", "Polycom_VVX400", "Polycom_VVX411",
            "Polycom-335", "Polycom-650", "Polycom-5000", "Polycom-501",
            "Polycom_VVX310", "Polycom_VVX311", "Polycom_VVX600"
           ]

            #Removed from nw_device_type dictionary
                #  "7940": "Cisco 7940", "7960": "Cisco 7940", "8186": "Algo_8180"
nw_device_type = {
                "310": [NDtypes[18], MAC_prefix[3]], "321": [NDtypes[3], MAC_prefix[15]], "331": [NDtypes[3], MAC_prefix[17]], "560": [NDtypes[6], MAC_prefix[23]],
                "311": [NDtypes[19], MAC_prefix[4]], "300": [NDtypes[0], MAC_prefix[1]], "301": [NDtypes[0], MAC_prefix[2]], "335": [NDtypes[14], MAC_prefix[18]],
                "401": [NDtypes[11], MAC_prefix[6]], "411": [NDtypes[13], MAC_prefix[8]], "410": [NDtypes[1], MAC_prefix[7]], "500": [NDtypes[2], MAC_prefix[9]],
                "400": [NDtypes[12], MAC_prefix[5]], "501": [NDtypes[17], MAC_prefix[22]], "650": [NDtypes[15], MAC_prefix[25]], "330": [NDtypes[3], MAC_prefix[16]],
                "601": [NDtypes[5], MAC_prefix[24]], "450": [NDtypes[7], MAC_prefix[20]], "550": [NDtypes[6], MAC_prefix[23]], "600": [NDtypes[2], MAC_prefix[31]],
                "6000": [NDtypes[9], MAC_prefix[27]], "5000": [NDtypes[16], MAC_prefix[28]], "8800": [NDtypes[8], MAC_prefix[30]],
                "8500": ["Polycom-8000", MAC_prefix[30]], "7000": [NDtypes[8], MAC_prefix[29]]
                #"VOIP": [NDtypes[2], MAC_prefix[]]
                }


def polycom_Mac_extraction(Phonemodel):
    '''Searches for Polycom Mac-addresses'''
    mac_list = []
    with open("<YOUR CSV FILE HERE>", "r") as csv_file:
        contents = csv.DictReader(csv_file)

        with open("<YOUR CSV FILE HERE>", "a", newline="") as updated:
            csv_writer = csv.DictWriter(updated, fieldnames=csv_headers, delimiter=",")

            for line in contents:
                    pattern = re.compile(rf"(0004\w+|64\w+)")
                    matches = pattern.finditer(line[" Device Name"])
                    pattern_two = re.compile(rf"{Phonemodel}-UA")
                    matches_two = pattern_two.finditer(line[" User Agent"])

                    for mac, user_agent in zip(matches, matches_two):
                        if user_agent.group(0) in line[" User Agent"]:
                            mac_address = mac.group(0)
                            line[" New DName"] = nw_device_type[Phonemodel][1] + "-" + mac_address
                            csv_writer.writerow(line)
                            mac_list.append(mac_address)

                            output = f"USER AGENT: {line[' Device Name']}--{line[' User Agent']}"
    return


def polycom():
    '''Matches the Device Name with the Newly Device Name
        and outputs into a sperate CSV file'''

    cnt = 0
    with open("Book1.csv", "r") as csv_file:
        contents = csv.DictReader(csv_file)

        with open("broadsoft_users.csv", "w", newline="") as matched_file:
            csv_writer = csv.DictWriter(matched_file, fieldnames=csv_headers, delimiter=",")
            csv_writer.writeheader()

            for line in contents:
                for model in phone_models:
                    pattern = re.compile(rf"(IP_{model}-UA|VX_{model}-UA)")
                    matches = pattern.finditer(line[" User Agent"])

                    for match in matches:
                        if match.group(0) in line[" User Agent"]:
                            line[" New DName"] = line[" Device Name"]
                            line[" New DType"] = nw_device_type[model][0]
                            csv_writer.writerow(line)
                            cnt += 1

                            print(f"GROUP -- {match.group(0)}")
                            print()
                            output =f"USER AGENT: {line[' Device Name']}--{line[' User Agent']}"
                            print(output)
                            print(match)
                            print(f"MODEL: {model}\n\n")
                        else:
                            not_match.append(f"{line[' Device Name']}--{line[' User Agent']}")
    return cnt

def counter():
    '''Counts the number of
        lines contained in the CSB File'''

    cnt = 0
    true_false = None
    pattern = re.compile(r"")

    with open("broadsoft_users.csv") as count_entry:
        csv_counter = csv.DictReader(count_entry)

        for line in csv_counter:
            cnt += 1
            matches = pattern.finditer(line[" User Agent"])

            for match in matches:
                if match.group(0) in line[" User Agent"]:
                    true_false = True
                    print(line[" User Agent"])
                else:
                    true_false = False
                    print(true_false)
    return cnt




if __name__ == "__main__":
    polycom()
    for x in phone_models:
         polycom_Mac_extraction(x)
    panasonicNetgen.pana_net()
    ciscoPhones.cisco()


    #print(counter())


