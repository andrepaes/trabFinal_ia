import urllib2
import json
import requests

# url = "http://dev.virtualearth.net/REST/v1/Elevation/Bounds?bounds=4.9481206,72.4849751,51.000577,-1.311836&rows=480&cols=280&key=AqVU8R9xdbPoAP-1C7DV_M-DyYBof5YACHOeaYXKVHysi19HJbXw22soyL9vcpLG"
url = "http://dev.virtualearth.net/REST/v1/Elevation/List?points=41.8591656,-3.6817918,41.8591656,-3.6417918&key=AqVU8R9xdbPoAP-1C7DV_M-DyYBof5YACHOeaYXKVHysi19HJbXw22soyL9vcpLG"
# req = urllib2.Request(url)
req = requests.get(url)
response = json.loads(req.content)
# opener = urllib2.build_opener()
# contents = opener.open(req)
# json = json.loads(contents.read())
print response