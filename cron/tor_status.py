#!/usr/bin/env python2.7
import redis
import urllib2
import json

infra_api = "http://jabber.khrypt.ooo:1337" # Change to your endpoint
r = redis.Redis(unix_socket_path = "/var/run/redis/redis.sock") # Change to your Redis socket

try:
	response = urllib2.urlopen("%s/status/tor" % (infra_api))
	tor_status = response.read()
except:
	pass

try:
	tor_status = json.loads(tor_status)
except:
	raise Exception("Malformed JSON received")

r.hmset("khryptooo_tor", tor_status)
