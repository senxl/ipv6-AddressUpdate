import re
import socket
import os
import time
import platform
import requests

# 每步动态域名登录信息
meibu_hostname = 'xxx.msns.cn'
meibu_passwd = 'xxxxxx'


# 全局变量
current = ''
root = ''

# 记录数据目录设定
if platform.system() == 'Windows':
    root = 'C:/Users/Public/msns-ddns-update/'
    os.system('powershell mkdir ' + root)
elif platform.system() == 'Linux':
    root = '/root/msns-ddns-update/'
    os.system('mkdir ' + root)

# 获取IPv6地址接口
def get_ipv6_address():
    try:
        output = requests.get('https://api6.ipify.org?format=json')
        result = re.findall(r"(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})", output.text, re.I)
        # print(result)
        return result[0][0]
    except:
        return ''

##每步动态域名更新
def meibu_update():
    # 1数据包格式
    udpdata = ("sdsipv6" + meibu_hostname + "###" +
               meibu_passwd + "###" + current + "end###")

    # 2创建socket对象
    # 参数一 指定用ipv4版本，参数2 指定用udp协议
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 3用socket对象发送
    # 参数1是内容 参数2是地址和端口
    udp_socket.sendto(udpdata.encode('utf-8'), ('main.sds.cn', 60001))

    # 4关闭socket对象
    udp_socket.close()

def ipFileSave():
    # 写入ipv6地址
    with open(root + "addr6.history", "w") as f:
        f.write(current)

def logSave(isUpdate):
    # 写入日志到本地
    if (isUpdate == True):
        with open(root + "addr6.log", "a+") as f:
            format_time = time.strftime(
                "%Y-%m-%d | %H:%M:%S", time.localtime(time.time()))   # 格式化日期
            f.write(format_time + ' | --- IPv6 address updated\n')
    else:
        with open(root + "addr6.log", "a+") as f:
            format_time = time.strftime(
                "%Y-%m-%d | %H:%M:%S", time.localtime(time.time()))   # 格式化日期
            f.write(format_time + ' | --- IPv6 address unchanged\n')

def run_update():
    if (current != ''):
        meibu_update()
        time.sleep(1)
        meibu_update()
        time.sleep(1)
        meibu_update()

        ipFileSave()
        logSave(True)

def startUpdate():
    global current
    # 读取ipv6地址
    current = get_ipv6_address()
    print(current)
    try:
        with open(root + "addr6.history", "r") as f:
            addr = f.readline()
            fileTime = int(os.path.getmtime(root + "addr6.history"))
            nowTime = time.time()
            #ip更新时间天数
            day = (nowTime - fileTime)/60/60/24

            if ((addr != current) or (day > 18)):
                run_update()
            # else:
            #     logSave(False)
    except:
        run_update()

if __name__ == '__main__':
    # startUpdate()
    while True:
        startUpdate()
        #每隔5分钟检测
        time.sleep(5*60)
