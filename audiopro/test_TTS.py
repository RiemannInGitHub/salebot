#encoding=utf-8  
import wave
import urllib,urllib2,pycurl
import base64
import json
import sys
import struct
import os
reload(sys)
sys.setdefaultencoding('utf-8')
try:
    # python 3
    from urllib.parse import urlencode
except ImportError:
    # python 2
    from urllib import urlencode

##get tokenormat
def get_token():
	apiKey = "0XyzNfIwZeSqDN8oZWR54Qon"
	secretKey = "92971d401d3df1bd2869afebc04df63b"

	auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials" + "&client_id=" + apiKey + "&client_secret=" + secretKey;

	res = urllib2.urlopen(auth_url)
	json_data = res.read()
	return json.loads(json_data)['access_token']

 ##post text to server
def use_cloud(token):
	text = "广汽传祺新年开门红全系劲销超4.6万再创新高"
 	cuid = "38:c9:86:13:93:1f"# my Mac MAC
 	srv_url = 'http://tsn.baidu.com/text2audio'
 	values = {'cuid':cuid,'tok':token,'tex':text.encode("UTF-8"),'lan':"zh",'ctp': 1,'per': 0}
 	post_data = urllib.urlencode(values)
 	print post_data
 	req = urllib2.Request(srv_url,post_data)
 	print req
 	response = urllib2.urlopen(req)
 	print response.getcode()
 	the_page = response.read()
 	print len(the_page)
 	print the_page[1]#,struct.unpack('x',the_page)

if __name__ == '__main__':
 		token = get_token()
 		use_cloud(token)