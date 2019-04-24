import rospy
from darknet_ros_msgs.msg import BoundingBoxes
import time

#as below open project not using pycharm from "from src.clientFlask1" instead of "from clientFlask1"
from clientFlask1 import write_json_file_DayActivity, read_json_file_DayActivity,dayActivity_RepoFormat

global headerTimeOld

headerTimeOld = 0

def callback(msg):

# 0	  		1		2			3		4			5			6			7				8
#'seq:', '11897', 'stamp:', 'secs:', '1545287058', 'nsecs:', '815070391', 'frame_id:', '"detection"'
    global headerTimeOld    
    headerTime = int(str(msg.header).split()[4])
    #print ("=======0=========", (headerTime)," ---Old----  ",  (headerTimeOld) )
    if((headerTime - headerTimeOld ) > 60):
        print ("=======day activity detection=========",headerTime)  
        headerTimeOld = (headerTime)
    else:
        return 
    
    '''
    0 Class:
    1 "sitting"
    2 probability:
    3 0.845878005028
    4 xmin:
    5 46
    6 ymin:
    7 206
    8 xmax:
    9 573
    10 ymax:
    11 471
    '''
    boxMsg= str(msg.bounding_boxes[0]).split() #rospy.get_caller_id()   )
#    for idx in range(len(boxMsg)):
#	    print (idx, boxMsg[idx])

    json_data = read_json_file_DayActivity( "client_dayActivity.json")


 
    if(boxMsg[1] == '"sitting"'):
            json_data["sit_cum_time"] += 1
	    #print ("\n ------[%s]-----------------if \n",boxMsg[1])
	    write_json_file_DayActivity("client_dayActivity.json",dayActivity_RepoFormat(json_data["sit_cum_time"], json_data["stand_cum_time"]))
    elif(boxMsg[1] == '"standing"'):
            json_data["stand_cum_time"] += 1
            write_json_file_DayActivity("client_dayActivity.json",dayActivity_RepoFormat(json_data["sit_cum_time"], json_data["stand_cum_time"]))
    else:
	    print ("\n -----------------------else \n")
    
    #rospy.loginfo(msg.bounding_boxes.xmin,msg.bounding_boxes.ymin,msg.bounding_boxes.xmax,msg.bounding_boxes.ymax)
 

def listener():

    rospy.init_node('subscribeDayActivity', anonymous=True)
    # print ("1",time.time())
    # print (time.strftime("%Y-%m-%d"))

    # subscribe and publish related topic
    rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, callback)

    #print("Before 0 %s" % time.ctime())    
    #rospy.sleep(10)
     
    rospy.loginfo("---- inside, listener ... Waiting for Bounding Box, Starting Tracker")
    rospy.wait_for_message('/darknet_ros/bounding_boxes', BoundingBoxes)
 
    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()

 

if __name__ == '__main__':
	try:
            listener()
            rospy.spin()
	except rospy.ROSInterruptException:
            rospy.loginfo("Day activity tracking terminated by user")

