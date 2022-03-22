from flask import Flask, request, abort
from asyncio.windows_events import NULL
import json, requests
from flask import jsonify 
import time
import os
from fun import *

#======python的函數庫==========
import tempfile, os
import datetime
import time
#======python的函數庫==========


#初始化------------------------------------------------------------
url = requests.get("https://kaikai5.herokuapp.com/getjson")
text =  url.text 
data = json.loads(text)
mes_time=data['time']
mes_message=data['message']

state = 0
cost_time_data = NULL


app = Flask(__name__)
#------------------------------------------------------------------

@app.route('/')
def hello_world():
    return "Hello, World!"

#@app.route('/getjson')
#def getjson():
#    global mesg
#    global mes_time
#    json = {"time" :mes_time , "message" :mesg}
#    return jsonify(json)

# 監聽所有來自 /callback 的 Post Request
@app.route("/line_bot_return")
def callback():
    global mes_time
    global mes_message
    global state
    global cost_time_data

    #重heroku端抓取line傳送的訊息    
    url = requests.get("https://kaikai5.herokuapp.com/getjson")
    text =  url.text
    data = json.loads(text)

    #印出讀入的訊息與時間
    #print("mes_time:",end='')
    #print(mes_time)
    #print("data['time']:")
    #print(data['time'])

    #如果不是收到尚未更新的訊息
    if(mes_time!=data['time']):
        #讀入訊息
        mes_time=data['time']
        mes_message=data['message']
        #印出訊息與時間
        print("------------------------------------")
        print("time : " + mes_time + "\na one message:" + mes_message)
        #print("****************************************************************")
        #當已知記帳總類(state != 0)
        if(state != 0):
            if(cost_time_data == NULL):
                #此讀入訊息為 記帳之時間與項目
                cost_time_data = mes_message
                print("cost_time&data is:",end='')
                print(cost_time_data)
                print("***********************************")
                return jsonify({"time" : time.ctime(time.time()) , "message" :"已收到您要記帳的項目:" + mes_message +"\n請輸入花費金額 EX(888))"})
            else:
                #此讀入訊息為 記帳之金額
                cost = mes_message
                print("cost_$$ is:",end='')
                print(cost)
                print("***********************************")
                #執行對excel做修改
                try:
                    excel(state,cost_time_data,cost)
                except:
                    cost_time_data = NULL
                    state = 0
                    print("存入excel時發生錯誤,系統存取失敗(excel可能有人正在使用中)\n請關閉excel後再重新嘗試")
                    print("***********************************")
                    return jsonify({"time" : time.ctime(time.time()) , "message" : "存入excel時發生錯誤\n系統存取失敗\n(可能有人正在使用中)\n請稍後重新嘗試\n\n請重新輸入要記帳的類別\n請輸入要記帳的類別EX(伙食、零食、飲料、其他花費)"})
                print("*****************************")
                print("*****  add successful  ******")
                print("*****************************")
                cost_time_data = NULL
                state = 0
                return jsonify({"time" : time.ctime(time.time()) , "message" : "已收到金額:" + mes_message + "\n您已成功記帳\n請輸入要記帳的類別EX(伙食、零食、飲料、其他花費)"})
        #此讀入訊息為 記帳之總類
        elif( (('伙食' == mes_message )| ('零食' == mes_message)) |(( '飲料' == mes_message )|( '其他花費' == mes_message ) )):
            if('伙食' == mes_message):
                state = 1
            elif(('零食' == mes_message )|( '飲料' == mes_message)):
                state = 2
            elif('其他花費' == mes_message):
                state = 3
            print("已收到類別為:",end = '')
            print(mes_message)
            print("***********************************")
            return jsonify({"time" : time.ctime(time.time()) , "message" :"您要記帳的類別:" + mes_message +"\n請輸入時間與花費項目\nEX(2022.03.33 晚餐)"})
        #其餘情況
        else:
            print("此為無用途之訊息")
            print("***********************************")
            return jsonify({"time" : time.ctime(time.time()) , "message" :"收到訊息:" + mes_message +"\n請輸入要記帳的類別\n請輸入要記帳的類別EX(伙食、零食、飲料、其他花費)"})
    print("***********************************")
    print("********** 系統發生異常  **********")
    print("***********************************")
    return jsonify({"time" : time.ctime(time.time()) , "message" :">< 404 error 404 ><"})
           
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8081))
    app.run(host='0.0.0.0', port=port)

