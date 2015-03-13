#!/usr/bin/env python2.7
import redis
import urllib2
import json

infra_api = "http://jabber.khrypt.ooo:1337" # Change to your endpoint
r = redis.Redis(unix_socket_path = "/var/run/redis/redis.sock") # Change to your Redis socket

try:
	response = urllib2.urlopen("%s/status/ups" % (infra_api))
	ups_status = response.read()
except:
	ups_status = json.dumps({"status": "broken_link", "charge": 0})

try:
	ups_status = json.loads(ups_status)
except:
	raise Exception("Malformed JSON received")

r.hmset("khryptooo_ups", ups_status)
