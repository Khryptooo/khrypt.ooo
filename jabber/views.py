from django.http import HttpResponse
from django.template import RequestContext, loader
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import GeoIP
import xmpp

@csrf_exempt # TEMP bad idea
def register(request):
	if request.method != "POST":
		return HttpResponse("")

	try:
		username = request.POST["username"].split("@")[0]
		username += "@khrypt.ooo"
		password = request.POST["password"]
	except:
		return HttpResponse("")

	ip = request.META.get("HTTP_X_FORWARDED_FOR").split(',')[-1].strip()
	gi = GeoIP.open("/usr/share/GeoIP/GeoIP.dat", GeoIP.GEOIP_STANDARD)
	c  = gi.country_name_by_addr(ip)

	if c != "Cambodia":
		return HttpResponse("RESTRICTED")

	jid = xmpp.JID(username)
	cli = xmpp.Client(jid.getDomain())
	cli.connect()
	xmpp.features.getRegInfo(cli, jid.getDomain(), sync=True)

	if xmpp.features.register(cli, jid.getDomain(), {"username": jid.getNode(), "password": password}):
		return HttpResponse("OK")

	return HttpResponse("ERROR")
