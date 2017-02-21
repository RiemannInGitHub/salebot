# encoding=utf-8
import wave
import urllib
import urllib2
import pycurl
import base64
import json
import os
import sys


# get token
def get_token():
    apiKey = "0XyzNfIwZeSqDN8oZWR54Qon"
    secretKey = "92971d401d3df1bd2869afebc04df63b"

    auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials" + \
        "&client_id=" + apiKey + "&client_secret=" + secretKey

    res = urllib2.urlopen(auth_url)
    json_data = res.read()
    return json.loads(json_data)['access_token']


def dump_res(buf):
    global text
    # print "字符串类型"
    # print (buf)
    a = eval(buf)
    # print type(a)
    if a['err_msg']=='success.':
        #print a['result'][0]#终于搞定了，在这里可以输出，返回的语句
        text = a['result'][0]
        # print text
    else:
        text = a['err_msg']

 # post audio to server
def get_audio(file_position):
    fp = wave.open(file_position, 'rb')
    nf = fp.getnframes()
    audio_len = nf * 2
    audio_data = fp.readframes(nf)
    return (audio_data, audio_len)

def use_cloud(token, audio_data, audio_len):
    cuid = "38:c9:86:13:93:1f"  # my Mac MAC
    srv_url = 'http://vop.baidu.com/server_api' + '?cuid=' + cuid + '&token=' + token
    http_header = [
        'Content-Type: audio/wav;rate=16000',
        'Content-Length: %d' % audio_len
    ]

    c = pycurl.Curl()
    c.setopt(pycurl.URL, str(srv_url))  # curl doesn't support unicode
    #c.setopt(c.RETURNTRANSFER, 1)
    c.setopt(c.HTTPHEADER, http_header)  # must be list, not dict
    c.setopt(c.POST, 1)
    c.setopt(c.CONNECTTIMEOUT, 300)
    c.setopt(c.TIMEOUT, 30)
    c.setopt(c.WRITEFUNCTION, dump_res)
    c.setopt(c.POSTFIELDS, audio_data)
    c.setopt(c.POSTFIELDSIZE, audio_len)
    # c.setopt(c.VERBOSE, True)
    c.perform()  # pycurl.perform() has no return val
    c.close()

def audio2text(file_position):
    token = get_token()
    audio_data, audio_len = get_audio(file_position)
    use_cloud(token, audio_data, audio_len)
    return text

if __name__ == '__main__':
    file_position = "/Users/riemann/Documents/riemann/Audios/lee1.wav"
    audio2text(file_position)
    print text