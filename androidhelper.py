import os
import re
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


def get_pc_ip():
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


def remote_connet_inital():
    cmd = "adb tcpip 5555"
    result = exec_command(cmd)


def get_device_ip():
    cmd = "adb shell ifconfig wlan0".format()
    result = run_command_on_shell(cmd)
    print(result)
    ip = re.search(r"inet addr:(\d+\.){3}(\d+)", result[1])
    return (ip.group(0).split(":")[1])


def remote_connect_device(ip):
    cmd = "adb connect {}".format(ip)
    result = exec_command(cmd)
    if "connected" in str(result):
        return True
    else:
        return False


def remote_disconnect_device(ip):
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
    cmd = "adb shell settings put global http_proxy {}:{}".format(ip, port)
    exec_command(cmd)


PATH = lambda p: os.path.abspath(p)

# # 利用adb 截取Android手机图像，并且保存到本地
# def screenshot():
#     path = PATH(os.getcwd() + "/screenshot")
#     timestamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
#     os.popen("adb wait-for-device")
#     os.popen("adb shell screencap -p /data/local/tmp/tmp.png")
#
#     if not os.path.isdir(PATH(os.getcwd() + "/screenshot")):
#         os.makedirs(path)
#
#     os.popen("adb pull /data/local/tmp/tmp.png " + PATH(path + "/" + timestamp + ".png"))
#     os.popen("adb shell rm /data/local/tmp/tmp.png")
#     print("success")
import time

pc_ip = get_pc_ip()

if __name__ == '__main__':
    print("current pc ip is {}".format(get_pc_ip()))
    device = find_devices()

    if len(device) > 1:
        print(device)
        remote_connet_inital()
        print("start success")
        ip = device[-1].split(":")[0]
        print(ip)
        print("phone ip is: {}".format(ip))

        print("get ip is {}".format(get_pc_ip()))

        contiune = input("Do you want to go ahead y/n, please unplug your cable")
        if contiune == 'y':

            if remote_connect_device(ip):

                print(find_devices())

                set_proxy(get_pc_ip(), port)
            else:
                print("cannot start")
        else:
            print("end!")

    elif len(device) ==1:
        remote_connet_inital()
        print("start success")

        time.sleep(3)
        ip = get_device_ip()
        print(ip)
        contiune = input("Do you want to go ahead y/n, please unplug your cable")
        if contiune == 'y':

            if remote_connect_device(ip):

                print(find_devices())

                set_proxy(pc_ip, port)
            else:
                print("cannot start")
    else:
        print("no devices")

else:
    print("no informaiton")
