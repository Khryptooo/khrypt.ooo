from django.http import HttpResponse
from django.template import RequestContext, loader
from django.conf import settings
import redis
import json
import socket

def index(request):
    template = loader.get_template("khryptooo/en/index.html")
    context = RequestContext(request, {"selected": "index"})
    return HttpResponse(template.render(context))

def torService(request):
    template = loader.get_template("khryptooo/en/tor_service.html")
    context = RequestContext(request, {"selected": "services"})
    return HttpResponse(template.render(context))

def serviceStatus(request):
	template = loader.get_template("khryptooo/en/service_status.html")
	REDIS_SOCKET = getattr(settings, "REDIS_SOCKET")
	r = redis.Redis(unix_socket_path = REDIS_SOCKET)
	ups_info = r.hgetall("khryptooo_ups")

	if not ups_info:
		ups_info = {"status": "N/A", "charge": 0}

	if DoesServiceExist("jabber.khrypt.ooo", 5222):
		jabber_status = "Online"
	else:
		jabber_status = "Offline"

	if DoesServiceExist("jabber.khrypt.ooo", 443):
		tor_status = "Online"
	else:
		tor_status = "Offline"

	tor_info = r.hgetall("khryptooo_tor")

	if not tor_info:
		tor_info = {"running": False}
		tor_status = "Offline"
	else:
		tor_info["flags"] = json.loads(tor_info["flags"])

	context = RequestContext(request, {"selected": "service_status", "jabber_status": jabber_status, "tor_status": tor_status, "tor_info": tor_info, "ups_status": ups_info["status"], "ups_charge": ups_info["charge"] })

	return HttpResponse(template.render(context))

def DoesServiceExist(host, port):
	captive_dns_addr = ""
	host_addr = ""

	try:
		captive_dns_addr = socket.gethostbyname("dev.null.khrypt.ooo")
	except:
		pass
	try:
		host_addr = socket.gethostbyname(host)

		if (captive_dns_addr == host_addr):
			return False
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(1)
		s.connect((host, port))
		s.close()
	except:
		return False

	return True
