#load definition of configlet section headers
#the list is ORDERED, please remember to add sections of config with no dependencies
#first in that least, and higher level dependencies last to avoid errors when pushing
#config to the target device that has unresolved dependencies
TRUNKS =  [
			'wireless tag policy',
			'wireless tag site',
			'wireless profile flex',
			'ap\s+([a-z0-9]{4}.[a-z0-9]{4}.[a-z0-9]{4})'
			]