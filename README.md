[![DEVNET](https://upload.wikimedia.org/wikipedia/en/f/f8/CiscoDevNet2.png)](https://developer.cisco.com)

# Simple Python script to slice Cisco config and export via SSH to another device

## Features
- Script is useful for device config migration / replication

### Assumptions
- Place a copy of "show running" text file in the src_cfg folder
- Update environment.env file with your device ip & credentials
- Update trunks.py file to indiciate which sections of the source runconfig will be extracted
- Sample trunks.py file includes Cisco 9800 Wireless Lan Controller "configlets":
"Wireless Policy Tag", "Wireless Site Tag", "Flex Profile", "Static AP MAC address mappings"
- This script is useful when you have to replicate a large operational WLC configuration to N+1 controller

## Sample Cisco 9800 WLC config extraction
```
TRUNKS =  [
			'wireless tag policy',
			'wireless tag site',
			'wireless profile flex',
			'ap\s+([a-z0-9]{4}.[a-z0-9]{4}.[a-z0-9]{4})'
			]
```

## Operation
With the above configuration, the script is expected to execute as following:
- in the source running configuration, extract all 'sections' of the runconfig that begin with 'wireless tag policy'
- replicate the extracted sections of the config above to the target ip address of the device defined under environment.env
- repeat the above for each of the subsequent config section definitions in the ordered TRUNKS list

## Requirements
- ciscoconfparse
- netmiko


## References
- http://www.pennington.net/py/ciscoconfparse/index.html
- https://pynet.twb-tech.com/blog/automation/netmiko.html

