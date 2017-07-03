#!/usr/bin/env python2.7
# author aperrier

from datetime import datetime
import urllib2
import json

url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
fileout_allow = "cloudfront-allow.conf"
fileout_nginx = "cloudfront-nginx.conf"
ip_internal = []

datenow = datetime.now()
req = urllib2.Request(url)

try:
    # 200
    opener = urllib2.build_opener()
    f = opener.open(req)
    json = json.loads(f.read())

    allowf = open(fileout_allow, 'w')
    nginxf = open(fileout_nginx, 'w')

    allowf.write("# generate "+str(datenow)+" (CloudFront IP ranges)\n")
    nginxf.write("# generate "+str(datenow)+" (CloudFront IP ranges)\n")

    for i in range(0, len(json["prefixes"])):
    	if json["prefixes"][i]["service"] == "CLOUDFRONT":
        	allowf.write("allow "+json["prefixes"][i]["ip_prefix"]+";\n")
                nginxf.write("set_real_ip_from "+json["prefixes"][i]["ip_prefix"]+";\n")

    allowf.write("\n# Company IP\n")

    for k in range(0, len(ip_internal)):
        allowf.write("allow "+ip_internal[k]+";\n")

    nginxf.write("\n# use any of the following two\nreal_ip_header CF-Connecting-IP;\n#real_ip_header X-Forwarded-For;")

    allowf.close()
    nginxf.close()
except urllib2.HTTPError as e:
    print('Error: '+e.code)