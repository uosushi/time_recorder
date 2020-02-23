import json, time
from datetime import datetime

class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if type(obj).__name__ == "datetime":
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return obj

red = "\033[31m"
bold = "\033[1m"
end = "\033[0m"

while True:
    command = input(bold+">> "+end)
    if command == "record start":
        timestamp = datetime.now()
        fr = open("save.json", "r")
        data = json.load(fr)
        fr.close()
        if data["record"][-1][1] == "start":
            print(bold+red+"caution: now recording."+end) # 前回のレコードが終了処理を済ませていない時
        else:
            fw = open("save.json","w")
            data["record"].append([timestamp,"start"])
            json.dump(data, fw, cls=DatetimeEncoder)
            fw.close()
            print(bold+"now recording..."+end)
    if command == "record end":
        timestamp = datetime.now()
        fr = open("save.json", "r")
        data = json.load(fr)
        fr.close()
        if data["record"][-1][1] == "end":
            print(bold+red+"caution: The record being recorded does not exist."+end) # 前回のレコードが終了処理を済ませていない時
        else:
            fw = open("save.json","w")
            timedelta_obj = timestamp-datetime.strptime(data["record"][-1][0],"%Y-%m-%d %H:%M:%S")
            timedelta_total_seconds = timedelta_obj.total_seconds()
            print(bold+red+"total_seconds: "+str(timedelta_total_seconds)+end)
            data["sum"] += timedelta_total_seconds
            data["record"].append([timestamp,"end"])
            json.dump(data, fw, cls=DatetimeEncoder)
            fw.close()
    elif command == "record show":
        fr = open("save.json", "r")
        data = json.load(fr)
        record = data["record"]
        record_total = data["sum"]
        fr.close()
        for i in record:
            print(bold+" | ".join(i)+end)
        print(bold+red+"total_seconds: "+str(record_total)+end)
    elif command == "exit()":
        print(bold+"Bye!"+end)
        break