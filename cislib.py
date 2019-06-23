# -*- coding: utf-8 -*-
import os
import requests
import json
import urllib3
import sys
import pickle
import datetime
import date_converter
from hurry.filesize import size
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def maketimestamp(date):
    """Convert date into linux timestampe"""
    date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    timestamp = date_converter.date_to_timestamp(date_time_obj)
    return timestamp


def cispost(server, authtoken, url):
    """Generic POST Routine for CIS"""
    headers1 = {'Content-Type': 'application/json; charset=UTF-8', 'Authorization': authtoken, }
    server = "https://" + server + ":8344/" + url

    print(server)

    response = requests.post(server, headers=headers1, verify=False)

    token = json.loads(response.text)
    return token


def activity(server, authtoken, agent, volume, start):
    temp = tierlist(server, authtoken)
    id1 = tierid(volume, agent, temp)
    s1 = datetime.datetime.now()
    s1 = s1.isoformat()
    s1 = s1.replace("T", " ")
    start = str(int(maketimestamp(start)))
    s1 = str(int(maketimestamp(s1)))
    headers1 = {'Content-Type': 'application/json; charset=UTF-8', 'cross-domain': 'true', 'Authorization': authtoken, }
    server1 = "https://" + server + ":8344/api/v1/mgmt/summary/filesize"

    temp1 = {'startdate': start, 'enddate': s1, 'tierid': id1}

    rep = requests.post(server1, params=temp1, headers=headers1, verify=False)

    token = json.loads(rep.text)
    filecount = token
    server1 = "https://" + server + ":8344/api/v1/mgmt/pertier/updown"
    rep = requests.post(server1, params=temp1, headers=headers1, verify=False)
    token = json.loads(rep.text)
    filesize = token

    results = filesize
    results.update(filecount)

    return results


def tierlist(server, authtoken):
    """List of tiersfrom CIS"""
    url = "api/v1/policy/tiers/get_list"
    temp = cispost(server, authtoken, url)
    return temp


def poldump(server, authtoken, filename):
    """Dunmp Policies to File"""
    try:
        fileloc = open(filename, 'wb')
    except:
        print("Location Invalid")
        sys.exit()
    temp = pollist(server, authtoken)
    pickle.dump(temp, fileloc)
    print("\nPolices Written to \t:" + filename)
    fileloc.close()
    return


def polload(filename):
    try:
        fileloc = open(filename, 'rb')
    except:
        print("Location Invalid")
        sys.exit()

    policies = pickle.load(fileloc)

    print("\nLoaded from \t:" + filename)

    print("Name")
    print("----")
    for line in policies:
        print(line["name"])
    fileloc.close()
    return policies


def pollad(server, authtoken, plist):
    for line in plist:
        line["id"] = "0"
        resp = polcreate(server, authtoken, line["name"] + "new", line["description"], line)
        print("")


def pollist(server, authtoken):
    """List of Policies from CIS"""
    url = "api/v1/policy/policies/get_list"
    temp = cispost(server, authtoken, url)
    return temp


def polcreate(server, authtoken, polname, description, template):
    headers1 = {'Content-Type': 'application/json; charset=UTF-8', 'Authorization': authtoken, }
    server = "https://" + server + ":8344/api/v1/policy/policies/add"
    temp1 = createtemplate
    temp1["name"] = polname
    temp1["description"] = description

    response = requests.post(server, json=temp1, headers=headers1, verify=False)

    print(response)


# token=json.loads(response.text)


def cisauth(server, user, password):
    """CIS Authentication"""
    headers1 = {'Content-Type': 'application/json; charset=UTF-8', }
    data1 = {"username": user, "password": password, }
    server = "https://" + server + ":8344/api/v1/auth/user/gettoken"

    response = requests.post(server, json=data1, headers=headers1, verify=False)
    token = json.loads(response.text)
    return token["authtoken"]


def cloudaccounts(server, authtoken):
    """List of cloud accounts"""
    headers1 = {'Content-Type': 'application/json; charset=UTF-8', 'Authorization': authtoken, }
    server = "https://" + server + ":8344/api/v1/policy/cloudaccounts/get_list"

    response = requests.post(server, headers=headers1, verify=False)

    token = json.loads(response.text)

    return token


