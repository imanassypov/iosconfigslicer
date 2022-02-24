#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Copyright (c) 2021 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

__author__ = "Igor Manassypov, System Architect"
__email__ = "imanassy@cisco.com"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2021 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

from ciscoconfparse import CiscoConfParse
from netmiko import ConnectHandler
import time
from dotenv import load_dotenv, dotenv_values
import sys
import os
import logging
from datetime import datetime

ENV_FILE='environment.env'

#input config source folder location
CFG_IN_FOLDER=''
CFG_IN=''

#LOG
LOG_FOLDER=''
LOG_FORMAT="%(message)s"

TIME_FORMAT = "%m/%d/%Y-%H:%M:%S"

PARENTS =  [
			'wireless tag policy',
			'wireless tag site',
			'wireless profile flex',
			'ap\s+([a-z0-9]{4}.[a-z0-9]{4}.[a-z0-9]{4})'
			]

#read in execution parameters
dn = os.path.dirname(os.path.realpath(__file__))
env_full_path = os.path.join(dn,ENV_FILE)
env_dict = dotenv_values(env_full_path)

#target ssh connection handle
target_ssh = {}

def timestamp():
	return (datetime.now().strftime(TIME_FORMAT))

try:
	# connection string for target device ssh
	target_ssh = {
	'device_type': env_dict['DEVICE_TYPE'],
	'host': env_dict['TARGET_HOST'],
	'username': env_dict['TARGET_USERNAME'],
	'password': env_dict['TARGET_PASSWORD'],
	'global_delay_factor': int(env_dict['GLOBAL_DELAY_FACTOR']),
	}

	#input config source file
	CFG_IN_FOLDER = env_dict['CFG_IN_FOLDER']
	CFG_IN_FOLDER = os.path.join(dn, CFG_IN_FOLDER) 
	CFG_IN = os.path.join(CFG_IN_FOLDER, env_dict['CFG_IN'])

	LOG_FOLDER=os.path.join(dn,env_dict['LOG_FOLDER'])
	logging.basicConfig(filename = os.path.join(LOG_FOLDER,env_dict['CFG_IN']+'.log'),
						filemode='w',
						format = LOG_FORMAT,
						level = logging.INFO,)
	log = logging.getLogger()
	log.info(timestamp())

except Exception as e:
    print(e)

try:
	print (f"Connecting to: {target_ssh['host']}")
	net_connect_target = ConnectHandler(**target_ssh)
	print (f"Connected, prompt: {net_connect_target.find_prompt()}")
except Exception as e:
	print(e)

try:
	print (f"Parsing from input: {CFG_IN}")
	parse = CiscoConfParse(CFG_IN)
except Exception as e:
	print(e)

#def crawl_children (obj: ciscoconfparse.models_cisco.IOSCfgLine):
def crawl_children (obj: list, cli):
	for child_obj in obj:
		cli = cli + str.strip(child_obj.text) + "\n"

		if (len(child_obj.children) > 0):
			cli = crawl_children(child_obj.children, cli)
	return cli

for p in PARENTS:
	cli = ""
	print (f"[{timestamp()}] Parsing trunk: {p}")
	log.info(f"---TRUNK--- {p}")
	start_parse_time = time.time()
	for obj in parse.find_objects(p):
		cli += obj.text + "\n"
		cli += str.strip(crawl_children(obj.children,"")) + "\n"
	end_parse_time = time.time()

	print (f"[{timestamp()}] Trunk parsed in: {end_parse_time-start_parse_time}")

	start_ssh_time = time.time()
	result = net_connect_target.send_config_set(cli.split("\n"))
	end_ssh_time = time.time()
	log.info(result)
	print (f"[{timestamp()}] Config set pushed in: {end_ssh_time-start_ssh_time}")
