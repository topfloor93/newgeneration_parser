import re


def get_log(file_name):
    log_file = "log\\" + file_name
    fd = open(log_file, 'r')
    log = fd.readlines()
    return log


def remove_trash(logs):
    rv = []
    for log in logs:
        temp = re.sub('[^A-Za-z0-9:,]+', '', log)
        if temp == '':
            pass
        else:
            rv.append(temp)
    return rv


def parse_test_opt(logs):
    temp = 'TestOptions,'
    for i in range(0, 8):
        temp += logs.pop(0) + ","
    temp = temp[:len(temp)]
    logs.insert(0, temp)
    return logs


def is_group(attr):
    for i in attr:
        if i == ':':
            return False
        elif i == ',':
            return True

    return


#def make_dict(logs):
    #temp = []
    #for log in logs:
        #temp = log.split(',')
        #if is_group(log):
        #    make_dict(temp)
        #else:
        #temp = log.split(',')


def run():
    log = get_log("TCP\\case1.txt")
    log = remove_trash(log)
    log = parse_test_opt(log)
    print(log)


if __name__ == "__main__":
    run()
