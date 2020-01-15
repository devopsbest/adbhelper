import os
import socket

from adb_helper.adbhelper import find_devices, run_command_on_shell, exec_command

'''
    adb tcpip 5555

    adb connect ip
       
设置代理：
adb shell settings put global http_proxy 代理IP地址:端口号
如：
adb shell settings put global http_proxy 127.0.0.1:8888
移除代理：
adb shell settings delete global http_proxy
adb shell settings delete global global_http_proxy_host
adb shell settings delete global global_http_proxy_port
'''

port = "8888"

goole_proxy_host = "cnshhq-w0007"
google_proxy_port = "1083"


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


import re


def remote_connet_inital():
    cmd = "adb tcpip 5555"
    exec_command(cmd)


def get_device_ip():
    cmd = "adb shell ifconfig wlan0"
    result = run_command_on_shell(cmd)
    print(result)
    ip = re.search(r"inet addr:(\d+\.){3}(\d+)", result[1])
    return (ip.group(0).split(":")[1])


def remote_connect(ip):
    cmd = "adb connect {}".format(ip)
    exec_command(cmd)


def remote_disconnect(ip):
    cmd = "adb disconnect {}".format(ip)
    exec_command(cmd)


def remove_proxy():
    cmd1 = "adb shell settings delete global http_proxy"
    cmd2 = "adb shell settings delete global global_http_proxy_host"
    cmd3 = "adb shell settings delete global global_http_proxy_port"
    exec_command(cmd1)
    exec_command(cmd2)
    exec_command(cmd3)


def set_proxy(ip, port):
    remove_proxy()
    cmd = "adb shell settings put global http_proxy {}:{}".format(ip, port)
    os.popen(cmd)


import time

PATH = lambda p: os.path.abspath(p)


# 利用adb 截取Android手机图像，并且保存到本地
def screenshot():
    path = PATH(os.getcwd() + "/screenshot")
    timestamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    os.popen("adb wait-for-device")
    os.popen("adb shell screencap -p /data/local/tmp/tmp.png")

    if not os.path.isdir(PATH(os.getcwd() + "/screenshot")):
        os.makedirs(path)

    os.popen("adb pull /data/local/tmp/tmp.png " + PATH(path + "/" + timestamp + ".png"))
    os.popen("adb shell rm /data/local/tmp/tmp.png")
    print("success")


if __name__ == '__main__':

    print(get_host_ip())
    device = find_devices()
    print(device)
    remote_connet_inital()
    result = input("Do you want to contiune:y/n")
    if result == 'y':
        print("go")

        if len(device) >=1:



            print(get_device_ip())

            remove_proxy()
            remote_disconnect(get_device_ip())
        else:
            print("no device find")