def runstats(server, authtoken):
    """Running Policy Stats"""
    headers1 = {'Content-Type': 'application/json; charset=UTF-8', 'Authorization': authtoken, }
    server = 'https://' + server + ":8344/api/v1/policy/tiers/get_list_latest_run"

    response = requests.post(server, headers=headers1, verify=False)

    stats = json.loads(response.text)
    print(stats)
    print()
    for line in stats:
        print(line["agentName"])
        print()
        print("Primary Volume\t:" + line["primaryVolume"])
        print("Status\t\t:" + line["lastRunstatus"])
        print("Last Error\t:" + line["LastErrorDetails"])
        print("Start Time\t:" + line["startTime"])
        print("End Time\t:" + line["endTime"])
        print()

    return stats


def polid(name, pol):
    """return policy id based on policy list"""
    temp1 = list(filter(lambda x: x["agentName"] == agent and x["primaryVolume"] == volume, pol))
    idnum = temp1[0]["id"]
    return idnum


def tierid(volume, agent, volist):
    print(volist)
    """return tierid based on vollst"""
    temp1 = list(filter(lambda x: x["agentName"] == agent and x["primaryVolume"] == volume, volist))
    print (temp1)
    try:
        idnum = temp1[0]["id"]
    except:
        idnum = "0"
    return idnum


def runpolicy(volume, agent, temp, server, authtoken):
    """Run Policy via rest"""
    headers1 = {'Content-Type': 'application/json; charset=UTF-8', 'Authorization': authtoken, }
    idnum = tierid(volume, agent, temp)
    data1 = {"id": idnum}
    server = "https://" + server + ":8344/api/v1/policy/tiers/trigger_job"

    response = requests.post(server, json=data1, headers=headers1, verify=False)
    token = json.loads(response.text)
    print(token)
    return


def graph123(server, volume, agent, start, end, interval, filename, authtoken):
    headers1 = {'Content-Type': 'application/json; charset=UTF-8', 'Authorization': authtoken, }

    server1 = "https://" + server + ":8344/api/v1/mgmt/graphdata"

    temp = tierlist(server, authtoken)
    id1 = tierid(volume, agent, temp)

    start = str(int(maketimestamp(start)))
    end = str(int(maketimestamp(end)))
    headers1 = {'Content-Type': 'application/json; charset=UTF-8', 'cross-domain': 'true', 'Authorization': authtoken, }

    temp1 = {'startdate': start, 'enddate': end, 'interval': interval, 'tierid': id1, }

    rep = requests.post(server1, params=temp1, headers=headers1, verify=False)

    token = json.loads(rep.text)

    with open(filename, mode='w') as csv_file:
        fieldnames = ['timestamp', 'file_count', 'size']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for line in token["up_graph"]:
            date = datetime.datetime.fromtimestamp(int(line["timestamp"]))
            print(str(date) + "\t:" + str(line["file_count"]) + "\t" + size(line["size"]))
            line["timestamp"] = str(date)
            line["size"] = size(line["size"])
            writer.writerow(line)
    return token


def tiersummary(server, authtoken, date, filename):
    """Stat Summary for all active Tiers"""

    tiers = tierlist(server, authtoken)
    with open(filename, mode='w') as csv_file:
        fieldnames = ['server-volume', 'download_size', 'upload_size', 'uploadfilecount', 'downloadfilecount']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for line in tiers:
            templine = {}
            print(line["agentName"], line["primaryVolume"], line["id"])
            temp = activity("udoes01a.bskyb.com", authtoken, line["agentName"], line["primaryVolume"], date)
            server = line["agentName"] + "/" + line["primaryVolume"]

            # templine={"server-volume":server,"download_size":size(temp["download_size"]),"upload_size":size(temp["upload_size"]),"uploadfilecount":temp["uploadfilecount"],"downloadfilecount":temp["downloadfilecount"]}
            templine = {"server-volume": server, "download_size": temp["download_size"],
                        "upload_size": temp["upload_size"], "uploadfilecount": temp["uploadfilecount"],
                        "downloadfilecount": temp["downloadfilecount"]}
            writer.writerow(templine)

        print()
