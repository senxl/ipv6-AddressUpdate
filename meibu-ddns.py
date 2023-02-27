import re
import os
import time
import platform
import requests

# 每步动态域名登录信息
meibu_hostname = 'xxxx.msns.cn'
meibu_passwd = 'xxxxxxx'

# dynv6动态域名登录信息
dynv6_hostname = 'xxxx.dns.army'
dynv6_passwd = 'xxxxxxx'


# 全局变量
current = ''
root = ''

# 记录数据目录设定
if platform.system() == 'Windows':
    root = 'C:/Users/Public/ddns-update/'
    os.system('powershell mkdir -Force ' + root)
elif platform.system() == 'Linux':
    root = '/root/ddns-update/'
    os.system('mkdir -p ' + root)

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
    # 数据http_get访问
    requests.get('http://www.meibu.com/ipv6zdz.asp?ipv6=' + current + '&name=' + meibu_hostname + '&pwd=' + meibu_passwd)

##dynv6动态域名更新
def dynv6_update():
    # 数据http_get访问
    requests.get('http://dynv6.com/api/update?hostname=' + dynv6_hostname + '&token=' + dynv6_passwd + '&ipv6=' + current)
    
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
        #每步更新
        meibu_update()
        time.sleep(1)

        #dynv6更新
        dynv6_update()

        ipFileSave()
        logSave(True)

def startUpdate():
    global current
    # 读取ipv6地址
    current = get_ipv6_address()
    print(current)
    # run_update()
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
    startUpdate()
    while False:
        startUpdate()
        #每隔5分钟检测
        time.sleep(5*60)
