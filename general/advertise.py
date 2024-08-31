# Advertise the variables and hangair ip to the master server
import os
import re
import requests

from time import sleep
from typing import Dict, Any

def sniff_vars(file: str) -> Dict[str, Dict[str, Dict[str, Any]]]:
	with open(file, "r") as f:
		content = f.read()
	matches = re.findall("^[A-Z_0-9]+? =? .+", content, re.MULTILINE)
	db = {}
	for match in matches:
		if "=" in match:
			key, value = match.split("=")
			db[key.strip()] = {}
			value = value.strip()
			val, comment = value.split("#") if "#" in value else (value, "")
			db[key.strip()]["value"] = val.strip()
			db[key.strip()]["default"] = val.strip()
			db[key.strip()]["comment"] = comment.strip()
	return {file: db}

def process_files(directory: str) -> Dict[str, Dict[str, Dict[str, Any]]]:
	a = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith(".py") and f != "advertise.py"]
	collection = {}
	for file in a:
		collection.update(sniff_vars(os.path.join(directory, file)))
	return collection

if __name__ != "__main__":
	__import__("sys").exit(1)

report = process_files((os.sep).join(__file__.split(os.sep)[:-1]))

serv_url = "https://palcat.feec.vutbr.cz/init"

while True:
	try:
		resp = requests.post(serv_url, json=report)
		if resp.status_code == 200:
			break
	except Exception as e:
		pass
	sleep(5)
