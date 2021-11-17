import os
import json


def dump():
    global file_num
    global ids
    des_path = os.path.join(des_dir, str(file_num) + "json")
    file_num += 1
    with open(des_path, "w") as f:
        for id_num in ids:
            f.write(str(id_num) + "\n")
    ids = []


if __name__ == '__main__':
    src_dir = "ids"
    des_dir = "des"
    if not os.path.exists(des_dir):
        os.mkdir(des_dir)

    file_num = 0
    ids = []
    for file in os.listdir(src_dir):
        print(file)
        src_path = os.path.join(src_dir, file)

        with open(src_path, "r") as f:
            contents = json.load(f)  # ["contents"]

        for item in contents:
            ids.append(item["illust_id"])

        if len(ids) >= 2000:
            dump()

    if len(ids) > 0:
        dump()
