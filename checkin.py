import requests as re
import json
import time
import eventRec

checkinAtp = json.loads(open("config.json", "r").read())['checkinAttempt'] + 1
null = None
date = time.strftime("%Y-%m-%d", time.localtime())




para = json.loads(open("postpara.json", "r",encoding='utf-8').read())
key,value=[0]*len(para),[0]*len(para)
n=len(para)

i=0
for item in para.items():
    key[i]=item[0]
    value[i]=item[1]
    i+=1
    
dic={key[i]:value[i] for i in range(n)}
dic=json.dumps(dic)
print(dic)



def print_cur_status(cookies):
    data = eval(re.get("https://fangkong.hnu.edu.cn/api/v1/clockincount/getcountlist", cookies=cookies).content.decode(
        "utf-8"))["data"]
    return ("\n打卡教师： " + str(data["TeacherCount"]) + "\n" +
            "打卡本科生： " + str(data["UndergraduateCount"]) + "\n" +
            "打卡研究生： " + str(data["GraduateCount"]) + "\n" +
            "总打卡人数：" + str(data["AllCount"]))


def checkin(cookies):
    """

    :param cookies:
    :return: if fail
    """
    checkinCount = 0
    if get_today_temp(cookies) == 0:
        print("(-) 开始重新打卡")
        print("-----------------\nSTART ATTEMPT")
        while True:
            if checkinCount >= checkinAtp:
                raise Exception("try too much times")
            checkinCount += 1
            try:
                                status = re.post("https://fangkong.hnu.edu.cn/api/v1/clockinlog/add", headers = {'Content-Type': 'application/json'}, data=dic, cookies=cookies).content.decode("utf-8")
                                print(status)
            except Exception as e:
                print("(X) ATTEMPT: " + str(checkinCount) + " --- " + str(e))
                continue
            if get_today_temp(cookies) == 0:
                print("(X) ATTEMPT: " + str(checkinCount) + " --- " + eval(status)['msg'])
            else:
                eventRec.ok_msg(msg="checkin successfully")
                print("(√) " + "打卡成功!")
                break
    else:
        eventRec.ok_msg(msg="checkin successfully")
        print("(-) 检测到已经打过卡")


def get_today_temp(cookies):
    a = eval(re.get("https://fangkong.hnu.edu.cn/api/v1/clockinlog/find?datestr=" + date,
                    cookies=cookies).content.decode("utf-8"))
    return 0 if a["code"] == 1 else a["data"]["Temperature"]
