#from asyncio.windows_events import NULL
#from email import message
#import json, requests
#from pyparsing import null_debug_action 
#import time
#import xlrd
#import os
#from fun import*
#url = requests.get("https://kaikai5.herokuapp.com/getjson")
#text =  url.text 
#
#data = json.loads(text)
#mes_message=data['message']
#mes_time=data['time']
#
#control_val = 0
#
#cost_time = NULL
#cost = NULL
#
#while(True):
#    url = requests.get("https://kaikai5.herokuapp.com/getjson")
#    text =  url.text
#    data = json.loads(text)
#    if(mes_time!=data['time']):
#        mes_time=data['time']
#        mes_message=data['message']
#        print("----------------------------------------------------------------")
#        print("time : " + mes_time + "\na one message:" + mes_message)
#        if(control_val!=0):
#            if(cost_time==NULL):
#                cost_time = mes_message
#                print("cost_time already")
#            else:
#                cost = mes_message
#                excel(control_val,cost_time,cost)
#                print("successful")
#                cost_time = NULL
#                cost = NULL
#
#        elif(mes_message=='伙食'):
#            control_val = 1
#        elif(mes_message=='零食'):
#            control_val = 2
#        elif(mes_message=='飲料'):
#            control_val = 2
#        elif(mes_message=='其他花費'):
#            control_val = 3
#    time.sleep(1)

from flask import Flask, request, abort
from asyncio.windows_events import NULL
from email import message
import json, requests
from pyparsing import null_debug_action
from flask import jsonify 
import time
import xlrd
import os
from fun import *

#======python的函數庫==========
import tempfile, os
import datetime
import time
#======python的函數庫==========

#*****my ******************
now_time = 0#time.ctime(time.time())
mesg = "null"
state = 0
#***************************

#初始化------------------------------------------------------------
url = requests.get("https://kaikai5.herokuapp.com/getjson")
text =  url.text 

data = json.loads(text)
mes_message=data['message']
mes_time=data['time']
app = Flask(__name__)
#------------------------------------------------------------------

@app.route('/')
def hello_world():
    return "Hello, World!"

@app.route('/getjson')
def getjson():
    global mesg
    global now_time
    #print("now time is :")
    #print(now_time)
    #print("\n and message is : ") 
    #print(mesg)
    json = {"time" :now_time , "message" :mesg}
    return jsonify(json)

# 監聽所有來自 /callback 的 Post Request
@app.route("/line_bot_return")
def callback():
    url = requests.get("https://kaikai5.herokuapp.com/getjson")
    text =  url.text
    data = json.loads(text)
    if(mes_time!=data['time']):
        mes_time=data['time']
        mes_message=data['message']
        print("----------------------------------------------------------------")
        print("time : " + mes_time + "\na one message:" + mes_message)
        if(control_val != 0):
            if(cost_time_data == NULL):
                cost_time_data = mes_message
                print("cost_time&data is:",end='')
                print(cost_time_data)
                print("-----------------------------------")
                return jsonify({"已收到您要記帳的項目:" + mes_message +"\n請輸入花費金額\nEX(888))"})
            else:
                cost = mes_message
                print("cost_$$ is:",end='')
                print(cost)
                print("-----------------------------------")
                excel(control_val,cost_time_data,cost)
                print("*****************************")
                print("*****  add successful  ******")
                print("*****************************")
                cost_time_data = NULL
                cost = NULL
                return jsonify({"time" :now_time , "message" : "已收到金額:" + mes_message + "\n您已成功記帳\n請輸入要記帳的類別EX(伙食、零食、飲料、其他花費)"})
       
        elif(mes_message=='伙食' | mes_message=='零食' | mes_message=='飲料' | mes_message=='其他花費'):
            if(mes_message=='伙食'):
                control_val = 1
            elif(mes_message=='零食' | mes_message=='飲料'):
                control_val = 2
            elif(mes_message=='其他花費'):
                control_val = 3
            print("已收到類別為",end = '')
            print(mes_message)
            print("----------------------------------")
            return jsonify({"time" :now_time , "message" :"您要記帳的類別:" + mes_message +"\n請輸入時間與花費項目\nEX(2022.03.33 晚餐)"})
        else:
            return jsonify({"time" :now_time , "message" :"收到訊息:" + mes_message +"\n請輸入要記帳的類別\n請輸入要記帳的類別EX(伙食、零食、飲料、其他花費)"})
           
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8081))
    app.run(host='0.0.0.0', port=port)

