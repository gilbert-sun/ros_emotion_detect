import schedule,time,os


def job():
    os.system("python client_dayActivity.py")
    os.system("python client_faceType_emotion.py")
    os.system("python client_dayFalling.py")
    print("Now time: [%s]\n" % time.ctime())
    print("Python Crontab working...")

#schedule.every(0.1).minutes.do(job)
# schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)