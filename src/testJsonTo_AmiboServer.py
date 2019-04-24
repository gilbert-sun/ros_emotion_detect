
import os, pytz
import requests, time, datetime
import json, codecs

from darknet_ros_msgs.msg import BoundingBoxes
import time
#as below open project not using pycharm from "from src.clientFlask1" instead of "from clientFlask1"
from src.clientFlask1 import write_json_file_DayActivity, read_json_file_DayActivity,dayActivity_RepoFormat
#from clientFlask1 import write_json_file_DayActivity, read_json_file_DayActivity,dayActivity_RepoFormat



def read_json_file_DayActivity(wfile):
    json_data = ""

    if not os.path.exists(wfile):
        f = open(wfile, 'wb')
        json_data = json.loads( '{"device_id": "DeviceUser-Test","record_time": "2018-12-1","sit_cum_time": 0,"stand_cum_time": 0}' )
        json.dump(json_data, codecs.getwriter('utf-8')(f), indent=4,
                  ensure_ascii=False)
        f.close()

    with open(wfile, 'r') as f:
        data = f.read()

        json_data = json.loads(data)

    #print( "1-----json data: ---1-",json_data)#json.dumps(json_data))
    return json_data


def write_json_file_DayActivity(wfile ,Str):

    json_data = read_json_file_DayActivity (wfile)

    with open(wfile, 'wb') as f:

        json_data["record_time"]=Str["record_time"]

        json_data["sit_cum_time"]=Str["sit_cum_time"]

        json_data["stand_cum_time"]=Str["stand_cum_time"]
    #(json.loads(json.dumps(Str["stand_cum_time"], indent = 4, ensure_ascii = False )))

        json.dump(json_data , codecs.getwriter('utf-8')(f), indent = 4,
               ensure_ascii = False)
        print("3-----json data: ----\n", json.dumps(json_data) )



def write_json_file(wfile ,Str):
    json_data = ""

    if not os.path.exists(wfile):
        f = open(wfile, 'wb')
        json_data = json.loads( '{"device_id": "DeviceUser-Test", "statistic_list": []}' )
        json.dump(json_data, codecs.getwriter('utf-8')(f), indent=4,
                  ensure_ascii=False)
        f.close()

    with open(wfile, 'r') as f:
        data = f.read()
        #print (type(data))
        json_data = json.loads(data)
        #print ("--",type(json_data))
        json_data["statistic_list" ].append (json.loads(json.dumps(Str, indent = 4, ensure_ascii = False )))
    #print( "1-----json data: ----",json.dumps(json_data))

    with open(wfile, 'wb') as f:
        json.dump(json_data , codecs.getwriter('utf-8')(f), indent = 4,
               ensure_ascii = False)
        print("3-----json data: ----\n", json.dumps(json_data))

def fallPosition_RepoFormat(px,py,pz):
    return ( {"detect_time": int(time.time()),"position": "{\"x\":"+ str(px) + ", \"y\":"+str(py)+", \"z\":"+ str(pz)+"}"} )

def face_RepoFormat(ans1,ans2):
    return {"type": ans1, "confident": ans2, "detect_time":int(time.time())}

def dayActivity_RepoFormat(ansSit,ansStand):
    #"%Y-%m-%d %H:%M:%S"
    return {"stand_cum_time": int(ansStand), "sit_cum_time": int(ansSit), "record_time": time.strftime("%Y-%m-%d")}

def showJson(fname='temp1.json'):
    with open(fname, 'r') as f:
        data = f.read()
        json_data = json.loads(data)
    print("=========debug============",json.dumps(json_data))
    return (json_data)

def client_dayActivity():
    print ("\n-------client_dayActivity--------begin")
    with open("jsonPath.txt","r") as f:
        pathName = f.readlines()
        print (pathName)
    return showJson(pathName +"client_dayActivity.json")

def client_dayFalling():
    print ("\n-------client_dayFalling--------begin")
    with open("jsonPath.txt","r") as f:
        pathName = f.readlines()
        print (pathName)
    return showJson(pathName +"client_fall.json")

def client_faceType_emotion():
    print ("\n-------client_faceType_emotion--------begin")
    with open("jsonPath.txt","r") as f:
        pathName = f.readlines()
        print (pathName)
    return showJson(pathName +"client_faceType_emotion.json")

if __name__ == '__main__':
    #
    # json_data = read_json_file_DayActivity( "client_dayActivity.json")
    #
    # json_data["sit_cum_time"] += 1
    # json_data["stand_cum_time"] += 1
    #
    # print(write_json_file_DayActivity("client_dayActivity.json", dayActivity_RepoFormat(json_data["sit_cum_time"] , json_data["stand_cum_time"])))

    os.getcwd()

