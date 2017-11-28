# -*- coding: utf-8 -*-
import numpy as np
from datetime import datetime
import wave
import time
import urllib, urllib2
import pycurl
import base64
import json
import os
import sys
import commands
import time

FAN_GPIO = 29


reload(sys)
sys.setdefaultencoding( "utf-8" )

save_count = 0
save_buffer = []
t = 0
sum = 0
time_flag = 0
flag_num = 0
filename = 'asr.wav'
commun = '1'
answer = '1'
duihua = '1'

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def get_token():
    apiKey = "dpWei1rMPNcGrzQIejZlRa0O"
    secretKey = "3c6922a1ba33bc3cbc6953056cde02d8"
    auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey;
    res = urllib2.urlopen(auth_url)
    json_data = res.read()
    return json.loads(json_data)['access_token']

def dump_res(buf):
    global duihua
    print "字符串类型"
    print (buf)
    a = eval(buf)
    print type(a)
    if a["err_msg"]=="success.":
        duihua = a["result"][0]
        print duihua
    else :
    	print 'failget!!'
    	duihua="fail"

def use_cloud(token):
    fp = wave.open(filename, 'rb')
    nf = fp.getnframes()
    f_len = nf * 2
    audio_data = fp.readframes(nf)
    cuid = "9127702" #产品id
    srv_url = 'http://vop.baidu.com/server_api' + '?cuid=' + cuid + '&token=' + token
    http_header = [
        'Content-Type: audio/pcm; rate=8000',
        'Content-Length: %d' % f_len
    ]

    c = pycurl.Curl()
    c.setopt(pycurl.URL, str(srv_url)) #curl doesn't support unicode
    #c.setopt(c.RETURNTRANSFER, 1)
    c.setopt(c.HTTPHEADER, http_header)   #must be list, not dict
    c.setopt(c.POST, 1)
    c.setopt(c.CONNECTTIMEOUT, 30)
    c.setopt(c.TIMEOUT, 30)
    c.setopt(c.WRITEFUNCTION, dump_res)
    c.setopt(c.POSTFIELDS, audio_data)
    c.setopt(c.POSTFIELDSIZE, f_len)
    c.perform() #pycurl.perform() has no return val

# 将data中的数据保存到名为filename的WAV文件中
def save_wave_file(filename, data):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLING_RATE)
    wf.writeframes("".join(data))
    wf.close()

token = get_token()
print	 "token"
print token
print "token"
key = 'dpWei1rMPNcGrzQIejZlRa0O'
api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='
commands.getoutput('sudo gpio mode '+str(FAN_GPIO)+' OUTPUT')
while(True):
    #time.sleep(5)
    time.sleep(3)
    os.system('sudo arecord -D "plughw:1,0" -f S16_LE -d 4 -r 8000 /home/pi/Public/asr.wav')
    print "delayt2s"
    time.sleep(3)
    #print "startRecord"
    use_cloud(token)
    print "result"
    print duihua
    site = duihua
    #os.system('sudo rm  /home/pi/Public/asr.wav')
    #print "workCheck"
    if "fail" in site: #在返回的文本里寻找“开”
    	time.sleep(15)
    if "开" in site: #在返回的文本里寻找“开”
    	print "work"
        commands.getoutput('sudo gpio write '+str(FAN_GPIO)+' 1')
        
       	answer = '好的，正在为您开灯，请稍后'
       	url = "http://tsn.baidu.com/text2audio?tex="+answer+"&lan=zh&per=0&pit=1&spd=7&cuid=b827ebdd1672&ctp=1&tok=24.5c811e2f04b4be6d96a2dae66b169dde.2592000.1514039148.282335-9127702"
       	os.system('mplayer "%s"'%(url))
       	time.sleep(5)
       	#os.system('cd /home/pi/Desktop/scripts&&./light on')
        commands.getoutput('sudo gpio write '+str(FAN_GPIO)+' 1')
        #commands.getoutput('sudo rm asr.wav')
    if "关" in site:
       	answer = '好的，正在为为您关灯，请稍后'
       	url = "http://tsn.baidu.com/text2audio?tex="+answer+"&lan=zh&per=0&pit=1&spd=7&cuid=b827ebdd1672&ctp=1&tok=24.5c811e2f04b4be6d96a2dae66b169dde.2592000.1514039148.282335-9127702"
       	os.system('mplayer "%s"'%(url))
       #os.system('cd /home/pi/Desktop/scripts&&./light off
      	#print "notwork"
      	time.sleep(5)
      	#commands.getoutput('sudo rm asr.wav')
       	commands.getoutput('sudo gpio write '+str(FAN_GPIO)+' 0')
   	#if "音乐" in site:
       	#answer = '好的，正在为为您关灯，请稍后'
       	#url = "http://lhttp.qingting.fm/live/387/64k.mp3"
       	
 		#os.system('sudo mplayer http://lhttp.qingting.fm/live/387/64k.mp3')
       #os.system('cd /home/pi/Desktop/scripts&&./light off
      	#print "notwork"
      	#time.sleep(5)
      	#commands.getoutput('sudo rm asr.wav')
       	#commands.getoutput('sudo gpio write '+str(FAN_GPIO)+' 0')

    
