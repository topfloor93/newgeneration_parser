import re
import json
import glob


def get_log(file_name):
    fd = open(file_name, 'r')
    log = fd.readlines()
    return log


def remove_trash(logs):
    rv = []
    for log in logs:
        temp = re.sub('[^A-Za-z0-9:,.\-]+', '', log)
        if temp == '':
            pass
        else:
            rv.append(temp)
    return rv


def parse_test_opt(logs):
    temp = 'TestOptions,'
    for i in range(0, 8):
        temp += logs.pop(0) + ","
    temp = temp[:len(temp)-1]
    logs.insert(0, temp)
    return logs


def is_group(attr):
    for i in attr:
        if i == ':':
            return False
        elif i == ',':
            return True

    return


def make_dict(logs):
    rv = {}
    cnt = 0
    flag = 0
    for log in logs:
        if "Linklayertype" in str(log):
            flag = 1
            cnt += 1
            rv["Packet No" + str(cnt)] = {}
        if "PacketNo" in str(log):
            flag = 1
            cnt += 1
            rv["Packet No" + str(cnt)] = {}
            continue
        if "Finished" in str(log):
            continue

        if flag == 0:
            if is_group(log):
                temp = log.split(',')
                if temp[0] == '':
                    return None
                rv[temp[0]] = make_dict(temp[1:])
            else:
                if ',' in log:
                    chunks = log.split(",")
                    for attr in chunks:
                        temp = attr.split(":")
                        rv[temp[0]] = attr[len(temp[0])+1:]
                else:
                    temp = log.split(":")
                    rv[temp[0]] = log[len(temp[0])+1:]
        else:
            if is_group(log):
                temp = log.split(',')
                if temp[0] == '':
                    return None
                rv["Packet No" + str(cnt)][temp[0]] = make_dict(temp[1:])
            else:
                if ',' in log:
                    chunks = log.split(",")
                    for attr in chunks:
                        temp = attr.split(":")
                        rv["Packet No" + str(cnt)][temp[0]] = attr[len(temp[0])+1:]
                else:
                    temp = log.split(":")
                    rv["Packet No" + str(cnt)][temp[0]] = log[len(temp[0])+1:]

    return rv


def get_files():
    rv = []
    second_path = glob.glob("log\\*")
    for sp in second_path:
        rv += glob.glob(sp + "\\*")

    for idx, attr in enumerate(rv):
        rv[idx] = attr.split(".")[0]
    return rv


def run():
    file_list = get_files()
    for file_name in file_list:
        logs_dict = {}
        logs = get_log(file_name + ".txt")
        logs = remove_trash(logs)
        logs = parse_test_opt(logs)
        logs_dict = make_dict(logs)

        json_log = json.dumps(logs_dict, indent=4)
        f = open(file_name + ".json", "w")
        f.write(json_log)
        f.close()


if __name__ == "__main__":
    run()
    #print(get_files())
