#!/Users/dshepherd/PycharmProjects/cislib/venv/bin/python3
from cislib import *
import os
import sys

temp = sys.argv
volume = temp[1]
agent = temp[2]
server = "udoes01a.bskyb.com"
authtoken = cisauth(server, "install", "installn0v3ll")
temp2 = tierlist(server, authtoken)
if temp2 == "0":
    print("VOLUME or TIER not found...")
    sys.exit()
temp1 = runpolicy(volume, agent, temp2, server, authtoken)
print(temp)
