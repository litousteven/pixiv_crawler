from pixivpy3 import *
import json
import datetime
import os
from constant import *

if __name__ == '__main__':
    dump_dir = "ids"
    date_format = "%Y%m%d"
    start_date_str = "20210815"
    end_date_str = "20211115"

    if not os.path.exists(dump_dir):
        os.mkdir(dump_dir)

    start_date = datetime.datetime.strptime(start_date_str, date_format)
    end_date = datetime.datetime.strptime(end_date_str, date_format)
    delta = datetime.timedelta(days=1)

    current_date = start_date
    api = PixivAPI()
    api.set_cookie(cookie)
    while (end_date - current_date).days > 0:

        current_date_str = current_date.strftime(date_format)
        current_date_int = int(current_date_str)
        print(current_date_str)

        contents = []
        for p in range(1, 100):

            json_result = api.ranking(mode="daily", date=current_date_int, p=p)
            if "error" in json_result:
                break
            contents += json_result["contents"]

        path = os.path.join(dump_dir, current_date_str + ".json")
        with open(path, "w") as f:
            json.dump(contents, f)

        current_date += delta
